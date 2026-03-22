import os
from flask import Blueprint, request, jsonify
from google import genai

from dotenv import load_dotenv

load_dotenv()

summarize_blueprint = Blueprint('summarize', __name__)

# -------- GEMINI -------- #
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None
MODEL = "gemini-2.5-flash"

# -------- LOCAL MODEL -------- #
tokenizer = None
local_model = None


def load_local_model():
    global tokenizer, local_model
    if tokenizer is None:
        print("⚠️ Loading local T5 model...")
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        tokenizer = AutoTokenizer.from_pretrained("t5-small")
        local_model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")


def local_summarize(text):
    load_local_model()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    outputs = local_model.generate(inputs.input_ids, max_length=100)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def summarize_text(texts):
    summaries = []

    for text in texts:
        text = text[:3000]

        # ---- GEMINI FIRST ---- #
        if client:
            try:
                prompt = f"Summarize in 3-4 sentences:\n\n{text}"
                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt
                )

                if response.text:
                    summaries.append(response.text)
                    continue

            except Exception as e:
                print("Gemini failed:", e)

        # ---- FALLBACK ---- #
        try:
            summaries.append(local_summarize(text))
        except Exception as e:
            summaries.append(f"Failed: {e}")

    return summaries


@summarize_blueprint.route("/", methods=["POST"])
def summarize():
    data = request.get_json()

    if not data or "texts" not in data:
        return jsonify({"error": "Provide a list of texts"}), 400

    return jsonify({"summaries": summarize_text(data["texts"])})
