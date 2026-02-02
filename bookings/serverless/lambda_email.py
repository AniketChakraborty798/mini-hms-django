"""
SERVERLESS FUNCTION (Concept)

This function represents AWS Lambda.
It is stateless and event-driven.
"""

def lambda_handler(event, context=None):
    to = event["to"]
    subject = event["subject"]
    message = event["message"]

    print("----- SERVERLESS EMAIL FUNCTION -----")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Message: {message}")
    print("------------------------------------")

    return {
        "statusCode": 200,
        "body": "Email handled by serverless function"
    }

"""
AWS Lambda style serverless function.
Can be deployed without code changes.
Triggered by Django as an event.
"""
