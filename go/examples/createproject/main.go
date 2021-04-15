package main

import (
	"log"
	"net/http"
	"os"

	"github.com/couchbasecloud/rest-api-examples/go/utils"
)

type ProjectCreatePayload struct {
	Name string `json:"name"`
}

func main() {
	if len(os.Args) != 2 {
		log.Fatal("usage: go run main.go <project-name>")
	}

	c := utils.NewClient()

	payload := ProjectCreatePayload{
		Name: os.Args[1],
	}

	resp, err := c.Do(http.MethodPost, "/v2/projects", payload)
	if err != nil {
		log.Fatal(err)
	}

	_ = utils.PrettyPrint(resp)
}
