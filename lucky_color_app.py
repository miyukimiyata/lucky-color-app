import streamlit as st
import random
import datetime

st.set_page_config(
    page_title="飛行機ラッキーカラー 占い",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------
# セッション初期化
# ---------------------------
defaults = {
    "step": "input",
    "user_name": "",
    "user_name2": "",
    "current_result": None,
    "show_airplane": False,
    "course_type": "normal",
    "is_pair_mode": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------------------
# CSS
# ---------------------------
st.markdown("""
<style>
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stHeader"] { display: none !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
header { visibility: hidden !important; }

html, body, [class*="css"] {
    font-family: "Hiragino Sans", "Yu Gothic", "Meiryo", sans-serif;
}

.stApp {
    min-height: 100vh;
    overflow-x: hidden;
}

.block-container {
    max-width: 560px;
    margin: 0 auto;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

.main-title {
    font-size: clamp(1.4rem, 4vw, 2.1rem);
    color: #007bb5;
    text-align: center;
    margin: 20px 0 18px 0;
    font-weight: 800;
    line-height: 1.45;
}

.clouds {
    font-size: clamp(1.5rem, 4vw, 2.2rem);
    text-align: center;
    margin-bottom: 6px;
}

.result-card {
    background: rgba(255,255,255,0.96);
    border-radius: 20px;
    padding: 20px 18px;
    text-align: center;
    box-shadow: 0 8px 18px rgba(0,0,0,0.08);
    margin: 10px 0 20px 0;
    border: 3px dashed #81d4fa;
}

.fortune-text {
    font-size: clamp(2.3rem, 9vw, 4.6rem);
    font-weight: 900;
    color: #ff3d00;
    margin: 14px 0;
    line-height: 1.2;
    text-shadow: 1px 1px 0 #fff;
}

.section-title {
    font-size: 1rem;
    color: #666;
    font-weight: 700;
    margin-top: 8px;
    margin-bottom: 4px;
}

.color-name {
    font-size: clamp(1.9rem, 6vw, 2.9rem);
    font-weight: 800;
    margin: 8px 0;
    line-height: 1.2;
}

.item-name {
    font-size: clamp(1.05rem, 4vw, 1.45rem);
    font-weight: 700;
    color: #00897b;
    background-color: #e0f2f1;
    border-radius: 12px;
    padding: 10px 14px;
    display: inline-block;
    margin: 8px auto;
    word-break: keep-all;
}

.airline-name {
    font-size: 1rem;
    color: #555;
    line-height: 1.4;
}

.mamechishiki {
    font-size: 0.98rem;
    color: #333;
    margin-top: 12px;
    line-height: 1.65;
    text-align: left;
    background-color: #fff9c4;
    padding: 14px;
    border-radius: 12px;
    border-left: 5px solid #ffeb3b;
}

div[data-testid="stTextInput"] label p {
    font-size: 1.08rem;
    font-weight: 700;
    color: #007bb5;
}

div[data-testid="stTextInput"] input {
    font-size: 1.08rem;
    padding: 12px;
    border-radius: 12px;
    border: 2px solid #81d4fa;
}

div.stButton > button {
    font-weight: 700;
    border-radius: 14px;
    padding: 0.9rem 0.8rem;
    min-height: 62px;
    width: 100%;
    border: none;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}

.flight-btn button {
    background: #1e88e5 !important;
    color: white !important;
}

.funny-btn button {
    background: #fb8c00 !important;
    color: white !important;
}

.animal-btn button {
    background: #ec407a !important;
    color: white !important;
}

.gachi-btn button {
    background: #3949ab !important;
    color: white !important;
}

.pair-btn button {
    background: #e53935 !important;
    color: white !important;
}

.retry-btn button {
    background: #4caf50 !important;
    color: white !important;
}

.airplane-animation {
    text-align: center;
    font-size: 3rem;
    margin: 4px 0 12px 0;
    animation: floatPlane 1.2s ease-in-out infinite;
}

@keyframes floatPlane {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}

.birthday-box {
    background-color: #fff9c4;
    padding: 22px;
    border-radius: 20px;
    text-align: center;
    font-size: clamp(1.4rem, 6vw, 2.3rem);
    font-weight: 900;
    color: #e65100;
    margin-bottom: 18px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.12);
    border: 4px dashed #ff9800;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# 背景色
# ---------------------------
bg_color = "#e0f7fa"
if st.session_state.step == "result" and st.session_state.current_result:
    current = st.session_state.current_result
    t = current.get("type")
    if t == "golden":
        bg_color = "#fff8e1"
    elif t == "funny":
        bg_color = "#fff9c4"
    elif t == "animal":
        bg_color = "#fce4ec"
    elif t == "gachi":
        bg_color = "#e8eaf6"
    elif t == "pair":
        bg_color = "#ffebee"

st.markdown(
    f"<style>.stApp {{ background-color: {bg_color} !important; }}</style>",
    unsafe_allow_html=True
)

# ---------------------------
# データ
# ---------------------------
fortunes = [
    "ひいてびっくり吉 🌟",
    "ふつうと見せかけて吉 ⭐",
    "ギリギリセーフ吉 ✨",
    "謎のミラクル吉 🍀"
]

items = [
    "🛫 飛行機の模型",
    "🍦 ソフトクリーム",
    "🎟️ 展望デッキのチケット",
    "🛂 パスポート",
    "🧳 スーツケース"
]

colors_data = [
    {
        "color": "青",
        "theme_color": "#005baa",
        "airline": "ANA",
        "emoji": "🔵",
        "knowledge": "関空から飛ぶANAの飛行機は、世界中の空を青く染めているよ！青色は『安全』や『信頼』のシンボルでもあるんだって。"
    },
    {
        "color": "赤",
        "theme_color": "#cc0000",
        "airline": "JAL",
        "emoji": "🔴",
        "knowledge": "JALの飛行機のしっぽには、赤い鶴のマークがついているよ！ツルは長生きのお守りで縁起がいいんだ。"
    },
    {
        "color": "ピンク",
        "theme_color": "#e6007e",
        "airline": "Peach（ピーチ）",
        "emoji": "🌸",
        "knowledge": "関空生まれのPeachは、名前の通り鮮やかなピンク色でとってもかわいい飛行機！"
    },
    {
        "color": "黒",
        "theme_color": "#333333",
        "airline": "スターフライヤー",
        "emoji": "⚫",
        "knowledge": "真っ黒な飛行機『スターフライヤー』は、夜の星空みたいでかっこいい！"
    },
    {
        "color": "白",
        "theme_color": "#aaaaaa",
        "airline": "スカイマークなど",
        "emoji": "⚪",
        "knowledge": "雲みたいな真っ白い飛行機！翼の先のマークにも注目してみてね。"
    }
]

animal_fortunes = [
    {
        "fortune": "キャプテン・パンダ運 🐼",
        "item": "🐼 パンダの「おひるね枕」",
        "result": {
            "color": "ささいろグリーン",
            "theme_color": "#2e7d32",
            "airline": "もふもふ航空",
            "emoji": "🎋",
            "knowledge": "パンダは笹をたくさん食べて眠るんだ！たっぷり寝たらスッキリ元気になれるよ！"
        },
        "type": "animal"
    },
    {
        "fortune": "そらとぶ ペンギン運 🐧",
        "item": "🍦 ひえひえ「ソフトクリーム」",
        "result": {
            "color": "こおり色ブルー",
            "theme_color": "#81d4fa",
            "airline": "スノーウィングス",
            "emoji": "❄️",
            "knowledge": "ペンギンは空を飛べないけど、海を飛ぶように泳ぐんだ！"
        },
        "type": "animal"
    },
    {
        "fortune": "ふわふわ ウサギCAさん運 🐰",
        "item": "🎀 うさ耳「カチューシャ」",
        "result": {
            "color": "いちごミルク",
            "theme_color": "#f8bbd0",
            "airline": "キャロットエアー",
            "emoji": "🍓",
            "knowledge": "ウサギみたいにピョンと元気いっぱいで活躍できそう！"
        },
        "type": "animal"
    },
    {
        "fortune": "くいしんぼう クマ機長運 🐻",
        "item": "🍯 とろ〜り「はちみつ」",
        "result": {
            "color": "はちみつゴールド",
            "theme_color": "#ffb300",
            "airline": "ベアーフライト",
            "emoji": "🍯",
            "knowledge": "おいしいご飯を食べれば、どんなフライトも大成功！"
        },
        "type": "animal"
    },
    {
        "fortune": "おしゃべり インコパイロット運 🐦",
        "item": "✒️ カラフルな「はねのペン」",
        "result": {
            "color": "レインボー",
            "theme_color": "#ab47bc",
            "airline": "パロットジェット",
            "emoji": "🌈",
            "knowledge": "いろんな人とお話しして楽しい一日になりそう！"
        },
        "type": "animal"
    }
]

special_fortunes = [
    {
        "fortune": "鼻毛が伸びる運 👃",
        "item": "🧦 先生の穴あき靴下",
        "result": {
            "color": "鼻水スカイブルー",
            "theme_color": "#4fc3f7",
            "airline": "ヒミツの航空",
            "emoji": "💧",
            "knowledge": "飛行機に乗ると気圧の変化でポテチの袋がふくらむことがあるよ！"
        }
    },
    {
        "fortune": "おならが止まらない運 💨",
        "item": "🩲 予備のパンツ（3枚）",
        "result": {
            "color": "ぷうぷうイエロー",
            "theme_color": "#ffeb3b",
            "airline": "オナラ航空",
            "emoji": "💨",
            "knowledge": "高いところでは袋や空気の入り方が変わって見えることもあるよ！"
        }
    },
    {
        "fortune": "顔がパンパン運 🍞",
        "item": "🍬 誰かの食べかけの飴",
        "result": {
            "color": "アンパンレッド",
            "theme_color": "#e53935",
            "airline": "パンパンエアー",
            "emoji": "🔴",
            "knowledge": "飛行機の中では、ポテトチップスの袋がパンパンに膨らむことがあるよ！"
        }
    },
    {
        "fortune": "逆立ち歩き運 🙃",
        "item": "📖 逆さまの教科書",
        "result": {
            "color": "まっさかさまパープル",
            "theme_color": "#9c27b0",
            "airline": "さかさま航空",
            "emoji": "👾",
            "knowledge": "アクロバット飛行機は、特別な飛び方ができるものもあるよ。"
        }
    }
]

gachi_fortunes = [
    {
        "fortune": "大吉 ⭐ 神レベルの運勢",
        "item": "望遠鏡 🔭",
        "result": {
            "color": "ミッドナイトブルー",
            "theme_color": "#1a237e",
            "airline": "スターライト",
            "emoji": "🌠",
            "knowledge": "夜の飛行機から見る星空は、まるで宇宙空間みたいにきれい！"
        },
        "type": "gachi"
    },
    {
        "fortune": "中吉 🌙 月のパワー全開",
        "item": "コンパス 🧭",
        "result": {
            "color": "ムーンライトシルバー",
            "theme_color": "#607d8b",
            "airline": "ルナ・フライト",
            "emoji": "🌒",
            "knowledge": "昔は星や月を見て方角を知ることもあったんだ。"
        },
        "type": "gachi"
    },
    {
        "fortune": "小吉 🌌 天の川のひらめき",
        "item": "星図帳 🗺️",
        "result": {
            "color": "ギャラクシーパープル",
            "theme_color": "#4a148c",
            "airline": "ミルキーウェイ",
            "emoji": "🌌",
            "knowledge": "空気の澄んだ上空では、星がよりきれいに見えることもあるよ。"
        },
        "type": "gachi"
    },
    {
        "fortune": "神秘吉 ☄️ 流れ星のキセキ",
        "item": "星座早見盤 ☄️",
        "result": {
            "color": "オーロラグリーン",
            "theme_color": "#004d40",
            "airline": "オーロラジェット",
            "emoji": "☄️",
            "knowledge": "流れ星みたいに一瞬のキラキラした出会いがあるかも！"
        },
        "type": "gachi"
    }
]

pair_fortunes = [
    {
        "fortune": "相性 1000% 💖 運命のフライト",
        "item": "ペアのチケット 🎟️🎟️",
        "result": {
            "color": "ラブラブピンク",
            "theme_color": "#d81b60",
            "airline": "ハートフルエアー",
            "emoji": "💘",
            "knowledge": "パイロットと副操縦士のように、二人の息はピッタリ！"
        },
        "type": "pair"
    },
    {
        "fortune": "相性 80% 💕 名コンビ誕生",
        "item": "おそろいのキーホルダー",
        "result": {
            "color": "ハッピーレッド",
            "theme_color": "#e53935",
            "airline": "スマイルフライト",
            "emoji": "💞",
            "knowledge": "両方の翼があって初めて飛べるように、協力すると強いよ！"
        },
        "type": "pair"
    },
    {
        "fortune": "相性 60% 😊 なかよし急上昇",
        "item": "はんぶんこのドーナツ 🍩",
        "result": {
            "color": "フレンドオレンジ",
            "theme_color": "#ff9800",
            "airline": "フレンドリー航空",
            "emoji": "🤝",
            "knowledge": "少しずつ仲良くなれるよ。"
        },
        "type": "pair"
    },
    {
        "fortune": "相性 120% 🚀 宇宙まで飛べる仲",
        "item": "ジェットエンジン 🚀",
        "result": {
            "color": "パッションレッド",
            "theme_color": "#b71c1c",
            "airline": "ギャラクシーペア",
            "emoji": "🔥",
            "knowledge": "二人のパワーを合わせたらロケットみたいに最強かも！？"
        },
        "type": "pair"
    }
]

birthday_list = {
    "いちな": "0601",
    "みつき": "0602",
    "りと": "0603",
    "えいこう": "0604",
    "すず": "0605",
    "えま": "0606",
    "ひなの": "0607",
    "ふうが": "0608",
    "ゆう": "0609",
    "みひろ": "0610",
    "しょうり": "0611",
    "りょうま": "0612",
    "じゅきあ": "0613",
    "りゅうき": "0614",
    "はるた": "0330",
    "しょうま": "0616",
    "じょうたろう": "0617",
    "あやと": "0618",
    "しょうた": "0619",
    "ひろむ": "0329"
}

# ---------------------------
# 関数
# ---------------------------
def to_hiragana(text):
    return "".join(
        chr(ord(c) - 0x60) if 0x30A1 <= ord(c) <= 0x30F6 else c
        for c in text
    )

def get_golden_jackpot():
    return {
        "fortune": "🏆 黄金の超絶ウルトラ大吉 🏆",
        "item": "🥇 幻の黄金の航空券",
        "result": {
            "color": "ピカピカの黄金（ゴールド）",
            "theme_color": "#d4af37",
            "airline": "伝説の黄金フライト！",
            "emoji": "🌟",
            "knowledge": "めったに出ない超大当たり！今日は最高の一日になるかも！"
        },
        "type": "golden"
    }

def generate_fortune(course):
    if random.randint(1, 20) == 1:
        return get_golden_jackpot()

    if course == "normal":
        return {
            "fortune": random.choice(fortunes),
            "item": random.choice(items),
            "result": random.choice(colors_data),
            "type": "normal"
        }

    if course == "funny":
        ret = random.choice(special_fortunes).copy()
        ret["type"] = "funny"
        return ret

    if course == "animal":
        ret = random.choice(animal_fortunes).copy()
        ret["type"] = "animal"
        return ret

    if course == "gachi":
        ret = random.choice(gachi_fortunes).copy()
        ret["type"] = "gachi"
        return ret

    if course == "pair":
        ret = random.choice(pair_fortunes).copy()
        ret["type"] = "pair"
        return ret

    return get_golden_jackpot()

def execute_fortune(course):
    st.session_state.course_type = course
    st.session_state.current_result = generate_fortune(course)
    st.session_state.show_airplane = True
    st.session_state.step = "result"
    st.rerun()

# ---------------------------
# UI
# ---------------------------
st.markdown('<div class="clouds">☁️ ✈️ ☁️ ✈️ ☁️</div>', unsafe_allow_html=True)
st.markdown(
    '<h1 class="main-title">✨ 浜田子供会 ✨<br>ラッキー占い ✈️</h1>',
    unsafe_allow_html=True
)

if st.session_state.step == "input":
    if not st.session_state.is_pair_mode:
        user_input = st.text_input(
            "おなまえをいれてね！",
            value=st.session_state.user_name,
            placeholder="ひらがなでいれてね",
            max_chars=15
        )
        st.session_state.user_name = user_input
    else:
        st.markdown(
            '<div style="text-align:center; font-weight:bold; color:#e53935; font-size:1.15rem; margin-bottom:10px;">💕 ２人のなまえをいれてね！ 💕</div>',
            unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        with col1:
            user_input = st.text_input(
                "おなまえ 1",
                value=st.session_state.user_name,
                placeholder="ひらがな",
                max_chars=15
            )
            st.session_state.user_name = user_input
        with col2:
            user_input2 = st.text_input(
                "おなまえ 2",
                value=st.session_state.user_name2,
                placeholder="ひらがな",
                max_chars=15
            )
            st.session_state.user_name2 = user_input2

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="flight-btn">', unsafe_allow_html=True)
        btn_normal = st.button("🔵 スカイ運勢", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="animal-btn">', unsafe_allow_html=True)
        btn_animal = st.button("🌸 アニマル運", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="funny-btn">', unsafe_allow_html=True)
        btn_funny = st.button("🟠 お笑いフライト", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="gachi-btn">', unsafe_allow_html=True)
        btn_gachi = st.button("🌌 星空・血液型", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

    st.markdown('<div class="pair-btn">', unsafe_allow_html=True)
    if st.session_state.is_pair_mode:
        btn_pair = st.button("❤️ この2人で占う！", use_container_width=True)
    else:
        btn_pair = st.button("❤️ 相性チェック", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if btn_normal:
        st.session_state.user_name = user_input.strip() if user_input.strip() else "おともだち"
        execute_fortune("normal")

    if btn_funny:
        st.session_state.user_name = user_input.strip() if user_input.strip() else "おともだち"
        execute_fortune("funny")

    if btn_animal:
        st.session_state.user_name = user_input.strip() if user_input.strip() else "おともだち"
        execute_fortune("animal")

    if btn_gachi:
        st.session_state.user_name = user_input.strip() if user_input.strip() else "おともだち"
        execute_fortune("gachi")

    if btn_pair:
        if not st.session_state.is_pair_mode:
            st.session_state.is_pair_mode = True
            st.rerun()
        else:
            name1 = st.session_state.user_name.strip() or "おともだち1"
            name2 = st.session_state.user_name2.strip() or "おともだち2"
            st.session_state.user_name = f"{name1} ＆ {name2}"
            execute_fortune("pair")

elif st.session_state.step == "result":
    if st.session_state.get("show_airplane", False):
        st.markdown('<div class="airplane-animation">✈️</div>', unsafe_allow_html=True)
        st.session_state.show_airplane = False

    name = st.session_state.user_name
    hira_name = to_hiragana(name)
    current = st.session_state.current_result

    JST = datetime.timezone(datetime.timedelta(hours=9))
    today_str = datetime.datetime.now(JST).strftime("%m%d")
    is_birthday = (hira_name in birthday_list and birthday_list[hira_name] == today_str)

    if is_birthday:
        st.balloons()
        st.markdown(
            '<div class="birthday-box">おたんじょうび<br>おめでとう！🎂✨</div>',
            unsafe_allow_html=True
        )

    greeting_text = f"{name}さん、今日のアナタは…"
    if st.session_state.course_type == "pair":
        greeting_text = "二人の相性は…"

    fortune = current["fortune"]
    item = current["item"]
    result = current["result"]
    text_color = result["theme_color"]

    golden_border = ""
    if current.get("type") == "golden":
        golden_border = "border: 5px solid #ffca28; box-shadow: 0 0 22px rgba(255, 215, 0, 0.55);"

    html_content = f"""
    <div class="result-card" style="{golden_border}">
        <div class="section-title">【{greeting_text}】</div>
        <div class="fortune-text">{fortune}</div>
        <hr style="border: 1px dashed #ccc; margin: 8px 0;">
        <div class="section-title">✨ ラッキーカラー ✨</div>
        <div class="color-name" style="color: {text_color};">{result['emoji']} {result['color']}</div>
        <div class="airline-name">イメージ：{result['airline']} ✈️</div>
        <hr style="border: 1px dashed #ccc; margin: 8px 0;">
        <div class="section-title">🎁 ラッキーアイテム 🎁</div>
        <div class="item-name">{item}</div>
        <div class="mamechishiki"><strong>💡 関空の飛行機 豆知識 💡</strong><br>{result['knowledge']}</div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

    st.markdown('<div class="retry-btn">', unsafe_allow_html=True)
    if st.button("🔄 もう一度あそぶ", use_container_width=True):
        st.session_state.step = "input"
        st.session_state.is_pair_mode = False
        st.session_state.user_name = ""
        st.session_state.user_name2 = ""
        st.session_state.current_result = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="clouds" style="margin-top:16px; margin-bottom:24px;">☁️ ✨ ☁️ ✨ ☁️</div>',
    unsafe_allow_html=True
)
