import json

def send_email(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Serverless AWS Lambda email handler working"
        })
    }
