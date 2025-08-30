# file: app/agent.py
import json
import datetime
import uuid
from . import prompts
from .schemas import InventionInput

def LLM_CALL(system_prompt: str, user_prompt: str, temperature=0.0):
    """
    This is a placeholder for the actual LLM call.
    You need to implement this function to call your language model
    (e.g., OpenAI's GPT, Anthropic's Claude, etc.).

    Args:
        system_prompt: The system prompt to guide the LLM.
        user_prompt: The user prompt with the specific instructions.
        temperature: The temperature for the LLM call.

    Returns:
        The raw text response from the LLM.
    """
    raise NotImplementedError("Plug your LLM API here. For example, use the openai library.")

def run_patent_agent(inp: InventionInput):
    """
    Runs the LeanPatentAgent orchestration.
    """
    # 1) normalize input
    data = inp.dict()
    data['date'] = data.get('date') or datetime.date.today().isoformat()
    data['meta_id'] = str(uuid.uuid4())

    # 2) PREPROCESS
    try:
        pre_response = LLM_CALL(prompts.SYSTEM_PROMPT, prompts.PREPROCESS_PROMPT.format(input_json=json.dumps(data)), temperature=0.0)
        preprocess_json = json.loads(pre_response)
    except Exception as e:
        raise Exception(f"Preprocess failed: {e}")

    data['preprocess'] = preprocess_json

    # 3) DRAFT
    try:
        draft_resp = LLM_CALL(prompts.SYSTEM_PROMPT, prompts.DRAFT_PROMPT.format(input_json=json.dumps(data)), temperature=0.0)
        draft_json = json.loads(draft_resp)['draft']
    except Exception as e:
        raise Exception(f"Draft failed: {e}")

    data['draft'] = draft_json

    # 4) REASON
    try:
        reason_resp = LLM_CALL(prompts.SYSTEM_PROMPT, prompts.REASON_PROMPT.format(input_json=json.dumps(data)), temperature=0.0)
        reason_json = json.loads(reason_resp)['reasoning']
    except Exception as e:
        reason_json = {"novelty_assessment":{"verdict":"Unclear","confidence":0.0,"reasons":[str(e)]}}

    data['reasoning'] = reason_json

    # 5) QUALITY
    try:
        quality_resp = LLM_CALL(prompts.SYSTEM_PROMPT, prompts.QUALITY_PROMPT.format(input_json=json.dumps(data)), temperature=0.0)
        quality_json = json.loads(quality_resp)['quality']
    except Exception as e:
        quality_json = {"overall_pass": False, "fixes":[str(e)]}

    data['quality'] = quality_json

    # 6) ASSEMBLE
    try:
        assemble_resp = LLM_CALL(prompts.SYSTEM_PROMPT, prompts.ASSEMBLE_PROMPT.format(input_json=json.dumps(data)), temperature=0.0)
        final_json = json.loads(assemble_resp)
    except Exception as e:
        raise Exception(f"Assemble failed: {e}")

    # optionally export to docx/xml (can be called asynchronously in your infra)
    final_json['audit'] = {"model":"YOUR_MODEL", "temperature":0.0}
    return final_json
