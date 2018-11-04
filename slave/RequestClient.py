import requests
import json

LeadIP = "localhost"
LeadReqestPort = "5001"

def read_file(filepath):
    file = open(filepath, "rb").read()
    return file

def make_payload(method,params):
    return {
        "method":method,
        "params":params,
        "jsonrpc":"2.0",
        "id":0,
    }

def remote_call(payload):
    url = "http://localhost:5001"
    headers = {'content-type':'application/json'}
    return requests.post(url, data = json.dumps(payload), headers=headers).json()

def main():
    payload = make_payload("registerNode",{"ip":"192.168.0.99"})
    response = remote_call(payload)

    #assert response["result"] == 3
    assert response["jsonrpc"]
    assert response["id"] == 0

if __name__ == "__main__":
    main()
