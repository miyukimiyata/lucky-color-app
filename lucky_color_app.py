import streamlit as st
import random

st.set_page_config(
    page_title="飛行機ラッキーカラー占い",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------
# セッションの初期化（画面の切り替えを管理）
# ---------------------------
if "step" not in st.session_state:
    st.session_state.step = "input"
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "current_result" not in st.session_state:
    st.session_state.current_result = None
if "show_airplane" not in st.session_state:
    st.session_state.show_airplane = False

# ---------------------------
# カスタムCSS（空行なし）
# ---------------------------
st.markdown("""<style>
/* Streamlit UI elements hiding */
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stHeader"] { display: none !important; }
[data-testid="stFooter"] { display: none !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; display: none !important; }
header { visibility: hidden !important; display: none !important; }

.stApp { background-color: #e0f7fa; }
.block-container { padding-top: 4rem; padding-bottom: 2rem; max-width: 500px; }
.main-title { font-size: clamp(1.3rem, 4.5vw, 2rem); color: #007bb5; text-align: center; text-shadow: 1px 1px 2px #fff; margin-top: 60px; margin-bottom: 20px; font-weight: bold; line-height: 1.4; }
.result-card { background-color: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: clamp(15px, 4vw, 25px); text-align: center; box-shadow: 0px 8px 16px rgba(0,0,0,0.1); margin: 10px 0 20px 0; border: 3px dashed #81d4fa; display: flex; flex-direction: column; gap: 10px; }
.fortune-text { font-size: clamp(2.5rem, 10vw, 4rem); font-weight: 900; color: #d32f2f; text-shadow: 1px 1px 0 #fff, -1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 2px 2px 4px rgba(0,0,0,0.2); margin: 5px 0; line-height: 1.2; }
.section-title { font-size: clamp(0.9rem, 3vw, 1.1rem); color: #666; font-weight: bold; margin-top: 5px; margin-bottom: 2px; }
.color-name { font-size: clamp(2rem, 7vw, 3rem); font-weight: bold; margin: 5px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); line-height: 1.2; }
.item-name { font-size: clamp(1.2rem, 4.5vw, 1.6rem); font-weight: bold; color: #00897b; background-color: #e0f2f1; border-radius: 12px; padding: 10px 15px; display: inline-block; margin: 0 auto; box-shadow: 0px 2px 4px rgba(0,0,0,0.05); word-break: keep-all; }
.airline-name { font-size: clamp(1rem, 3.5vw, 1.3rem); color: #555; line-height: 1.3; }
.mamechishiki { font-size: clamp(0.95rem, 3.5vw, 1.1rem); color: #333; margin-top: 10px; line-height: 1.6; text-align: left; background-color: #fff9c4; padding: 15px; border-radius: 12px; border-left: 6px solid #ffeb3b; word-wrap: break-word; }
.clouds { font-size: clamp(1.5rem, 5vw, 2.5rem); text-align: center; margin-bottom: 5px; animation: float 3s ease-in-out infinite; line-height: 1.2; }
@keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-6px); } 100% { transform: translateY(0px); } }

/* 飛行機アニメーション用CSS */
@keyframes flyRight {
    0% { transform: translateX(-20vw) translateY(0) rotate(0deg); opacity: 1; }
    50% { transform: translateX(50vw) translateY(-10vh) rotate(-10deg); opacity: 1; }
    100% { transform: translateX(120vw) translateY(-20vh) rotate(-20deg); opacity: 1; }
}
.airplane-animation {
    position: fixed;
    top: 40%;
    left: -100px;
    font-size: 5rem;
    z-index: 99999;
    animation: flyRight 2.5s ease-in-out forwards;
    pointer-events: none;
    text-shadow: 2px 2px 5px rgba(0,0,0,0.2);
}

div.stButton > button { background-color: #ff9800; color: white; font-weight: bold; border-radius: 50px; padding: 10px 10px; font-size: clamp(1.2rem, 4vw, 1.5rem); border: none; box-shadow: 0px 6px 12px rgba(255, 152, 0, 0.4); transition: all 0.2s; width: 100%; min-height: 60px; margin-top: 10px; }
div.stButton > button:hover { background-color: #f57c00; transform: scale(1.02); }
div.stButton > button:active { transform: scale(0.98); background-color: #e65100; box-shadow: 0px 2px 4px rgba(255, 152, 0, 0.4); }
div[data-testid="stTextInput"] label p { font-size: 1.2rem; font-weight: bold; color: #007bb5; }
div[data-testid="stTextInput"] input { font-size: 1.2rem; padding: 12px; border-radius: 15px; border: 2px solid #81d4fa; box-shadow: 0px 4px 6px rgba(0,0,0,0.05); }
div[data-testid="stTextInput"] input:focus { border-color: #007bb5; box-shadow: 0px 4px 10px rgba(0, 123, 181, 0.2); }
</style>""", unsafe_allow_html=True)

# ---------------------------
# データ定義
# ---------------------------
fortunes = ["大吉 🌟", "中吉 ⭐", "小吉 ✨", "吉 🍀"]
items = ["🛫 飛行機の模型", "🍦 ソフトクリーム", "🎟️ 展望デッキのチケット", "🛂 パスポート", "🧳 スーツケース"]
colors_data = [
    {"color": "青", "theme_color": "#005baa", "airline": "ANA", "emoji": "🔵", "knowledge": "関空から飛ぶANAの飛行機は、世界中の空を青く染めているよ！青色は『安全』や『信頼』のシンボルでもあるんだって。"},
    {"color": "赤", "theme_color": "#cc0000", "airline": "JAL", "emoji": "🔴", "knowledge": "JALの飛行機のしっぽ（垂直尾翼）には、赤い鶴（ツル）のマークがついているよ！ツルは長生きのお守りで縁起がいいんだ。"},
    {"color": "ピンク", "theme_color": "#e6007e", "airline": "Peach（ピーチ）", "emoji": "🌸", "knowledge": "関空生まれのPeach（ピーチ）は、名前の通り鮮やかなピンク色でとってもかわいい飛行機！大空を飛ぶ桃みたいだね。"},
    {"color": "黒", "theme_color": "#333333", "airline": "スターフライヤー", "emoji": "⚫", "knowledge": "真っ黒な飛行機『スターフライヤー』は、夜の星空みたいでかっこいい！座席も黒くて、ロケットのようなんだよ。"},
    {"color": "白", "theme_color": "#aaaaaa", "airline": "スカイマークなど", "emoji": "⚪", "knowledge": "雲みたいな真っ白い飛行機！スカイマークの飛行機は、翼の先にハートやスペードのマークがこっそり描かれていることがあるよ。探してみてね！"}
]

# お誕生日サプライズのターゲット設定
target_names = ["ゆうと", "あかり"]
month_keywords = ["3がつ", "3月", "さんがつ"]

def generate_fortune():
    return {
        "fortune": random.choice(fortunes),
        "item": random.choice(items),
        "result": random.choice(colors_data)
    }

# 共通ヘッダー
st.markdown('<div class="clouds">☁️ ✈️ ☁️ ✈️ ☁️</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">✨ 浜田子供会 ✨<br>ラッキー占い ✈️</h1>', unsafe_allow_html=True)


if st.session_state.step == "input":
    # ==========================================
    # 画面1：入力画面
    # ==========================================
    user_input = st.text_input("おなまえをいれてね！", placeholder="ひらがなでいれてね", max_chars=15)
    
    if st.button("✨ 占う！ ✨", use_container_width=True):
        st.session_state.user_name = user_input if user_input.strip() else "おともだち"
        st.session_state.current_result = generate_fortune()
        st.session_state.show_airplane = True
        st.session_state.step = "result"
        st.rerun()

elif st.session_state.step == "result":
    # ==========================================
    # 画面2：結果画面
    # ==========================================
    if st.session_state.get("show_airplane", False):
        st.markdown('<div class="airplane-animation">✈️</div>', unsafe_allow_html=True)
        st.session_state.show_airplane = False

    name = st.session_state.user_name
    
    # 1. サプライズ判定
    is_target = any(t in name for t in target_names)
    is_month = any(m in name for m in month_keywords)
    
    # 2. サプライズメッセージ表示（該当すれば）
    if is_target:
        st.balloons()
        st.markdown('<div style="background-color:#ffeb3b; padding:15px; border-radius:15px; text-align:center; font-size:clamp(1.2rem, 4vw, 1.5rem); font-weight:bold; color:#ff5722; margin-bottom:15px; box-shadow:0px 4px 10px rgba(0,0,0,0.1); border: 2px solid #ff9800; animation: float 2s ease-in-out infinite;">🎉 お誕生日おめでとう！ 🎉</div>', unsafe_allow_html=True)
    elif is_month:
        st.balloons()
        st.markdown('<div style="background-color:#ffeb3b; padding:15px; border-radius:15px; text-align:center; font-size:clamp(1.2rem, 4vw, 1.5rem); font-weight:bold; color:#ff5722; margin-bottom:15px; box-shadow:0px 4px 10px rgba(0,0,0,0.1); border: 2px solid #ff9800; animation: float 2s ease-in-out infinite;">🎂 3月生まれのみんな、おめでとう！ 🎂</div>', unsafe_allow_html=True)
        
    greeting_text = f"{name}ちゃん、今日のアナタは…"
    current = st.session_state.current_result
    fortune = current["fortune"]
    item = current["item"]
    result = current["result"]
    text_color = result["theme_color"]

    # 3.占い結果カードの描画（空行なし）
    html_content = f"""<div class="result-card">
<div class="section-title">【{greeting_text}】</div>
<div class="fortune-text">{fortune}</div>
<hr style="border: 1px dashed #ccc; margin: 5px 0;">
<div class="section-title">✨ ラッキーカラー ✨</div>
<div class="color-name" style="color: {text_color};">{result['emoji']} {result['color']}</div>
<div class="airline-name">イメージ：{result['airline']} ✈️</div>
<hr style="border: 1px dashed #ccc; margin: 5px 0;">
<div class="section-title">🎁 ラッキーアイテム 🎁</div>
<div class="item-name">{item}</div>
<div class="mamechishiki"><strong>💡 関空の飛行機 豆知識 💡</strong><br>{result['knowledge']}</div>
</div>"""

    st.markdown(html_content, unsafe_allow_html=True)

    # 4. 戻るボタン
    if st.button("🔄 もういちど占う", use_container_width=True):
        st.session_state.step = "input"
        st.session_state.user_name = ""
        st.rerun()

# 共通フッター
st.markdown('<div class="clouds" style="margin-top:15px;">☁️ ✨ ☁️ ✨ ☁️</div>', unsafe_allow_html=True)
