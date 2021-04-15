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
	if len(os.Args) != 3 {
		log.Fatal("usage: go run main.go <cluster-id> <ip>")
	}

	c := utils.NewClient()

	payload := AllowListRequest{
		CIDR:     os.Args[2],
		RuleType: "permanent",
	}

	resp, err := c.Do(http.MethodPost, "/v2/clusters/"+os.Args[1]+"/allowlist", payload)
	if err != nil {
		log.Fatal(err)
	}

	_ = utils.PrettyPrint(resp)
}
