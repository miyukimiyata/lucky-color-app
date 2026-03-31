import streamlit as st

st.set_page_config(layout="wide")

# -------------------
# 初期状態
# -------------------
if "zones" not in st.session_state:
    st.session_state.zones = {
        "1区": 0,
        "2区": 0,
        "3区": 0,
        "4区": 0,
        "5区": 0,
        "7区": 0,
        "8区": 0,
        "9区A": 0,
        "9区B": 0,
        "9区D": 0,
        "9区E": 0,
        "9区F": 0,
        "9区G": 0,
        "10区": 0,
        "11区": 0,
    }

# -------------------
# 状態
# -------------------
status_labels = ["未着手", "担当完了", "役員完了"]
status_colors = ["#bdbdbd", "#ffd54f", "#66bb6a"]

# -------------------
# 切り替え処理
# -------------------
def toggle(zone):
    st.session_state.zones[zone] = (st.session_state.zones[zone] + 1) % 3

# -------------------
# CSS
# -------------------
st.markdown("""
<style>
.map-container {
    position: relative;
    width: 100%;
    max-width: 700px;
    margin: auto;
}

.map-image {
    width: 100%;
    border-radius: 10px;
}

.zone-btn {
    position: absolute;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    padding: 8px 12px;
    font-weight: bold;
    color: white;
    border: none;
}
</style>
""", unsafe_allow_html=True)

st.title("📍 廃品回収 状態管理")

# -------------------
# 地図表示
# -------------------
st.image("map.png", use_container_width=True)

# -------------------
# 座標（ざっくり配置）
# ※ここはあとで微調整できます
# -------------------
positions = {
    "1区": (55, 65),
    "2区": (45, 55),
    "3区": (50, 75),
    "4区": (60, 85),
    "5区": (65, 95),
    "7区": (40, 95),
    "8区": (45, 85),
    "9区A": (30, 30),
    "9区B": (35, 50),
    "9区D": (60, 30),
    "9区E": (50, 45),
    "9区F": (55, 40),
    "9区G": (65, 40),
    "10区": (20, 90),
    "11区": (15, 75),
}

# -------------------
# ボタン配置
# -------------------
for zone, (x, y) in positions.items():
    status = st.session_state.zones[zone]
    color = status_colors[status]

    st.markdown(f"""
    <div style="
        position:absolute;
        left:{x}%;
        top:{y}%;
        transform: translate(-50%, -50%);
    ">
        <button style="
            background:{color};
            border-radius:50%;
            padding:10px;
            color:white;
            border:none;
            font-size:12px;
        ">
            {zone}
        </button>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------
# タップUI（代替）
# -------------------
st.markdown("### ▼ 状態をタップして変更")

zones_list = list(st.session_state.zones.keys())

for zone in zones_list:
    status = st.session_state.zones[zone]
    label = status_labels[status]
    color = status_colors[status]

    button_html = f"""
    <div style="
        background:{color};
        padding:14px 10px;
        border-radius:16px;
        text-align:center;
        font-weight:bold;
        color:#333;
        margin-bottom:8px;
        line-height:1.5;
        font-size:1.2rem;
    ">
        {zone}<br>{label}
    </div>
    """

    st.markdown(button_html, unsafe_allow_html=True)
    if st.button("状態を変更", key=f"btn_{zone}", use_container_width=True):
        toggle(zone)
        st.rerun()

# -------------------
# 凡例
# -------------------
st.markdown("### ■ 状態")
for i, label in enumerate(status_labels):
    st.markdown(f"<div style='color:{status_colors[i]}; font-weight:bold'>{label}</div>", unsafe_allow_html=True)
