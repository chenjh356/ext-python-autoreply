# ext-python-autoreply
e小天python自动回复

## 模块需求
- websocket_client
- websockets
- python3.X

安装

`pip install websocket_client`

`pip install websockets`

## 功能
- 个人微信号信息自动回复
- 群@消息记录，并自动回复

文件说明：
- main.py是主文件，可以在上面扩展自动回复条件，功能等
- config.py是配置文件，上面配置自动回复的文字，最大回复次数
- reply_time.py是记录回复次数的文件

## 使用步骤
- 先搜索AutoReply，添加后回到个人中心，安装
- 安装好之后打开e小天的客户端界面，打开“插件目录”，进入文件夹“AutoReply”
- 编辑config.py的设置，保存
- 回到插件管理页面，点击启动即可
