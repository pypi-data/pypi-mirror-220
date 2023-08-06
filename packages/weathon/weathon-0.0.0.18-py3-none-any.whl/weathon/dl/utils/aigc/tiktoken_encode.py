import tiktoken
from tiktoken import Encoding
from typing import Dict

def tiktoken_encode(model:str="gpt-3.5-turbo", prompt:str="this is a test") -> Dict:
    assert model and prompt, "model name or prompt must not be empty!"
    encoding:Encoding = tiktoken.encoding_for_model(model)
    assert encoding, f"unknown encoding, model={model}"

    tokens = encoding.encode(prompt)
    return dict(model=model, prompt=prompt, token_len=len(tokens), tokens=tokens)

if __name__ == "__main__":
    tiktoken_encode(model="gpt-3.5-turbo", prompt="this is a test , i like apple")