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