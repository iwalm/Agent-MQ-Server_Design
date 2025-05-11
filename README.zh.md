<!-- <运行项目的详细步骤 - 作者:林锦秋> -->

1. 环境准备
1.1 安装Python
 在VSCode终端中执行：
  pip install boto3 python-dotenv

建议直接添加源使用 pip install boto3 python-dotenv -i https://pypi.tuna.tsinghua.edu.cn/simple  
 
1.2 配置AWS凭证
浏览器访问AWS管理控制台
使用根账户或 IAM 用户登录。
创建 IAM 用户（如果尚未创建）
分配权限
生成 Access Key ID和 Secret Access Key 
将密钥配置到代码中

方法1（推荐）：通过环境变量配置  
  在项目根目录新建 .env 文件，内容如下：
  AWS_ACCESS_KEY_ID=你的AccessKey
  AWS_SECRET_ACCESS_KEY=你的SecretKey
  AWS_REGION=eu-north-1
 
方法2：通过AWS CLI配置  
  安装AWS CLI后运行：
  bash
  aws configure. 项目结构
确保项目
  输入AccessKey、SecretKey、Region（eu-north-1）。

2文件如下组织：

Agent-MQ-Server_Design/
├── agent.py            # Agent端代码
├── server.py           # Server端代码
├── requirements.txt    # 依赖列表（可选）
└── .env                # 环境变量文件（可选）

3. 修改代码中的队列URL 
在 agent.py 和 server.py 中，确认以下队列URL与AWS账户匹配：
python
 agent.py
receivequeue_url = 'https://sqs.eu-north-1.amazonaws.com/AWS账户ID/Server'
sendqueue_url = 'https://sqs.eu-north-1.amazonaws.com/AWS账户ID/Agent'
registration_url = 'https://sqs.eu-north-1.amazonaws.com/AWS账户ID/register'
 server.py
queue_url = 'https://sqs.eu-north-1.amazonaws.com/AWS账户ID/Agent'

4. 运行代码
4.1 启动Agent端
打开 agent.py，按 F5 或点击 Run > Start Debugging。
预期输出：

  Sent agent information to SQS: {"agent_id": "xxxx", "hostname": "your-pc"}

  首次运行会生成 agent.lock 文件并注册。

4.2 启动Server端
 新建一个终端（Ctrl+Shift+），运行：
bash
python server.py
 预期输：
  Sent message: hello





<!-- <使用项目的详细步骤 - 作者:林锦秋> -->

1. 启动服务组件
步骤1：启动Agent端  
 作用：监听任务队列，接收并执行命令。  
 操作：在终端运行Agent端代码。  
  python agent.py
   预期输出：  
  Sent agent information to SQS: {"agent_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "hostname": "your-pc"}
  Polling messages from queue...

步骤2：启动Server端  
作用：向任务队列发送命令，并监听结果队列（可选）。  
操作：在另一终端运行Server端代码。  
  python server.py
  
 预期输出：  
  Sent message: "hello"

2. 发送自定义命令
方法1：通过Server端代码动态发送命令 
 修改 server.py 中的 message_body，例如：  
  python
  server.py
  message_body = ping 8.8.8.8  # 发送网络检测命令
重新运行 server.py，Agent端将执行该命令并返回结果。

方法2：通过AWS控制台手动发送消息 
1. 进入AWS SQS控制台，找到 Agent 队列。  
2. 点击 发送消息，输入消息内容（如 ls -l）。  
3. Agent端自动接收并执行命令，结果发送到 Server 队列。

3. 查看执行结果
方式1：通过Server端监听结果队列  
 若Server端代码包含结果队列监听逻辑（需自行扩展），运行后会显示返回结果：  
  Received response from Agent-xxxx: "64 bytes from 8.8.8.8: icmp_seq=0 ttl=117 time=25.3 ms"
  
方式2：在AWS控制台查看消息 
1. 进入 Server 队列的 接收消息界面。  
2. 点击 轮询消息，查看Agent返回的结果。

3. 多Agent扩展（负载均衡）
步骤1：启动多个Agent实例  
 复制 agent.py 为 agent2.py，修改 LOCK_FILE 名称（避免冲突）：  
  python
  agent2.py
  LOCK_FILE = 'agent2.lock'

 运行多个Agent：  
  python agent.py  # 原Agent
  python agent2.py # 新Agent
  
步骤2：验证分布式执行
 Server端发送多条命令，观察不同Agent实例的日志输出，确认任务被均匀分配。

5. 调试与监控
调试建议  
 日志检查：  
   Agent端：查看命令执行输出和错误信息。  
   Server端：确认消息发送成功。  
 AWS SQS监控：  
   在AWS控制台查看队列的 消息数量 和 延迟时间，确保消息正常流动。

关键命令示例  
 发送复杂命令：  
 python
   server.py
  message_body = "df -h"  # 查看磁盘空间
  
 结果示例：  
  Received response: "Filesystem      Size  Used Avail Use% Mounted on ..."
  
6. 安全与最佳实践
1. 限制命令权限：  
  避免发送高危命令（如 rm -rf /），或在代码中添加白名单过滤。  
2. 定期轮换AWS凭证：  
  在IAM控制台中定期生成新的Access Key，并更新 .env 文件。  
3. 启用SQS死信队列（DLQ）：  
   处理无法被消费的消息，避免队列阻塞。

总结
1. 启动服务：分别运行Agent和Server端。  
2. 发送命令：通过代码或AWS控制台下发指令。  
3. 查看结果：从Server端日志或AWS队列中获取执行结果。  
4. 扩展与监控：支持多Agent负载均衡，并通过AWS控制台监控消息流。  
通过上述步骤，可以灵活使用该分布式任务系统，实现远程命令执行、结果收集和任务调度。