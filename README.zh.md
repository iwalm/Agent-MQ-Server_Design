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