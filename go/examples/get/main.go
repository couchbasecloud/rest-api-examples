package main

import (
	"log"
	"net/http"
	"os"

	"github.com/couchbasecloud/rest-api-examples/go/utils"
)

type AllowListRequest struct {
	CIDR     string `json:"cidrBlock"`
	RuleType string `json:"ruleType"`
}

func main() {
	if len(os.Args) != 2 {
		log.Fatal("usage: go run main.go <endpoint>")
	}

	c := utils.NewClient()

	resp, err := c.Do(http.MethodGet, os.Args[1], nil)
	if err != nil {
		log.Fatal(err)
	}

	_ = utils.PrettyPrint(resp)
}
