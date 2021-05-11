# 小美 - 美业预约机器人

机器人通过PaddleNLP预训练模型理解中文，使用Rasa构建主要Chatbot逻辑，并通过[chat-operator](https://github.com/xanthous-tech/chat-operator)对接Wechaty。

[项目](https://aistudio.baidu.com/aistudio/projectdetail/1899120)[介绍](./notebook.ipynb)

# 项目运行

## 项目依赖

* Python 3.7.9
* Pipenv

## 运行步骤

1. 首先运行 `make install` 通过pipenv安装依赖
2. 安装依赖之后运行 `make train` 训练机器人模型
3. 复制 `.env.local.template` 至 `.env.local` 然后添加企业微信相关变量 (`actions/calendar.py` 内有生成 `calendar_id` 相关代码)
3. 运行Action Server - `make actionserver`
4. 运行主服务器 `make server`
5. 根据 [chat-operator项目README](https://github.com/xanthous-tech/chat-operator) 运行chat-operator

# License

[MIT](./LICENSE)
