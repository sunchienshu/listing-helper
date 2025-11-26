<!-- end list -->
import streamlit as st
import google.generativeai as genai
import os

# 1. 页面基础设置
st.set_page_config(page_title="亚马逊 Listing 助手", page_icon="🛍️")
st.title("🛍️ 亚马逊 Listing 写作助手")

# 2. 读取密码箱里的 API Key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ 还没有配置 API Key！请在 Streamlit 后台的 Secrets 里添加。")
    st.stop()

# 3. 设置 AI 模型
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. 界面布局
with st.sidebar:
    st.header("⚙️ 选项设置")
    tone = st.selectbox("语气风格", ["专业 (Professional)", "有吸引力 (Engaging)", "简洁 (Concise)"])
    lang = st.selectbox("输出语言", ["English (英语)", "German (德语)", "French (法语)"])

st.info("💡 使用说明：输入中文或英文的产品参数，AI 将自动生成符合亚马逊格式的文案。")

# 5. 输入框
product_input = st.text_area("请输入产品信息（关键词、参数、卖点）：", height=150, placeholder="例如：运动水壶，32oz，不锈钢，双层真空保温，防漏盖子...")

# 6. 按钮与生成逻辑
if st.button("🚀 开始生成 Listing", type="primary"):
    if not product_input:
        st.warning("请先输入一点内容再点击生成哦！")
    else:
        with st.spinner('AI 正在疯狂打字中...'):
            try:
                # 给 AI 的指令
                prompt = f"""
                请作为亚马逊资深运营，用 {tone} 的语气，使用 {lang} 语言，根据以下产品信息撰写 Listing。
                包含：Title (标题), Bullet Points (五点描述), Product Description (产品描述)。
                产品信息：{product_input}
                """
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                st.success("生成成功！")
            except Exception as e:
                st.error(f"出错了，请检查网络或 Key: {e}")