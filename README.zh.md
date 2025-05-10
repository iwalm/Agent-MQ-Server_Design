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