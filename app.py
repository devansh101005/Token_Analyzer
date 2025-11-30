import streamlit as st
import tiktoken

st.set_page_config(page_title="GPT Token Analyzer", layout="wide")

st.title("GPT Token Analyzer")

# Text input
text = st.text_area("Enter your text", height=200)

# Model selector
model = st.selectbox(
    "Select Model",
    ["gpt-4o", "gpt-4o-mini"]
)

if st.button("Analyze"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        enc = tiktoken.encoding_for_model(model)

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

        cost = (len(tokens) / 1_000_000) * PRICE_PER_1M[model]
        st.write(f"**Estimated Cost:** ${cost:.4f}")

        compare = st.checkbox("Compare with gpt-4o-mini tokenizer")

        if compare:
            enc2 = tiktoken.encoding_for_model("gpt-4o-mini")
            tokens2 = enc2.encode(text)
            st.write(f"**gpt-4o-mini tokens:** {len(tokens2)}")
