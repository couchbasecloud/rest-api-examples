package main

import (
	"log"
	"net/http"
	"os"

	"github.com/couchbasecloud/rest-api-examples/go/utils"
)

type UserCreatePayload struct {
	Username string             `json:"username"`
	Password string             `json:"password"`
	Access   []UserCreateAccess `json:"access"`
}

type UserCreateAccess struct {
	Name  string   `json:"name"`
	Roles []string `json:"roles"`
}

func main() {
	if len(os.Args) != 5 {
		log.Fatal("usage: go run main.go <cluster-id> <username> <password> <bucket>")
	}

	c := utils.NewClient()

	payload := UserCreatePayload{
		Username: os.Args[2],
		Password: os.Args[3],
		Access: []UserCreateAccess{
			{
				Name:  os.Args[4],
				Roles: []string{"data_writer", "data_reader"},
			},
		},
	}

	resp, err := c.Do(http.MethodPost, "/v2/clusters/"+os.Args[1]+"/users", payload)
	if err != nil {
		log.Fatal(err)
	}

	_ = utils.PrettyPrint(resp)
}
