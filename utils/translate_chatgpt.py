import openai
import os
from dotenv import load_dotenv

# .env файлыг ачааллана
load_dotenv()

# API key-г авах
openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_to_mongolian(text: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Та англи өгүүлбэрийг зөвхөн Монгол хэл рүү орчуулна."},
                {"role": "user", "content": f"Орчуул: {text}"}
            ],
            temperature=0.3
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"❌ Орчуулгын алдаа: {e}")
        return text
