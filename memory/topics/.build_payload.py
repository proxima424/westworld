import base64, json

with open('memory/topics/anomalies.md', 'rb') as f:
    content = f.read()

payload = {
    "message": "anomalies: note base64 approval friction during applicant-triage",
    "content": base64.b64encode(content).decode(),
    "sha": "ca93b7c48a21d47f49e5da02dfb0ad917c8e8fc9",
    "branch": "main",
    "author": {"name": "Aeon", "email": "aeon@westworld.park"},
    "committer": {"name": "Aeon", "email": "aeon@westworld.park"},
}

with open('memory/topics/.anomalies-payload.json', 'w') as f:
    json.dump(payload, f)

print("written")
