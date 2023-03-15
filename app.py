# -*- coding:utf-8 -*-
import gradio as gr
import os
import sys
import argparse
from utils import *
from presets import *

my_api_key = ""  # 在这里输入你的 API 密钥

# if we are running in Docker
if os.environ.get('dockerrun') == 'yes':
    dockerflag = True
else:
    dockerflag = False

authflag = False

if dockerflag:
    my_api_key = os.environ.get('my_api_key')
    if my_api_key == "empty":
        print("Please give a api key!")
        sys.exit(1)
    # auth
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    if not (isinstance(username, type(None)) or isinstance(password, type(None))):
        authflag = True
else:
    if not my_api_key and os.path.exists("api_key.txt") and os.path.getsize("api_key.txt"):
        with open("api_key.txt", "r") as f:
            my_api_key = f.read().strip()
    if os.path.exists("auth.json"):
        with open("auth.json", "r") as f:
            auth = json.load(f)
            username = auth["username"]
            password = auth["password"]
            if username != "" and password != "":
                authflag = True

gr.Chatbot.postprocess = postprocess

with gr.Blocks(css=customCSS) as demo:
    history = gr.State([])
    token_count = gr.State([])
    promptTemplates = gr.State(load_template(get_template_names(plain=True)[0], mode=2))
    TRUECOMSTANT = gr.State(True)
    FALSECONSTANT = gr.State(False)
    topic = gr.State("Untitled Conversation History")

    with gr.Row():
        with gr.Column():
            keyTxt = gr.Textbox(show_label=True, placeholder=f"Type your OpenAI API-key...", value=my_api_key,
                                type="password", visible=not HIDE_MY_KEY, label="API-Key")
        with gr.Column():
            with gr.Row():
                model_select_dropdown = gr.Dropdown(label="Select Model", choices=MODELS, multiselect=False,
                                                    value=MODELS[0])
                use_streaming_checkbox = gr.Checkbox(label="Streaming", value=True, visible=enable_streaming_option)
    chatbot = gr.Chatbot()  # .style(color_map=("#1D51EE", "#585A5B"))
    with gr.Row():
        with gr.Column(scale=12):
            user_input = gr.Textbox(show_label=False, placeholder="Type your message...").style(
                container=False)
        with gr.Column(min_width=50, scale=1):
            submitBtn = gr.Button("Send", variant="primary")
    with gr.Row():
        emptyBtn = gr.Button("New Dialogue")
        retryBtn = gr.Button("Regenerate")
        delLastBtn = gr.Button("Delete Last Dialogue")
        reduceTokenBtn = gr.Button("Summarize Dialogue")
    status_display = gr.Markdown("status: ready")

    systemPromptTxt = gr.Textbox(show_label=True, placeholder=f"Enter System Prompt...", label="System prompt",
                                 value=initial_prompt).style(container=True)

    with gr.Accordion(label="Load Prompt Template", open=False):
        with gr.Column():
            with gr.Row():
                with gr.Column(scale=6):
                    templateFileSelectDropdown = gr.Dropdown(label="Select Prompt File",
                                                             choices=get_template_names(plain=True), multiselect=False,
                                                             value=get_template_names(plain=True)[0])
                with gr.Column(scale=1):
                    templateRefreshBtn = gr.Button("Refresh")
                    templaeFileReadBtn = gr.Button("Read Template")
            with gr.Row():
                with gr.Column(scale=6):
                    templateSelectDropdown = gr.Dropdown(label="Loading Prompt template",
                                                         choices=load_template(get_template_names(plain=True)[0],
                                                                               mode=1), multiselect=False,
                                                         value=load_template(get_template_names(plain=True)[0], mode=1)[
                                                             0])
                with gr.Column(scale=1):
                    templateApplyBtn = gr.Button("Apply")
    with gr.Accordion(label="Save/Load History", open=False):
        with gr.Column():
            with gr.Row():
                with gr.Column(scale=6):
                    saveFileName = gr.Textbox(
                        show_label=True, placeholder=f"Enter saved file name here...", label="Set file name",
                        value="Dialogue History").style(container=True)
                with gr.Column(scale=1):
                    saveHistoryBtn = gr.Button("Save Dialogue")
            with gr.Row():
                with gr.Column(scale=6):
                    historyFileSelectDropdown = gr.Dropdown(label="Load Dialogue",
                                                            choices=get_history_names(plain=True), multiselect=False,
                                                            value=get_history_names(plain=True)[0])
                with gr.Column(scale=1):
                    historyRefreshBtn = gr.Button("Refresh")
                    historyReadBtn = gr.Button("Load Dialogue")
    # inputs, top_p, temperature, top_k, repetition_penalty
    with gr.Accordion("Parameter", open=False):
        top_p = gr.Slider(minimum=-0, maximum=1.0, value=1.0, step=0.05,
                          interactive=True, label="Top-p (nucleus sampling)", )
        temperature = gr.Slider(minimum=-0, maximum=5.0, value=1.0,
                                step=0.1, interactive=True, label="Temperature", )

    user_input.submit(predict, [keyTxt, systemPromptTxt, history, user_input, chatbot, token_count, top_p, temperature,
                                use_streaming_checkbox, model_select_dropdown],
                      [chatbot, history, status_display, token_count], show_progress=True)
    user_input.submit(reset_textbox, [], [user_input])

    submitBtn.click(predict, [keyTxt, systemPromptTxt, history, user_input, chatbot, token_count, top_p, temperature,
                              use_streaming_checkbox, model_select_dropdown],
                    [chatbot, history, status_display, token_count], show_progress=True)
    submitBtn.click(reset_textbox, [], [user_input])

    emptyBtn.click(reset_state, outputs=[chatbot, history, token_count, status_display], show_progress=True)

    retryBtn.click(retry,
                   [keyTxt, systemPromptTxt, history, chatbot, token_count, top_p, temperature, use_streaming_checkbox,
                    model_select_dropdown], [chatbot, history, status_display, token_count], show_progress=True)

    delLastBtn.click(delete_last_conversation,
                     [chatbot, history, token_count, use_streaming_checkbox, model_select_dropdown], [
                         chatbot, history, token_count, status_display], show_progress=True)

    reduceTokenBtn.click(reduce_token_size, [keyTxt, systemPromptTxt, history, chatbot, token_count, top_p, temperature,
                                             use_streaming_checkbox, model_select_dropdown],
                         [chatbot, history, status_display, token_count], show_progress=True)

    saveHistoryBtn.click(save_chat_history, [
        saveFileName, systemPromptTxt, history, chatbot], None, show_progress=True)

    saveHistoryBtn.click(get_history_names, None, [historyFileSelectDropdown])

    historyRefreshBtn.click(get_history_names, None, [historyFileSelectDropdown])

    historyReadBtn.click(load_chat_history, [historyFileSelectDropdown, systemPromptTxt, history, chatbot],
                         [saveFileName, systemPromptTxt, history, chatbot], show_progress=True)

    templateRefreshBtn.click(get_template_names, None, [templateFileSelectDropdown])

    templaeFileReadBtn.click(load_template, [templateFileSelectDropdown], [promptTemplates, templateSelectDropdown],
                             show_progress=True)

    templateApplyBtn.click(get_template_content, [promptTemplates, templateSelectDropdown, systemPromptTxt],
                           [systemPromptTxt], show_progress=True)

# 默认开启本地服务器，默认可以直接从IP访问，默认不创建公开分享链接
demo.title = "Amuro.ai"

if __name__ == "__main__":
    # if running in Docker
    if dockerflag:
        if authflag:
            demo.queue().launch(server_name="0.0.0.0", server_port=7860, auth=(username, password))
        else:
            demo.queue().launch(server_name="0.0.0.0", server_port=7860, share=False)
    # if not running in Docker
    else:
        if authflag:
            demo.queue().launch(share=False, auth=(username, password))
        else:
            demo.queue().launch(server_name="0.0.0.0", server_port=7860, share=False)  # 改为 share=True 可以创建公开分享链接
        # demo.queue().launch(server_name="0.0.0.0", server_port=7860, share=False) # 可自定义端口
        # demo.queue().launch(server_name="0.0.0.0", server_port=7860,auth=("在这里填写用户名", "在这里填写密码")) # 可设置用户名与密码
        # demo.queue().launch(auth=("在这里填写用户名", "在这里填写密码")) # 适合Nginx反向代理
