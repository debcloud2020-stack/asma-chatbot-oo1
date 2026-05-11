# Azure AI Foundry Chatbot (Python + Streamlit)

A minimal, working chatbot that connects to an Azure AI Foundry model deployment and serves a chat UI in the browser.

## Project structure

```
foundry-chatbot/
├── app/
│   ├── main.py             # Streamlit UI (the chat page)
│   ├── foundry_client.py   # Wrapper around the Foundry API
│   └── config.py           # Loads env vars
├── .env.example            # Copy to .env and fill in your keys
├── .gitignore
├── requirements.txt
└── README.md
```

## Step 1 — Get your Foundry credentials

1. Go to **Azure AI Foundry portal** → `https://ai.azure.com`
2. Open (or create) your **project**.
3. In the left nav: **Models + endpoints** → deploy a model (e.g. `gpt-4o-mini`). Note the **deployment name**.
4. Click the deployment → copy:
   - **Target URI / Endpoint** (looks like `https://<resource>.openai.azure.com/`)
   - **Key** (one of the two API keys)

## Step 2 — Set up VS Code locally

1. Install **Python 3.10+** and **VS Code**.
2. In VS Code install extensions: *Python*, *Pylance*.
3. Open a terminal in VS Code (`Ctrl+` `` ` ``) and run:

```bash
git clone <or create folder>  foundry-chatbot
cd foundry-chatbot
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

## Step 3 — Configure secrets

```bash
cp .env.example .env      # macOS/Linux
copy .env.example .env    # Windows
```

Edit `.env` and paste in your real endpoint, key, and deployment name.

## Step 4 — Run it

```bash
streamlit run app/main.py
```

Browser opens at `http://localhost:8501`. Type a question in the chat input and the bot replies.

## How it works

- **`app/main.py`** — Streamlit page. Stores message history in `st.session_state`, renders the chat with `st.chat_message`, takes input with `st.chat_input`.
- **`app/foundry_client.py`** — Thin wrapper on the `openai` SDK using `AzureOpenAI`. Maintains conversation history so each turn has context.
- **`app/config.py`** — Loads env vars via `python-dotenv` and validates the required ones are present.

## Customizing

- **Change the bot's personality**: edit `SYSTEM_PROMPT` in `.env`.
- **Different model**: deploy another model in Foundry and update `MODEL_DEPLOYMENT_NAME`.
- **Tuning**: use the sidebar sliders for temperature / max tokens.

## Troubleshooting

| Error | Fix |
|---|---|
| `Missing required environment variables` | Check `.env` exists in project root and has values. |
| `401 Unauthorized` | Wrong API key or endpoint. Re-copy from Foundry portal. |
| `DeploymentNotFound` | `MODEL_DEPLOYMENT_NAME` must match the *deployment name* in Foundry, not the model name. |
| `streamlit: command not found` | Activate your venv, then `pip install -r requirements.txt`. |
