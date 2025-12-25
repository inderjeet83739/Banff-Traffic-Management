import json
from typing import Dict, Any
import pandas as pd
import requests

MODEL_NAME = "qwen2.5:3b"
OLLAMA_HOST = "http://192.168.1.109:11434"  # cámbialo si usas ollama.aquiles.online


def _run_ollama(prompt: str) -> str:
    """Call Ollama HTTP API and return the raw text response."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    resp = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json=payload,
        timeout=60,
        verify=False
    )
    resp.raise_for_status()
    data = resp.json()
    return data["response"]


def build_answer(
    question: str,
    intent: str,
    df: pd.DataFrame,
    slots: Dict[str, Any]
) -> str:
    """
    Use the LLM to generate a natural language answer
    based ONLY on the SQL result table + user question + intent.
    """

    if df is None or df.empty:
        return "I could not find any data in the database for that question."

    # Limit rows/columns so the prompt doesn't explode
    df_limited = df.head(20).copy()
    table_dict = df_limited.to_dict(orient="records")
    columns = list(df_limited.columns)

    table_json = json.dumps(table_dict, default=str)

    prompt = f"""
You are a data assistant for the Banff parking and mobility project.

You receive:
1) The user's natural language question.
2) The selected SQL intent.
3) A small table with the SQL result (rows + columns).
4) Some extracted slots (such as hour, date, weather).

Your job:
- Explain the answer in clear, simple English.
- Base your answer ONLY on the table data provided.
- Do NOT invent numbers or dates that are not in the table.
- If the table does not contain enough information, clearly say that.
- If the question is about occupancy, visitors, residents, or vehicles,
  make sure you mention the key numbers and any obvious pattern.
- Be concise (2–4 sentences).

USER QUESTION:
{question}

INTENT:
{intent}

SLOTS:
{json.dumps(slots, default=str)}

SQL RESULT COLUMNS:
{columns}

SQL RESULT ROWS (JSON list of records):
{table_json}

Now, answer the user in English using only this data.
"""

    try:
        answer = _run_ollama(prompt).strip()
        return answer
    except Exception as e:
        # Fallback very simple answer if the LLM fails
        first_row = df_limited.iloc[0].to_dict()
        return (
            "I had a problem contacting the language model, "
            "but here is the first row of data I found: "
            f"{first_row}"
        )
