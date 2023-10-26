from flask import Flask, request, jsonify
import boto3
import time
import uuid
import json
import mysql.connector

app = Flask(__name__)

unique_id = uuid.uuid4()
timestamp = int(time.time() * 1000)

# Initialize AWS SQS client
sqs = boto3.client('sqs', region_name='eu-north-1')
sendqueue_url = 'https://sqs.eu-north-1.amazonaws.com/701545181846/Server'
receivequeue_url = 'https://sqs.eu-north-1.amazonaws.com/701545181846/Agent'
registration_url = 'https://sqs.eu-north-1.amazonaws.com/701545181846/register'

# Connect to MySQL/MariaDB database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'hack',
    'database': 'agents'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS agents (
        uuid VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    )
''')


#cursor.execute('''
#    ALTER TABLE passwords
#    ADD COLUMN type VARCHAR(255)
#''')

conn.commit()
conn.close()

@app.route('/send-command', methods=['POST'])
def send_command():
    agent_id = '77af07e9-6c43-4050-bc25-a49f8a89de0c'  # Unique ID for the agent
    data = request.get_json()
    command = data.get('command')
    message_data = {
        'agent_id': agent_id,
        'message': command
    }
    message_body = json.dumps(message_data)
    deduplication_id = f"{timestamp}-{unique_id}"
    
    # Send the command to SQS queue
    sqs.send_message(QueueUrl=sendqueue_url, MessageBody=message_body)
    
    return 'Command sent to agents.'

@app.route('/receive-response', methods=['GET'])
def receive_response():
    # Receive response messages from SQS queue
    #client_message_group_id = 'FromClient'
    response = sqs.receive_message(QueueUrl=receivequeue_url, MaxNumberOfMessages=1)
    
    if 'Messages' in response:
        response_message = response['Messages'][0]['Body']
        # Delete the message from the queue
        sqs.delete_message(QueueUrl=receivequeue_url, ReceiptHandle=response['Messages'][0]['ReceiptHandle'])
        return jsonify({'response': response_message})
    else:
        return jsonify({'response': 'No response from agents.'})
    
@app.route('/register_agents', methods=['POST'])
def register_agents():
    # Receive response messages from SQS queue
    #client_message_group_id = 'FromClient'
    response = sqs.receive_message(QueueUrl=registration_url, MaxNumberOfMessages=1)

    # Process received messages
    if 'Messages' in response:
        response_message = response['Messages'][0]['Body']
        message_body = json.loads(response_message)  # Parse the JSON string to a dictionary
        agent_id = message_body.get('agent_id')
        agent_hostname = message_body.get('hostname')
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('INSERT INTO agents (uuid, name) VALUES (%s, %s)', (agent_id, agent_hostname))
        conn.commit()

        # Delete the message from the queue
        sqs.delete_message(QueueUrl=registration_url, ReceiptHandle=response['Messages'][0]['ReceiptHandle'])
        return jsonify({'response': 'Registration Complete'})
    else:
        return jsonify({'response': 'No response from agents.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3030)
