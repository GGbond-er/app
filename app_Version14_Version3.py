import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import os
import base64

# =============== 登录页面配置 ===============
APP_DISPLAY_NAME = "👨‍⚕️智能鱼疾检测系统"
LOGIN_LOGO_PATH = "login_logo.png"   # 可选：登录页左侧图标
LOGIN_CARD_WIDTH_PX = 760

def _img_to_base64(path: str):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

def _do_rerun():
    """兼容不同版本的 rerun"""
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

def render_login_page():
    """
    登录页面（装饰用）
    - 已移除密码占位提示文字 & 说明提示
    - 已移除显示/隐藏密码按钮
    - 标题整体居中
    - 去除顶部多余白色方块（通过 CSS 覆盖默认主容器背景）
    """
    st.set_page_config(
        page_title=APP_DISPLAY_NAME,
        page_icon="🐟",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    st.markdown(f"""
    <style>
        body, .stApp {{
            background: radial-gradient(circle at 30% 30%, #eef6ff 0%, #f5f8fb 55%, #ffffff 100%) !important;
        }}
        /* 去除默认主容器白色块与阴影 */
        .block-container {{
            background: transparent !important;
            box-shadow: none !important;
            padding-top: 0.5rem !important;
        }}
        /* 登录外部封装 */
        .login-wrapper {{
            max-width: {LOGIN_CARD_WIDTH_PX}px;
            margin: 2.2rem auto 3rem auto;
        }}
        .login-card {{
            background: #ffffff;
            border: 1px solid #dce3eb;
            border-radius: 14px;
            padding: 2rem 2.4rem 2.4rem 2.4rem;
            box-shadow: 0 4px 16px -4px rgba(30,64,175,0.10), 0 2px 6px rgba(0,0,0,0.04);
            position: relative;
        }}
        /* 标题区域（居中） */
        .login-head {{
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1.2rem;
            margin-bottom: 1.8rem;
            text-align: center;
            flex-wrap: wrap;
        }}
        .login-logo {{
            width: 70px; height: 70px; border-radius: 18px;
            background: linear-gradient(135deg,#22c55e,#16a34a);
            display: flex; align-items: center; justify-content: center;
            font-size: 2.1rem; color:#fff; font-weight: 700;
            box-shadow: 0 4px 10px -2px rgba(22,163,74,.38);
        }}
        .login-text-block {{
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }}
        .login-title {{
            font-size: 2.05rem; font-weight: 800; line-height: 1.15;
            background: linear-gradient(90deg,#0f3e8a,#1d79ff);
            -webkit-background-clip: text; color: transparent;
            letter-spacing: .5px;
            white-space: nowrap;
        }}
        @media (max-width: 680px) {{
            .login-title {{ white-space: normal; }}
        }}
        .login-sub {{
            font-size: .9rem; color:#60708a; margin-top:.35rem;
        }}
        .login-footer {{
            margin-top: 1.8rem; font-size: .75rem; color:#94a3b8; text-align: right;
        }}
        .stTextInput label {{
            font-weight:500; color:#334155 !important;
        }}
        .login-btn button {{
            background: #1d72ff !important;
            border: 1px solid #1b66e6 !important;
            color:#fff !important;
            font-weight:600;
            padding:.55rem 1.4rem;
            border-radius: 9px !important;
            box-shadow: 0 2px 6px rgba(29,114,255,.35);
        }}
        .login-btn button:hover {{
            background:#1663dd !important; border-color:#1559c6 !important;
        }}
    </style>
    """, unsafe_allow_html=True)

    logo_b64 = _img_to_base64(LOGIN_LOGO_PATH)

    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        # 顶部标题
        if logo_b64:
            st.markdown(
                f"""
                <div class="login-head">
                    <div><img src="data:image/png;base64,{logo_b64}"
                              style="width:70px;height:70px;border-radius:18px;box-shadow:0 4px 10px -2px rgba(0,0,0,.15);" /></div>
                    <div class="login-text-block">
                        <div class="login-title">{APP_DISPLAY_NAME}</div>
                        <div class="login-sub">多模态鱼类健康辅助 · 智能识别 / 分析 / 诊断 / 交流</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="login-head">
                    <div class="login-logo">🐟</div>
                    <div class="login-text-block">
                        <div class="login-title">{APP_DISPLAY_NAME}</div>
                        <div class="login-sub">多模态鱼类健康辅助 · 智能识别 / 分析 / 诊断 / 交流</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # 表单
        with st.form("login_form", clear_on_submit=False):
            account = st.text_input("账号名称", key="login_account", placeholder="例如：farmer_001")
            password = st.text_input("账号密码", key="login_password", type="password", placeholder="")
            login_clicked = st.form_submit_button("登录", use_container_width=False)
            if login_clicked:
                st.session_state.logged_in = True
                st.session_state.current_user = (account or "").strip() or "访客用户"
                _do_rerun()

        st.markdown('<div class="login-footer">© 2025 渔康智鉴 | Demo 登录界面</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 未登录：显示登录页
if not st.session_state.get("logged_in", False):
    render_login_page()
    st.stop()

# =============== 已登录后主程序 ===============

SIDEBAR_TU_AN_WIDTH = 44
SIDEBAR_WENZI_WIDTH = 170
HOME_WENZI_WIDTH = 520

BRAND_LOGO_PATH = "tu_an.png"
BRAND_TEXT_PATH = "wenzi.png"

st.set_page_config(
    page_title="渔康智鉴",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 顶部退出登录
logout_col = st.columns([0.86, 0.14])[1]
with logout_col:
    if st.button("退出登录", help="返回登录页"):
        st.session_state.logged_in = False
        _do_rerun()

# 主应用 CSS（保持原样）
st.markdown(f"""
<style>
    .main-header {{ font-size: 3rem; color: #1f77b4; text-align: center; margin: 4rem 0 1rem 0; line-height: 1.3; scroll-margin-top: 5rem; }}
    .sub-header {{ font-size: 1.2rem; color: #2ca02c; text-align: center; margin-bottom: 1.25rem; }}
    .feature-list {{ font-size: 1.1rem; line-height: 2; margin-left: 1.5rem; }}
    .divider {{ margin: 0.75rem 0 1.25rem 0; border-top: 1px solid #e6e6e6; }}
    .preset-question {{ margin: 0.5rem 0; padding: 0.5rem; border: 1px solid #ddd; border-radius: 0.5rem; cursor: pointer; }}
    .preset-question:hover {{ background-color: #f5f5f5; }}
    .block-container {{ padding-top: 1.75rem; }}
    .qa-tagline {{ text-align: center; color: #ff4d4f; font-size: 0.95rem; font-weight: 600; margin: -0.1rem 0 0.75rem 0; }}

    .sidebar-brand {{ display: flex; align-items: center; gap: 8px; padding: 10px 6px 2px 6px; }}
    .sidebar-logo {{ width: {SIDEBAR_TU_AN_WIDTH}px; height: auto; display: block; }}
    .sidebar-wenzi {{ width: {SIDEBAR_WENZI_WIDTH}px; height: auto; display: block; }}
    .sidebar-brand-spacer {{ height: 0.25rem; }}

    .home-title {{ display: flex; justify-content: center; margin: 2rem 0 1rem 0; width: 100%; scroll-margin-top: 5rem; }}
    .home-wenzi {{ width: {HOME_WENZI_WIDTH}px; max-width: 85vw; height: auto; display: block; }}

    .title-divider {{ height: 3px; background: linear-gradient(90deg, #1e90ff, #2c7be5); border-radius: 2px; width: 82%; margin: 0.15rem auto 0.9rem auto; }}
    .section-label {{ font-size: 1rem; font-weight: 700; color: #334155; margin: 0.25rem 0 0.5rem 0; text-align: left; }}
    .greeting {{ display: inline-flex; align-items: center; gap: 10px; background: #f0f7ff; border: 1px solid #d6e6ff; color: #0f3e8a; padding: 10px 12px; border-radius: 12px; margin: 0.25rem 0 1.1rem 0; }}
    .greeting .icon {{ background: #ffd782; color: #915c00; display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px; border-radius: 6px; font-size: 16px; }}

    .ai-hr {{ border: 0; height: 0; border-top: 6px solid #7c8aa0; width: 100%; margin: 0.5rem 0 0.9rem 0; border-radius: 2px; }}
    .ai-hr-line {{ height: 6px; 背景: #7c8aa0; border-radius: 2px; width: 100%; margin: 0.5rem 0 0.9rem 0; }}
    .ai-hint-subtitle {{ color: #64748b; font-size: 0.9rem; margin: 0.1rem 0 0.6rem 0; text-align: left; width: 100%; }}

    .forum-title {{ font-size: 1.8rem; font-weight: 900; color: #111827; margin: 3.2rem 0 1.0rem 0; line-height: 1.25; scroll-margin-top: 5rem; display: flex; align-items: center; gap: .5rem; }}
    .forum-section-title {{ font-size: 1.6rem; font-weight: 800; color: #0f172a; margin: 0.75rem 0 0.5rem 0; display:flex; align-items:center; gap:.5rem; }}
    .post-title {{ font-size: 1.2rem; font-weight: 700; color: #0f172a; }}
    .post-block {{ border: 1px solid #e5e7eb; border-radius: 12px; padding: 12px 14px; margin: 10px 0; background:#fff; }}
    .post-meta {{ color: #64748b; font-size: 0.92rem; margin-top: 4px; }}

    .heat-wrap {{ margin-top: 6px; }}
    .heat-label {{ color:#475569; font-size: .9rem; margin-bottom: 4px; }}
    .heat-track {{ width: 100%; height: 8px; background: #e2e8f0; border-radius: 9999px; overflow: hidden; }}
    .heat-fill {{ height: 100%; background: linear-gradient(90deg,#1e90ff,#2c7be5); border-radius: 9999px; width: 0%; }}

    .read-btn {{ border: 1px solid #e5e7eb; background:#fff; color:#0f172a; padding: 4px 10px; border-radius: 8px; font-size: .9rem; }}
    .read-btn:hover {{ background:#f8fafc; border-color:#cbd5e1; }}

    .article-title {{ font-size: 2.6rem; font-weight: 900; color:#111827; margin: .1rem 0 .6rem 0; }}
    .article-meta {{ color:#64748b; font-size: 1.05rem; margin-bottom: 1.2rem; }}
    .expert-reply {{ font-size: 1.3rem; font-weight: 800; color:#0f172a; margin: 1rem 0 .5rem 0; }}
    .article-content {{ font-size: 1.18rem; line-height: 1.9; color:#1f2937; }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label {{ justify-content: flex-start !important; text-align: left !important; width: 100%; }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label p {{ text-align: left !important; margin: 0; }}

    .detect-btn {{
        background: #b0a6ff;
        color: #fff;
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        font-size: 1.05rem;
        cursor: pointer;
        box-shadow: 0 2px 6px rgba(0,0,0,.08);
    }}
    .detect-btn:hover {{ background: #a497ff; }}
    .detect-btn:active {{ transform: translateY(1px); }}
</style>
""", unsafe_allow_html=True)

logo_b64 = _img_to_base64(BRAND_LOGO_PATH)
wenzi_b64 = _img_to_base64(BRAND_TEXT_PATH)

with st.sidebar:
    if logo_b64 and wenzi_b64:
        st.markdown(
            f"""
            <div class="sidebar-brand">
                <img class="sidebar-logo" src="data:image/png;base64,{logo_b64}" />
                <img class="sidebar-wenzi" src="data:image/png;base64,{wenzi_b64}" />
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        brand_container = st.container()
        col_logo, col_word = brand_container.columns([1, 4])
        with col_logo:
            if os.path.exists(BRAND_LOGO_PATH):
                st.image(BRAND_LOGO_PATH, width=SIDEBAR_TU_AN_WIDTH)
            else:
                st.info("缺少 tu_an.png（放到应用根目录）")
        with col_word:
            if os.path.exists(BRAND_TEXT_PATH):
                st.image(BRAND_TEXT_PATH, width=SIDEBAR_WENZI_WIDTH)
            else:
                st.info("缺少 wenzi.png（放到应用根目录）")

    st.markdown('<div class="sidebar-brand-spacer"></div>', unsafe_allow_html=True)
    st.title("导航")
    st.caption(f"当前用户：{st.session_state.get('current_user','访客')}")

PAGE_WELCOME = "🎉欢迎"
PAGE_CAPTURE = "📸开始识别"
PAGE_DATA = "🔍数据查询"
PAGE_QA = "🧠问答助手"
PAGE_FORUM = "📢交流论坛"

page = st.sidebar.radio("选择页面", [PAGE_WELCOME, PAGE_CAPTURE, PAGE_DATA, PAGE_QA, PAGE_FORUM])

if page == PAGE_DATA:
    with st.sidebar:
        with st.expander("📝 操作说明", expanded=False):
            st.markdown(
                """<div style="white-space: pre-line;">
1.📊识别结果：展示患病种类及数目的原始数据、柱状图和饼状图。
 2.📈趋势分析：展示患病数目随时间变化的原始数据及趋势图。
 3.🧠建议生成：解释通义千问大模型提供的治疗建议。
</div>""",
                unsafe_allow_html=True
            )

if page == PAGE_CAPTURE:
    with st.sidebar:
        with st.expander("📝 操作说明", expanded=False):
            st.markdown(
                "1.📹 模型支持图片、视频、摄像头三种数据来源<br>"
                "2.🎚️ 通过调节置信度可以提高模型识别质量<br>"
                " 3.🚀 点击「开始检测」按钮输出结果",
                unsafe_allow_html=True
            )
        with st.expander("⚙️ 高级选项", expanded=False):
            st.markdown("**置信度阈值**")
            confidence = st.slider("置信度阈值", 0.70, 0.99,
                                   float(st.session_state.get("confidence", 0.90)), 0.01, format="%.2f")
            st.session_state["confidence"] = confidence
            c1, c2 = st.columns(2)
            with c1: st.caption("0.70")
            with c2: st.markdown('<div style="text-align:right;color:#64748b;">0.99</div>', unsafe_allow_html=True)
            with st.expander("数据来源", expanded=False):
                source = st.radio("请选择来源", ["图片", "视频", "摄像头"],
                                  index=["图片","视频","摄像头"].index(st.session_state.get("source","图片")),
                                  horizontal=True)
                st.session_state["source"] = source

if page == PAGE_QA:
    with st.sidebar:
        with st.expander("📝 操作说明", expanded=False):
            st.markdown(
                "- 1.💬 输入问题：在下方输入框中输入你的问题，点击发送按钮。\n"
                "- 2.🔍 查看回答：系统会根据知识图谱和通义千问模型生成回答，并展示在聊天记录中。\n"
                "- 3.✨ 查看示例问题：点击上方的示例问题按钮，快速获取常见问题的回答。"
            )

if page == PAGE_WELCOME:
    with st.sidebar:
        with st.expander("🧰 各个页面功能说明", expanded=False):
            st.markdown("""
1. 🎉欢迎页面：展示应用特色及技术架构介绍。
2. 📸开始识别页面：支持图片、视频、摄像头三种数据来源的鱼类疾病智能识别。
3. 🔍数据查询页面：可视化展示鱼类健康状况数据，提供柱状图、饼图分析和AI治疗建议。
4. 🧠问答助手页面：基于通义千问大模型的智能问答系统，提供鱼类养殖专业咨询。
5. 📢交流论坛页面：养殖户交流平台，包含热门帖子、最新发帖和专家回复功能。
            """)

def write_reply_sidebar(post_key="post1"):
    with st.sidebar:
        with st.expander("📝我要回复", expanded=False):
            reply = st.text_area("评论内容", height=120, key=f"{post_key}_reply")
            author = st.text_input("作者", value="匿名", key=f"{post_key}_author")
            c1, c2 = st.columns(2)
            with c1: submit = st.button("立即发布", key=f"{post_key}_submit")
            with c2: refresh = st.button("刷新数据", key=f"{post_key}_refresh")
            if f"{post_key}_comments" not in st.session_state:
                st.session_state[f"{post_key}_comments"] = []
            if submit:
                if not reply:
                    st.warning("请先填写评论内容。")
                else:
                    st.session_state[f"{post_key}_comments"].append({
                        "content": reply,
                        "author": author or "匿名",
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.success("评论已发布！")
            if refresh:
                _do_rerun()

def call_qwen_api(prompt: str):
    try:
        api_key = (
            os.getenv("DASHSCOPE_API_KEY")
            or (st.secrets.get("DASHSCOPE_API_KEY") if hasattr(st, "secrets") else None)
        )
        if not api_key:
            return "未配置通义千问 API Key。请设置环境变量 DASHSCOPE_API_KEY 或在 Streamlit 的 secrets 中配置。"

        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {
            "model": "qwen-turbo",
            "input": {"messages": [
                {"role": "system", "content": "你是一个鱼类疾病专家，专门回答关于鱼类健康、疾病治疗和预防的问题。请提供专业、准确的建议。"},
                {"role": "user", "content": prompt}
            ]},
            "parameters": {"result_format": "message"}
        }
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        if "output" in result and "choices" in result["output"] and result["output"]["choices"]:
            return result["output"]["choices"][0]["message"]["content"]
        else:
            return "获取回答时出错：接口返回内容不完整，请检查 API Key 或参数。"
    except requests.Timeout:
        return "请求超时，请稍后重试或检查网络连接。"
    except requests.HTTPError as e:
        try:
            err = response.json()
        except Exception:
            err = {"message": str(e)}
        return f"HTTP 错误：{err}"
    except Exception as e:
        return f"调用API时出错: {str(e)}"

# ---------------- 主内容 ----------------
if page == PAGE_WELCOME:
    if wenzi_b64:
        st.markdown(f'<div class="home-title"><img class="home-wenzi" src="data:image/png;base64,{wenzi_b64}" /></div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<h1 class="main-header">渔康智鉴</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">基于深度学习和生成式人工智能的多维度鱼类养殖助手</p>', unsafe_allow_html=True)

    video_path = "video-2.mp4"
    if os.path.exists(video_path):
        left, center, right = st.columns([1, 2, 1])
        with center:
            st.video(video_path, format="video/mp4", start_time=0)
    else:
        st.info("未找到 video-2.mp4，请确保文件位于应用根目录。")

    st.markdown("### 功能介绍")
    for feature in ["鱼类疾病智能识别与诊断", "养殖数据可视化分析", "个性化治疗建议与预防措施", "鱼类健康知识问答"]:
        st.markdown(f"- **{feature}**")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 技术架构\n本系统采用先进的深度学习技术和生成式人工智能模型，结合专业鱼类疾病知识库，为鱼类养殖提供全方位的智能支持。")

elif page == PAGE_CAPTURE:
    img_path = "photo1.jpg"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.info("未找到 photo1.jpg，请将其放到应用根目录。")

elif page == PAGE_DATA:
    st.markdown('<h1 class="main-header">🔍 数据查询</h1>', unsafe_allow_html=True)
    try:
        df = pd.read_excel("data.xlsx")
        df.columns = [str(c).strip() for c in df.columns]
        category_cols = [
            c for c in df.columns
            if (not str(c).startswith("Unnamed")) and c not in ("鱼类总数", "时间", "患病总数")
        ]
        dist_series = pd.to_numeric(df.loc[0, category_cols], errors="coerce").fillna(0)
        total_val = pd.to_numeric(df.loc[0, "鱼类总数"], errors="coerce")
        if pd.isna(total_val) or total_val <= 0:
            total_val = float(dist_series.sum())
        df_display = pd.DataFrame({
            "类别": category_cols,
            "数量": dist_series.values.astype(int),
            "占比(%)": (dist_series / total_val * 100).round(2)
        })
        df_display_total = pd.concat(
            [df_display, pd.DataFrame([{"类别": "总数", "数量": int(round(total_val)), "占比(%)": 100.00}])],
            ignore_index=True
        )

        st.success("数据加载成功！")
        st.subheader("原始数据（清洗后）")
        st.dataframe(df_display_total, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("鱼类健康状况分布（柱状图）")
            st.bar_chart(df_display.set_index('类别')[['数量']], use_container_width=True)
        with col2:
            st.subheader("鱼类健康状况分布（饼图）")
            try:
                import plotly.express as px
                fig = px.pie(df_display, values="数量", names="类别", title="鱼类健康状况分布")
                st.plotly_chart(fig, use_container_width=True)
            except ImportError:
                st.info("饼图需要 plotly 库支持。请在 requirements.txt 中添加 'plotly>=5.15.0'")

        st.markdown("---")
        with st.expander("📈 趋势分析", expanded=False):
            st.subheader("患病鱼总数随时间变化趋势")
            first_col = df.columns[0]
            time_row_idx = df.index[df[first_col].astype(str).str.contains("时间", na=False)]
            sick_row_idx = df.index[df[first_col].astype(str).str.contains("患病总数", na=False)]
            if len(time_row_idx) and len(sick_row_idx):
                time_pos = df.index.get_loc(time_row_idx[0])
                sick_pos = df.index.get_loc(sick_row_idx[0])
                time_row = pd.Series(df.iloc[time_pos, 1:]).replace("None", np.nan).dropna()
                sick_row = pd.Series(df.iloc[sick_pos, 1:]).replace("None", np.nan)
                sick_row = pd.to_numeric(sick_row, errors="coerce").dropna()
                min_len = min(len(time_row), len(sick_row))
                time_row = time_row.iloc[:min_len]
                sick_row = sick_row.iloc[:min_len]
                time_num = pd.to_numeric(time_row, errors="coerce")
                time_dt = pd.to_datetime(time_num, unit="D", origin="1899-12-30", errors="coerce")
                if time_dt.isna().any():
                    time_dt = pd.to_datetime(time_row.astype(str), errors="coerce")
                trend_df = pd.DataFrame({
                    "时间": time_dt.to_numpy(),
                    "患病鱼总数": sick_row.to_numpy()
                }).dropna().reset_index(drop=True)
                if len(trend_df) == 0:
                    st.info("趋势数据无法解析，请检查 Excel 中“时间/患病总数”两行数据格式。")
                else:
                    show_df = trend_df.copy()
                    if np.issubdtype(show_df["时间"].dtype, np.datetime64):
                        show_df["时间"] = pd.to_datetime(show_df["时间"]).dt.strftime("%Y-%m-%d")
                    st.markdown("#### 趋势分析原始数据（对齐后）")
                    st.dataframe(show_df, use_container_width=True)
                    try:
                        import plotly.express as px
                        fig = px.line(trend_df, x="时间", y="患病鱼总数",
                                      title="患病鱼总数随时间变化趋势",
                                      labels={"时间": "时间", "患病总数": "患病鱼总数"})
                        fig.update_traces(line=dict(color='gray', width=3))
                        fig.update_traces(mode='lines+markers', marker=dict(size=6))
                        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', font=dict(size=12))
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown("**趋势分析要点：**")
                        if len(trend_df) > 1:
                            max_sick = int(trend_df["患病鱼总数"].max())
                            min_sick = int(trend_df["患病鱼总数"].min())
                            avg_sick = float(trend_df["患病鱼总数"].mean())
                            st.write(f"- 最高患病数：{max_sick} 尾")
                            st.write(f"- 最低患病数：{min_sick} 尾")
                            st.write(f"- 平均患病数：{avg_sick:.1f} 尾")
                            if trend_df["患病鱼总数"].iloc[-1] > trend_df["患病鱼总数"].iloc[0]:
                                st.write("- 📈 总体呈上升趋势，需加强疾病防控")
                            elif trend_df["患病鱼总数"].iloc[-1] < trend_df["患病鱼总数"].iloc[0]:
                                st.write("- 📉 总体呈下降趋势，防控措施有效")
                            else:
                                st.write("- ➡️ 患病数量保持稳定")
                    except ImportError:
                        st.info("折线图需要 plotly 库支持。请在 requirements.txt 中添加 'plotly>=5.15.0'")
            else:
                st.info("未在首列找到“时间”或“患病总数”两行，请检查 Excel 表结构。")

        st.markdown("## 💡 建议")
        st.markdown('<div class="ai-hr-line"></div>', unsafe_allow_html=True)
        st.markdown('<div class="ai-hint-subtitle">🔍 基于 <b>通义千问</b> 大模型的建议生成</div>', unsafe_allow_html=True)
        with st.expander("🚀通义千问 建议", expanded=False):
            st.markdown("""
根据模型检测，您的鱼类患有溃疡病、眼部病变、鳍部病变、腐烂鳃四种疾病。这类复合感染可能由细菌、真菌或寄生虫引起，需要及时采取综合治疗措施，以防止病情恶化。为了帮助您有效管理鱼群健康，我建议如下治疗方案：

1.🧱隔离病鱼：立即将患病鱼类转移到单独的治疗缸中，避免疾病传播给其他健康鱼只。确保治疗缸的水质清洁，并保持适宜的温度和氧气水平。
2.💧改善水质：检查并优化主缸和治疗缸的水质参数，包括 pH 值（6.5-7.5）、氨氮和亚硝酸盐（尽可能接近零）。定期换水（建议每周 25-30%），并添加水质稳定剂以减少应激。
3.💊药物治疗：
- 溃疡病/鳍部病变：土霉素或呋喃西林（按说明剂量），连续 5-7 天。
- 眼部病变：甲基蓝药浴（每 10 升水 1-2 毫升），15-20 分钟/天，3-5 天。
- 腐烂鳃：盐浴（1-3 g/L），10-15 分钟/天，可配合磺胺类制剂。
4.🍔营养支持：提供高营养、易消化饲料，补充维生素，增强免疫力。
5.🔭监测与调整：每天观察并记录治疗进展，必要时咨询兽医或水产专家。
            """)

    except Exception as e:
        st.error(f"数据加载失败: {str(e)}")
        st.info("请确保 data.xlsx 文件存在于当前目录中")

elif page == PAGE_FORUM:
    if st.session_state.get("forum_view") == "detail_post1":
        write_reply_sidebar("post1")
        if st.button("← 返回列表"):
            st.session_state.pop("forum_view", None)
            _do_rerun()

        st.markdown('<div class="article-title">乌鳢(黑鱼)养殖出现烂鳃病如何防治？</div>', unsafe_allow_html=True)
        st.markdown('<div class="article-meta">作者：云南黑鱼养殖户 | 发布时间：2025-09-03 14:31:00</div>', unsafe_allow_html=True)
        st.markdown('<hr style="border:0; height:2px; background:#111;" />', unsafe_allow_html=True)
        st.markdown('<div class="expert-reply">李潮副研究员回复：</div>', unsafe_allow_html=True)
        content_html = """
<div class="article-content">
<p>防治方法：</p>
<ol>
  <li>认真仔细检查病鱼的症状，准确诊断病原，然后对症下药治疗。</li>
  <li>细菌性烂鳃病的防治方法与出血性败血病相同。</li>
  <li>寄生虫性烂鳃病的防治，先用 0.5 mg/L 晶体敌百虫全池泼洒，杀灭寄生虫。隔两天，再用 0.3 mg/L 强氯精全池泼洒灭菌，以防寄生虫叮咬的伤口继发感染。</li>
</ol>
</div>
"""
        st.markdown(content_html, unsafe_allow_html=True)

        if st.session_state.get("post1_comments"):
            st.markdown("### 最新回复")
            for c in reversed(st.session_state["post1_comments"][-10:]):
                st.markdown(f"- {c['content']}  — {c['author']} 于 {c['time']}")

    else:
        with st.sidebar:
            with st.expander("📝我要发贴", expanded=False):
                title = st.text_input("文章标题")
                content = st.text_area("文章内容", height=160)
                author = st.text_input("作者", value="匿名")
                pin = st.checkbox("置顶帖子", value=False)
                c1, c2 = st.columns(2)
                with c1: submit = st.button("立即发布")
                with c2: refresh = st.button("刷新数据")
                if "forum_posts" not in st.session_state:
                    st.session_state.forum_posts = []
                if submit:
                    if not title or not content:
                        st.warning("请填写完整的标题和内容后再发布。")
                    else:
                        st.session_state.forum_posts.append({
                            "title": title, "content": content, "author": author or "匿名",
                            "pinned": pin, "heat": 0,
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        st.success("发布成功！已加入最新帖子。")
                if refresh:
                    _do_rerun()

        st.markdown('<div class="forum-title">📢 交流论坛</div>', unsafe_allow_html=True)
        st.markdown('<div class="forum-section-title">🔥 热门帖子</div>', unsafe_allow_html=True)

        hot_posts = [
            {"prefix": "🥇", "title": "乌鳢(黑鱼)养殖出现烂鳃病如何防治？", "heat": 42, "author": "云南黑鱼养殖户", "time": "2025-09-03 14:31:00"},
            {"prefix": "🥈", "title": "稻田养鲫鱼如何防除敌害？", "heat": 29, "author": "广东鲫鱼养殖户", "time": "2025-08-02 18:24:00"},
            {"prefix": "🥉", "title": "养泥鳅水质优劣如何观察及处理方法？", "heat": 21, "author": "湖北泥鳅养殖户", "time": "2025-09-20 10:49:00"},
        ]
        for i, p in enumerate(hot_posts):
            heat_pct = max(0, min(100, int(p["heat"])))
            card = st.container()
            with card:
                tcol, bcol = st.columns([0.85, 0.15])
                with tcol:
                    st.markdown(f'<div class="post-title">{p["prefix"]} {p["title"]}</div>', unsafe_allow_html=True)
                with bcol:
                    if st.button("阅读全文", key=f"hot_read_{i}", help="查看此帖详情", type="secondary", use_container_width=True):
                        if i == 0:
                            st.session_state["forum_view"] = "detail_post1"
                        else:
                            st.info("该帖详情页即将上线～")
                st.markdown(f'<div class="post-meta">作者：{p["author"]} | 发布时间：{p["time"]}</div>', unsafe_allow_html=True)
                st.markdown(f'''
<div class="heat-wrap">
  <div class="heat-label">热度值：{p["heat"]}</div>
  <div class="heat-track"><div class="heat-fill" style="width:{heat_pct}%;"></div></div>
</div>
''', unsafe_allow_html=True)

        st.markdown('<div class="forum-section-title" style="margin-top:0.75rem;">📰 最新帖子</div>', unsafe_allow_html=True)

        if "forum_posts" in st.session_state and st.session_state.forum_posts:
            for j, p in enumerate(reversed(st.session_state.forum_posts[-3:])):
                heat_val = int(p.get("heat", 0))
                heat_pct = max(0, min(100, heat_val))
                card = st.container()
                with card:
                    tcol, bcol = st.columns([0.85, 0.15])
                    with tcol:
                        st.markdown(f'<div class="post-title">🆕 {p["title"]}</div>', unsafe_allow_html=True)
                    with bcol:
                        st.button("阅读全文", key=f"latest_user_read_{j}", type="secondary", use_container_width=True)
                    st.markdown(f'''
<div class="heat-wrap">
  <div class="heat-label">热度值：{p["heat"]:02d}</div>
  <div class="heat-track"><div class="heat-fill" style="width:{heat_pct}%;"></div></div>
''', unsafe_allow_html=True)
                    st.markdown(f'<div class="post-meta">作者：{p.get("author","匿名")} | 发布时间：{p.get("created_at","")}</div>', unsafe_allow_html=True)

        latest_posts = [
            {"title": "如何降低泥鳅的饲养成本？", "heat": 4, "author": "湖北泥鳅养殖户", "time": "2025-10-03 10:49:00"},
            {"title": "怎么在鲟鱼水花开口期提高养殖收益？", "heat": 3, "author": "浙江鲟鱼养殖户", "time": "2025-10-02 15:22:00"},
            {"title": "鲶鱼养殖如何增产？", "heat": 7, "author": "四川鲶鱼养殖户", "time": "2025-10-01 12:48:00"},
        ]
        for k, p in enumerate(latest_posts):
            heat_pct = max(0, min(100, int(p["heat"])))
            card = st.container()
            with card:
                tcol, bcol = st.columns([0.85, 0.15])
                with tcol:
                    st.markdown(f'<div class="post-title">{p["title"]}</div>', unsafe_allow_html=True)
                with bcol:
                    st.button("阅读全文", key=f"latest_read_{k}", type="secondary", use_container_width=True)
                st.markdown(f'''
<div class="heat-wrap">
  <div class="heat-label">热度值：{p["heat"]:02d}</div>
  <div class="heat-track"><div class="heat-fill" style="width:{heat_pct}%;"></div></div>
</div>
''', unsafe_allow_html=True)
                st.markdown(f'<div class="post-meta">作者：{p["author"]} | 发布时间：{p["time"]}</div>', unsafe_allow_html=True)

elif page == PAGE_QA:
    st.markdown('<h1 class="main-header">🧠渔康智鉴AI助手</h1>', unsafe_allow_html=True)
    st.markdown('<div class="title-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="qa-tagline">🐟 一位资深的水产养殖专家，能助您解决各类养殖问题 🐟</div>', unsafe_allow_html=True)

    st.markdown('<h4 class="section-label">试试这些常见问题：</h4>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    def ask_and_show(q):
        st.session_state.setdefault("messages", []).append({"role": "user", "content": q})
        with st.spinner("思考中..."):
            a = call_qwen_api(q)
        st.session_state["messages"].append({"role": "assistant", "content": a})

    with col1:
        if st.button("草鱼患溃疡病如何治疗？", key="q1"): ask_and_show("草鱼患溃疡病如何治疗？")
        if st.button("鲢鱼同时患眼部病变、鳍部病变如何治疗？", key="q2"): ask_and_show("鲢鱼同时患眼部病变、鳍部病变如何治疗？")
    with col2:
        if st.button("幼苗期鳙鱼患溃疡病如何治疗？", key="q3"): ask_and_show("幼苗期鳙鱼患溃疡病如何治疗？")
        if st.button("当鱼出现腐烂鳃时如何快速治疗？", key="q4"): ask_and_show("当鱼出现腐烂鳃时如何快速治疗？")

    st.markdown(
        '<div class="greeting"><span class="icon">🧡</span>'
        '<span>你好，我是渔康智鉴问答助手。有任何关于鱼类健康与养殖的问题都可以问我！🥳</span></div>',
        unsafe_allow_html=True
    )

    st.markdown("### 对话记录")
    for m in st.session_state.get("messages", []):
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("请输入您的问题..."):
        st.session_state.setdefault("messages", []).append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                ans = call_qwen_api(prompt)
                st.markdown(ans)
                st.session_state["messages"].append({"role": "assistant", "content": ans})

    if st.button("重置会话"):
        st.session_state["messages"] = []
        _do_rerun()