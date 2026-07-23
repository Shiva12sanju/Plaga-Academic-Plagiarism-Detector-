from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import torch
import math

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

model.eval()


def calculate_perplexity(text):

    if not text.strip():
        return 0

    text = text[:1000]

    encodings = tokenizer(
        text,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model(
            encodings.input_ids,
            labels=encodings.input_ids
        )

    loss = outputs.loss

    ppl = math.exp(loss.item())

    return round(ppl,2)