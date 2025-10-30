from transformers import AutoProcessor, AutoModelForCausalLM
import torch
from PIL import Image

model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    attn_implementation="sdpa"
)
processor = AutoProcessor.from_pretrained(model_id)

image = Image.open("homework.png").convert("RGB")
prompt = "Describe this image in one sentence."

inputs = processor(images=image, text=prompt, return_tensors="pt").to(model.device)
out = model.generate(**inputs, max_new_tokens=64)
print(processor.decode(out[0], skip_special_tokens=True))
