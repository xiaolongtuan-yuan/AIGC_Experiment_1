# -*- coding: utf-8 -*-
"""
@Time ： 2024/11/2 19:43
@Auth ： xiaolongtuan
@File ：image_search.py
"""
import os

import openai
import requests
api_key = os.getenv("SERPAPI_KEY")
if not api_key:
    raise ValueError("API密钥未找到，请在环境变量中设置'SERPAPI_KEY'。")
def google_image_search(query, num_images, save_dir="images"):
    search_engine_id = 'google_images'

    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "engine": search_engine_id,
        "api_key": api_key,
        "num": num_images
    }
    response = requests.get(url, params=params)
    results = response.json()
    # 创建保存目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    saved_images = []
    for index, item in enumerate(results.get("images_results", [])):
        image_url = item.get("original")
        image_title = item.get("title")
        try:
            image_path = os.path.join(save_dir, f"{query}_{index + 1}.jpg")
            download_image(image_url, image_path)
            saved_images.append(image_path)
        except Exception as e:
            print(f"Failed to download image: {image_url}, error: {e}")
        if len(saved_images) >= num_images:
            break

    return saved_images


def download_image(image_url, save_path):
    """
    下载图片并保存到本地。
    参数：
    - image_url: str，图片的URL
    - save_path: str，保存图片的路径（包括文件名和扩展名）

    返回值：
    - bool，是否下载成功
    """
    try:
        # 发起请求下载图片数据
        response = requests.get(image_url)
        response.raise_for_status()  # 检查请求是否成功

        # 将图片数据写入文件
        with open(save_path, "wb") as f:
            f.write(response.content)

        print(f"图片已成功保存到 {save_path}")
        return True
    except Exception as e:
        print(f"下载图片失败: {e}")
        return False


def extract_keyword(text):
    """
    使用 OpenAI API 从一句话中提取最重要的关键词。

    参数：
    - text: str，输入的文本

    返回值：
    - str，提取出的关键词
    """
    # 从环境变量获取 API 密钥
    openai.api_key = os.getenv("OPENAI_KEY")

    if not openai.api_key:
        raise ValueError("API密钥未找到，请在环境变量中设置 'OPENAI_KEY'。")

    messages = [{
        'role': 'user',
        'content': f"从以下句子中提取最重要的一个关键词：\n\n{text}\n\n关键词："
    }]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=10,
        temperature=0
    )

    # 提取关键词
    keyword = response.choices[0].message.content.strip()
    return keyword

def get_relative_images(query):
    keyword = extract_keyword(query)
    print(keyword)
    query = keyword
    num_images = 5
    saved_images = google_image_search(query, num_images)
    images = []
    for image in saved_images:
        images.append({
            "image_path": image,
            "topic": keyword
        })

    return images

if __name__ == '__main__':
    # query = "酒店"
    # num_images = 5
    # saved_images = google_image_search(query, num_images)
    #
    # # 打印保存的图片路径和标题
    # for image_path, image_title in saved_images:
    #     print(f"图片路径: {image_path}, 图片标题: {image_title}")

    text = "酒店经营情况"
    keyword = extract_keyword(text)
    print(keyword)
    query = keyword
    num_images = 5
    saved_images = google_image_search(query, num_images)
    for image_path in saved_images:
        print(f"图片路径: {image_path}")