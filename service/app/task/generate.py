import requests
from requests.exceptions import Timeout

from app.models import ComfortBotParams
from app.config import Config, Paths
from app.task import Singleton

data_path = Paths.RESOURCES_DIR.joinpath("persona.txt")
prompt = open(data_path, "r", encoding="utf-8").read()


class CompletionExecutor(metaclass=Singleton):
    def __init__(self):
        self._host = Config.HOST

    def execute(self, completion_request, max_retries=2):
        headers = {
            "X-NCP-CLOVASTUDIO-API-KEY": Config.API_KEY,
            "X-NCP-APIGW-API-KEY": Config.PRIMARY_KEY,
            "X-NCP-CLOVASTUDIO-REQUEST-ID": Config.REQUEST_ID,
            "Content-Type": "application/json; charset=utf-8",
        }
        for i in range(max_retries):
            try:
                with requests.post(
                    self._host + "/testapp/v1/chat-completions/HCX-DASH-001",
                    headers=headers,
                    json=completion_request,
                    timeout=2,
                ) as resp:
                    response = resp.json()

                if response["status"]["code"] != "20000":
                    raise ConnectionError(
                        "HCX request ERROR " + response["status"]["message"]
                    )

                return response

            except Timeout as e:
                if i < max_retries - 1:
                    print(f"HCX Timeout retry {i + 1}")
                    continue
                else:
                    raise ConnectionError(f"HCX-003 {str(e.__repr__())}")


class Comfort:
    def __init__(self, params):
        self.params: ComfortBotParams = params

    @staticmethod
    def remove_after_last_punctuation(text):
        last_punc_index = max(text.rfind("."), text.rfind("?"), text.rfind("!"))
        if last_punc_index != -1:
            text = text[: last_punc_index + 1]
        return text

    @staticmethod
    def normalize_text_emotion(sentence: str):
        mapping = str.maketrans(
            {"ᄒ": "ㅎ", "ᄏ": "ㅋ", "ᄐ": "ㅌ", "ᅲ": "ㅠ", "ᄋ": "ㅇ"}
        )
        sen = sentence.translate(mapping).replace("ᅮᅮ", "ㅜㅜ")
        return sen

    @staticmethod
    def get_input():
        return {
            "maxTokens": 128,
            "temperature": 0.5,
            "topK": 0,
            "topP": 0.75,
            "repeatPenalty": 5.0,
            "stopBefore:": ["\n"],
            "seed": 0,
        }

    def generate(self):
        request_data = Comfort.get_input()
        request_data["messages"] = [{"role": "system", "content": prompt}]
        request_data["messages"] += self.params.records
        request_data["messages"].append(
            {"role": "user", "content": self.params.utterance}
        )

        print(request_data)
        response = CompletionExecutor().execute(request_data)

        response = response["result"]["message"]["content"]
        response = response.replace("오복이 :", "").replace("오복이 :", "")
        response = response.replace('"', "").strip()

        if len(response) > 60:
            response = Comfort.remove_after_last_punctuation(response)

        return Comfort.normalize_text_emotion(response)
