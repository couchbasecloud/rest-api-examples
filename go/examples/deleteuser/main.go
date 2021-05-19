package main

import (
	"log"
	"net/http"
	"os"

	"github.com/couchbasecloud/rest-api-examples/go/utils"
)

func main() {
	if len(os.Args) != 3 {
		log.Fatal("usage: go run main.go <cluster-id> <username>")
	}

	c := utils.NewClient()

	resp, err := c.Do(http.MethodDelete, "/v2/clusters/"+os.Args[1]+"/users/"+os.Args[2], nil)
	if err != nil {
		log.Fatal(err)
	}

	_ = utils.PrettyPrint(resp)
}
