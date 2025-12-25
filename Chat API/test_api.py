import requests

API = "http://localhost:8081/chat"

tests = [
    "How many visitors were there today?"
]

for q in tests:
    print("\n➡️ QUESTION:", q)
    res = requests.post(API, json={"question": q})
    print("STATUS:", res.status_code)
    print("RAW:", res.text)   # <--- ESTO ES LO IMPORTANTE