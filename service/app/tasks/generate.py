from openai import OpenAI
from app.models import ComfortBotParams
from app.config import Config, Paths

data_path = Paths.RESOURCES_DIR.joinpath("persona.txt")
prompt = open(data_path, "r", encoding="utf-8").read()
client = OpenAI(api_key=Config.OPENAI_API_KEY)


class Comfort:
    def __init__(self, params):
        self.params: ComfortBotParams = params

    @staticmethod
    def remove_after_last_punctuation(text):
        last_punc_index = max(text.rfind("."), text.rfind("?"), text.rfind("!"))
        if last_punc_index != -1:
            text = text[: last_punc_index + 1]
        return text

    def generate(self):
        messages = [{"role": "system", "content": prompt}]
        messages += self.params.records
        messages.append({"role": "user", "content": self.params.utterance})

        response = client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo-0125",
            max_tokens=100,
            temperature=0.6,
        )
        print(messages)
        response = response.choices[0].message.content

        if len(response) > 60:
            response = Comfort.remove_after_last_punctuation(response)

        return response
