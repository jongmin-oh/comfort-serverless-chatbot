import time
import boto3


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("kakao-chatbot-chat-records")


def save_record(userId, utterance, role):
    response = table.put_item(
        Item={
            "userId": userId,
            "timestamp": int(time.time()),
            "role": role,
            "content": utterance,
        }
    )
    return response


def fatch_records(userId) -> list:
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("userId").eq(userId),
        Limit=10,  # 최대 10개 항목만 반환
        ProjectionExpression="#r, content",  # role과 content 항목만 반환
        ExpressionAttributeNames={"#r": "role"},  # 예약어 대체
        ScanIndexForward=False,
    )
    response = response["Items"]
    response.reverse()
    return response
