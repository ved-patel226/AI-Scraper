from ollama import chat
import re


class LLM_CHAT:
    def __init__(self, model="deepseek-r1:8b"):
        self.model = model

    def get_response(self, text, screenshot=None):

        stream = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": text,
                    "images": ["screenshot.png"],
                }
            ],
            stream=True,
        )

        res = []

        for chunk in stream:
            print(chunk["message"]["content"], end="", flush=True)
            res.append(chunk["message"]["content"])

        res = "".join(res)

        res = re.sub(r"<think>.*?</think>", "", res, flags=re.DOTALL)
        print("\n")

        return res.strip()
