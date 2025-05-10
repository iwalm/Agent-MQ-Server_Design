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

