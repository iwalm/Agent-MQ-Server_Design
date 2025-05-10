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