import paho.mqtt.client as mqtt
import socket
import json
import requests
import threading
from datetime import datetime

IP = "192.168.0.24"
PORT = 8520
MQTT_BROKER_PORT = 1883
BASE_URL = f"http://{IP}:{PORT}"
MQTT_TOPIC = "management"

# client = mqtt.Client()
# client.connect(IP, MQTT_BROKER_PORT, 60)


def open_session() -> str:
    """Opens a session on the attestation server. The session is used to 
    store multiple requests eg. attest or verify requests.

    Returns
    -------
    string
        session as a JSON string.
    """
    response = requests.post(f"{BASE_URL}/v2/sessions/open")
    if response.ok:
        return response.json()
    else:
        return ''


def close_session(id):
    """
    Closes the request provided as a parameter

    Parameters
    ----------
    id : string
        id of the session to be closed.

    """

    # TODO: change this to return something when successful.
    close = requests.delete(f"{BASE_URL}/v2/session/{id}")
    return close


def get_policy_id() -> str:
    """
    Retrieves the policy id from the API.

    Returns
    -------
    string
        policy id as a string.
    """
    response = requests.get(
        f"{BASE_URL}/v2/policy/name/TPMIdentityAttestation")

    if response.ok:
        return response.json()['itemid']
    else:
        return ''


def create_dict(payload, sid) -> dict:
    """
    Creates a dictionary with the necessary information.

    The data is retrieved from the API and the values are stored in the correct
    place for the attestation to be successful.

    Returns
    -------
    dict 
        the newly created dictionary.
    """
    if payload["device"]["hostname"]:
        hostname = payload["device"]["hostname"]
    else:
        return {}
    response = requests.get(f"{BASE_URL}/v2/element/name/{hostname}")

    if not response.ok:
        return {}

    element = response.json()

    tpm = element["tpm2"]["tpm0"]
    eid = element["itemid"]

    pid = get_policy_id()

    akname = tpm["ekname"]
    ekpub = tpm["ekpem"]
    cps = {"a10_tpm_send_ssl": element["a10_tpm_send_ssl"],
           "akname": akname, "ekpub": ekpub}

    o = {"eid": eid, "pid": pid, "cps": cps, "sid": sid}

    print(o)

    return o


def attest(o: dict) -> str:
    """
    Main function for the attestation procedure. Posts given object to the
    /v2/attest endpoint.

    Parameters
    ----------
    o : dict 
        dictionary with the necessary fields for attest.
    """
    response = requests.post(f"{BASE_URL}/v2/attest",
                             json=o, headers={"Content-Type": "application/json"})
    if response.ok:
        return response.json()
    else:
        return ''


def verify(o: dict) -> str:
    """
    Verifies the given dictionary. Makes a POST request to the API which then
    verifies the data.

    Parameters
    ----------
    o : dict
        dictionary with the data to be verified.

    Returns
    -------
    string
        JSON object.
    """
    response = requests.post(
        f"{BASE_URL}/v2/verify", headers={"Content-Type": "application/json"}, data=json.dumps(o))

    if response.ok:
        return response.json()
    else:
        return ''


def check_validity(payload: dict):
    """
    Main function of the program. Creates a dictionary from data gathered from the API
    and verifies it. The ruleset is currently hard-coded as a TPM2CredentialVerify but
    this could be changed in the future. Publishes the results to the MQTT topic set as
    a constant.

    Parameters
    ----------
    payload : dict
        this is currently unused.
    """
    # These still need to have error handling implemented.
    # MQTT error messages to be sent.
    sid = open_session()

    o = create_dict(payload, sid)

    if not o:
        payload.update({"event": "device validation fail"})
        # payload.update({"valid": False})
        payload["device"]["valid"] = False
        payload.update({"message": "object creation failed"})
        # client.publish(MQTT_TOPIC, json.dumps(payload))
        return payload

    cid = attest(o)

    if not cid:
        payload.update({"event": "device validation fail"})
        # payload.update({"valid": False})
        payload["device"]["valid"] = False
        payload.update({"message": "attestation failed"})
        # client.publish(MQTT_TOPIC, json.dumps(payload))
        return json.dumps(payload)

    rul = ["tpm2rules/TPM2CredentialVerify", {}]

    o.update({"cid": cid['claim']})
    # This needed?
    o.update({"sid": sid})
    o.update({"rule": rul})

    result = verify(o)

    if not result:
        return {"error": "verification failed"}

    o.update({"result": result["result"]})

    close_session(sid)

    # payload.update({"valid": True})
    payload["device"]["valid"] = True
    payload.update({"itemid": o.get("eid")})
    payload.update({"event": "device validation ok"})
    payload.update({"message": "validation successful"})
    payload["timestamp"] = datetime.now().strftime("%d.%m.%Y, %H:%M:%S")

    print(payload)

    # client.publish(MQTT_TOPIC, json.dumps(payload))
    return payload


def run():
    """
    Runs all the things. Set the MQTT client to listen on the management channel.
    When message is received, start a new thread which does the attestation and
    verification. 
    """
#    def on_connect(client, userdata, flags, rc):
#        client.subscribe("management/verify")
#
#    def on_message(client, userdata, msg):
#        print(msg.payload)
#        x = threading.Thread(target=check_validity(json.loads(msg.payload)))
#        x.start()

    # client.on_message = on_message
    # client.on_connect = on_connect
    # client.loop_forever()
