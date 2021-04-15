package utils

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"

	"github.com/couchbasecloud/rest-api-examples/go/client"
)

func NewClient() *client.Client {
	return client.New(os.Getenv("BASE_URL"), os.Getenv("ACCESS_KEY"), os.Getenv("SECRET_KEY"))
}

func PrettyPrint(resp *http.Response) error {
	rb, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	if len(rb) == 0 {
		fmt.Printf(`{"status":"%d"}`+"\n", resp.StatusCode)
		return nil
	}

	fmt.Printf(`{"status":"%d","results":%s}`+"\n", resp.StatusCode, string(rb))
	return nil
}

func Unmarshal(body io.Reader, v interface{}) error {
	rb, err := ioutil.ReadAll(body)
	if err != nil {
		return err
	}

	return json.Unmarshal(rb, v)
}
