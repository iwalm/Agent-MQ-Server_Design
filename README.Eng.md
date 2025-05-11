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

