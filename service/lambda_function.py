import json

from app.models import ComfortBotParams, skillTemplate
from app.tasks.generate import Comfort
from app.tasks.record import save_record, fatch_records


def lambda_handler(event, context):
    body = event["body"]
    body = json.loads(body)

    userId = body["userRequest"]["user"]["id"]
    utterance = body["userRequest"]["utterance"]
    save_record(userId, utterance, "user")
    records = fatch_records(userId)

    params = ComfortBotParams(userId=userId, records=records, utterance=utterance)
    comfort = Comfort(params)
    chatbot_response = comfort.generate()

    save_record(userId, chatbot_response, "assistant")
    return skillTemplate.send_response(chatbot_response)
