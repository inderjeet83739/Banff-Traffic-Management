from fastapi import FastAPI
from intent_classifier import classify_sql_intent
from sql_templates import SQL_TEMPLATES
from db import run_sql
from llm_sql_answer import build_answer

# -----------------------------------------
# FastAPI APP  (debe ir ANTES de los @app)
# -----------------------------------------
app = FastAPI()

# -----------------------------------------
# Chat endpoint
# -----------------------------------------
@app.post("/chat")
def chat(payload: dict):
    question = payload["question"]

    # 1. Classify intent
    result = classify_sql_intent(question)
    intent = result["intent"]
    slots = result.get("slots", {})

    # 2. Build SQL query
    sql = SQL_TEMPLATES[intent].format(**slots)

    # 3. Execute SQL
    df = run_sql(sql)

    # 4. Generate natural language answer using LLM
    answer = build_answer(question, intent, df, slots)

    return {
        "answer": answer,
        "sql": sql,
        "intent": intent,
        "slots": slots
    }
