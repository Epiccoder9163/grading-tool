import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor

model_id = "google/gemma-3-12b-pt"  # Multimodal: image-text-to-text

# Choose one of the two load configs:

USE_4BIT = True  # set False to try bfloat16 unquantized

if USE_4BIT:
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        attn_implementation="flash_attention_2",  # if available; otherwise remove
    )
    dtype = torch.bfloat16
else:
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        attn_implementation="flash_attention_2",  # if available; otherwise remove
    )
    dtype = torch.bfloat16

processor = AutoProcessor.from_pretrained(model_id)

# Load an image
image = Image.open("example.jpg").convert("RGB")

# Your multimodal prompt (instruction + question)
prompt = (
    "You are a helpful vision-language assistant. "
    "Describe the key elements of this image and infer the likely context.\n"
)

# Prepare inputs (image + text) for Gemma 3
inputs = processor(
    images=image,
    text=prompt,
    return_tensors="pt",
).to(model.device)

# Optional: set generation params
gen_kwargs = {
    "max_new_tokens": 256,
    "temperature": 0.7,
    "top_p": 0.9,
}

with torch.no_grad():
    output_ids = model.generate(**inputs, **gen_kwargs)

# Decode output
# Some processors expose a tokenizer; use processor to decode when available
text = processor.tokenizer.decode(
    output_ids[0],
    skip_special_tokens=True
)

# If the decode includes the original prompt, strip it; Gemma often returns full context
# A simple heuristic:
response = text[len(prompt):].strip() if text.startswith(prompt) else text
print(response)
