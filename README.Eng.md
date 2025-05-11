<!-- <Detailed Steps to Run the Project - Author: Lin Jinqiu> -->  

1. Environment Preparation  
1.1 Install Python Dependencies  
 Execute in the VSCode terminal:    
  pipinstall boto3 python-dotenv  
  
Recommended: Use a mirror source for faster installation:  
    
  pip install boto3 python-dotenv -i https://pypi.tuna.tsinghua.edu.cn/simple  
  

1.2 Configure AWS Credentials  
1. Access the AWS Management Console via a browser.  
2. Log in using your root account or an IAM user.  
3. Create an IAM user (if not already created):  
   Assign the AmazonSQSFullAccess policy.  
   Generate Access Key ID and Secret Access Key.  
4. Integrate credentials into the code:  

Method 1 (Recommended): Environment Variables  
Create a `.env` file in the project root with:  
   
  AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY  
  AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY  
  AWS_REGION=eu-north-1   

Method 2: AWS CLI Configuration  
Install the AWS CLI and run: 
  bash
  aws configure  
   Input your AccessKey, SecretKey, and Region (eu-north-1).  



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