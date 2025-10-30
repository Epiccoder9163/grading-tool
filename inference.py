import torch
from transformers import Qwen3VLForConditionalGeneration, AutoProcessor
from PIL import Image

# LLM used in Transformers
model = "Qwen/Qwen3-VL-8B-Instruct"

# LLM prompt
prompt = "Describe this image"

# Confirm ROCm is active
print("HIP version:", torch.version.hip)
print("CUDA available:", torch.cuda.is_available())
print("Device name:", torch.cuda.get_device_name(0))

# Initialize vLLM
vllm = Qwen3VLForConditionalGeneration.from_pretrained(
    model,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    attn_implementation="sdpa",  # use PyTorch's ROCm-optimized attention
 )

# Initialize processor
processor = AutoProcessor.from_pretrained("Qwen/Qwen3-VL-8B-Instruct")

def run(image):
    messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": image,
            },
            {"type": "text", "text": prompt},
        ],
    }
]