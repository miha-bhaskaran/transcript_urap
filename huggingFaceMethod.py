import os
from unittest.mock import patch
from transformers import AutoProcessor, AutoModelForCausalLM, dynamic_module_utils
import requests
from PIL import Image

# Define the fixed_get_imports function
def fixed_get_imports(filename: str | os.PathLike) -> list[str]:
    """Work around for https://huggingface.co/microsoft/phi-1 5/discussions/72."""
    if not str(filename).endswith("/modeling_florence2.py"):
        return original_get_imports(filename)
    imports = original_get_imports(filename)
    if "flash_attn" in imports:
        imports.remove("flash_attn")
    return imports

# Save the original get_imports function
original_get_imports = dynamic_module_utils.get_imports

# Patch the get_imports function
model_id = 'microsoft/Florence-2-large'
with patch("transformers.dynamic_module_utils.get_imports", fixed_get_imports):
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

# Load image
url = "https://transcriptmiha.s3.us-east-2.amazonaws.com/trans/page-2.png"
image = Image.open(requests.get(url, stream=True).raw)

# Define the run_example function
def run_example(task_prompt, text_input=None):
    if text_input is None:
        prompt = task_prompt
    else:
        prompt = task_prompt + text_input
    inputs = processor(text=prompt, images=image, return_tensors="pt")
    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=1024,
        num_beams=3
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    parsed_answer = processor.post_process_generation(generated_text, task=task_prompt, image_size=(image.width, image.height))
    print(parsed_answer)

# Call the run_example function
prompt = "<OCR>"
run_example(prompt)

