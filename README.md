# Token_Analyzer

**Overview**
- **Project:**: `Token_Analyzer` — a lightweight Streamlit app for counting and estimating tokens and cost for several LLM models.
- **Primary file:**: `app.py` — Streamlit UI and token-count logic.

**What it does**
- Loads text or a prompt (system + user), tokenizes it using `tiktoken` when an exact tokenizer is available, and shows:
  - Token count
  - Token IDs and decoded token text (when available)
  - Estimated cost for the selected model
  - A fallback token-estimate heuristic for models where exact tokenizers are not available

**Supported models (from `app.py`)**
- OpenAI (exact token counts when `tiktoken` supports the tokenizer):
  - `GPT-4o` (`gpt-4o`) — price per 1M: $5.00
  - `GPT-4o Mini` (`gpt-4o-mini`) — price per 1M: $0.15
  - `GPT-4 Turbo (Legacy)` (`gpt-4-turbo`) — tokenizer: `cl100k_base`, price per 1M: $10.00
  - `GPT-3.5 Turbo` (`gpt-3.5-turbo`) — tokenizer: `cl100k_base`, price per 1M: $0.50
- Google / Anthropic (estimated tokens — app uses a heuristic):
  - `Gemini 1.5 Flash` — estimated price per 1M: $0.35
  - `Gemini 1.5 Pro` — estimated price per 1M: $3.50
  - `Claude 3.5 Sonnet` — estimated price per 1M: $3.00
  - `Claude 3 Haiku` — estimated price per 1M: $0.25

**Tokenization behavior**
- If the selected model's `MODEL_CONFIG` has `exact_tokens: True`, the app will attempt to use the `tiktoken` encoding returned by `tiktoken.get_encoding(...)` or `tiktoken.encoding_for_model(...)` (via `get_tokenizer()` in `app.py`) to calculate an exact token count and display token breakdowns.
- For models marked `exact_tokens: False`, the app uses a simple heuristic: each token ≈ 4 characters (i.e., `len(text) // 4`) as a conservative estimate and displays a warning that the value is estimated.

Cost formula used in the app:

```
cost = (token_count / 1_000_000) * price_per_1m
```

**Setup and Run**

Prerequisites
- Python 3.8+ (the app uses `streamlit` and `tiktoken`).
- A virtual environment is recommended.

Install dependencies
1. Create and activate a virtual environment (PowerShell examples):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install requirements:

```powershell
pip install -r requirements.txt
```

Run the app

```powershell
streamlit run app.py
```

**Usage**

- Open the Streamlit URL shown in the terminal (usually `http://localhost:8501`).
- Enter your text in the main text box OR use the Prompt Playground to enter a `System Prompt` and a `User Prompt`. The app will combine these when both are provided.
- Select a model from the `Select Model` dropdown and click `Analyze`.
- When `exact_tokens` is True for the selected model, you'll see token IDs and a token breakdown. When False, you'll see an estimated token count and a warning.
- If the selected model is an OpenAI model, there's an optional checkbox to compare token counts with the `gpt-4o-mini` tokenizer.

**Troubleshooting**

- If `tiktoken` raises a `KeyError` while trying to resolve an encoding, the app attempts to call `tiktoken.get_encoding(...)` for known encoding names (like `cl100k_base`). If you encounter other encoding names that `tiktoken` does not support, update the `MODEL_CONFIG` in `app.py` to provide a supported tokenizer or set `exact_tokens` to `False` for that model.
- If Streamlit or `tiktoken` fails to import, ensure your environment is activated and `pip install -r requirements.txt` completed without errors.

**Files of interest**

- `app.py` — main Streamlit app that includes `MODEL_CONFIG`, input UI, tokenization & cost logic.
- `requirements.txt` — Python dependencies used by the project (install with `pip`).

**Notes for maintainers / contributions**

- The token model list and pricing is defined in the `MODEL_CONFIG` dictionary inside `app.py`. Update that dictionary to add/remove models or to change prices.
- Keep the `exact_tokens` flag aligned to whether `tiktoken` provides a reliable tokenizer for the model.
- If you add models with custom tokenizers, update `get_tokenizer()` in `app.py` accordingly.

**License**

- Will update soon

**Contact / Further improvements**

- Consider adding tests for the tokenizer fallback behavior and for cost calculations.
- Optionally add a small example `texts/` folder containing sample prompts for quick testing.

Enjoy! — Open `app.py` and run the Streamlit app to analyze tokens for your prompts and text.
