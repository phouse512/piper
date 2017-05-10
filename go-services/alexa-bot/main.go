package main

import (
	"encoding/json"
	"io"
	"io/ioutil"
	"log"
	"net/http"
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

	response := AlexaResponse{Version: "1.0"}
	response.Response.OutputSpeech.Type = "PlainText"
	response.Response.OutputSpeech.Text = "Hello there, Philip"

	log.Println("body: ", string(request_body))

	response_string, _ := json.Marshal(response)
	io.WriteString(w, string(response_string))
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
}
