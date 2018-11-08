#! /usr/bin/python3
import json
import requests
import netifaces as ni
from uuid import getnode as get_mac
import codeversion from lead.codeversion

class ClientNode:
    leadIP = "172.24.1.1"
    leadReqestPort = "5001"
    leadCommunicationPort = "5002"

    def __init__(self, port):
        self.register()

    def start(self):
        # Starts the communication service as a server
        run_simple(get_ip(),leadCommunicationPort,application)

    def read_file(self, filepath):
        file = open(filepath, "rb").read()
        return file

    def make_payload(self, method, params):
        return {
            "method":method,
            "params":params,
            "jsonrpc":"2.0",
            "id":0,
        }

    def get_ip(self):
        return ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

    def remote_call(self, payload):
        url = "http://"+self.leadIP+":"+self.leadReqestPort
        headers = {'content-type':'application/json'}
        return requests.post(url, data = json.dumps(payload), headers=headers).json()

    def getCodeVersion():
        pass

    def register(self):
        payload = make_payload(
            "registerNode",
            {
                "ip": get_ip(),
                "mac": hex(get_mac()),
                "code": getCodeVersion()
            }
        )
        response = remote_call(payload)

        #assert response["result"] == 3
        # assert response["jsonrpc"]
        # assert response["id"] == 0

#SERVER PART START
    @dispatcher.add_method
    def write_file(**kwargs):
        TO = os.getcwd()+"\\"+kwargs["filename"]
        file = open(TO, "ab")
        file.write(kwargs["bytes"])
        file.close()
        # IF TRUE AND X > 0 ASK FOR RANDOM NODE REPLICACE TO THAT
        # ELSE RETURN
        return "success"

    @dispatcher.add_method
    def read_file(**kwargs):
        return read_file(kwargs["filename"])

    @dispatcher.add_method
    def delete_file(**kwargs):
        os.remove(kwargs["filename"])
        return "success"

    @Request.application
    def application(request):
        response = JSONRPCResponseManager.handle(request.data, dispatcher)
        print(request.data)
        return Response(response.json,mimetype='application/json')
#SERVER PART END

if __name__ == "__main__":
    client = ClientNode(5000)
    register()
    client.start()
