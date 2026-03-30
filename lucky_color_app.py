import streamlit as st
import random
import datetime
import time
import streamlit.components.v1 as components

st.set_page_config(
    page_title="飛行機ラッキーカラー 占い",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------
# セッションの初期化
# ---------------------------
if "step" not in st.session_state:
    st.session_state.step = "input"
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_name2" not in st.session_state:
    st.session_state.user_name2 = ""
if "current_result" not in st.session_state:
    st.session_state.current_result = None
if "show_airplane" not in st.session_state:
    st.session_state.show_airplane = False
if "course_type" not in st.session_state:
    st.session_state.course_type = "normal"
if "is_pair_mode" not in st.session_state:
    st.session_state.is_pair_mode = False

# ---------------------------
# カスタムCSS＆JS（ボタン色変更用）
# ---------------------------
st.markdown("""<style>
/* Streamlit UI elements hiding */
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stHeader"] { display: none !important; }
[data-testid="stFooter"] { display: none !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; display: none !important; }
header { visibility: hidden !important; display: none !important; }

/* Dynamic Background & Global No-Overflow Settings */
* {
    box-sizing: border-box !important;
}
html, body {
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: hidden !important;
    margin: 0;
    padding: 0;
    height: auto !important;
    min-height: 100vh !important;
}
.stApp { 
    transition: background-color 0.5s ease; 
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: hidden !important;
    height: auto !important;
    min-height: 100vh !important;
}
.block-container { 
    padding-top: 1.5rem; 
    padding-bottom: 6rem !important; 
    max-width: 500px; 
    margin: 0 auto !important;
    overflow-x: hidden !important;
    padding-left: 15px !important;
    padding-right: 15px !important;
}
.main-title { font-size: clamp(1.3rem, 4.5vw, 2rem); color: #007bb5; text-align: center; text-shadow: 1px 1px 2px #fff; margin-top: 20px; margin-bottom: 20px; font-weight: bold; line-height: 1.4; }
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

/* スマホでも強制的に2列にするための設定（中央寄せ徹底） */
div[data-testid="stHorizontalBlock"] {
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 10px !important;
    padding: 0 !important; /* 中央寄せを徹底するためここはゼロ、コンテナ余白に依存 */
    box-sizing: border-box !important;
    width:100% !important;
    margin: 0 auto !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    width:42% !important; /* ボタンの横幅を42%に縮小 */
    max-width:42% !important;
    flex: 0 0 42% !important;
    min-width:0 !important;
}

/* Course Buttons Container (Plump & 3D) */
div.stButton > button { 
    font-weight: bold; 
    border-radius: 16px; 
    padding: 8px 2px; 
    border: none; 
    box-shadow: 0px 6px 0px rgba(0, 0, 0, 0.15), 0px 10px 12px rgba(0, 0, 0, 0.2); 
    transition: all 0.1s ease-in-out; 
    width:100%; 
    height: 100px;
    margin-bottom: 12px; 
    color: #ffffff; 
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    line-height: 1.2;
    overflow: hidden;
}
div.stButton > button > div {
    width:100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
div.stButton > button:hover { 
    transform: translateY(3px); 
    box-shadow: 0px 5px 0px rgba(0, 0, 0, 0.15), 0px 8px 10px rgba(0, 0, 0, 0.2); 
    filter: brightness(1.1); 
}
div.stButton > button:active, div.stButton > button:focus:active { 
    transform: translateY(8px); 
    box-shadow: 0px 0px 0px rgba(0, 0, 0, 0.15), 0px 2px 4px rgba(0, 0, 0, 0.2); 
    outline: none;
}
div.stButton > button p {
    width:100%;
    margin: 0;
    text-align: center;
    white-space: nowrap !important;
    overflow: hidden;
    text-overflow: clip; /* スマホで1行に収まるように */
}

div[data-testid="stTextInput"] label p { font-size: 1.2rem; font-weight: bold; color: #007bb5; }
div[data-testid="stTextInput"] input { font-size: 1.2rem; padding: 12px; border-radius: 15px; border: 2px solid #81d4fa; box-shadow: 0px 4px 6px rgba(0,0,0,0.05); }

/* Animation Overlays */
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
</style>""", unsafe_allow_html=True)

# ボタンのスタイル適用JS
components.html("""
<script>
function styleButtons() {
    const btns = window.parent.document.querySelectorAll('button');
    btns.forEach(btn => {
        const p = btn.querySelector('p');
        if(!p) return;
        const text = p.innerText;
        
        if(text.includes('スカイ運勢')) {
            btn.style.backgroundColor = '#1e88e5'; 
            if(p.dataset.styled !== "1") {
                p.innerHTML = '<span style="font-size:clamp(1.5rem, 5vw, 2.2rem); display:block; margin-bottom:2px;">🔵</span><span style="font-size:clamp(0.55rem, 2.4vw, 0.75rem); font-weight:bold; letter-spacing:-0.5px;">【王道】スカイ運勢</span>';
                p.dataset.styled = "1";
            }
        }
        else if(text.includes('お笑いフライト')) {
            btn.style.backgroundColor = '#fb8c00';
            if(p.dataset.styled !== "1") {
                p.innerHTML = '<span style="font-size:clamp(1.5rem, 5vw, 2.2rem); display:block; margin-bottom:2px;">🟠</span><span style="font-size:clamp(0.55rem, 2.4vw, 0.75rem); font-weight:bold; letter-spacing:-0.5px;">【爆笑】お笑いフライト</span>';
                p.dataset.styled = "1";
            }
        }
        else if(text.includes('アニマル運')) {
            btn.style.backgroundColor = '#ec407a';
            if(p.dataset.styled !== "1") {
                p.innerHTML = '<span style="font-size:clamp(1.5rem, 5vw, 2.2rem); display:block; margin-bottom:2px;">🌸</span><span style="font-size:clamp(0.55rem, 2.4vw, 0.75rem); font-weight:bold; letter-spacing:-0.5px;">【もふもふ】アニマル運</span>';
                p.dataset.styled = "1";
            }
        }
        else if(text.includes('星空・血液型')) {
            btn.style.backgroundColor = '#3949ab';
            if(p.dataset.styled !== "1") {
                p.innerHTML = '<span style="font-size:clamp(1.5rem, 5vw, 2.2rem); display:block; margin-bottom:2px;">🌌</span><span style="font-size:clamp(0.55rem, 2.4vw, 0.75rem); font-weight:bold; letter-spacing:-0.5px;">【ガチ】星空・血液型</span>';
                p.dataset.styled = "1";
            }
        }
        else if(text.includes('相性チェック') || text.includes('この2人で占う')) {
            btn.style.backgroundColor = '#e53935';
            btn.style.height = '120px'; /* 相性チェックだけ少し高くして操作しやすく */
            if(text.includes('この2人で占う') && p.dataset.styled !== "2") {
                p.innerHTML = '<span style="font-size:clamp(1.8rem, 6vw, 2.5rem); display:block; margin-bottom:4px;">❤️</span><span style="font-size:clamp(0.75rem, 3.2vw, 1.0rem); font-weight:bold;">この2人で占う！</span>';
                p.dataset.styled = "2";
            } else if (!text.includes('この2人で占う') && p.dataset.styled !== "1") {
                p.innerHTML = '<span style="font-size:clamp(1.8rem, 6vw, 2.5rem); display:block; margin-bottom:4px;">❤️</span><span style="font-size:clamp(0.75rem, 3.2vw, 1.0rem); font-weight:bold;">【二人で】相性チェック</span>';
                p.dataset.styled = "1";
            }
        }
        else if(text.includes('もう一度')) {
            btn.style.backgroundColor = '#4caf50';
            btn.style.height = '100px';
            btn.style.marginBottom = '50px';
            if(p.dataset.styled !== "1") {
                p.innerHTML = '<span style="font-size:clamp(1.8rem, 6vw, 2.5rem); display:block; margin-bottom:4px;">🔄</span><span style="font-size:clamp(0.9rem, 3.5vw, 1.2rem); font-weight:bold;">もう一度あそぶ</span>';
                p.dataset.styled = "1";
            }
        }
    });
}
styleButtons();
const observer = new MutationObserver(styleButtons);
observer.observe(window.parent.document.body, { childList: true, subtree: true });
</script>
""", height=0, width=0)

# 背景色の動的変更
bg_color = "#e0f7fa" # Default (スカイ運勢)
if st.session_state.step == "result" and st.session_state.current_result:
    current = st.session_state.current_result
    if current.get("type") == "golden": bg_color = "#fff8e1"
    elif current.get("type") == "funny": bg_color = "#fff9c4"
    elif current.get("type") == "animal": bg_color = "#fce4ec"
    elif current.get("type") == "gachi": bg_color = "#e8eaf6"
    elif current.get("type") == "pair": bg_color = "#ffebee"

st.markdown(f"<style>.stApp {{ background-color: {bg_color} !important; }}</style>", unsafe_allow_html=True)

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

animal_fortunes = [
    {"fortune": "キャプテン・パンダ運 🐼", "item": "🐼 パンダの「おひるね枕」", "result": {"color": "ささいろグリーン", "theme_color": "#2e7d32", "airline": "もふもふ航空", "emoji": "🎋", "knowledge": "パンダは笹をたくさん食べて眠るんだ！飛行機でたっぷり寝たら、スッキリ元気になれるよ！"}, "type": "animal", "animation_emojis": ["🐼", "🎋", "🍃"]},
    {"fortune": "そらとぶ ペンギン運 🐧", "item": "🍦 ひえひえ「ソフトクリーム」", "result": {"color": "こおり色ブルー", "theme_color": "#81d4fa", "airline": "スノーウィングス", "emoji": "❄️", "knowledge": "ペンギンは空を飛べないけど海を飛ぶように泳ぐんだ！君も自由に大空を飛べるよ！"}, "type": "animal", "animation_emojis": ["🐧", "❄️"]},
    {"fortune": "ふわふわ ウサギCAさん運 🐰", "item": "🎀 うさ耳「カチューシャ」", "result": {"color": "いちごミルク", "theme_color": "#f8bbd0", "airline": "キャロットエアー", "emoji": "🍓", "knowledge": "CAさんは飛行機の中でいろんなお世話をしてくれる優しい人たち。ウサギみたいにピョンと跳ねて活躍しよう！"}, "type": "animal", "animation_emojis": ["🐰", "🥕", "💖"]},
    {"fortune": "くいしんぼう クマ機長運 🐻", "item": "🍯 とろ〜り「はちみつ」", "result": {"color": "はちみつゴールド", "theme_color": "#ffb300", "airline": "ベアーフライト", "emoji": "🍯", "knowledge": "クマの機長はちょっと食いしん坊かも？おいしいご飯を食べれば、どんなフライトも大成功！"}, "type": "animal", "animation_emojis": ["🐻", "🐝", "🍯"]},
    {"fortune": "おしゃべり インコパイロット運 🐦", "item": "✒️ カラフルな「はねのペン」", "result": {"color": "レインボー", "theme_color": "#ab47bc", "airline": "パロットジェット", "emoji": "🌈", "knowledge": "おしゃべりなインコは、パイロットの通信みたいだね！いろんな人とお話しして楽しい一日になりそう！"}, "type": "animal", "animation_emojis": ["🐦", "🎵", "✨"]}
]

special_fortunes = [
    {"fortune": "鼻毛が伸びる運 👃", "item": "🧦 先生の穴あき靴下", "result": {"color": "鼻水スカイブルー", "theme_color": "#4fc3f7", "airline": "ヒミツの航空", "emoji": "💧", "knowledge": "飛行機に乗ると気圧の変化でおならが出やすくなるんだって！ホントだよ！"}},
    {"fortune": "おならが止まらない運 💨", "item": "🩲 予備のパンツ（3枚）", "result": {"color": "ぷうぷうイエロー", "theme_color": "#ffeb3b", "airline": "オナラ航空", "emoji": "💨", "knowledge": "パイロットは、実はおならを我慢しながら運転してるかも！？（ウソだよ！）"}},
    {"fortune": "顔がパンパン運 🍞", "item": "🍬 誰かの食べかけの飴", "result": {"color": "アンパンレッド", "theme_color": "#e53935", "airline": "パンパンエアー", "emoji": "🔴", "knowledge": "飛行機の中では、ポテトチップスの袋がパンパンに膨らむよ！顔も膨らむかも！？"}},
    {"fortune": "逆立ち歩き運 🙃", "item": "📖 逆さまの教科書", "result": {"color": "まっさかさまパープル", "theme_color": "#9c27b0", "airline": "さかさま航空", "emoji": "👾", "knowledge": "飛行機は逆さまに飛ぶこともできるんだよ（本物のアクロバット飛行機ね！）。"}},
    {"fortune": "迷子の子猫運 🐱", "item": "🎀 ネコ耳カチューシャ", "result": {"color": "にゃんにゃんホワイト", "theme_color": "#212121", "airline": "ニャンコエアー", "emoji": "🐾", "knowledge": "飛行機のタイヤは、車よりずっと分厚くて丈夫なんだよ！猫の肉球とは大違い！"}},
    {"fortune": "宿題が消える運 🪄", "item": "🖍️ 魔法の消しゴム", "result": {"color": "まぼろし透明色", "theme_color": "#b0bec5", "airline": "マジックジェット", "emoji": "👻", "knowledge": "飛行機は雷に打たれても大丈夫なように作られているんだ。魔法みたいでしょ？"}},
    {"fortune": "宇宙人にさらわれる運 👽", "item": "🛸 アルミホイルの帽子", "result": {"color": "未確認グリーン", "theme_color": "#4caf50", "airline": "UFO", "emoji": "👽", "knowledge": "飛行機に乗ってるときに見える星空は、地上よりずっと綺麗だよ！宇宙人に会えるかも？"}},
    {"fortune": "うひょー！大爆笑 🤣", "item": "🕶️ 先生のサングラス", "result": {"color": "ヘンテコ色", "theme_color": "#009688", "airline": "ヒミツ", "emoji": "💧", "knowledge": "飛行機は、おならをブーンと出すと空に浮くんだよ（ウソだよ、エンジンだよ！）。"}},
    {"fortune": "げらげら運 😆", "item": "💩 ニセモノのうんち", "result": {"color": "うんち色ゴールド！", "theme_color": "#d4af37", "airline": "ナイショ", "emoji": "💩", "knowledge": "パイロットは、実は寝ながら運転してるんだよ（ウソだよ、ちゃんと見てるよ！）。"}}
]

gachi_fortunes = [
    {"fortune": "大吉 ⭐ 神レベルの運勢", "item": "望遠鏡 🔭", "result": {"color": "ミッドナイトブルー", "theme_color": "#1a237e", "airline": "スターライト", "emoji": "🌠", "knowledge": "夜の飛行機から見る星空は、まるで宇宙空間！君の未来も星みたいに輝いてるよ。"}, "type": "gachi"},
    {"fortune": "中吉 🌙 月のパワー全開", "item": "コンパス 🧭", "result": {"color": "ムーンライトシルバー", "theme_color": "#607d8b", "airline": "ルナ・フライト", "emoji": "🌒", "knowledge": "昔の船や飛行機は星や月の位置を見て方角を知ったんだ。迷っても月が教えてくれるよ。"}, "type": "gachi"},
    {"fortune": "小吉 🌌 天の川のひらめき", "item": "星図帳 🗺️", "result": {"color": "ギャラクシーパープル", "theme_color": "#4a148c", "airline": "ミルキーウェイ", "emoji": "🌌", "knowledge": "空気の澄んだ上空では天の川までハッキリ見えるよ。今日はひらめきが冴える日！"}, "type": "gachi"},
    {"fortune": "神秘吉 ☄️ 流れ星のキセキ", "item": "星座早見盤 ☄️", "result": {"color": "オーロラグリーン", "theme_color": "#004d40", "airline": "オーロラジェット", "emoji": "☄️", "knowledge": "飛行機の上から流れ星を見ると、なんだか自分と同じ速さで飛んでいるように見えるかも！？"}, "type": "gachi"}
]

pair_fortunes = [
    {"fortune": "相性 1000% 💖 運命のフライト", "item": "ペアのチケット 🎟️🎟️", "result": {"color": "ラブラブピンク", "theme_color": "#d81b60", "airline": "ハートフルエアー", "emoji": "💘", "knowledge": "飛行機のパイロットと副操縦士のように、二人の息はピッタリ！無敵のコンビだね！"}, "type": "pair"},
    {"fortune": "相性 80% 💕 名コンビ誕生", "item": "おそろいのキーホルダー", "result": {"color": "ハッピーレッド", "theme_color": "#e53935", "airline": "スマイルフライト", "emoji": "💞", "knowledge": "飛行機は両方の翼があって初めて飛べるんだ。二人で協力すれば何でもできるよ！"}, "type": "pair"},
    {"fortune": "相性 60% 😊 なかよし急上昇", "item": "はんぶんこのドーナツ 🍩", "result": {"color": "フレンドオレンジ", "theme_color": "#ff9800", "airline": "フレンドリー航空", "emoji": "🤝", "knowledge": "飛行機のエンジンは、力を合わせてぐんぐん進む！二人も少しずつ仲良くなれるよ。"}, "type": "pair"},
    {"fortune": "相性 120% 🚀 宇宙まで飛べる仲", "item": "ジェットエンジン 🚀", "result": {"color": "パッションレッド", "theme_color": "#b71c1c", "airline": "ギャラクシーペア", "emoji": "🔥", "knowledge": "二人のパワーを合わせたら、飛行機を飛び越えてロケットみたいに宇宙まで行けちゃうかも！？"}, "type": "pair"}
]

birthday_list = {
    "いちな": "0601", "みつき": "0602", "りと": "0603", "えいこう": "0604",
    "すず": "0605", "えま": "0606", "ひなの": "0607", "ふうが": "0608",
    "ゆう": "0609", "みひろ": "0610", "しょうり": "0611", "りょうま": "0612",
    "じゅきあ": "0613", "りゅうき": "0614", "はるた": "0330", "しょうま": "0616",
    "じょうたろう": "0617", "あやと": "0618", "しょうた": "0619", "ひろむ": "0329"
}

def to_hiragana(text):
    return "".join(chr(ord(c) - 0x60) if 0x30A1 <= ord(c) <= 0x30F6 else c for c in text)

def get_golden_jackpot():
    return {
        "fortune": "🏆 黄金の超絶ウルトラ大吉 🏆",
        "item": "🥇 幻の黄金の航空券",
        "result": {
            "color": "ピカピカの黄金（ゴールド）", 
            "theme_color": "#d4af37", 
            "airline": "伝説の黄金フライト！", 
            "emoji": "🌟", 
            "knowledge": "めったに出ない超大当たり！今日は神様もびっくりするほど、最高の一日になるよ！お土産ゲット！"
        },
        "type": "golden",
        "animation_emojis": ["🏆", "🥇", "✨", "💰", "🎊"]
    }

def generate_fortune(course):
    # 🌟 20回に1回(5%)の大当たり判定
    if random.randint(1, 20) == 1:
        return get_golden_jackpot()

    if course == "normal":
        return {
            "fortune": random.choice(fortunes),
            "item": random.choice(items),
            "result": random.choice(colors_data),
            "type": "normal",
            "animation_emojis": ["✈️", "☁️", "🌤️"]
        }
    elif course == "funny":
        ret = random.choice(special_fortunes).copy()
        ret["type"] = "funny"
        ret["animation_emojis"] = ["💩", "🤣", "💨", "👃", "🍞"]
        return ret
    elif course == "animal":
        ret = random.choice(animal_fortunes).copy()
        ret["type"] = "animal"
        if "animation_emojis" not in ret:
            ret["animation_emojis"] = ["🐾", "🐼", "🐻", "🐰"]
        return ret
    elif course == "gachi":
        ret = random.choice(gachi_fortunes).copy()
        ret["type"] = "gachi"
        ret["animation_emojis"] = ["⭐", "🌠", "🌙", "🔭"]
        return ret
    elif course == "pair":
        ret = random.choice(pair_fortunes).copy()
        ret["type"] = "pair"
        ret["animation_emojis"] = ["💖", "💕", "💘", "😍"]
        return ret
    
    return get_golden_jackpot() # Fallback

def execute_fortune(course):
    st.session_state.course_type = course
    st.session_state.current_result = generate_fortune(course)
    st.session_state.show_airplane = True
    st.session_state.step = "result"
    st.rerun()

# ---------------------------
# UI 描画
# ---------------------------
st.markdown('<div class="clouds">☁️ ✈️ ☁️ ✈️ ☁️</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">✨ 浜田子供会 ✨<br>ラッキー占い ✈️</h1>', unsafe_allow_html=True)

if st.session_state.step == "input":
    # 名前入力（相性チェックモードで切り替え）
    if not st.session_state.is_pair_mode:
        user_input = st.text_input("おなまえをいれてね！", value=st.session_state.user_name, placeholder="ひらがなでいれてね", max_chars=15)
        st.session_state.user_name = user_input
    else:
        st.markdown('<div style="text-align:center; font-weight:bold; color:#e53935; font-size:1.2rem; margin-bottom:10px;">💕 ２人のなまえをいれてね！ 💕</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            user_input = st.text_input("おなまえ 1", value=st.session_state.user_name, placeholder="ひらがな", max_chars=15)
            st.session_state.user_name = user_input
        with col2:
            user_input2 = st.text_input("おなまえ 2", value=st.session_state.user_name2, placeholder="ひらがな", max_chars=15)
            st.session_state.user_name2 = user_input2

    # ボタン表示（2列グリッド）
    col_left, col_right = st.columns(2)
    with col_left:
        btn_normal = st.button("🔵 スカイ運勢", use_container_width=True)
        btn_animal = st.button("🌸 アニマル運", use_container_width=True)
    with col_right:
        btn_funny = st.button("🟠 お笑いフライト", use_container_width=True)
        btn_gachi = st.button("🌌 星空・血液型", use_container_width=True)
        
    st.markdown('<div style="margin-top:5px;"></div>', unsafe_allow_html=True)
    
    if st.session_state.is_pair_mode:
        btn_pair = st.button("❤️ この2人で占う！（相性チェック実行）", use_container_width=True)
    else:
        btn_pair = st.button("❤️ 相性チェック", use_container_width=True)

    # 実行制御
    if btn_normal:
        st.session_state.user_name = user_input if user_input.strip() else "おともだち"
        execute_fortune("normal")
    if btn_funny:
        st.session_state.user_name = user_input if user_input.strip() else "おともだち"
        execute_fortune("funny")
    if btn_animal:
        st.session_state.user_name = user_input if user_input.strip() else "おともだち"
        execute_fortune("animal")
    if btn_gachi:
        st.session_state.user_name = user_input if user_input.strip() else "おともだち"
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
    # 飛行機アニメーション
    if st.session_state.get("show_airplane", False):
        placeholder = st.empty()
        placeholder.markdown('<div class="airplane-animation">✈️</div>', unsafe_allow_html=True)
        time.sleep(1.5)
        placeholder.empty()
        st.session_state.show_airplane = False

    name = st.session_state.user_name
    hira_name = to_hiragana(name)
    current = st.session_state.current_result
    
    # 誕生日判定 (今日の日付 MMDD)
    JST = datetime.timezone(datetime.timedelta(hours=9))
    today_str = datetime.datetime.now(JST).strftime("%m%d")
    is_birthday = (hira_name in birthday_list and birthday_list[hira_name] == today_str)
    
    if is_birthday:
        st.balloons()
        cracker_html = """
        <style>
        @keyframes fall { 0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; } 100% { transform: translateY(110vh) rotate(360deg); opacity: 0; } }
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
        st.markdown('<div style="background-color:#fff9c4; padding:25px; border-radius:20px; text-align:center; font-size:clamp(1.5rem, 6vw, 2.5rem); font-weight:900; color:#e65100; margin-bottom:20px; box-shadow:0px 8px 16px rgba(0,0,0,0.15); border: 4px dashed #ff9800; animation: float 2s ease-in-out infinite;">おたんじょうび<br>おめでとう！🎂✨</div>', unsafe_allow_html=True)
        
    greeting_text = f"{name}さん、今日のアナタは…"
    if st.session_state.course_type == "pair":
        greeting_text = f"二人の相性は…"

    # アニメーション絵文字の降らせる演出
    emojis = current.get("animation_emojis", ["✨", "🌟"])
    anim_html = """
    <style>
    @keyframes floatDown {
        0% { transform: translateY(-10vh) translateX(0vw) scale(1) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        50% { transform: translateY(50vh) translateX(5vw) scale(1.2) rotate(180deg); }
        90% { opacity: 1; }
        100% { transform: translateY(110vh) translateX(-5vw) scale(1) rotate(360deg); opacity: 0; }
    }
    .course-anim { position: fixed; top: -10%; font-size: 3.5rem; animation: floatDown ease-in forwards; z-index: 99998; pointer-events: none; }
    </style>
    """
    for i in range(12):
        left = random.randint(0, 90)
        duration = random.uniform(3.5, 6.0)
        delay = random.uniform(0, 1.5)
        icon = random.choice(emojis)
        anim_html += f'<div class="course-anim" style="left: {left}vw; animation-duration: {duration}s; animation-delay: {delay}s;">{icon}</div>'
    st.markdown(anim_html, unsafe_allow_html=True)

    fortune = current["fortune"]
    item = current["item"]
    result = current["result"]
    text_color = result["theme_color"]

    # 輝く大当たり演出
    golden_border = "border: 5px solid #ffca28; box-shadow: 0px 0px 30px rgba(255, 215, 0, 0.8);" if current.get("type") == "golden" else ""

    html_content = f"""<div class="result-card" style="{golden_border}">
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

    if st.button("🔄 もう一度あそぶ", use_container_width=True):
        st.session_state.step = "input"
        st.session_state.is_pair_mode = False
        st.session_state.user_name = ""
        st.session_state.user_name2 = ""
        st.rerun()

st.markdown('<div class="clouds" style="margin-top:15px; margin-bottom:50px;">☁️ ✨ ☁️ ✨ ☁️</div>', unsafe_allow_html=True)
