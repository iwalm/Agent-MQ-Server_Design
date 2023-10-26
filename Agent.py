import subprocess
import time
import boto3
import uuid
import json
import signal
import sys
import os
import socket


unique_id = uuid.uuid4()
timestamp = int(time.time() * 1000)
#agent_id = 'agent-1'

# Initialize AWS SQS client
sqs = boto3.client('sqs', region_name='eu-north-1')
sendqueue_url = 'https://sqs.eu-north-1.amazonaws.com/701545181846/Agent'
receivequeue_url = 'https://sqs.eu-north-1.amazonaws.com/701545181846/Server'
registration_url = 'https://sqs.eu-north-1.amazonaws.com/701545181846/register'

LOCK_FILE = 'agent.lock'

def generate_agent_id():
    if not os.path.exists(LOCK_FILE):
        agent_id = str(uuid.uuid4())
        hostname = socket.gethostname()
        agent_info = {'agent_id': agent_id, 'hostname': hostname}
        with open(LOCK_FILE, 'w') as file:
            json.dump(agent_info, file)
        agent_info = agent_info
        message_body = json.dumps(agent_info)
        sqs.send_message(QueueUrl=registration_url, MessageBody=message_body)
        print(f"Sent agent information to SQS: {message_body}")
    else:
        print("Registration not needed")

# Get or generate agent ID only if the lock file does not exist
agent_registration = generate_agent_id()

def get_agent_id():
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, 'r') as file:
            agent_info = json.load(file)
            return agent_info['agent_id']
        
agent_id = get_agent_id()

def run_command(command):
    try:
        # Run the command and capture the output
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return output
    except subprocess.CalledProcessError as e:
        # If the command execution fails, return the error message
        return f"Error: {e.output}"
    
def signal_handler(sig, frame):
    print("\nReceived Ctrl + C. Exiting...")
    sys.exit(0)

# Register the signal handler for Ctrl + C
signal.signal(signal.SIGINT, signal_handler)

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