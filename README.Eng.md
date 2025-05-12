《author:ouyuanyuan》

Here is the detailed English translation of the running and usage instructions for the distributed device management system:
 I. Environment Preparation

 1. Hardware/Software Requirements
OS: Linux/macOS/Windows (for both agent and server)
Python: 3.7+
AWS Account (for SQS service)
Network: Devices and control server must be able to access AWS SQS

 2. Dependency Installation
bash
Clone project (assuming repo exists)
git clone <repo_url>
cd <project_dir>

 Install dependencies
pip install -r requirements.txt


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
  }
Response example:
json
{
  "status": "success",
  "command_id": "cmd_abcd1234",
  "message": "Command sent to device(s)"
}

 Broadcast command (all devices)
bash
curl -X POST http://localhost:5000/api/v1/commands \
  -d '{"command": "date"}'


3. Retrieving Responses

 Poll for responses
bash
curl http://localhost:5000/api/v1/responses

Response example:
json
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
  d '{"command": "free -h"}'

 2. Get responses after 5 sec
sleep 5
curl http://localhost:5000/api/v1/responses

 Case 2: Automated Testing
bash
# Execute test script
curl -X POST http://localhost:5000/api/v1/commands \
  d '{
    "command": "python /tests/run_tests.py",
    "timeout": 600
  }'
 Case 3: Firmware Updates
bash
 Phase 1: Download
curl -X POST http://localhost:5000/api/v1/commands \
  -d '{"command": "download_update.sh"}'

 Phase 2: Apply update
curl -X POST http://localhost:5000/api/v1/commands \
  -d '{"command": "apply_update.sh"}'

 V. Troubleshooting

 Common Issue 1: Device Not Registered
 Symptom: Empty device list
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
      attribute-names ApproximateNumberOfMessages

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

1. Security Enhancements:
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





<!-- <Add detailed steps to run the project - Author: Lin Jinqiu> -->  

2. Project Structure  
Ensure the project is organized as follows:  
  
Agent-MQ-Server_Design/  
├── agent.py            # Agent-side code  
├── server.py           # Server-side code  
├── requirements.txt    # Dependency list (optional)  
└── .env                # Environment variables (optional)  

3. Update Queue URLs in Code  
Verify the following queue URLs in agent.py and server.py match your AWS account:  
python  
agent.py  
receivequeue_url = 'https://sqs.eu-north-1.amazonaws.com/AWS_ACCOUNT_ID/Server'  
sendqueue_url = 'https://sqs.eu-north-1.amazonaws.com/AWS_ACCOUNT_ID/Agent'  
registration_url = 'https://sqs.eu-north-1.amazonaws.com/AWS_ACCOUNT_ID/register'  
 server.py  
queue_url = 'https://sqs.eu-north-1.amazonaws.com/AWS_ACCOUNT_ID/Agent'  

4. Run the Code  
4.1 Start the Agent-Side  
Open agent.py in VSCode.  
 Press F5 or navigate to Run > Start Debugging.  
Expected Output:  
  bash  
  Sent agent information to SQS: {"agent_id": "xxxx", "hostname": "your-pc"}  
   
Note: A agent.lock file will be generated upon first run for registration.  

4.2 Start the Server-Side  
 Open a new terminal (`Ctrl+Shift+``) and execute:  
  bash  
  python server.py  
    
Expected Output:  
  bash  
  Sent message: hello  
    

 Key Notes:  
Security: Never commit .env or credentials to version control.  
Queue Validation: Ensure SQS queues (Agent, Server, register) exist in the eu-north-1 region.  
Troubleshooting: Check AWS CloudWatch logs for SQS API errors if messages fail to deliver.


<!-- <Detailed Steps to Use the Project - Author: Lin Jinqiu> -->  


1. Launch Service Components 

Step 1: Start the Agent-Side 
 Purpose: Monitors the task queue, receives and executes commands.  
  Operation: Run the Agent-side code in a terminal:    
  python agent.py  
   
 Expected Output:  
  Sent agent information to SQS: {"agent_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "hostname": "your-pc"}  
  Polling messages from queue...  
    

Step 2: Start the Server-Side 
 Purpose: Sends commands to the task queue and optionally monitors the result queue.  
 Operation: Run the Server-side code in a separate terminal:  
  python server.py    
 Expected Output:  
  Sent message: "hello"   

2. Send Custom Commands  

Method 1: Dynamically Send Commands via Server-Side Code  
 Modify the message_body in server.py, e.g.:  
 python  
 server.py  
  message_body = "ping 8.8.8.8"  # Send network diagnostic command  
 Re-run server.py. The Agent will execute the command and return results.  

Method 2: Manually Send Messages via AWS Console 
1. Navigate to the AWS SQS Console and locate the Agent queue.  
2. Click Send message and input the command (e.g., ls -l).  
3. The Agent will automatically receive, execute, and send results to the `Server` queue.  

4. View Execution Results  

Approach 1: Monitor Results via Server-Side Logic  
 If the Server-side code includes result queue monitoring (requires customization), the output will display:  
  Received response from Agent-xxxx: "64 bytes from 8.8.8.8: icmp_seq=0 ttl=117 time=25.3 ms"   

Approach 2: View Messages in AWS Console 
1. Navigate to the Server queue and access the Poll messages interface.  
2. Click Poll for messages to retrieve Agent responses.  
3. Multi-Agent Scaling (Load Balancing)  

Step 1: Launch Multiple Agent Instances  
 Duplicate agent.py as agent2.py and modify the LOCK_FILE name to avoid conflicts:  
python  
agent2.py  
  LOCK_FILE = 'agent2.lock'  

 Run multiple Agents:  
  python agent.py   # Original Agent  
  python agent2.py  # New Agent  
 

Step 2: Validate Distributed Execution  
 Send multiple commands from the Server-side and observe logs across Agent instances to confirm task distribution.  

5. Debugging & Monitoring 

Debugging Recommendations
 Log Inspection:  
   Agent-side: Check command execution outputs and error messages.  
   Server-side: Verify message delivery status.  
 AWS SQS Monitoring:  
   Monitor queue metrics (Messages Visible, Approximate Age of Oldest Message) in the AWS Console.  

Key Command Examples
 Send Complex Commands:  
 python  
  server.py  
  message_body = "df -h"  # Check disk space  
 Result Example:  
  Received response: "Filesystem      Size  Used Avail Use% Mounted on ..."  
   
6. Security & Best Practices 
1. Restrict Command Permissions:  
 Avoid high-risk commands (e.g., rm -rf /) or implement allowlist filtering in code.  
2. Rotate AWS Credentials Regularly:  
 Generate new Access Keys periodically via the IAM Console and update the .env file.  
3. Enable SQS Dead-Letter Queues (DLQ):  
 Handle undeliverable messages to prevent queue congestion.  

Summary
1. Service Initialization: Launch Agent and Server components.  
2. Command Dispatch: Send instructions programmatically or via the AWS Console.  
3. Result Retrieval: Collect outputs through Server logs or SQS queues.  
4. Scalability & Monitoring: Support multi-Agent load balancing and monitor workflows via AWS tools.  
This distributed task system enables remote command execution, result aggregation, and scalable task orchestration.  

Key Technical Notes:  
 Idempotency: Ensure command handlers are idempotent to avoid duplicate executions.  
 Error Handling: Implement retries with jitter for transient SQS errors.  
 Cost Optimization: Use `ShortPolling` for high-frequency queues and `LongPolling` for cost-sensitive workloads.





<6agent.py程序分析 黄钰慧编写>
I. Analysis of the Purpose and Function of 6agent.py:
    The goal of this project is to build a message feedback system using AWS SQS queue service.
    The system mainly implements the following functions:

    1. Message Receiving Function
        - The program continuously checks a specific SQS queue through a loop.
        - This queue is located in the eu-north-1 region and is named "six".
        - Each time it checks, it can retrieve up to 1 message at most.

    2. Message Display Function
        - When a message is received, the program immediately displays the message content on the console.
        - The display format is "Received message: message content".

    3. Message Forwarding Function
        - The program copies the body of the received message completely.
        - Then it sends the copied content back to the same queue.
        - This operation produces an effect of message duplication.

    4. Message Deletion Function
        - After completing the message forwarding, the program immediately sends a deletion command to the queue.
        - The deletion operation uses the ReceiptHandle of the message for identification.
        - This can prevent the same message from being processed repeatedly.

<6server.py程序分析 黄钰慧编写>
II. Analysis of the Purpose and Function of 6server.py:
    The 6server.py program is used to send test messages to the AWS SQS queue regularly.
    The program mainly implements three functions:

    1. Message Sending Function
        - The program sends messages to the specified queue through a loop every second.
        - The target queue is located in the eu-north-1 region and is named "six".
        - The message sending interval is controlled by time.sleep(1) to avoid over-consuming system resources.

    2. Message Format Setting
        - Currently, all message contents are fixed as "hello".
        - Users can modify the message content according to actual needs:
            * Changing it to dynamically generated timestamps
            * Or using simulated sensor data

    3. Sending Status Confirmation
        - Each time a message is successfully sent, the program displays "Sent message: hello" on the console.
        - This kind of log recording method can help users confirm whether the message has entered the queue normally.




# Agent-MQ-Server_Design
A minimal Prototype to for Agent Server communications over a MQ channel by using Python
邓兰春撰写（gitee名：muye3）：
Software 1: VS Code
    1. VS Code Download:
        To run this project, you need to download Visual Studio Code first.
        Download link: https://code.visualstudio.com/Download
        (Check "Add to PATH" to enable terminal access to the code command.)

    2. Install VS Code Extensions:
        1.Python (Microsoft)    : Provides Python language support (debugging, IntelliSense).

        2.Pylance               : Enhances type checking and code completion.

        3.Docker                : Required if using Docker to run RabbitMQ/Redis.

        4.SQLite                : Enables visualization of SQLite databases.

    3. Create a Virtual Environment (After Installing Dependencies):
        Run the following commands in the project's root directory:

        # Create a virtual environment (Windows)  
        python -m venv .venv  
        # Activate the environment (Windows)  
        .venv\Scripts\activate  

Software 2: AWS SQS
    AWS SQS does not require installation. Simply log in to your AWS account to create and manage queues.
    Login URL: https://console.aws.amazon.com/sqs/

    Note:

    Alternative: RabbitMQ (open-source, supports complex routing, high reliability).

    RabbitMQ download: https://www.rabbitmq.com/docs/download

Software 3: MySQL
    1. Download:
        Free download available at: https://dev.mysql.com/downloads/mysql/

    2. Installation Steps:
        1.Run the installer:

            Double-click the downloaded .msi file (e.g., mysql-installer-community-8.0.xx.msi).

        2.Select installation type:

            Choose Developer Default (recommended for development) or Custom (for advanced users).

        3.Configure MySQL Server:

            Set a root user password (remember this!).

            Select Standalone MySQL Server.

        4.Complete installation:

            Check Start MySQL Server at System Startup (enables auto-start).

            Click Execute → Finish.


### <--凌浩文-->

### II. Purpose and Function Description of the Agent copy.py

#### 1. **Purpose Description**

1. **Distributed Task Scheduling**:

   - Leverages AWS SQS for the reception and execution of distributed tasks, making it suitable for scenarios that require remote control or automated task processing.
2. **Automated Task Processing**:

   - Can be used to automate the processing of tasks in the queue, such as log collection and data processing.
3. **Learning and Demonstration**:

   - Serves as an example for learning AWS SQS and the Boto3 library, helping developers understand how to interact with AWS SQS using Python, including receiving, sending messages, and executing commands.

#### 2. **Function Description**

1. **Generate a Unique Agent ID and Register**:

   - Upon the first run, checks if the lock file `agent.lock` exists. If not, generates a unique agent ID and stores the agent information (including the agent ID and hostname) in the lock file.
   - Sends the agent information to the registration queue `registration_url` to complete the agent registration.
2. **Retrieve Agent ID**:

   - Reads the agent ID from the lock file for subsequent message processing.
3. **Receive Messages**:

   - Receives messages from the specified receive queue `receivequeue_url`, with a maximum of 1 message received at a time.
4. **Process Messages**:

   - Parses the received message content (in JSON format) to extract the agent ID and command content from the message.
   - If the agent ID in the message matches the current agent ID, the command is executed.
5. **Execute Commands**:

   - Uses the `subprocess` module to execute the command and captures the command output or error messages.
6. **Send Results**:

   - Sends the execution results of the command to the specified send queue `sendqueue_url`.
7. **Delete Processed Messages**:

   - Deletes the processed messages from the receive queue after command execution and result transmission.
8. **Continuous Operation**:

   - Runs in an infinite loop, checking the receive queue every 5 seconds to continuously process new messages.
9. **Graceful Exit**:

   - Supports graceful exit via Ctrl + C.


# Agent-MQ-Server_Design
A minimal Prototype to for Agent Server communications over a MQ channel by using Python

### Installation Guide （此部分由黎忻慧贡献）
1.Required dependencies(You can directly install them in the project's virtual environment via pip install package_name.)
```bash
#Related to AWS Command Line Interface Tools
pip install awscli==1.29.71  # A command-line tool for interacting with Amazon Web Services (AWS)
pip install boto==2.49.0  # An older Python AWS SDK for communicating with AWS services
pip install boto3==1.28.71  # The latest Python AWS SDK for interacting with AWS services (e.g., S3, EC2, etc.)
pip install botocore==1.31.71  # The core library of boto3, providing low-level communication with AWS services
pip install s3transfer==0.7.0  # A library for efficient data transfer between local storage and Amazon S3

#Related to Encryption
pip install bcrypt==4.0.1  # A library for implementing password hashing to enhance password storage security
pip install cryptography==41.0.5  # Provides implementations of common encryption algorithms, such as symmetric and asymmetric encryption
pip install PyNaCl==1.5.0  # Python bindings based on the NaCl encryption library for secure encryption, signing, etc.

#Utility Libraries
pip install blinker==1.6.3  # A Python library for implementing the publish-subscribe pattern to decouple communication between code components
pip install click==8.1.7  # A Python library for creating command-line interfaces, facilitating the building of user-friendly command-line tools
pip install colorama==0.4.4  # Used to add colors and styles to the terminal for more readable output
pip install decorator==5.1.1  # Provides decorator-related functions to modify the behavior of functions or classes
pip install docutils==0.16  # Used for processing and converting Python documentation, such as converting reStructuredText to other formats
pip install fabric==3.2.2  # A library for simplifying remote system management and deployment tasks
pip install importlib-metadata==6.8.0  # Used to obtain metadata of Python packages at runtime
pip install invoke==2.2.0  # A Python library for managing and running tasks, similar to the make tool
pip install itsdangerous==2.1.2  # Used to generate and verify security tokens, often for session management in web applications
pip install Jinja2==3.1.2  # A powerful template engine for generating dynamic text, such as HTML pages
pip install jmespath==1.0.1  # A library for efficient querying in JSON data
pip install MarkupSafe==2.1.3  # Used to safely handle markup (e.g., HTML, XML) in web applications
pip install paramiko==3.3.1  # A Python library for remote connections, command execution, and file transfer via the SSH protocol
pip install prettytable==3.9.0  # Used to print data in beautiful table format for improved output display
pip install pyasn1==0.5.0  # Used for processing ASN.1 (Abstract Syntax Notation One) data, applied in scenarios like network protocols
pip install pycparser==2.21  # A Python library for parsing C language syntax, applicable for code analysis
pip install python-dateutil==2.8.2  # Provides powerful date and time processing functions, extending the datetime functionality of the Python standard library
pip install PyYAML==6.0.1  # Used for reading and writing YAML format data in Python
pip install rsa==4.7.2  # Implements the RSA encryption algorithm for encryption, decryption, signing, and verification
pip install six==1.16.0  # Helps with code compatibility between Python 2 and Python 3
pip install urllib3==1.26.18  # A library for handling HTTP requests, enhancing the urllib functionality of the Python standard library
pip install wcwidth==0.2.8  # Used to determine the display width of Unicode characters in the terminal
pip install Werkzeug==3.0.1  # Provides various tools and libraries for Python web development, serving as the foundation for frameworks like Flask
pip install wrapt==1.15.0  # Used to implement function and class decoration, proxying, etc.
pip install zipp==3.17.0  # Used for handling Python zip file operations, providing an interface to access zip files

#Related to Web Frameworks
pip install flask==3.0.0  # A lightweight Python web framework for quickly building web applications
```
2. Specific operation steps
Step 1: Create a virtual environment. You can execute the following commands in the terminal:
# For Windows systems
python -m venv myenv  (myenv is the name of the virtual environment)
# For Linux or macOS systems
python3 -m venv myenv

Step 2: Activate the virtual environment
After creating the virtual environment, you need to activate it. The activation commands are as follows:
# For Windows systems
myenv\Scripts\activate
# For Linux or macOS systems
source myenv/bin/activate

Step 3: Install dependencies
When the virtual environment is activated, you can install the dependencies required by the project. You can install them one by one, or write all the dependencies into a requirements.txt file and then install them in batches.
# Install dependencies one by one
According to the provided list of dependencies, execute the pip install commands sequentially in the terminal. For example:
pip install awscli==1.29.71
pip install boto==2.49.0
# Install dependencies in batches
First, copy all the dependency information into a file named requirements.txt. Then, execute the following command in the terminal for batch installation:
pip install -r requirements.txt

Step 4: Verify the installation
After the dependencies are installed, you can view the installed packages by using the following command:
pip list 


<!-- <Technical Analysis of Server.pyde - Authored by Tian Jiaqi> -->

This is a C2 (Command and Control) server system based on the Flask framework.:

Main Functionalities:

    Provides 3 API endpoints:
        Send commands
        Receive responses
        Register agents
    Uses MySQL database to store agent registration data
    Implements asynchronous messaging via SQS
Applicable Scenarios:
    IoT device management
    Red team operations (penetration testing)
    Distributed task scheduling (scenarios requiring centralized control)
    
Code Characteristics Summary:
    Hybrid communication model:
        Asynchronous queue (SQS) + Synchronous HTTP (Flask)
    Stateless API with persistent database storage
    No authentication mechanism (security consideration)
    Hardcoded agent_id (static agent identification)

Key Technical Points:
    Asynchronous Communication
        Uses SQS to decouple server and agents, avoiding direct TCP connections
    Data Persistence
        MySQL ensures agent registration data is retained
    Lightweight Protocol
        JSON format balances readability and transmission efficiency 

<!-- <Technical Specification: server_copy.py - Author: Tian Jiaqi> -->

System Architecture:
    Flask-based server implementation for remote device management

Functional Overview:
    Implements bidirectional device communication via message queue
    Provides centralized control plane for distributed systems

Core Modules:

    Command Dispatcher:
        REST Endpoint: /send-command (POST)
        Protocol: HTTP/1.1
        Payload: JSON-encoded command object
        Queue: AWS SQS (Standard Queue)
        QoS: At-least-once delivery

    Response Handler: 
        REST Endpoint: /receive-response (GET)
        Polling: Short-polling implementation
        Queue: Dedicated SQS response queue
        Response: application/json (RFC 8259 compliant)
        Status Codes: Standard HTTP response codes

Operational Contexts:

    IoT Device Fleet Management
    Automated Test Orchestration 
    Distributed Task Coordination
