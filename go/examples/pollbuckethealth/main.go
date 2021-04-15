package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/couchbasecloud/rest-api-examples/go/utils"
)

const (
	BucketStatusHealthy = "healthy"
)

type HealthResponse struct {
	BucketStats struct {
		HealthStats    map[string]string `json:"healthStats"`
		Status         string            `json:"status"`
		TotalCount     int               `json:"totalCount"`
		UnhealthyCount int               `json:"unhealthyCount"`
	} `json:"bucketStats"`
}

func main() {
	if len(os.Args) != 3 {
		log.Fatal("usage: go run main.go <cluster-id> <bucket-name>")
	}

	c := utils.NewClient()

	var (
		health         string
		healthResponse HealthResponse
	)

	for health != BucketStatusHealthy {
		resp, err := c.Do(http.MethodGet, "/v2/clusters/"+os.Args[1]+"/health", nil)
		if err != nil {
			log.Fatal(err)
		}

		if err := utils.Unmarshal(resp.Body, &healthResponse); err != nil {
			log.Fatal(err)
		}

		health = healthResponse.BucketStats.HealthStats[os.Args[2]]
		if health == "" {
			health = "N/A"
		}

		fmt.Printf(`{"bucket":"%s","health":"%s"}`+"\n", os.Args[2], health)
		time.Sleep(time.Second * 5)
	}

	resp, err := c.Do(http.MethodGet, "/v2/clusters/"+os.Args[1]+"/health", nil)
	if err != nil {
		log.Fatal(err)
	}

	_ = utils.PrettyPrint(resp)
}
