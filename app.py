import streamlit as st
import tiktoken

MODEL_CONFIG = {
    # ======================
    # OPENAI (Exact tokens)
    # ======================
    "GPT-4o": {
        "provider": "openai",
        "model_name": "gpt-4o",
        "tokenizer": "gpt-4o",
        "price_per_1m": 5.00,
        "exact_tokens": True
    },
    "GPT-4o Mini": {
        "provider": "openai",
        "model_name": "gpt-4o-mini",
        "tokenizer": "gpt-4o-mini",
        "price_per_1m": 0.15,
        "exact_tokens": True
    },
    "GPT-4 Turbo (Legacy)": {
        "provider": "openai",
        "model_name": "gpt-4-turbo",
        "tokenizer": "cl100k_base",
        "price_per_1m": 10.00,
        "exact_tokens": True
    },
    "GPT-3.5 Turbo": {
        "provider": "openai",
        "model_name": "gpt-3.5-turbo",
        "tokenizer": "cl100k_base",
        "price_per_1m": 0.50,
        "exact_tokens": True
    },

    # ======================
    # GOOGLE GEMINI (Estimated tokens)
    # ======================
    "Gemini 1.5 Flash": {
        "provider": "google",
        "model_name": "gemini-1.5-flash",
        "price_per_1m": 0.35,
        "exact_tokens": False
    },
    "Gemini 1.5 Pro": {
        "provider": "google",
        "model_name": "gemini-1.5-pro-001",
        "price_per_1m": 3.50,
        "exact_tokens": False
    },

    # ======================
    # ANTHROPIC CLAUDE (Estimated tokens)
    # ======================
    "Claude 3.5 Sonnet": {
        "provider": "anthropic",
        "model_name": "claude-3-5-sonnet-20240620",
        "price_per_1m": 3.00,
        "exact_tokens": False
    },
    "Claude 3 Haiku": {
        "provider": "anthropic",
        "model_name": "claude-3-haiku-20240307",
        "price_per_1m": 0.25,
        "exact_tokens": False
    }
}




#st.caption(f"Tokenizer used: `{model_info['tokenizer']}`")


st.set_page_config(page_title="GPT Token Analyzer", layout="wide")

st.title("GPT Token Analyzer")

# Text input
text = st.text_area("Enter your text", height=200)

st.subheader("Prompt Playground")

system_prompt = st.text_area(
    "System Prompt",
    placeholder="e.g. You are a helpful AI tutor who explains simply.",
    height=120
)

user_prompt = st.text_area(
    "User Prompt",
    placeholder="e.g. Explain how transformers work.",
    height=120
)

combined_prompt = ""

if system_prompt.strip():
    combined_prompt += f"System: {system_prompt}\n\n"

if user_prompt.strip():
    combined_prompt += f"User: {user_prompt}"

if not combined_prompt.strip():
    combined_prompt = text  # fallback to old text box

input_text = combined_prompt


def estimate_tokens(text: str) -> int:
    # industry standard heuristic
    return max(1, len(text) // 4)

def get_tokenizer(model_info):
    tokenizer = model_info.get("tokenizer")

    # If tokenizer is a known encoding name
    if tokenizer in ["cl100k_base", "p50k_base", "r50k_base"]:
        return tiktoken.get_encoding(tokenizer)

    # Otherwise treat it as model name
    return tiktoken.encoding_for_model(tokenizer)



# Model selector
# model = st.selectbox(
#     "Select Model",
#     ["gpt-4o", "gpt-4o-mini"]
# )
selected_model = st.selectbox(
    "Select Model",
    list(MODEL_CONFIG.keys())
)



if st.button("Analyze"):
    if not input_text.strip():
        st.warning("Please enter some text.")
    else:
        #enc = tiktoken.encoding_for_model(model)
        model_info = MODEL_CONFIG[selected_model]

        # try:
        #     enc = tiktoken.encoding_for_model(model_info["tokenizer"])
        # except KeyError:
        #     enc = tiktoken.get_encoding(model_info["tokenizer"])
        #
        # tokens = enc.encode(text)
        # decoded = enc.decode(tokens)
        if model_info["exact_tokens"]:
            #enc = tiktoken.encoding_for_model(model_info["tokenizer"])
            enc = get_tokenizer(model_info)
            tokens = enc.encode(input_text)
            token_count = len(tokens)
        else:
            tokens = None
            token_count = estimate_tokens(input_text)
            st.warning("⚠ Token count is an estimate for this model.")


        with st.expander("View Combined Prompt"):
            st.code(input_text, language="text")


        col1, col2 = st.columns(2)

        # with col1:
        #     st.subheader("Results")
        #     st.write(f"**Token Count:** {len(tokens)}")
        #     st.write("**Tokens (IDs):**")
        #     st.write(tokens)
        #
        # with col2:
        #     st.subheader("Token Breakdown")
        #     for t in tokens:
        #         st.code(f"{t} → '{enc.decode([t])}'")
        with col1:
            st.subheader("Results")
            st.write(f"**Token Count:** {token_count}")

            if tokens is not None:
                st.write("**Tokens (IDs):**")
                st.write(tokens)

        with col2:
            st.subheader("Token Breakdown")
            if tokens is not None:
                for t in tokens:
                    st.code(f"{t} → '{enc.decode([t])}'")
            else:
                st.info("Token breakdown not available for this model.")

        PRICE_PER_1M = {
            "gpt-4o": 5.00,
            "gpt-4o-mini": 0.15
        }

        # cost = (len(tokens) / 1_000_000) * PRICE_PER_1M[model]
        # st.write(f"**Estimated Cost:** ${cost:.4f}")
        #token_count = len(tokens)


        cost = (token_count / 1_000_000) * model_info["price_per_1m"]

        #st.write(f"**Token Count:** {token_count}")
        st.write(f"**Estimated Cost:** ${cost:.6f}")

        #compare = st.checkbox("Compare with gpt-4o-mini tokenizer")
        if model_info["provider"] == "openai":
            compare = st.checkbox("Compare with gpt-4o-mini tokenizer")

            if compare:
                enc2 = tiktoken.encoding_for_model("gpt-4o-mini")
                tokens2 = enc2.encode(input_text)
                st.write(f"**gpt-4o-mini tokens:** {len(tokens2)}")

