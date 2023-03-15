# -*- coding:utf-8 -*-
customCSS = """
code {
    display: inline;
    white-space: break-spaces;
    border-radius: 6px;
    margin: 0 2px 0 2px;
    padding: .2em .4em .1em .4em;
    background-color: rgba(175,184,193,0.2);
}
pre code {
    display: block;
    white-space: pre;
    background-color: hsla(0, 0%, 0%, 72%);
    border: solid 5px var(--color-border-primary) !important;
    border-radius: 10px;
    padding: 0 1.2rem 1.2rem;
    margin-top: 1em !important;
    color: #FFF;
    box-shadow: inset 0px 8px 16px hsla(0, 0%, 0%, .2)
}
"""

summarize_prompt = "请总结以上对话，不超过100字。" # 总结对话时的 prompt
MODELS = ["gpt-3.5-turbo"] # 可选的模型

# 错误信息
standard_error_msg = "☹️发生了错误：" # 错误信息的标准前缀
error_retrieve_prompt = "请检查网络连接，或者API-Key是否有效。" # 获取对话时发生错误
connection_timeout_prompt = "连接超时，无法获取对话。" # 连接超时
read_timeout_prompt = "读取超时，无法获取对话。" # 读取超时
proxy_error_prompt = "代理错误，无法获取对话。" # 代理错误
ssl_error_prompt = "SSL错误，无法获取对话。" # SSL 错误
no_apikey_msg = "API key长度不是51位，请检查是否输入正确。" # API key 长度不足 51 位

max_token_streaming = 3500 # 流式对话时的最大 token 数
timeout_streaming = 15 # 流式对话时的超时时间
max_token_all = 3500 # 非流式对话时的最大 token 数
timeout_all = 200 # 非流式对话时的超时时间
enable_streaming_option = True  # 是否启用选择选择是否实时显示回答的勾选框
HIDE_MY_KEY = False # 如果你想在UI中隐藏你的 API 密钥，将此值设置为 True
