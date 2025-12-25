import json
import requests

MODEL_NAME = "qwen2.5:3b"
OLLAMA_HOST = "http://192.168.1.109:11434"

def classify_sql_intent(question: str):
    prompt = f"""
You are a SQL intent classifier for Banff parking analytics.
Your job: return a JSON with "intent" + "slots".

INTENTS:
- total_vehicles_anytime
- visitors_anytime
- residents_anytime
- total_occupancy_at_time
- occupancy_by_weather
- occupancy_by_hour
- peak_occupancy_day
- low_occupancy_day

SLOTS:
Extract: date, start, end, hour, weather, temp.

Return ONLY valid JSON.
Question: {question}
"""

    res = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
        timeout=40,
        verify=False
    )

    raw = res.json()["response"]

    try:
        return json.loads(raw)
    except:
        return {"intent": "total_vehicles_anytime", "slots": {}}
