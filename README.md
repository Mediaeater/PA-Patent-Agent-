# Lean Patent Agent

This project provides a framework for an AI-powered agent that assists in drafting patent applications. The "LeanPatentAgent" takes an invention description as input and generates a structured patent draft, including claims, descriptions, and other sections.

The agent is designed to be used with a large language model (LLM) and follows a multi-step orchestration process to generate the different parts of the patent application.

## Project Structure

The project is structured as a FastAPI application:

```
.
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI application and endpoint
│   ├── agent.py        # Core agent orchestration logic
│   ├── schemas.py      # Pydantic models for API I/O
│   ├── prompts.py      # Prompts for the LLM
│   └── utils.py        # Helper functions (e.g., quality checks, exporters)
├── patent-agent.txt    # The original specification document
└── README.md
```

## Getting Started

### Prerequisites

*   Python 3.8+
*   An API key for a large language model (e.g., OpenAI, Anthropic)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Implement the LLM Call

Before you can run the application, you need to implement the `LLM_CALL` function in `app/agent.py`. This function is responsible for making the actual API call to your chosen language model.

Open `app/agent.py` and replace the `NotImplementedError` in the `LLM_CALL` function with your LLM API call logic. For example, if you are using the OpenAI API, your implementation might look like this:

```python
# file: app/agent.py
import openai

def LLM_CALL(system_prompt: str, user_prompt: str, temperature=0.0):
    """
    This is a placeholder for the actual LLM call.
    You need to implement this function to call your language model.
    """
    openai.api_key = "YOUR_OPENAI_API_KEY"  # It's better to use environment variables for keys

    response = openai.ChatCompletion.create(
        model="gpt-4",  # or another model of your choice
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )
    return response.choices[0].message['content']
```

### Running the Application

Once you have implemented the `LLM_CALL` function, you can run the FastAPI application using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## API Usage

You can interact with the agent by sending a POST request to the `/generate` endpoint. The API documentation is available at `http://127.0.0.1:8000/docs`.

### Example Request

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/generate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "AI-guided drone for crop health monitoring",
  "readme_content": "A drone uses hyperspectral imaging and an on-device model to detect crop disease in real time, sends geo-tagged alerts, and autonomously replans flight path to re-scan hotspots.",
  "prior_art": [],
  "inventor": ["Alice Inventor"],
  "jurisdiction": "USPTO"
}'
```

This will return a JSON object containing the full patent draft.
