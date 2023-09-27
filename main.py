from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import re
import subprocess
import os
from fastapi.staticfiles import StaticFiles
from fastapi import Depends, HTTPException
import shutil

app = FastAPI()
app.mount("/static", StaticFiles(directory="/download"), name="static")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class videourl(BaseModel):
    videourl: str

def clean_vtt_content(vtt_content):
    # Use regex to remove lines with timestamps and formatting
    cleaned_content = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*?\n", "", vtt_content)

    # Use regex to remove the <time><c>...</c> patterns
    cleaned_content = re.sub(r'<\d+:\d+:\d+\.\d+><c>.*?</c>', '', cleaned_content)

    return cleaned_content

# 定义全局变量
global_md_file_path = ""
global_video_id = ""

def download_subtitles_and_convert(url):
    global global_md_file_path, global_video_id
    # Extract video ID from URL
    video_id = url.split('=')[-1]
    global_video_id = video_id
    vtt_file_path = os.path.join(os.getcwd(), video_id + ".en.vtt")

    # Step 1: Use subprocess.run to call youtube-dl command to download subtitles
    output_template = "row-data/" + video_id
    print (output_template)
    command = ["youtube-dl", "--write-auto-sub", "--skip-download", "-o", video_id, url]
    subprocess.run(command)

    # 检查VTT文件是否存在
    if not os.path.exists(vtt_file_path):
        print("自动生成的字幕未找到，尝试下载原始字幕...")

        # 尝试下载原始字幕
        command = ["youtube-dl", "--write-sub", "--skip-download", "-o", video_id, url]
        subprocess.run(command)

        # 再次检查VTT文件是否存在
        if not os.path.exists(vtt_file_path):
            print("VTT文件未找到。下载可能失败。")
            return

    # Clean the VTT content
    with open(vtt_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        cleaned_content = clean_vtt_content(content)

    # Write cleaned content back to the VTT file
    with open(vtt_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

    # Step 2: Use pandoc to convert .vtt file to .md format
    md_file_path = os.path.splitext(vtt_file_path)[0] + ".md"
    command = ["pandoc", vtt_file_path, "-o", md_file_path]
    subprocess.run(command)

    command = ["python3", "main-web.py", md_file_path, "1、根据语义合理划分句子和段落;2、仅翻译为中文，不要总结和编造信息；3不需要附带任何引导语或前缀。"]
    print ("尝试处理文件！")
    subprocess.run(command)
    # 将数据赋值给全局变量
    global_md_file_path = md_file_path
    
    return md_file_path , video_id


@app.post("/your-backend-endpoint")
def receive_url(url_data: videourl):
    url = url_data.videourl
    download_subtitles_and_convert(url)
    md_file_path = global_md_file_path
    video_id = global_video_id
    print (md_file_path)
    print (type(video_id))
    final_file_name = "{}.ensplit_final.docx".format(video_id)
    # 定义目标路径
    final_file_name = "{}.ensplit_final.docx".format(video_id)
    final_file_path = "{}".format(final_file_name)
    destination_path = 'download/{}'.format(final_file_name)
    try:
        shutil.move(final_file_path, destination_path)
        print ('文件移动成功')
    except:
        print ('移动文件失败')
        pass
    print (url_data.videourl)  # 打印到控制台来检查
    # 这只是返回一个下载链接给前端
    download_link = "http://127.0.0.1:8000/static/{}".format(final_file_name)
    print ('!!!')
    print (download_link)
    return {"status": "success","downloadLink": download_link}


@app.post('/get-download-link')
def get_download_link():
    # 这只是返回一个下载链接给前端
    download_link = "my-vue-project/V8rCBb4GkC4.ensplit_mid.txt"
    return {"status": "success", "downloadLink": download_link}

