# resume_parser.py — LOCAL INFERENCE WITH TINYLLAMA (1.1B)

import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from utils.text_extractor import extract_text_from_pdf, extract_text_from_docx
from utils.validator import extract_json_from_response, normalize_skills, clean_social_media

# Model ID for TinyLlama 1.1B Chat
MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Load tokenizer and model ONCE at startup
tokenizer = None
model = None

def load_model():
    """Load model and tokenizer once to avoid reloading on every request."""
    global tokenizer, model
    if tokenizer is None or model is None:
        print("🔄 Loading TinyLlama-1.1B-Chat-v1.0... (This may take 30-60 seconds)")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16,  # Use half precision to save memory
            device_map="auto",          # Automatically uses GPU if available
            trust_remote_code=True
        )
        print("✅ TinyLlama loaded successfully!")

def parse_resume(file_path: str) -> dict:
    # Step 1: Extract text from PDF or DOCX
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Only .pdf and .docx supported")

    # Step 2: Load prompt template
    with open(os.path.join("models", "llama3_prompt_template.txt"), "r") as f:
        prompt_template = f.read()
    prompt = prompt_template.format(resume_text=text)

    # Step 3: Load model if not already loaded
    load_model()

    # Step 4: Format input for TinyLlama chat template
    messages = [
        {"role": "system", "content": "You are a resume parser. Return only JSON."},
        {"role": "user", "content": prompt}
    ]

    # Apply chat template and tokenize
    input_ids = tokenizer.apply_chat_template(
        messages,
        return_tensors="pt",
        add_generation_prompt=True
    ).to(model.device)

    # Step 5: Generate response
    outputs = model.generate(
        input_ids,
        max_new_tokens=1024,
        temperature=0.1,
        top_p=0.9,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id
    )

    # Step 6: Decode output (skip input prompt)
    response = tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)

    # Step 7: Extract JSON from response
    try:
        raw_data = extract_json_from_response(response)
    except Exception as e:
        raise ValueError(f"Failed to parse JSON from LLM response: {e}")

    # Step 8: Post-process
    raw_data["skills"] = normalize_skills(raw_data.get("skills", []))
    raw_data["social_media"] = clean_social_media(raw_data.get("social_media", {}))

    return raw_data