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
