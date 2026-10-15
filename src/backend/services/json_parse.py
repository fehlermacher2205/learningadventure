import json
def safe_parse_llm(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print("\n=== FAILED TO PARSE LLM RESPONSE ===")
        print(f"RAW TEXT:\n{text}")
        print("====================================\n")
        raise e
    
