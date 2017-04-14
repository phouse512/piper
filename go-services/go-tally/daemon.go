package main

import (
	"bufio"
	"encoding/json"
	"io"
	"io/ioutil"
	"log"
	"net"
	"time"
)

const (
	MAX_UNPROCESSED_PACKETS = 100
)

var (
	In            = make(chan *string, MAX_UNPROCESSED_PACKETS)
	flushInterval = int64(30)
	gauges        = make([]string, 1000)
	counters      = make([]string, 1000)
)

type DBConfig struct {
	Host     string `json:"host"`
	User     string `json:"user"`
	Database string `json:"database"`
	Password string `json:"password"`
}

func monitor() {
	period := time.Duration(flushInterval) * time.Second
	ticker := time.NewTicker(period)
	for {
		select {
		case <-ticker.C:
			log.Print("Ticker wheee")
		case s := <-In:
			log.Printf("Test: %s", s)
		}
	}
}

func handleMessage(conn io.ReadCloser, partialReads bool, out chan<- *string) {
	defer conn.Close()
	reader := bufio.NewReader(conn)

	for {
		message, err := reader.ReadString('\n')
		log.Printf("incoming message: %s", message)

		if err == io.EOF {
			log.Print("connection closed, EOF")
			break
		}

		if err != nil {
			break
		}
	}
}

func tcpListener() {
	address, err := net.ResolveTCPAddr("tcp", ":8173")
	if err != nil {
		log.Fatalf("ERROR: ResolveTCPAddr - %s", err)
	}

	listener, err := net.ListenTCP("tcp", address)
	if err != nil {
		log.Fatalf("ERROR: ListenTCP - %s", err)
	}
	defer listener.Close()

	for {
		conn, err := listener.AcceptTCP()
		if err != nil {
			log.Fatalf("ERROR: AcceptTCP - %s", err)
		}

		go handleMessage(conn, true, In)
	}
}

func main() {
	log.Println("Loading database credentials from JSON")
	file, err := ioutil.ReadFile("./db.json")
	if err != nil {
		log.Fatal("File error: ", err)
	}

	var dbConfig DBConfig
	json.Unmarshal(file, &dbConfig)

	go tcpListener()
	monitor()
}
