package main

import (
	"log"
	"net/http"
	"os"

	"github.com/couchbasecloud/rest-api-examples/go/utils"
)

type BucketCreatePayload struct {
	Name        string `json:"name"`
	MemoryQuota int    `json:"memoryQuota"`
}

func main() {
	if len(os.Args) != 3 {
		log.Fatal("usage: go run main.go <cluster-id> <bucket-name>")
	}

	c := utils.NewClient()

	payload := BucketCreatePayload{
		Name:        os.Args[2],
		MemoryQuota: 128,
	}

	resp, err := c.Do(http.MethodPost, "/v2/clusters/"+os.Args[1]+"/buckets", payload)
	if err != nil {
		log.Fatal(err)
	}

	_ = utils.PrettyPrint(resp)
}
