package main

import (
	"cloud.google.com/go/pubsub"
	"encoding/json"
	"fmt"
	"golang.org/x/net/context"
	"golang.org/x/oauth2"
	"golang.org/x/oauth2/google"
	"google.golang.org/api/gmail/v1"
	"google.golang.org/api/script/v1"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"
)

var (
	topic *pubsub.Topic

	gmailService  gmail.Service
	scriptService script.Service

	scriptConfig ScriptConfig
)

const maxMessages = 10

func main() {
	log.Println("Loading credentials from JSON")
	file, e := ioutil.ReadFile("./oauth_tokens.json")
	if e != nil {
		log.Printf("File error: %v\n", e)
		os.Exit(1)
	}
	var creds OauthResponse
	json.Unmarshal(file, &creds)

	scriptsFile, e := ioutil.ReadFile("./scripts.json")
	if e != nil {
		log.Printf("Scripts file error: %v\n", e)
		os.Exit(1)
	}
	json.Unmarshal(scriptsFile, &scriptConfig)

	ctx := context.Background()

	config := &oauth2.Config{
		ClientID:     creds.ClientID,
		ClientSecret: creds.ClientSecret,
		Endpoint:     google.Endpoint,
		Scopes:       []string{gmail.GmailReadonlyScope, script.MailGoogleComScope, script.DriveScope, "https://www.googleapis.com/auth/script.external_request"},
	}

	token := new(oauth2.Token)
	token.AccessToken = creds.AccessToken
	token.RefreshToken = creds.RefreshToken
	token.Expiry = creds.TokenExpiry
	token.TokenType = creds.TokenResponse.TokenType
	httpClient := config.Client(ctx, token)

	gmailService, err := gmail.New(httpClient)
	if err != nil {
		log.Fatal(err)
	}

	scriptService, err := script.New(httpClient)
	if err != nil {
		log.Fatal(err)
	}

	handleHistory(gmailService, scriptService, "me", 6451994)

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

type HistoryObject struct {
	EmailAddress string `json:"emailAddress"`
	HistoryID    uint64 `json:"historyId"`
}

type ScriptConfig struct {
	ScriptID string `json:"scriptId"`
}

type OauthResponse struct {
	TokenResponse struct {
		RefreshToken string `json:"refresh_token"`
		AccessToken  string `json:"access_token"`
		ExpiresIn    int    `json:"expires_in"`
		TokenType    string `json:"token_type"`
	} `json:"token_response"`
	TokenURI     string    `json:"token_uri"`
	Scopes       []string  `json:"scopes"`
	AccessToken  string    `json:"access_token"`
	TokenExpiry  time.Time `json:"token_expirty"`
	RefreshToken string    `json:"refresh_token"`
	RevokeURI    string    `json:"revoke_uri"`
	ClientID     string    `json:"client_id"`
	ClientSecret string    `json:"client_secret"`
}

func triggerScript(service *script.Service, messageId string) {

	new := make([]interface{}, 1)
	new[0] = messageId

	req := script.ExecutionRequest{
		Function:   "myFunction",
		Parameters: new,
	}

	resp, err := service.Scripts.Run(scriptConfig.ScriptID, &req).Do()
	if err != nil {
		log.Fatalf("Unable to execute Apps Script function. %v", err)
	}

	log.Printf("Response: %v", string(resp.Response))
}

func handleHistory(service *gmail.Service, scriptServ *script.Service, userId string, historyId uint64) {
	req := service.Users.History.List(userId).StartHistoryId(historyId).LabelId("Label_34").HistoryTypes("labelAdded")

	r, err := req.Do()
	if err != nil {
		log.Fatalf("Unable to retrieve history: %v", err)
	}

	log.Printf("Processing %v history records...\n", len(r.History))

	for _, h := range r.History {
		for _, m := range h.LabelsAdded {
			log.Printf("Personal receipt added on message with id: %s", m.Message.Id)

			triggerScript(scriptServ, m.Message.Id)
		}
	}
}

func pushHandler(w http.ResponseWriter, r *http.Request) {
	msg := &pushRequest{}
	if err := json.NewDecoder(r.Body).Decode(msg); err != nil {
		http.Error(w, fmt.Sprintf("Could not decode body: %v", err), http.StatusBadRequest)
		return
	}

	log.Printf("Received new message: %s", string(msg.Message.Data))
	log.Printf("Received ID message: %s", msg.Message.ID)

	var history HistoryObject
	json.Unmarshal(msg.Message.Data, &history)
	log.Printf("Message id here: %s", history.HistoryID)

	handleHistory(&gmailService, &scriptService, "me", history.HistoryID)
}
