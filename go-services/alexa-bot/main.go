package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	_ "github.com/lib/pq"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"
)

type AlexaResponse struct {
	Version  string `json:"version"`
	Response struct {
		OutputSpeech struct {
			Type string `json:"type"`
			Text string `json:"text"`
		} `json:"outputSpeech"`
	} `json:"response"`
}

type AlexaRequest struct {
	Version string `json:"version"`
	Session struct {
		New         bool   `json:"new"`
		SessionID   string `json:"sessionId"`
		Application struct {
			ApplicationID string `json:"applicationId"`
		} `json:"application"`
		User struct {
			UserID string `json:"userId"`
		} `json:"user"`
	} `json:"session"`
	Context struct {
		AudioPlayer struct {
			PlayerActivity string `json:"playerActivity"`
		} `json:"AudioPlayer"`
		System struct {
			Application struct {
				ApplicationID string `json:"applicationId"`
			} `json:"application"`
			User struct {
				UserID string `json:"userId"`
			} `json:"user"`
			Device struct {
				DeviceID            string `json:"deviceId"`
				SupportedInterfaces struct {
					AudioPlayer struct {
					} `json:"AudioPlayer"`
				} `json:"supportedInterfaces"`
			} `json:"device"`
			APIEndpoint string `json:"apiEndpoint"`
		} `json:"System"`
	} `json:"context"`
	Request struct {
		Type      string    `json:"type"`
		RequestID string    `json:"requestId"`
		Timestamp time.Time `json:"timestamp"`
		Locale    string    `json:"locale"`
		Intent    struct {
			Name               string `json:"name"`
			ConfirmationStatus string `json:"confirmationStatus"`
			Slots              struct {
				TimeFrame struct {
					Name               string `json:"name"`
					Value              string `json:"value"`
					ConfirmationStatus string `json:"confirmationStatus"`
				} `json:"TimeFrame"`
				AccountName struct {
					Name               string `json:"name"`
					Value              string `json:"value"`
					ConfirmationStatus string `json:"confirmationStatus"`
				} `json:"AccountName"`
			} `json:"slots"`
		} `json:"intent"`
		DialogState string `json:"dialogState"`
	} `json:"request"`
}

type Configuration struct {
	Host     string
	User     string
	Password string
	Database string
	Port     int
}

var config Configuration
var db *sql.DB

func init() {
	log.Println("Loading config file from ./config.json")
	file, e := ioutil.ReadFile("./config.json")
	if e != nil {
		log.Printf("File error loading config: %v", e)
		os.Exit(1)
	}

	json.Unmarshal(file, &config)
}

func setupDb() {
	log.Println("Setting up database with credentials")
	var err error

	db_string := fmt.Sprintf("host=%s user=%s password=%s dbname=%s sslmode=disable",
		config.Host, config.User, config.Password, config.Database)
	db, err = sql.Open("postgres", db_string)

	if err != nil {
		log.Fatalf("Couldn't open a db connection successfully with error: %v", err)
	}
}

func main() {
	log.Println("starting server")
	setupDb()

	http.HandleFunc("/piper/", alexaHandler)
	http.HandleFunc("/piper/spending/", getSpending)
	http.ListenAndServe(":8081", nil)
}

/*
* this is responsible for returning a balance for a given account and timeframe
* 	requires query parameters @timeframe and @account
 */
func getSpending(w http.ResponseWriter, r *http.Request) {
	log.Println("Received request on getSpending with params:", r.URL.Query())

	timeframe := r.URL.Query().Get("timeframe")
	account := r.URL.Query().Get("account")

	log.Printf("Received timeframe: %s and account: %s", timeframe, account)

	// query the account to make sure it exists
	rows, err := db.Query("SELECT id, name, category FROM balances where name like '%' || $1 || '%'", account)
	if err != nil {
		log.Fatalf("Failed executing account query with error: %v", err)
	}

	for rows.Next() {
		var id int
		var name string
		var category string
		err = rows.Scan(&id, &name, &category)

		fmt.Println("Received id: %d and name: %s", id, name)
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
}

func alexaHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("Received request: ", r.URL.Path[1:])
	log.Println("Method type: ", r.Method)

	defer r.Body.Close()
	request_body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		return
	}

	// time to serialize into object
	var request AlexaRequest
	err = json.Unmarshal(request_body, &request)
	if err != nil {
		log.Fatalf("unmarshal error:", err)
	}

	var outputText = fmt.Sprintf("Hello, you asked about money spent on %s for %s",
		request.Request.Intent.Slots.AccountName.Value,
		request.Request.Intent.Slots.TimeFrame.Value)

	response := AlexaResponse{Version: "1.0"}
	response.Response.OutputSpeech.Type = "PlainText"
	response.Response.OutputSpeech.Text = outputText

	log.Println("body: ", string(request_body))

	response_string, _ := json.Marshal(response)
	io.WriteString(w, string(response_string))
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
}
