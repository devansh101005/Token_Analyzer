import tiktoken


def estimate_tokens(text: str) -> int:
    """
    Estimate token count for models where exact tokenization is not available.
    Industry-standard approximation: ~4 chars per token.
    """
    return max(1, len(text) // 4)

def get_tokenizer(model_info):
    """
    Returns the correct tokenizer for OpenAI models.
    Uses encoding_for_model for new models,
    and get_encoding for tokenizer families like cl100k_base.
    """
    tokenizer = model_info.get("tokenizer")

    # If tokenizer is a known encoding name
    if tokenizer in ["cl100k_base", "p50k_base", "r50k_base"]:
        return tiktoken.get_encoding(tokenizer)

    # Otherwise treat it as model name
    return tiktoken.encoding_for_model(tokenizer)