import paho.mqtt.client as mqtt
import socket
import json
import requests
import threading

HOSTNAME = socket.gethostname()
IP = "192.168.11.79"
PORT = 8520
MQTT_BROKER_PORT = 1883
BASE_URL = f"http://{IP}:{PORT}"
MQTT_TOPIC = f"alert/{HOSTNAME}"

with open("/etc/iotDevice.json") as f:
    data = json.load(f)

ITEM_ID = data["item_id"]

client = mqtt.Client()
client.connect(IP, MQTT_BROKER_PORT, 60)


def open_session():
    session = requests.post(f"{BASE_URL}/v2/sessions/open")
    return session.json()


def close_session(id):
    close = requests.delete(f"{BASE_URL}/v2/session/{id}")
    print(close.text)


def get_policy_id():
    pid = requests.get(
        f"{BASE_URL}/v2/policy/name/TPMIdentityAttestation").json()
    return pid["itemid"]


def create_object():
    element = requests.get(f"{BASE_URL}/v2/element/name/{HOSTNAME}").json()
    tpm = element["tpm2"]["tpm0"]
    eid = element["itemid"]

    pid = get_policy_id()
    sid = open_session()

    akname = tpm["ekname"]
    ekpub = tpm["ekpem"]
    cps = {"a10_tpm_send_ssl": element["a10_tpm_send_ssl"],
           "akname": akname, "ekpub": ekpub}

    obj = {"eid": eid, "pid": pid, "cps": cps, "sid": sid}

    return obj


def attest(obj):
    claim = requests.post(f"{BASE_URL}/v2/attest",
                          json=obj, headers={"Content-Type": "application/json"})
    return claim.json()


def verify(obj):
    response = requests.post(
        f"{BASE_URL}/v2/verify", headers={"Content-Type": "application/json"}, data=json.dumps(obj))
    return response.json()


def check_validity(payload):
    o = create_object()
    session_id = o["sid"]["itemid"]

    cid = attest(o)["claim"]

    rul = ["tpm2rules/TPM2CredentialVerify", {}]

    o.update({"cid": cid})
    o.update({"sid": session_id})
    o.update({"rule": rul})

    result = verify(o)

    o.update({"result": result["result"]})

    close_session(session_id)

    client.publish(MQTT_TOPIC, json.dumps(o))


def run():
    def on_connect(client, userdata, flags, rc):
        client.subscribe("management")

    def on_message(client, userdata, msg):
        x = threading.Thread(target=check_validity(msg.payload))
        x.start()

    client.on_message = on_message
    client.on_connect = on_connect
    client.loop_forever()


if __name__ == '__main__':
    run()
