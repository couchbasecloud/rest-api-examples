package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/couchbasecloud/rest-api-examples/go/utils"
)

const (
	ClusterStatusReady = "ready"
)

type ClusterResponse struct {
	ID     string `json:"id"`
	Name   string `json:"name"`
	Status string `json:"status"`
}

func main() {
	clusterID := os.Args[1]
	if clusterID == "" {
		log.Fatal("usage: go run main.go <cluster-id>")
	}

	c := utils.NewClient()
	var clusterResponse ClusterResponse

	for clusterResponse.Status != ClusterStatusReady {
		resp, err := c.Do(http.MethodGet, "/v2/clusters/"+clusterID, nil)
		if err != nil {
			log.Fatal(err)
		}

		if err := utils.Unmarshal(resp.Body, &clusterResponse); err != nil {
			log.Fatal(err)
		}

		b, err := json.Marshal(clusterResponse)
		if err != nil {
			log.Fatal(err)
		}

		fmt.Println(string(b))
		time.Sleep(time.Second * 5)
	}

	resp, err := c.Do(http.MethodGet, "/v2/clusters/"+clusterID, nil)
	if err != nil {
		log.Fatal(err)
	}

	_ = utils.PrettyPrint(resp)
}
