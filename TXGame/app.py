from flask import Flask, render_template, make_response, request, jsonify
import cv2
import numpy as np
import io
import requests
from PIL import Image
import random

app = Flask(__name__)

# APIS for huggingface
API_URL = "https://api-inference.huggingface.co/models/nerijs/pixel-art-xl"
headers = {"Authorization": "Bearer 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"}

@app.route('/')
def home():
    return render_template('index.html') # 引用位于templates文件夹中的index.html文件

#  随机生成按钮的逻辑
@app.route('/random', methods=['POST'])
def process_image():
    #  设定队列，包含各种prompt
    random_gender = ['male', 'female']
    random_age = ['10', '20', '30', '40', '50', '60']
    random_wear = ['green dress', 'blue dress', 'black pants', 'white pants']
    random_hair = ['green', 'blue', 'red', 'pink', 'yellow']
    #  在此处可以添加更多选项
    random_prompt = random.choice(random_gender) + "," + random.choice(random_age) + "years old, " + random.choice(random_wear) + random.choice(random_hair)

    # text_to_generate_image = request.form['text']
    text_to_generate_image = "pixel art, no shadow, flat colors, solid background" + random_prompt  # 写prompt的地方

    # 使用修改后的query函数调用Hugging Face API
    image_bytes = query_hf_model({
        "inputs": text_to_generate_image,
    })

    # 将字节流转为Image对象然后保存到临时文件或内存
    image = Image.open(io.BytesIO(image_bytes))
    temp_image_path = 'temp_generated_image.png'
    image.save(temp_image_path)

    # 调用上述定义的函数删除背景并获取处理过的图像
    processed_image_bytes = remove_background_and_save(temp_image_path)

    # 设置响应并发送图像
    response = make_response(processed_image_bytes)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = 'attachment; filename=output.png'
    return response

#  用户生成图片的逻辑
@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.get_json()  # 获取JSON数据

    # 提取数据
    gender = data['gender']
    model = data['model']
    description = data['description']
    if gender == 'option1':
        gender = 'female'
    else:
        gender = 'male'

    const_text = "pixel art,simple, no shadow, flat colors, solid background"
    text_to_generate_image = const_text + gender + description

    # 使用修改后的query函数调用Hugging Face API
    image_bytes = query_hf_model({
        "inputs": text_to_generate_image,
    })

    # 将字节流转为Image对象然后保存到临时文件或内存
    image = Image.open(io.BytesIO(image_bytes))
    temp_image_path = 'temp_generated_image.png'
    image.save(temp_image_path)

    # 调用上述定义的函数删除背景并获取处理过的图像
    processed_image_bytes = remove_background_and_save(temp_image_path)

    # 设置响应并发送图像
    response = make_response(processed_image_bytes)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = 'attachment; filename=output.png'
    return response

# using huggingface model
def query_hf_model(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  # 增加错误处理
    print("Loading...")
    return response.content

# 使用opencv来处理背景，进行抠图处理
# 有缺陷，函数只能抠除在一定范围内的纯色背景，要么通过prompt可以设定背景颜色，要么找到一键抠图的大模型
def remove_background_and_save(image_path, output_path='output.png', lower_val=(150, 150, 150), upper_val=(220, 220, 220)):
    # 加载图像
    img = cv2.imread(image_path)

    # 转换图像到RGB (OpenCV 默认使用BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 为背景定义颜色范围
    lower = np.array(lower_val)  # 根据您背景的颜色调整这些值
    upper = np.array(upper_val)  # 根据您背景的颜色调整这些值

    # 创建一个mask，其中背景像素为白色(255)其余为黑色(0)
    mask = cv2.inRange(img, lower, upper)

    # 转换图像到RGBA以便可以拥有透明的像素
    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)

    # 使所有由mask匹配的像素变为透明
    img[mask == 255] = [0, 0, 0, 0]

    # 转换OpenCV图像为PIL图像
    img_pil = Image.fromarray(img)

    # 将结果保存到内存缓冲区，以便可以将其发送回web页面
    img_byte_arr = io.BytesIO()
    img_pil.save(img_byte_arr, format='PNG')

    # 也可以选择将文件保存到磁盘
    img_pil.save(output_path, format='PNG')

    img_pil.save('GameAssets/character.png', format='PNG')

    # 返回二进制图像数据，这样可以在响应中使用
    return img_byte_arr.getvalue()


if __name__ == '__main__':
    app.run(debug=True)