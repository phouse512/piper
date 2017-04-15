package main

import (
	"bufio"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	_ "github.com/lib/pq"
	"io"
	"io/ioutil"
	"log"
	"net"
	"regexp"
	"strconv"
	"strings"
	"sync"
	"time"
)

const (
	MAX_UNPROCESSED_PACKETS = 100
)

var (
	In            = make(chan *DataPoint, MAX_UNPROCESSED_PACKETS)
	flushInterval = int64(30)
	gauges        = make([]*DataPoint, 0)
	counters      = make([]*DataPoint, 0)
	re            = regexp.MustCompile(`\r?\n`)
	mutex         = &sync.Mutex{}
)

var (
	db *sql.DB
)

type DBConfig struct {
	Host     string `json:"host"`
	User     string `json:"user"`
	Database string `json:"database"`
	Password string `json:"password"`
}

type DataPoint struct {
	Key   string
	Value int64
	Type  string
	Time  time.Time
}

func parsePacket(message string) (*DataPoint, error) {
	results := strings.Split(message, ":")

	if len(results) != 3 {
		return nil, errors.New("improperly formatted message")
	}

	if !(results[0] == "c" || results[0] == "g") {
		return nil, errors.New("invalid data-type specified")
	}

	value, err := strconv.ParseInt(results[2], 10, 64)
	if err != nil {
		return nil, err
	}

	return &DataPoint{Key: results[1], Value: value, Type: results[0], Time: time.Now()}, nil
}

func flushGauges() {
	stmt, err := db.Prepare(`INSERT INTO gauges (key, value, created_at) VALUES ($1, $2, to_timestamp($3))`)
	if err != nil {
		log.Fatal("Couldn't prepare gauges sql:", err)
	}

	mutex.Lock()
	tmp := make([]*DataPoint, len(gauges))
	copy(tmp, gauges)
	gauges = nil
	mutex.Unlock()

	for _, packet := range tmp {
		_, err = stmt.Exec(packet.Key, packet.Value, packet.Time.Unix())
		if err != nil {
			log.Fatal("Error inserting row: ", err)
		}
	}

	log.Printf("Flushed %d gauges to DB", len(tmp))
}

func flushCounters() {
	stmt, err := db.Prepare(`INSERT INTO counters (key, value, created_at) VALUES ($1, $2, to_timestamp($3))`)
	if err != nil {
		log.Fatal("Couldn't prepare counter sql:", err)
	}

	mutex.Lock()
	tmp := make([]*DataPoint, len(counters))
	copy(tmp, counters)
	counters = nil
	mutex.Unlock()

	// copy to temp array and clear
	for _, packet := range tmp {
		_, err = stmt.Exec(packet.Key, packet.Value, packet.Time.Unix())
		if err != nil {
			log.Fatal("Error inserting row: ", err)
		}
	}

	log.Printf("Flushed %d counters to DB", len(tmp))
}

func monitor() {
	period := time.Duration(flushInterval) * time.Second
	ticker := time.NewTicker(period)
	for {
		select {
		case <-ticker.C:
			log.Print("time to flush")
			flushCounters()
			flushGauges()
		case s := <-In:
			log.Printf("Test: %v", s)
			readMessage(s)
			log.Printf("counters size: %d", len(counters))
		}
	}
}

func readMessage(dp *DataPoint) {
	if dp.Type == "g" {
		gauges = append(gauges, dp)
	} else if dp.Type == "c" {
		counters = append(counters, dp)
	}
}

func handleMessage(conn io.ReadCloser, partialReads bool, out chan<- *DataPoint) {
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

		cleanedMsg := re.ReplaceAllString(message, "")
		result, err := parsePacket(cleanedMsg)
		if err != nil {
			log.Print("invalid message given with error ", message, err)
			break
		}

		out <- result
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

	db_string := fmt.Sprintf("host=%s user=%s password=%s dbname=%s sslmode=disable", dbConfig.Host, dbConfig.User, dbConfig.Password, dbConfig.Database)
	db, err = sql.Open("postgres", db_string)
	if err != nil {
		log.Fatalf("Couldn't open a connection to the database.")
	}

	go tcpListener()
	monitor()
}
