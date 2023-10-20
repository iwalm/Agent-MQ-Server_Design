from flask import Flask, request, jsonify
import boto3
import time
import uuid 

app = Flask(__name__)

unique_id = uuid.uuid4()
timestamp = int(time.time() * 1000)

# Initialize AWS SQS client
sqs = boto3.client('sqs', region_name='eu-north-1')
sendqueue_url = 'https://sqs.eu-north-1.amazonaws.com/701545181846/send'
receivequeue_url = 'https://sqs.eu-north-1.amazonaws.com/701545181846/receive'

@app.route('/send-command', methods=['POST'])
def send_command():
    data = request.get_json()
    command = data.get('command')
    deduplication_id = f"{timestamp}-{unique_id}"
    
    # Send the command to SQS queue
    sqs.send_message(QueueUrl=sendqueue_url, MessageBody=command)
    
    return 'Command sent to agents.'

@app.route('/receive-response', methods=['GET'])
def receive_response():
    # Receive response messages from SQS queue
    client_message_group_id = 'FromClient'
    response = sqs.receive_message(QueueUrl=receivequeue_url, MaxNumberOfMessages=1)
    
    if 'Messages' in response:
        response_message = response['Messages'][0]['Body']
        # Delete the message from the queue
        sqs.delete_message(QueueUrl=receivequeue_url, ReceiptHandle=response['Messages'][0]['ReceiptHandle'])
        return jsonify({'response': response_message})
    else:
        return jsonify({'response': 'No response from agents.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3030)
