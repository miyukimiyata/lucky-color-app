import streamlit as st
import random
import datetime
import time

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
.fortune-text { font-size: clamp(3rem, 12vw, 5.5rem); font-weight: 900; color: #ff3d00; text-shadow: 2px 2px 0 #fff, -2px -2px 0 #fff, 2px -2px 0 #fff, -2px 2px 0 #fff, 4px 4px 10px rgba(0,0,0,0.3); margin: 15px 0; line-height: 1.3; animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
@keyframes popIn { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
.section-title { font-size: clamp(0.9rem, 3vw, 1.1rem); color: #666; font-weight: bold; margin-top: 5px; margin-bottom: 2px; }
.color-name { font-size: clamp(2rem, 7vw, 3rem); font-weight: bold; margin: 5px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); line-height: 1.2; }
.item-name { font-size: clamp(1.2rem, 4.5vw, 1.6rem); font-weight: bold; color: #00897b; background-color: #e0f2f1; border-radius: 12px; padding: 10px 15px; display: inline-block; margin: 0 auto; box-shadow: 0px 2px 4px rgba(0,0,0,0.05); word-break: keep-all; }
.airline-name { font-size: clamp(1rem, 3.5vw, 1.3rem); color: #555; line-height: 1.3; }
.mamechishiki { font-size: clamp(0.95rem, 3.5vw, 1.1rem); color: #333; margin-top: 10px; line-height: 1.6; text-align: left; background-color: #fff9c4; padding: 15px; border-radius: 12px; border-left: 6px solid #ffeb3b; word-wrap: break-word; }
.clouds { font-size: clamp(1.5rem, 5vw, 2.5rem); text-align: center; margin-bottom: 5px; animation: float 3s ease-in-out infinite; line-height: 1.2; }
@keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-6px); } 100% { transform: translateY(0px); } }

/* 飛行機アニメーション用CSS */
@keyframes flyUp {
    0% { transform: translateY(10vh) rotate(-45deg); opacity: 1; }
    100% { transform: translateY(-120vh) rotate(-45deg); opacity: 1; }
}
.airplane-animation {
    position: fixed;
    bottom: 0px;
    left: 50%;
    margin-left: -3rem;
    font-size: 6rem;
    z-index: 99999;
    animation: flyUp 1.5s ease-in forwards;
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
fortunes = ["ひいてびっくり吉 🌟", "ふつうと見せかけて吉 ⭐", "ギリギリセーフ吉 ✨", "謎のミラクル吉 🍀"]
items = ["🛫 飛行機の模型", "🍦 ソフトクリーム", "🎟️ 展望デッキのチケット", "🛂 パスポート", "🧳 スーツケース"]
colors_data = [
    {"color": "青", "theme_color": "#005baa", "airline": "ANA", "emoji": "🔵", "knowledge": "関空から飛ぶANAの飛行機は、世界中の空を青く染めているよ！青色は『安全』や『信頼』のシンボルでもあるんだって。"},
    {"color": "赤", "theme_color": "#cc0000", "airline": "JAL", "emoji": "🔴", "knowledge": "JALの飛行機のしっぽ（垂直尾翼）には、赤い鶴（ツル）のマークがついているよ！ツルは長生きのお守りで縁起がいいんだ。"},
    {"color": "ピンク", "theme_color": "#e6007e", "airline": "Peach（ピーチ）", "emoji": "🌸", "knowledge": "関空生まれのPeach（ピーチ）は、名前の通り鮮やかなピンク色でとってもかわいい飛行機！大空を飛ぶ桃みたいだね。"},
    {"color": "黒", "theme_color": "#333333", "airline": "スターフライヤー", "emoji": "⚫", "knowledge": "真っ黒な飛行機『スターフライヤー』は、夜の星空みたいでかっこいい！座席も黒くて、ロケットのようなんだよ。"},
    {"color": "白", "theme_color": "#aaaaaa", "airline": "スカイマークなど", "emoji": "⚪", "knowledge": "雲みたいな真っ白い飛行機！スカイマークの飛行機は、翼の先にハートやスペードのマークがこっそり描かれていることがあるよ。探してみてね！"}
]

# もふもふ動物系リスト
animal_fortunes = [
    {
        "fortune": "キャプテン・パンダ運 🐼",
        "item": "🐼 パンダの「おひるね枕」",
        "result": {"color": "ささいろグリーン", "theme_color": "#2e7d32", "airline": "もふもふ航空", "emoji": "🎋", "knowledge": "パンダは笹をたくさん食べて眠るんだ！飛行機でたっぷり寝たら、スッキリ元気になれるよ！"},
        "type": "animal",
        "animal_emoji": ["🐼", "🎋", "🍃"]
    },
    {
        "fortune": "そらとぶ ペンギン運 🐧",
        "item": "🍦 ひえひえ「ソフトクリーム」",
        "result": {"color": "こおり色ブルー", "theme_color": "#81d4fa", "airline": "スノーウィングス", "emoji": "❄️", "knowledge": "ペンギンは空を飛べないけど海を飛ぶように泳ぐんだ！君も自由に大空を飛べるよ！"},
        "type": "animal",
        "animal_emoji": ["🐧", "❄️"]
    },
    {
        "fortune": "ふわふわ ウサギCAさん運 🐰",
        "item": "🎀 うさ耳「カチューシャ」",
        "result": {"color": "いちごミルク", "theme_color": "#f8bbd0", "airline": "キャロットエアー", "emoji": "🍓", "knowledge": "CAさんは飛行機の中でいろんなお世話をしてくれる優しい人たち。ウサギみたいにピョンと跳ねて活躍しよう！"},
        "type": "animal",
        "animal_emoji": ["🐰", "🥕", "💖"]
    },
    {
        "fortune": "くいしんぼう クマ機長運 🐻",
        "item": "🍯 とろ〜り「はちみつ」",
        "result": {"color": "はちみつゴールド", "theme_color": "#ffb300", "airline": "ベアーフライト", "emoji": "🍯", "knowledge": "クマの機長はちょっと食いしん坊かも？おいしいご飯を食べれば、どんなフライトも大成功！"},
        "type": "animal",
        "animal_emoji": ["🐻", "🐝", "🍯"]
    },
    {
        "fortune": "おしゃべり インコパイロット運 🐦",
        "item": "✒️ カラフルな「はねのペン」",
        "result": {"color": "レインボー", "theme_color": "#ab47bc", "airline": "パロットジェット", "emoji": "🌈", "knowledge": "おしゃべりなインコは、パイロットの通信みたいだね！いろんな人とお話しして楽しい一日になりそう！"},
        "type": "animal",
        "animal_emoji": ["🐦", "♪", "🎵"]
    }
]

# わらちゃう結果リスト
special_fortunes = [
    {
        "fortune": "鼻毛が伸びる運 👃",
        "item": "🧦 先生の穴あき靴下",
        "result": {"color": "鼻水スカイブルー", "theme_color": "#4fc3f7", "airline": "ヒミツの航空", "emoji": "💧", "knowledge": "飛行機に乗ると気圧の変化でおならが出やすくなるんだって！ホントだよ！"}
    },
    {
        "fortune": "おならが止まらない運 💨",
        "item": "🩲 予備のパンツ（3枚）",
        "result": {"color": "ぷうぷうイエロー", "theme_color": "#ffeb3b", "airline": "オナラ航空", "emoji": "💨", "knowledge": "パイロットは、実はおならを我慢しながら運転してるかも！？（ウソだよ！）"}
    },
    {
        "fortune": "顔がパンパン運 🍞",
        "item": "🍬 誰かの食べかけの飴",
        "result": {"color": "アンパンレッド", "theme_color": "#e53935", "airline": "パンパンエアー", "emoji": "🔴", "knowledge": "飛行機の中では、ポテトチップスの袋がパンパンに膨らむよ！顔も膨らむかも！？"}
    },
    {
        "fortune": "逆立ち歩き運 🙃",
        "item": "📖 逆さまの教科書",
        "result": {"color": "まっさかさまパープル", "theme_color": "#9c27b0", "airline": "さかさま航空", "emoji": "👾", "knowledge": "飛行機は逆さまに飛ぶこともできるんだよ（本物のアクロバット飛行機ね！）。"}
    },
    {
        "fortune": "迷子の子猫運 🐱",
        "item": "🎀 ネコ耳カチューシャ",
        "result": {"color": "にゃんにゃんホワイト", "theme_color": "#212121", "airline": "ニャンコエアー", "emoji": "🐾", "knowledge": "飛行機のタイヤは、車よりずっと分厚くて丈夫なんだよ！猫の肉球とは大違い！"}
    },
    {
        "fortune": "宿題が消える運 🪄",
        "item": "🖍️ 魔法の消しゴム",
        "result": {"color": "まぼろし透明色", "theme_color": "#b0bec5", "airline": "マジックジェット", "emoji": "👻", "knowledge": "飛行機は雷に打たれても大丈夫なように作られているんだ。魔法みたいでしょ？"}
    },
    {
        "fortune": "宇宙人にさらわれる運 👽",
        "item": "🛸 アルミホイルの帽子",
        "result": {"color": "未確認グリーン", "theme_color": "#4caf50", "airline": "UFO", "emoji": "👽", "knowledge": "飛行機に乗ってるときに見える星空は、地上よりずっと綺麗だよ！宇宙人に会えるかも？"}
    },
    {
        "fortune": "うひょー！大爆笑 🤣",
        "item": "🕶️ 先生のサングラス",
        "result": {"color": "ヘンテコ色", "theme_color": "#009688", "airline": "ヒミツ", "emoji": "💧", "knowledge": "飛行機は、おならをブーンと出すと空に浮くんだよ（ウソだよ、エンジンだよ！）。"}
    },
    {
        "fortune": "げらげら運 😆",
        "item": "💩 ニセモノのうんち",
        "result": {"color": "うんち色ゴールド！", "theme_color": "#d4af37", "airline": "ナイショ", "emoji": "💩", "knowledge": "パイロットは、実は寝ながら運転してるんだよ（ウソだよ、ちゃんと見てるよ！）。"}
    }
]

# 誕生日リスト（ひらがな：MMDD）
birthday_list = {
    "いちな": "0601", "みつき": "0602", "りと": "0603", "えいこう": "0604",
    "すず": "0605", "えま": "0606", "ひなの": "0607", "ふうが": "0608",
    "ゆう": "0609", "みひろ": "0610", "しょうり": "0611", "りょうま": "0612",
    "じゅきあ": "0613", "りゅうき": "0614", "はるた": "0615", "しょうま": "0616",
    "じょうたろう": "0617", "あやと": "0618", "しょうた": "0619", "ひろむ": "0329"
}

def to_hiragana(text):
    """カタカナをひらがなに変換する"""
    return "".join(chr(ord(c) - 0x60) if 0x30A1 <= ord(c) <= 0x30F6 else c for c in text)

def generate_fortune():
    # 「爆笑系」「女子向けキラキラ系」「もふもふ動物系」が均等に出るように調整
    r = random.random()
    if r < 0.33:
        # 女子向けキラキラ系 (通常)
        return {
            "fortune": random.choice(fortunes),
            "item": random.choice(items),
            "result": random.choice(colors_data),
            "type": "normal"
        }
    elif r < 0.66:
        # 爆笑系
        ret = random.choice(special_fortunes).copy()
        ret["type"] = "funny"
        return ret
    else:
        # もふもふ動物系
        return random.choice(animal_fortunes)

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
        placeholder = st.empty()
        placeholder.markdown('<div class="airplane-animation">✈️</div>', unsafe_allow_html=True)
        time.sleep(1.5)
        placeholder.empty()
        st.session_state.show_airplane = False

    name = st.session_state.user_name
    hira_name = to_hiragana(name)
    
    # 日本時間で今日の日付を取得 (MMDD)
    JST = datetime.timezone(datetime.timedelta(hours=9))
    today_str = datetime.datetime.now(JST).strftime("%m%d")
    
    # 1. 判定（入力された名前がリストにあり、今日が誕生日か）
    is_birthday = (hira_name in birthday_list and birthday_list[hira_name] == today_str)
    
    # 2. 誕生日判定と演出
    if is_birthday:
        st.balloons()
        # お祝いの風船やクラッカーが画面いっぱいに舞う演出
        cracker_html = """
        <style>
        @keyframes fall {
            0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; }
            100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
        }
        .cracker { position: fixed; top: -10%; font-size: 3rem; animation: fall linear forwards; z-index: 99999; pointer-events: none; }
        </style>
        """
        for i in range(7):
            left = random.randint(0, 100)
            duration = random.uniform(2, 6)
            delay = random.uniform(0, 2.5)
            icon = random.choice(["🎉", "🎈", "✨", "🎂", "🎊", "🎁"])
            cracker_html += f'<div class="cracker" style="left: {left}vw; animation-duration: {duration}s; animation-delay: {delay}s;">{icon}</div>'
        st.markdown(cracker_html, unsafe_allow_html=True)
        
        # 大きなお祝いメッセージ
        st.markdown('<div style="background-color:#fff9c4; padding:25px; border-radius:20px; text-align:center; font-size:clamp(1.5rem, 6vw, 2.5rem); font-weight:900; color:#e65100; margin-bottom:20px; box-shadow:0px 8px 16px rgba(0,0,0,0.15); border: 4px dashed #ff9800; line-height:1.4; animation: float 2s ease-in-out infinite;">おたんじょうび<br>おめでとう！🎂✨</div>', unsafe_allow_html=True)
        
    greeting_text = f"{name}さん、今日のアナタは…"
    current = st.session_state.current_result
    
    # 3. 動物系の場合の演出強化
    if current.get("type") == "animal":
        animal_html = """
        <style>
        @keyframes hop {
            0% { transform: translateY(110vh) translateX(0) scale(1); opacity: 0; }
            10% { opacity: 1; }
            30% { transform: translateY(60vh) translateX(5vw) scale(1.1); }
            50% { transform: translateY(30vh) translateX(-5vw) scale(1.2); }
            70% { transform: translateY(0vh) translateX(5vw) scale(1.1); }
            100% { transform: translateY(-30vh) translateX(-2vw) scale(1); opacity: 0; }
        }
        .animal-hop { position: fixed; bottom: -10%; font-size: 4rem; animation: hop ease-out forwards; z-index: 99998; pointer-events: none; }
        </style>
        """
        emojis = current.get("animal_emoji", ["🐾", "✨"])
        for i in range(15):
            left = random.randint(0, 90)
            duration = random.uniform(3.0, 5.0)
            delay = random.uniform(0, 1.5)
            icon = random.choice(emojis)
            animal_html += f'<div class="animal-hop" style="left: {left}vw; animation-duration: {duration}s; animation-delay: {delay}s;">{icon}</div>'
        st.markdown(animal_html, unsafe_allow_html=True)

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
