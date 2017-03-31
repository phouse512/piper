package main

import (
	"cloud.google.com/go/pubsub"
	"encoding/json"
	"fmt"
	"golang.org/x/net/context"
	"log"
	"net/http"
	"os"
	"sync"
)

var (
	topic *pubsub.Topic

	messagesMu sync.Mutex
	messages   []string
)

const maxMessages = 10

func main() {
	fmt.Println("vim-go")

	ctx := context.Background()

	client, err := pubsub.NewClient(ctx, mustGetenv("GCLOUD_PROJECT"))
	if err != nil {
		log.Fatal(err)
	}

	topic, _ = client.CreateTopic(ctx, mustGetenv("PUBSUB_TOPIC"))

	http.HandleFunc("/pubsub/push", pushHandler)
	http.ListenAndServe(":8082", nil)
}

func mustGetenv(k string) string {
	v := os.Getenv(k)
	if v == "" {
		log.Fatalf("%s environment variable not set.", k)
	}

	return v
}

type pushRequest struct {
	Message struct {
		Attributes map[string]string
		Data       []byte
		ID         string `json:"message_id"`
	}
}

func pushHandler(w http.ResponseWriter, r *http.Request) {
	msg := &pushRequest{}
	if err := json.NewDecoder(r.Body).Decode(msg); err != nil {
		http.Error(w, fmt.Sprintf("Could not decode body: %v", err), http.StatusBadRequest)
		return
	}

	messagesMu.Lock()
	defer messagesMu.Unlock()

	messages = append(messages, string(msg.Message.Data))
	log.Printf("Received new message: %s", string(msg.Message.Data))
}
