import boto3

# Create an SQS client
sqs = boto3.client('sqs', region_name='eu-north-1')

# URL of your SQS queue
queue_url = 'https://sqs.eu-north-1.amazonaws.com/701545181846/six'

while True:
    # Receive messages from the queue
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
    
    # Process received messages
    for message in response.get('Messages', []):
        body = message['Body']
        print(f"Received message: {body}")
        
        # Echo back the received message
        sqs.send_message(QueueUrl=queue_url, MessageBody=body)
        
        # Delete the message from the queue
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
