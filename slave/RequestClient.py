#! /usr/bin/python3
import json
import requests
import netifaces as ni
from uuid import getnode as get_mac

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


def get_ip():
    return ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']


def remote_call(payload):
    url = "http://localhost:5001"
    headers = {'content-type':'application/json'}
    return requests.post(url, data = json.dumps(payload), headers=headers).json()


def main():
    payload = make_payload(
        "registerNode",
        {
            "ip": get_ip(),
            "mac": hex(get_mac())
        }
    )
    response = remote_call(payload)

    #assert response["result"] == 3
    assert response["jsonrpc"]
    assert response["id"] == 0

if __name__ == "__main__":
    main()
