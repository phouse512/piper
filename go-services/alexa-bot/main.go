package main

import (
	"io/ioutil"
	"log"
	"net/http"
)

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

	log.Println("body: ", string(request_body))
}
