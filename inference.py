import torch
from transformers import AutoTokenizer, AutoModel
from PIL import Image

# Confirm ROCm is active
print("HIP version:", torch.version.hip)
print("CUDA available:", torch.cuda.is_available())
print("Device name:", torch.cuda.get_device_name(0))

def run(image):
    # Load model
    model_name = "deepseek-ai/DeepSeek-OCR"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModel.from_pretrained(
        model_name,
        trust_remote_code=True,
        torch_dtype=torch.float16,
        device_map="auto",
        attn_implementation="flash_attention_2"
    )

    # Load and process image
    image = Image.open(image).convert("RGB")
    inputs = tokenizer(image, return_tensors="pt").to("cuda")
    outputs = model(**inputs)

    # Decode result
    decoded = tokenizer.batch_decode(outputs.logits.argmax(dim=-1), skip_special_tokens=True)
    return(decoded)