import gradio as gr
import requests


def upload_file(file):
    if file is None:
        return "请上传文件。"

    files = {'file': (file.name, open(file.name, 'rb'))}
    try:
        response = requests.post("http://localhost:8000/documents/upload", files=files)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return f"上传成功！文件名: {data['filename']}\n消息: {data['message']}\n已加载文件: {data['loaded_files']}"
            else:
                return "上传失败: " + str(data)
        else:
            return f"上传失败，状态码: {response.status_code}"
    except Exception as e:
        return f"上传出错: {str(e)}"


def chat_function(message, history):
    try:
        response = requests.post("http://localhost:8000/chat", json={"session_id": "1", "query": message})
        if response.status_code == 200:
            data = response.json()
            return data.get("answer", "无响应")
        else:
            return f"聊天失败，状态码: {response.status_code}"
    except Exception as e:
        return f"聊天出错: {str(e)}"


with gr.Blocks() as demo:
    gr.Markdown("# Allen Agent")

    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("## 聊天框")
            chat = gr.ChatInterface(
                fn=chat_function,
                title="与AI聊天"
            )

        with gr.Column(scale=1):
            gr.Markdown("## 文件上传")
            upload_btn = gr.UploadButton("上传文件", file_types=[".pdf", ".docx", ".txt"])  # 可以调整文件类型
            output = gr.Textbox(label="上传状态")
            upload_btn.upload(upload_file, upload_btn, output)

demo.launch()
