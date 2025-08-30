# file: app/main.py
from fastapi import FastAPI, HTTPException
from .schemas import InventionInput
from . import agent
import datetime
import uuid
import json

app = FastAPI(title="LeanPatentAgent")

@app.post("/generate")
def generate_patent(inp: InventionInput):
    """
    Endpoint to generate a patent draft from an invention description.
    """
    try:
        final_json = agent.run_patent_agent(inp)
        return final_json
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
