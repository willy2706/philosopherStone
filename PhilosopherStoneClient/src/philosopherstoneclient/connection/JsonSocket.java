/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package philosopherstoneclient.connection;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;

/**
 *
 * @author winsxx
 */
public class JsonSocket {
    private static final int CHUNKSIZE = 1024; 
    
    private final String host;
    private final int port;
    private final int timeout;
    private Socket socket;
    
    private final StringBuilder storedBuffer;
    
    public JsonSocket(String host, int port, int timeoutInMillis){
        this.host = host;
        this.port = port;
        this.timeout = timeoutInMillis;
        
        storedBuffer = new StringBuilder();
    }
        
    public String getHost(){
        return host;
    }
    public int getPort(){
        return port;
    }
    
    public void connect() throws IOException{
        socket = new Socket(host, port);
    }
    public void close() throws IOException{
        socket.close();
    }
            
    public String read() throws IOException{
        InputStream inFromServer = socket.getInputStream();
        DataInputStream in = new DataInputStream(inFromServer);
        
        //find first open curly bracket
        int start, end;
        boolean found;
        start = 0;
        found = false;
        while(!found){
            if(storedBuffer.length() == start){
                
                byte[] buffer = new byte[CHUNKSIZE];
                int bufferSize = in.read(buffer);
                if (bufferSize > 0) storedBuffer.append(new String(buffer));

            } else {
                
                if(storedBuffer.charAt(start) == '{'){
                    found = true;
                } else{
                    start++;
                }

            }
        }
        //End of finding curly bracket

        //find end close curly bracket
        int curlyBracketCount = 1;
        found = false;
        end = start+1;
        while(!found){
            if(storedBuffer.length() == end){

                byte[] buffer = new byte[CHUNKSIZE];
                int bufferSize = in.read(buffer);
                if (bufferSize > 0) storedBuffer.append(new String(buffer));

            } else {
                
                if(storedBuffer.charAt(end) == '{'){
                    curlyBracketCount++;
                    end++;
                } else if(storedBuffer.charAt(end) == '}'){
                    curlyBracketCount--;
                    if(curlyBracketCount == 0){
                        found = true;
                    } else {
                        end++;
                    }
                } else {
                    end++;
                }

            }
        }
        //End of finding curly bracket
        
        String jsonString = storedBuffer.substring(start, end+1);
        storedBuffer.delete(0, end+1);
        
        return jsonString;
    }
    
    public void write(String jsonString) throws IOException{
        OutputStream outToHost = socket.getOutputStream();
        DataOutputStream out = new DataOutputStream(outToHost);
        out.write(jsonString.getBytes());
    }
    
}
