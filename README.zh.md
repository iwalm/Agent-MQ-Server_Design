<运行项目的详细步骤 - 作者:林锦秋>
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

<6agent.py程序分析 黄钰慧编写>
一、分析为6agent.py的目的和功能：

    该项目的目标是利用AWS SQS队列服务构建消息回传系统。
    系统主要实现以下功能：

    1、消息接收功能
        - 程序通过循环不断检查特定SQS队列
        - 该队列位于eu-north-1区域，名称为six
        - 每次检查时最多获取1条消息

    2、消息显示功能
        - 当收到消息时，程序会立即将消息内容显示在控制台
        - 显示格式为"Received message: 消息内容"

    3、消息转发功能
        - 程序把收到的消息正文完整复制
        - 将复制的内容重新发送到同一个队列中
        - 这种操作会产生消息重复传递的效果

    4、消息删除功能
        - 完成消息转发后，程序立即向队列发送删除指令
        - 删除操作使用消息的ReceiptHandle识别码
        - 这样可以防止同一条消息被重复处理

<6server.py程序分析 黄钰慧编写>
二、分析为6server.py的目的和功能：

    6server.py程序用于向AWS SQS队列定期发送测试消息。
    该程序主要实现三个功能：

    1、消息发送功能
        - 程序通过循环每秒向指定队列发送消息
        - 目标队列位于eu-north-1区域，名称为six
        - 消息发送间隔由time.sleep(1)控制，避免系统资源被过度消耗

    2、消息格式设置
        - 当前所有消息内容固定为"hello"
        - 用户可根据实际需求修改消息内容，例如：
            * 改为动态生成的时间戳
            * 或模拟传感器数据

    3、发送状态确认
        - 每次成功发送消息后，程序会在控制台显示"Sent message: hello"提示信息
        - 这种日志记录方式可以帮助用户确认消息是否正常进入队列



# Agent-MQ-Server_Design
A minimal Prototype to for Agent Server communications over a MQ channel by using Python
邓兰春撰写（gitee名：muye3）：
软件一VS code：
    一.VS code下载：
        运行该项目需要预先下载Visual Studio Code软件，下载地址：https://code.visualstudio.com/Download(勾选 “添加到 PATH”方便终端调用 code 命令)

    二.安装VS code插件：
        1.Python (Microsoft)：Python 语言支持（调试、智能提示）
        2.Pylance           ：类型检查和代码补全
        3.Docker            ：如果使用 Docker 运行 RabbitMQ/Redis
        4.SQLite            ：可视化 SQLite 数据库

    三，在安装好依赖后创建虚拟环境
        在项目根目录下执行以下代码：
        # 创建虚拟环境（Windows）
        python -m venv .venv
        # 激活环境（Windows）
        .venv\Scripts\activate

软件二AWS SQS：
    AWS SQS无需安装，登录 AWS 账号即可创建和管理队列，登录地址：https://console.aws.amazon.com/sqs/

    注：（可用RabbitMQ替代AWS SQS，好处：开源、支持复杂路由、高可靠性。RabbitMQ下载地址：https://www.rabbitmq.com/docs/download）

软件三Mysql：
    一.下载地址：https://dev.mysql.com/downloads/mysql/（免费）

    二.安装步骤：
        运行安装程序

        1.双击下载的 .msi 文件（如 mysql-installer-community-8.0.xx.msi）。
        2.选择安装类型：
            勾选 Developer Default（开发默认配置）或 Custom（自定义）。
        3.配置 MySQL Server：
            设置 root 用户密码（务必牢记！）。
        4.选择 Standalone MySQL Server（独立服务器）。
        5.完成安装
            勾选 Start MySQL Server at System Startup（开机自启）。
            点击 Execute → Finish。


### <--凌浩文-->

### 二、Agent copy.py代码目的和功能描述

#### 1. **目的描述**

1.**分布式任务调度** ：

* 通过AWS SQS实现分布式任务的接收和执行，适用于需要远程控制或自动化任务的场景。

2.**自动化任务处理** ：

* 可以用于自动化处理队列中的任务，例如日志收集、数据处理等。

3.**学习和演示** ：

* 作为学习AWS SQS和Boto3库的示例，帮助开发者理解如何使用Python与AWS SQS进行交互，包括接收、发送消息和执行命令。

#### 2. **功能描述**

1.**生成唯一代理ID并注册** ：

* 在首次运行时，检查是否存在锁文件 `agent.lock`。如果不存在，生成一个唯一的代理ID，并将代理信息（包括代理ID和主机名）存储到锁文件中。
* 将代理信息发送到注册队列 `registration_url`，完成代理的注册。

 2.**获取代理ID** ：

* 从锁文件中读取代理ID，用于后续的消息处理。

3.**接收消息** ：

* 从指定的接收队列 `receivequeue_url`中接收消息，每次最多接收1条消息。

4.**处理消息** ：

* 解析接收到的消息内容（JSON格式），提取消息中的代理ID和命令内容。
* 如果消息中的代理ID与当前代理ID匹配，则执行命令。

5.**执行命令** ：

* 使用 `subprocess`模块执行命令，并捕获命令的输出或错误信息。

6.**发送结果** ：

* 将命令的执行结果发送到指定的发送队列 `sendqueue_url`。

7.**删除已处理消息** ：

* 在命令执行并发送结果后，从接收队列中删除已处理的消息。

8.**循环运行** ：

* 脚本运行在一个无限循环中，每隔5秒检查一次接收队列，持续处理新消息。

9.**优雅退出** ：

* 支持通过Ctrl + C优雅退出程序。


# Agent-MQ-Server_Design（代理消息队列服务器设计）
一个使用 Python 通过消息队列通道实现代理服务器通信的最小原型

### 安装指南（此部分由黎忻慧贡献）
1.所需依赖（可以通过pip install package_name在项目的虚拟环境中直接安装它们。）
# 与AWS命令行工具相关
pip install awscli==1.29.71  # 用于与亚马逊网络服务(AWS)交互的命令行工具
pip install boto==2.49.0  # 较旧的Python AWS SDK，用于与AWS服务通信
pip install boto3==1.28.71  # 最新的Python AWS SDK，用于与AWS服务交互(如S3、EC2等)
pip install botocore==1.31.71  # boto3的核心库，提供与AWS服务的底层通信
pip install s3transfer==0.7.0  # 用于本地存储和亚马逊S3之间高效数据传输的库

# 与加密相关
pip install bcrypt==4.0.1  # 用于实现密码哈希的库，增强密码存储安全性
pip install cryptography==41.0.5  # 提供常见加密算法的实现，如对称和非对称加密
pip install PyNaCl==1.5.0  # 基于NaCl加密库的Python绑定，用于安全加密、签名等

# 实用工具库
pip install blinker==1.6.3  # 用于实现发布-订阅模式的Python库，解耦代码组件间的通信
pip install click==8.1.7  # 用于创建命令行界面的Python库，便于构建用户友好的命令行工具
pip install colorama==0.4.4  # 用于在终端中添加颜色和样式，使输出更易读
pip install decorator==5.1.1  # 提供装饰器相关功能，修改函数或类的行为
pip install docutils==0.16  # 用于处理和转换Python文档，如将reStructuredText转换为其他格式
pip install fabric==3.2.2  # 简化远程系统管理和部署任务的库
pip install importlib-metadata==6.8.0  # 用于在运行时获取Python包的元数据
pip install invoke==2.2.0  # 用于管理和运行任务的Python库，类似于make工具
pip install itsdangerous==2.1.2  # 用于生成和验证安全令牌，常用于Web应用中的会话管理
pip install Jinja2==3.1.2  # 强大的模板引擎，用于生成动态文本，如HTML页面
pip install jmespath==1.0.1  # 用于在JSON数据中高效查询的库
pip install MarkupSafe==2.1.3  # 用于在Web应用中安全处理标记(如HTML、XML)
pip install paramiko==3.3.1  # 通过SSH协议进行远程连接、命令执行和文件传输的Python库
pip install prettytable==3.9.0  # 以美观的表格格式打印数据，改善输出显示
pip install pyasn1==0.5.0  # 用于处理ASN.1(抽象语法标记一)数据，应用于网络协议等场景
pip install pycparser==2.21  # 用于解析C语言语法的Python库，适用于代码分析
pip install python-dateutil==2.8.2  # 提供强大的日期和时间处理功能，扩展Python标准库的datetime功能
pip install PyYAML==6.0.1  # 用于在Python中读写YAML格式数据
pip install rsa==4.7.2  # 实现RSA加密算法，用于加密、解密、签名和验证
pip install six==1.16.0  # 帮助Python 2和Python 3之间的代码兼容
pip install urllib3==1.26.18  # 处理HTTP请求的库，增强Python标准库的urllib功能
pip install wcwidth==0.2.8  # 用于确定Unicode字符在终端中的显示宽度
pip install Werkzeug==3.0.1  # 为Python Web开发提供各种工具和库，是Flask等框架的基础
pip install wrapt==1.15.0  # 用于实现函数和类装饰、代理等
pip install zipp==3.17.0  # 用于处理Python zip文件操作，提供访问zip文件的接口

# 与Web框架相关
pip install flask==3.0.0  # 轻量级Python Web框架，用于快速构建Web应用

2.具体操作步骤
第一步：创建虚拟环境，可在终端里执行如下命令：
# Windows系统
python -m venv myenv   （myenv是虚拟环境的名称）
# Linux或macOS系统
python3 -m venv myenv

第二步：激活虚拟环境
创建好虚拟环境后，需要将其激活，激活命令如下：
# Windows系统
myenv\Scripts\activate
# Linux或macOS系统
source myenv/bin/activate

第三步：安装依赖
在虚拟环境激活的状态下，就可以安装项目所需的依赖了。既可以逐个安装，也可以将所有依赖写入requirements.txt文件，然后批量安装。
# 逐个安装依赖
按照提供的依赖列表，在终端中依次执行pip install命令，例如：
pip install awscli==1.29.71
pip install boto==2.49.0
# 批量安装依赖
首先，把所有依赖信息复制到一个名为requirements.txt的文件中。然后，在终端执行以下命令进行批量安装：
pip install -r requirements.txt

第四步：验证安装
依赖安装完成后，可以通过以下命令查看已安装的包：
pip list


<!-- <针对Server.pyde 的代码分析及其功能 田佳祺编写> -->

这是一个基于Flask框架的C2（Command and Control）服务器系统:

主要功能包含：
    提供3个API端点：发送命令、接收响应和注册代理
    使用MySQL数据库存储代理注册信息
    通过SQS实现异步消息传递

适用场景：
    物联网设备管理、
    红队测试、
    分布式任务调度等需要集中控制的场景

代码特征总结：
    采用异步队列(SQS) + 同步HTTP(Flask)的通信方式
    无状态API + 持久化数据库的状态管理
    无认证机制的安全控制
    硬编码agent_id

关键技术点：
    异步通信
        通过SQS解耦服务端和设备，避免直接TCP连接
    数据持久化
        MySQL确保设备注册信息不丢失
    轻量级协议
        JSON格式平衡可读性和传输效率

        
<!-- <server_copy.py程序分析 - 作者:田佳祺> -->
系统架构：
    基于Flask框架的远程设备管理服务端实现

功能概述：
    通过消息队列实现双向设备通信
    为分布式系统提供集中式控制平面

核心模块：

    指令调度器：
        REST端点：/send-command (POST)
        协议：HTTP/1.1
        载荷：JSON编码指令对象
        队列：AWS SQS（标准队列）
        服务质量：至少一次投递

    响应处理器：
        REST端点：/receive-response (GET)
        轮询机制：短轮询实现
        队列：专用SQS响应队列
        响应格式：application/json（符合RFC 8259规范）
        状态码：标准HTTP响应代码

应用场景：
    物联网设备集群管理
    自动化测试编排
    分布式任务协调
    
