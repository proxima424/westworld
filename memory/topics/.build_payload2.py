import base64, json

with open('memory/topics/anomalies.md', 'rb') as f:
    content = f.read()

payload = {
    "message": "anomalies: document lost-update race between concurrent Contents-API commits",
    "content": base64.b64encode(content).decode(),
    "sha": "8296daaba04d1b9df4434f54f5a71c220f79a90d",
    "branch": "main",
    "author": {"name": "Aeon", "email": "aeon@westworld.park"},
    "committer": {"name": "Aeon", "email": "aeon@westworld.park"},
}

with open('memory/topics/.anomalies-payload2.json', 'w') as f:
    json.dump(payload, f)

print("written")
