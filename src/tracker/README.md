# LoliHorizon - Tracker

By: Assistants of IF3230 - Parallel and Distributed Systems

## Development Environment

- Linux x86_64

- Go Language 1.4.2

## Requirements

** Environment Set **

Set the following lines to ```/etc/profile```:

    export PATH=$PATH:/usr/local/go/bin

    export GOPATH=$HOME/go

** Download MySQL Driver **

    $go get github.com/go-sql-driver/mysql

** For 1st MySQL use **

    $sudo chmod -R 755 /var/lib/mysql/

    $sudo mkdir /var/run/mysqld

    $sudo touch /var/run/mysqld/mysqld.sock

    $sudo chown -R mysql /var/run/mysqld/

    $sudo /etc/init.d/mysql start


## How to Run

- In release environment, please use ```nohup go run main.go & > my.log 2>&1&``` for running tracker process in background. After that, use ```echo $! > save_pid.txt``` to get Process ID.
