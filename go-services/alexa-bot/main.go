package main

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
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

func main() {
	log.Println("starting server")

	http.HandleFunc("/piper/", alexaHandler)
	http.ListenAndServe(":8081", nil)
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
