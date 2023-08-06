import subprocess
import requests
from requests.auth import HTTPDigestAuth
import json
import traceback
from OntimDevTool import G_auth_server
from OntimDevTool import G_secure_access
from OntimDevTool import get_password

def get_device_id():
    ret = subprocess.run(['fastboot', 'oem', 'get_device_id'], capture_output=True, timeout=5)
    device_id = ret.stderr.decode('ascii').split('\n')[0].split('(bootloader) ')[1].strip()
    print(f"Get device id: {device_id}")
    return device_id


def sign(project, data):
    print("Waiting for sign from anth server...")

    header = {"Content-Type": "application/json"}
    try:
        if G_secure_access:
            auth = HTTPDigestAuth("admin", get_password())
            ret = requests.get(G_auth_server + "Token/", auth = auth)
            token = json.loads(ret.content.decode('ascii'))['token']
            header["Authorization"] = "Bearer "+ token

        payload = {"project": project, "data": data}
        ret = requests.post(G_auth_server + "SignDIAG/", headers = header, data = json.dumps(payload))

        sign_resp = json.loads(ret.content.decode('ascii'))['data']
        #print(f"sign diag success, resp = {sign_resp}")
    except Exception as ex:
        print(traceback.print_exc())
        raise Exception(f"Failed to get the signature!!! Auth Server returns:\n{ret.content}")

    return sign_resp

def set_diag_port(data):
    if data:
        # open diag
        dia_tmp_file = "diag.bin"
        with open(dia_tmp_file, "w") as tmp_file:
            tmp_file.write(data)

        ret = subprocess.run(['fastboot', 'flash', 'diag', dia_tmp_file], capture_output=True, timeout=5)
        if ret.stderr.decode('ascii').find("Finished. Total time:") != -1:
            return True
        else:
            raise Exception(ret.stderr.decode('ascii'))
    else:
        # close diag
        ret = subprocess.run(['fastboot', 'oem', 'diag_lock'], capture_output=True, timeout=5)
        if ret.stderr.decode('ascii').find("Finished. Total time:") != -1:
            return True
        else:
            raise Exception(ret.stderr.decode('ascii'))

def open_diag_port(project):
    print("Please go into fastboot mode...")
    device_id = get_device_id()
    sigature = sign(project, device_id + "DIAG_ENABLE")
    ret = set_diag_port(sigature)
    if ret:
        print("Success to open the Diag Port.")
    else:
        print("Failed to open the Diag Port.")
    return ret

def close_diag_port():
    ret = set_diag_port(None)
    if ret:
        print("Success to close the Diag port.")
    else:
        print("Failed to close the Diag Port.")
    return ret


if __name__ == "__main__":
    open_diag_port("crusader_tf")
    # close_diag_port()
