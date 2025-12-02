import streamlit as st
import tiktoken

MODEL_CONFIG = {
    "GPT-4o": {
        "model_name": "gpt-4o",
        "tokenizer": "gpt-4o",
        "price_per_1m": 5.00
    },
    "GPT-4o Mini": {
        "model_name": "gpt-4o-mini",
        "tokenizer": "gpt-4o-mini",
        "price_per_1m": 0.15
    },
    "GPT-4 Turbo (legacy)": {
        "model_name": "gpt-4-turbo",
        "tokenizer": "cl100k_base",
        "price_per_1m": 10.00
    },
    "GPT-3.5 Turbo": {
        "model_name": "gpt-3.5-turbo",
        "tokenizer": "cl100k_base",
        "price_per_1m": 0.50
    }
}


#st.caption(f"Tokenizer used: `{model_info['tokenizer']}`")


st.set_page_config(page_title="GPT Token Analyzer", layout="wide")

st.title("GPT Token Analyzer")

# Text input
text = st.text_area("Enter your text", height=200)

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
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        #enc = tiktoken.encoding_for_model(model)
        model_info = MODEL_CONFIG[selected_model]

        try:
            enc = tiktoken.encoding_for_model(model_info["tokenizer"])
        except KeyError:
            enc = tiktoken.get_encoding(model_info["tokenizer"])

        tokens = enc.encode(text)
        decoded = enc.decode(tokens)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Results")
            st.write(f"**Token Count:** {len(tokens)}")
            st.write("**Tokens (IDs):**")
            st.write(tokens)

        with col2:
            st.subheader("Token Breakdown")
            for t in tokens:
                st.code(f"{t} → '{enc.decode([t])}'")

        PRICE_PER_1M = {
            "gpt-4o": 5.00,
            "gpt-4o-mini": 0.15
        }

        # cost = (len(tokens) / 1_000_000) * PRICE_PER_1M[model]
        # st.write(f"**Estimated Cost:** ${cost:.4f}")
        token_count = len(tokens)

        cost = (token_count / 1_000_000) * model_info["price_per_1m"]

        st.write(f"**Token Count:** {token_count}")
        st.write(f"**Estimated Cost:** ${cost:.6f}")

        compare = st.checkbox("Compare with gpt-4o-mini tokenizer")

        if compare:
            enc2 = tiktoken.encoding_for_model("gpt-4o-mini")
            tokens2 = enc2.encode(text)
            st.write(f"**gpt-4o-mini tokens:** {len(tokens2)}")
