import streamlit as st
import streamlit.components.v1 as components
import urllib.request
import json

st.set_page_config(page_title="Remote Desktop Cloud", layout="wide")
st.title("📱 שליטה מרחוק מלאה - סנכרון אוטומטי")

# כתובת ה-API הקבועה שלך מ-npoint.io
API_CONFIG_URL = "https://api.npoint.io/9b001b354d076b04b740"

# שליפה אוטומטית של הכתובות העדכניות מהענן
try:
    req = urllib.request.Request(API_CONFIG_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=3) as response:
        config_data = json.loads(response.read().decode())
        default_video = config_data.get("video_url", "")
        default_input = config_data.get("input_url", "")
except:
    default_video = ""
    default_input = ""

# הצגת הכתובות בסיידבר (מתעדכנות לבד, אבל אפשר גם לשנות ידנית במידת הצורך)
host_address = st.sidebar.text_input("כתובת השרת - וידאו", value=default_video)
input_host_address = st.sidebar.text_input("כתובת השרת - קלט", value=default_input)

if "streaming" not in st.session_state:
    st.session_state.streaming = False

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("התחל שידור"):
        st.session_state.streaming = True
with col2:
    if st.button("עצור שידור"):
        st.session_state.streaming = False

if st.session_state.streaming and host_address:
    st.sidebar.success("השידור מחובר אוטומטית!")
    
    stream_url = host_address.strip()
    if not stream_url.endswith("/stream"):
        stream_url = stream_url.rstrip("/") + "/stream"
        
    input_url = input_host_address.strip().rstrip("/")

    # הצגת הסטרים ושליטה חלקה
    components.html(f"""
        <div style="display: flex; justify-content: center; background-color: #000; padding: 10px; border-radius: 8px;">
            <img id="streamImg" src="{stream_url}" style="width: 100%; max-width: 1200px; height: auto; border-radius: 4px; cursor: crosshair;" 
                 onclick="
                    let rect = this.getBoundingClientRect();
                    let x = Math.round((event.clientX - rect.left) * (this.naturalWidth / rect.width));
                    let y = Math.round((event.clientY - rect.top) * (this.naturalHeight / rect.height));
                    fetch('{input_url}/click?x=' + x + '&y=' + y + '&btn=left', {{method: 'GET', mode: 'no-cors'}});
                 "
                 onerror="setTimeout(() => {{ this.src = '{stream_url}?t=' + Date.now(); }}, 1000);" />
        </div>
    """, height=650)

    # כפתורי גיבוי מהנייד
    b_col1, b_col2, b_col3 = st.columns(3)
    def send_click_command(cx, cy):
        try:
            urllib.request.urlopen(f"{input_url}/click?x={cx}&y={cy}&btn=left", timeout=2)
            st.toast(f"נשלחה לחיצה: X={cx}, Y={cy}")
        except Exception as ex:
            st.error(f"שגיאה: {ex}")

    with b_col1:
        if st.button("👈 שמאלה"): send_click_command(200, 500)
    with b_col2:
        if st.button("⏺️ מרכז"): send_click_command(500, 500)
    with b_col3:
        if st.button("👉 ימינה"): send_click_command(800, 500)

else:
    st.info("לחץ על **'התחל שידור'** (הכתובות יטענו אוטומטית מהענן).")
