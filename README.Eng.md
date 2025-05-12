Here is the detailed English translation of the running and usage instructions for the distributed device management system:
《by:oyy》
 I. Environment Preparation

 1. Hardware/Software Requirements
OS: Linux/macOS/Windows (for both agent and server)
Python**: 3.7+
AWS Account** (for SQS service)
Network**: Devices and control server must be able to access AWS SQS

 2. Dependency Installation
bash
Clone project (assuming repo exists)
git clone <repo_url>
cd <project_dir>

 Install dependencies
pip install -r requirements.txt
```

 3. AWS Configuration
1. Create SQS queues (3 required):
    command_queue`
    response_queue`
    registration_queue`
2. Update queue URLs in `config.py`
3. Configure AWS credentials:
bash
 Method 1: Environment variables
   export AWS_ACCESS_KEY_ID="your_access_key"
   export AWS_SECRET_ACCESS_KEY="your_secret_key"

 Method 2: AWS config file
 Edit ~/.aws/credentials


 II. Launching the System

 1. Start Control Plane (Server)
bash
Development mode
python server.py

 Production mode (recommended)
gunicorn -w 4 -b 0.0.0.0:5000 server:app
Successful launch indicator:
 Running on http://0.0.0.0:5000/

 2. Start Device Agent
On target devices:
bash
Normal mode
python agent.py

 With custom device ID (optional)
DEVICE_ID="my-device-001" python agent.py
Successful launch indicator:
Starting device agent (ID: xxxx-xxxx)
Device registered: xxxx-xxxx
III. Usage Guide

1. Device Management

 List all devices
bash
curl http://localhost:5000/api/v1/devices
```
Response example:json
{
  "status": "success",
  "data": {
    "device-001": {
      "status": "online",
      "last_seen": "2023-07-20T08:00:00Z",
      "capabilities": ["execute_shell"]
    }
  }
}
 Check specific device
bash
curl http://localhost:5000/api/v1/devices/device-001

 2. Command Operations

 Send command to specific device
bash
curl -X POST http://localhost:5000/api/v1/commands \
-H "Content-Type: application/json" \
  -d '{
    "device_id": "device-001",
    "command": "ls -l /",
    "timeout": 30
  }'
```
Response example:
```json
{
  "status": "success",
  "command_id": "cmd_abcd1234",
  "message": "Command sent to device(s)"
}

 Broadcast command (all devices)
```bash
curl -X POST http://localhost:5000/api/v1/commands \
  -d '{"command": "date"}'


3. Retrieving Responses

 Poll for responses
```bash
curl http://localhost:5000/api/v1/responses
```
Response example:
```json
{
  "status": "success",
  "responses": [
    {
      "device_id": "device-001",
      "command_id": "cmd_abcd1234",
      "response": {
        "exit_code": 0,
        "stdout": "total 64\ndrwxr-xr-x ...",
        "stderr": ""
      }
    }
  ]
}
 IV. Typical Use Cases

 Case 1: Batch Device Monitoring
bash
1. Send memory check command
curl -X POST http://localhost:5000/api/v1/commands \
  -d '{"command": "free -h"}'

 2. Get responses after 5 sec
sleep 5
curl http://localhost:5000/api/v1/responses

 Case 2: Automated Testing
bash
# Execute test script
curl -X POST http://localhost:5000/api/v1/commands \
  -d '{
    "command": "python /tests/run_tests.py",
    "timeout": 600
  }'
 Case 3: Firmware Updates
bash
# Phase 1: Download
curl -X POST http://localhost:5000/api/v1/commands \
  -d '{"command": "download_update.sh"}'

 Phase 2: Apply update
curl -X POST http://localhost:5000/api/v1/commands \
  -d '{"command": "apply_update.sh"}'

 V. Troubleshooting

 Common Issue 1: Device Not Registered
 Symptom**: Empty device list
 Checks:
  1. Verify agent logs show "Device registered"
  2. Check AWS SQS console for messages in registration queue
  3. Confirm queue URLs match in server/agent `config.py`
 Common Issue 2: Commands Not Executing
Debug steps:
  bash
   1. Check command queue
  aws sqs get-queue-attributes 
    queue-url <COMMAND_QUEUE_URL> 
    --attribute-names ApproximateNumberOfMessages

  2. Verify agent process
  ps aux | grep agent.py

   3. Check agent logs
  tail -f agent.log
Log Inspection Tips
bash
 Server logs (real-time)
tail -f server.log

 Agent logs (filter errors)
grep -i error agent.log
 VI. Production Recommendations

1. Security Enhancements**:
   Enable HTTPS (Nginx reverse proxy + SSL)
    Add JWT authentication in `config.py`
    Restrict SQS queue IAM policies

2. High Availability:
   bash
    Using PM2 for process management (example)
   pm2 start server.py --interpreter python3
   pm2 start agent.py --interpreter python3


3. Monitoring:
   Set health checks for `/api/v1/devices`
    Monitor SQS queue backlog
   Track command success rate metrics

This comprehensive guide enables you to successfully run and utilize the distributed device management system. The loosely-coupled architecture allows for easy extension of additional modules (e.g., database persistence, web console) as needed.