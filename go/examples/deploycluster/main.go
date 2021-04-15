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

type ProjectCreateResponse struct {
	Name string `json:"name"`
	ID   string `json:"id"`
}

type ClusterCreatePayload struct {
	Name      string                `json:"name"`
	CloudID   string                `json:"cloudId"`
	ProjectID string                `json:"projectId"`
	Servers   []ClusterCreateServer `json:"servers"`
}

type ClusterCreateServer struct {
	Size     int                    `json:"size"`
	Services []string               `json:"services"`
	Aws      ClusterCreateServerAWS `json:"aws"`
}

type ClusterCreateServerAWS struct {
	InstanceSize string `json:"instanceSize"`
	EbsSizeGib   int    `json:"ebsSizeGib"`
}

func main() {
	if len(os.Args) != 4 {
		log.Fatal("usage: go run main.go <cloud-id> <project-name> <cluster-name>")
	}

	c := utils.NewClient()

	projectCreatePayload := ProjectCreatePayload{
		Name: os.Args[2],
	}

	resp, err := c.Do(http.MethodPost, "/v2/projects", projectCreatePayload)
	if err != nil {
		log.Fatal(err)
	}

	var projectResponse ProjectCreateResponse
	if err := utils.Unmarshal(resp.Body, &projectResponse); err != nil {
		log.Fatal(err)
	}

	clusterCreatePayload := ClusterCreatePayload{
		Name:      os.Args[3],
		CloudID:   os.Args[1],
		ProjectID: projectResponse.ID,
		Servers: []ClusterCreateServer{
			{
				Size:     3,
				Services: []string{"data", "index", "query"},
				Aws: ClusterCreateServerAWS{
					InstanceSize: "m5.2xlarge",
					EbsSizeGib:   50,
				},
			},
		},
	}

	resp, err = c.Do(http.MethodPost, "/v2/clusters", clusterCreatePayload)
	if err != nil {
		log.Fatal(err)
	}

	loc := resp.Header.Get("location")
	resp, err = c.Do(http.MethodGet, loc, nil)
	if err != nil {
		log.Fatal(err)
	}

	_ = utils.PrettyPrint(resp)
}
