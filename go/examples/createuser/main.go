package main

import (
	"log"
	"net/http"
	"os"

	"github.com/couchbasecloud/rest-api-examples/go/utils"
)

type UserCreatePayload struct {
	Username         string             `json:"username,omitempty"`
	Password         string             `json:"password,omitempty"`
	AllBucketsAccess string             `json:"allBucketsAccess,omitempty"`
	Buckets          []UserCreateAccess `json:"buckets,omitempty"`
}

type UserCreateAccess struct {
	Name  string   `json:"bucketName"`
	Roles []string `json:"bucketAccess"`
}

func main() {
	if len(os.Args) != 5 {
		log.Fatal("usage: go run main.go <cluster-id> <username> <password> <bucket>")
	}

	c := utils.NewClient()

	perBucket := UserCreatePayload{
		Username: os.Args[2],
		Password: os.Args[3],
		Buckets: []UserCreateAccess{
			{
				Name:  os.Args[4],
				Roles: []string{"data_writer"},
			},
		},
	}

	resp, err := c.Do(http.MethodPut, "/v2/clusters/"+os.Args[1]+"/users", perBucket)
	if err != nil {
		log.Fatal(err)
	}

	_ = utils.PrettyPrint(resp)

	allBucket := UserCreatePayload{
		AllBucketsAccess: "data_reader",
	}

	resp, err = c.Do(http.MethodPut, "/v2/clusters/"+os.Args[1]+"/users/"+os.Args[2], allBucket)
	if err != nil {
		log.Fatal(err)
	}

	_ = utils.PrettyPrint(resp)
}
