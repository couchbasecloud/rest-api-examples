package main

import (
	"log"
	"net/http"
	"os"

	"github.com/couchbasecloud/rest-api-examples/go/utils"
)

func main() {
	if len(os.Args) != 2 {
		log.Fatal("usage: go run main.go <project-name>")
	}

	c := utils.NewClient()

	resp, err := c.Do(http.MethodDelete, "/v2/projects/"+os.Args[1], nil)
	if err != nil {
		log.Fatal(err)
	}

	_ = utils.PrettyPrint(resp)
}
