package tallyclient

import (
	"fmt"
	"log"
	"net"
)

type Client struct {
	host string
	port int
	conn net.Conn
}

func NewClient(host string, port int) (client *Client, error error) {
	c := new(Client)
	c.host = host
	c.port = port

	conn, err := net.Dial("tcp", fmt.Sprintf("%s:%d", host, port))
	if err != nil {
		log.Println("Received an error while trying to connect")
		return nil, err
	}

	c.conn = conn
	return c, nil
}

func (c *Client) Count(name string) {
	fmt.Fprintf(c.conn, fmt.Sprintf("c:%s:%d\n", name, 1))
}

func (c *Client) Gauge(name string, val int64) {
	fmt.Fprintf(c.conn, fmt.Sprintf("g:%s:%d\n", name, val))
}
