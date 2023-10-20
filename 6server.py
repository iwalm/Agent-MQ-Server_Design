import boto3
import time

# Create an SQS client
sqs = boto3.client('sqs', region_name='eu-north-1')

# URL of your SQS queue
queue_url = 'https://sqs.eu-north-1.amazonaws.com/701545181846/six'

while True:
    message_body = "hello"  # or any other message you want to send
    # Send the message
    sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)
    print(f"Sent message: {message_body}")
    time.sleep(1)  # Send a message every 1 second
