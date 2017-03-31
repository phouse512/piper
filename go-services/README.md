### go-services

This area is the test for new go services that support piper and personal data
flows. See below for instructions and deployment.

#### email subscriber

the current code in `subscriber.go` that is responsible for listening to Google
Cloud's pub/sub service. To run, it requires that the credentials are set
correctly on your running machine. If not already set up, use `gcloud auth
application-default login` to get the credentials locally. This also requires
the `gcloud` sdk installed on your machine.

To build, run `go build` from inside this directory.

To run, there are a couple of environment variables that must be set:
`GCLOUD_PROJECT` and `PUBSUB_TOPIC`. Example usage is here:

```
GCLOUD_PROJECT=<google project id> PUBSUB_TOPIC=<pubsub_topic_name> ./go-services
```

#### watch curl

This is the curl used to tell the Gmail API to send push notifications to our
pubsub setup:

```
curl -H "Content-Type: application/json" -H "Authorization: Bearer <api_key_here>"
-X POST -d '{"topicName":
"<topic_name>", "labelIds": ["INBOX"]}'
https://www.googleapis.com/gmail/v1/users/me/watch | jq .
```
