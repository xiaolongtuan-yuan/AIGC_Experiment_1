import os
import streamlit as st
from ppt_agent import PPTAgent

st.title("ChatPPT Generator")
st.write("Generate a slide presentation using AI!")

api_key = os.getenv("OPENAI_KEY")
if not api_key:
    raise ValueError("OPENAI_KEY密钥未找到，请在环境变量中设置'OPENAI_KEY'。")
chat_ppt = PPTAgent(api_key)

topic = st.text_input("PPT 主题")
num_slides = st.slider("页数", 5, 20, 8)
language = st.selectbox("选择语言", ["en", "cn"])
uploaded_files = st.file_uploader("请选择一个文件", type=["csv"],accept_multiple_files=True)
if uploaded_files is not None:
    # 显示上传的文件名
    for uploaded_file in uploaded_files:
        file_content = uploaded_file.read()
        file_content_str = file_content.decode("utf-8")
        save_directory = "files"
        save_path = os.path.join(save_directory, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(file_content)
        chat_ppt.upload_files(save_path)

generate_button = st.button("生成幻灯片", disabled=False)

if generate_button:
    with st.spinner("正在生成..."):
        try:
            ppt_content = chat_ppt.gen_ppt_content(topic, num_slides, language)
        except Exception as e:
            st.error(f"Error generating Slide: {e}")
            st.stop()

        title = ppt_content.get("title", "")
        st.title(f"Title: {title}")
        slides = ppt_content.get("pages", [])
        st.subheader(f"幻灯片共 {len(slides)} 页:")

        for index, slide in enumerate(slides):
            st.markdown(f"- Slide {index+1}: {slide.get('title','')}")

        try:
            ppt_file_name = chat_ppt.generate_ppt(ppt_content)
        except Exception as e:
            st.error(f"Error generating Slide: {e}")
            st.stop()

        # Provide a download link for the Slide
        st.write("生成成功!")
        st.write("下载幻灯片:")
        save_path = os.path.join('files', ppt_file_name)
        with open(save_path, "rb") as f:
            st.download_button("下载文件", f, ppt_file_name)
