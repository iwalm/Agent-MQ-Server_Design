
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
