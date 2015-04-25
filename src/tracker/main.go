package main

import (
    "bytes"
    "errors"
    "fmt"
    "net"
    "strconv"
    "strings"
    "sync"
    "time"
    "database/sql"
    "encoding/binary"
    "encoding/json"
    _ "github.com/go-sql-driver/mysql"
)

func Ip2long(ipAddr string) (uint32, error) {
    ip := net.ParseIP(ipAddr)
    if ip == nil {
        return 0, errors.New("wrong ipAddr format")
    }
    ip = ip.To4()
    return binary.BigEndian.Uint32(ip), nil
}

func Long2ip(ipLong uint32) string {
    ipByte := make([]byte, 4)
    binary.BigEndian.PutUint32(ipByte, ipLong)
    ip := net.IP(ipByte)
    return ip.String()
}

var (
        id int
        ip uint32
        port int
)

type LogValue struct {
    Ip string `json:"ip"`
    Port int `json:"port"`
}

type MessageInJSON struct {
    Status string `json:"status"`
    Value []LogValue `json:"value"`
}

type MessageOutJSON struct {
    Method string `json:"method"`
    Server []LogValue `json:"server"`
}

var db *sql.DB // database global_variable
var ip_address string // current IP address
var current_port int // current Port

/** Insert data to DB */
func InsertData(conn net.Conn, ip uint32, port int) {
    _, err := db.Query("INSERT IGNORE INTO client_info(ip, port) VALUES(?, ?)", ip, port)
    if err != nil {
        if conn != nil {
            RespondWithRealm(conn, errors.New("Error in database connection"))
        } else {
            fmt.Println(err.Error())
        }
    }
}

func DeleteData(ip uint32, port int) {
    _, err := db.Query("DELETE FROM client_info WHERE ip=? AND port=?", ip, port)
    if err != nil {
        fmt.Println(err.Error())
    }
}

/** Retrieve all available clients from DB */
func RetrieveData(conn net.Conn, code int) string { // code 0 = inbound; 1 = outbound
    rows, err := db.Query("SELECT * FROM client_info")
    if err != nil {
        RespondWithRealm(conn, errors.New("Error in database connection"))
    }
    defer rows.Close()
    messageObject := new(MessageInJSON)
    messageObject2 := new(MessageOutJSON)

    for rows.Next() {
        err := rows.Scan(&ip, &port)
        if err != nil {
            RespondWithRealm(conn, errors.New("Error in reading parameters"))
        }
        ip_str := Long2ip(ip)
        if err != nil {
            RespondWithRealm(conn, errors.New("IP address is not valid"))
        }
        if code == 0 {
            messageObject.Value = append(messageObject.Value, LogValue{Ip: ip_str, Port: port})
        } else if code == 1 {
            messageObject2.Server = append(messageObject2.Server, LogValue{Ip: ip_str, Port: port})
        }
        
    }

    var encodedMessage []byte
    if code == 0 {
        messageObject.Status = "ok";
        encodedMessage, _ = json.Marshal(messageObject)
    } else if code == 1 {
        messageObject2.Method = "serverStatus";
        encodedMessage, _ = json.Marshal(messageObject2)
    }

    err = rows.Err()
    if err != nil {
        RespondWithRealm(conn, errors.New("Error in JSON Marshal"))
    }

    return string(encodedMessage)
}

/** Handling connection from client */
func HandleConnection(conn net.Conn) {
    var ip_long string
    var port_int float64

    remoteAddress := conn.RemoteAddr().String() // broadcast statusServer except this address
    fmt.Println("**Initiate connection with " + remoteAddress  + "**")
    readBuf := make([]byte, 4096)
    conn.Read(readBuf) // accept JSON input from clients
    length := bytes.Index(readBuf, []byte{0})

    // Convert []byte to map interface
    var value map[string]interface{}
    err := json.Unmarshal(readBuf[:length], &value)
    if err != nil {
        RespondWithRealm(conn, errors.New("Error in JSON parsing"))
    }

    // Process data
    if value["method"] == nil { // check method exists
        RespondWithRealm(conn, errors.New("Missing parameter"))
    }
    method_string, ok:= value["method"].(string)
    if !ok {
        RespondWithRealm(conn, errors.New("Invalid 'method' datatype"))
    }

    data := RetrieveData(conn, 0)

    switch method_string {
        case "join":
            if value["ip"] == nil || value["port"] == nil { // check params exist
                RespondWithRealm(conn, errors.New("Missing parameter"))
            }
            ip_long, ok = value["ip"].(string)
            if !ok {
                RespondWithRealm(conn, errors.New("Invalid 'ip' datatype"))
            }
            ip_uint32, err := Ip2long(ip_long)
            if err != nil {
                RespondWithRealm(conn, errors.New("Unknown IP address"))
            }
            port_int, ok = value["port"].(float64)
            if !ok {
                RespondWithRealm(conn, errors.New("Invalid 'port' datatype"))
            }
            InsertData(conn, ip_uint32, int(port_int))

            var wg sync.WaitGroup
            rows, err := db.Query("SELECT * FROM client_info")
            if err != nil {
                RespondWithRealm(conn, errors.New("Error in database connection"))
            }
            defer rows.Close()
            for rows.Next() {
                err := rows.Scan(&ip, &port)
                if err != nil {
                    RespondWithRealm(conn, errors.New("Error in reading parameters"))
                }
                ip_str := Long2ip(ip)
                port_str:= strconv.Itoa(port)
                if ip_long != ip_str ||  port != int(port_int) { // exclude requester
                    wg.Add(1) // increment the wait group counter
                    go TimeoutCheck(ip_str + ":" + port_str, &wg)
                }
            }
            wg.Wait() // wait
            port_str := strconv.Itoa(int(port_int))
            go broadcastAll(ip_long + ":" + port_str) // async broadcast
        default:
            RespondWithRealm(conn, errors.New("Unsupported Method"))
    }

    data = RetrieveData(conn, 0) // retrieve new data
    _, err = conn.Write([]byte(data)) // send response
    if err != nil {
        RespondWithRealm(conn, errors.New("Error in writing response"))
    }
    conn.Close()
    fmt.Println("**Connection with " + remoteAddress + " ended**")
}

func sendServerStatus(address string, data string) {
    fmt.Println("Send to: " + address)
    conn, err := net.DialTimeout("tcp", address, 3 * time.Second) // 3 secs
    if err != nil {
        // handle errors
    }
    _, err = conn.Write([]byte(data)) // send response
    if err != nil {
        RespondWithRealm(conn, errors.New("Error in writing response"))
    }
    readBuf := make([]byte, 4096)
    conn.Read(readBuf)
    length := bytes.Index(readBuf, []byte{0})
    fmt.Println(address + " : " + string(readBuf[:length]))
    conn.Close()
}

func broadcastAll(address string) { // exclude requester address
    rows, err := db.Query("SELECT * FROM client_info")
    data := RetrieveData(nil, 1)
    if err != nil {
        // handle errors
    }
    defer rows.Close()
    for rows.Next() {
        err := rows.Scan(&ip, &port)
        if err != nil {
            // handle errors
        }
        ip_str := Long2ip(ip)
        port_str:= strconv.Itoa(port)
        currentAddress := ip_str + ":" + port_str
        if address != currentAddress { // exclude requester
            go sendServerStatus(currentAddress, data)
        }
    }
    fmt.Println("Send data: " + data)
}

func TimeoutCheck(address string, wg *sync.WaitGroup) {
    defer wg.Done()
    fmt.Println("Now checking " + address)
    connTest, err := net.DialTimeout("tcp", address, 3 * time.Second) // 3 secs
    if err != nil {
        fmt.Println("TimeoutCheck: " + err.Error())
        // remove from DB
        slc := strings.Split(address, ":")
        ip_long, err := Ip2long(slc[0])
        if err != nil {
            // handle error
        }
        port_int, err := strconv.Atoi(slc[1])
        if err != nil {
            // handle error
        }
        DeleteData(ip_long, port_int)
    } else {
        fmt.Println("TimeoutCheck: " + address + " is still active")
        connTest.Close()
    }
}

func main() {
    var err error
    addrs, err := net.InterfaceAddrs()
    if err != nil {
        // handle error
    }
    for _, a := range addrs {
        if ipnet, ok := a.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
           if ipnet.IP.To4() != nil {
               ip_address = ipnet.IP.String()
           }
        }
    }
    fmt.Println("**Initialize**")

    current_port = 8000
    fmt.Println("Your address is: " + ip_address + ":" + strconv.Itoa(current_port))
    /*
    ip_long, err := Ip2long(ip_address)
    if err != nil {
        // handle error
    }
    */
    db, err = sql.Open("mysql","root@tcp(127.0.0.1:3306)/sister_tracker")
    // InsertData(nil, ip_long, current_port) // add own IP address information
    fmt.Println("**Finish Initializing**")

    // Open Connection
    ln, err := net.Listen("tcp", ":" + strconv.Itoa(current_port))
    if err != nil {
        // handle error
    }

    for {
        conn, err := ln.Accept() // this blocks until connection or error
        if err != nil {
            // handle error
            continue
        }
        go HandleConnection(conn) // a goroutine handles conn so that the loop can accept other connections
    }
    defer db.Close()
}

/** Send error response to client */
func RespondWithRealm(conn net.Conn, err error) {
    errorMessage := err.Error()
    message := "{\"status\": \"error\", \"description\": \""+ errorMessage +"\"}"
    _, err = conn.Write([]byte(message)) // send response
    if err != nil {
        // handle error
    }
    conn.Close()
}
