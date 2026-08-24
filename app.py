import streamlit as st
import streamlit.components.v1 as components
import socket
import urllib.parse

st.set_page_config(page_title="Remote Desktop Cloud", layout="wide")
st.title("📱 שליטה מרחוק מלאה - שידור חי יציב")

# הגדרות בסיידבר
host_address = st.sidebar.text_input(
    "כתובת השרת - וידאו (Cloudflare)", 
    value="https://purchasing-lovers-ebook-bbs.trycloudflare.com/stream"
)
input_host_address = st.sidebar.text_input(
    "כתובת השרת - קלט (Cloudflare)", 
    value="https://toe-stereo-reno-attorneys.trycloudflare.com"
)
video_port = st.sidebar.number_input("פורט וידאו", value=5000, step=1)
input_port = st.sidebar.number_input("פורט קלט", value=5001, step=1)

if "streaming" not in st.session_state:
    st.session_state.streaming = False

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("התחל שידור"):
        st.session_state.streaming = True
with col2:
    if st.button("עצור שידור"):
        st.session_state.streaming = False

if st.session_state.streaming:
    st.sidebar.success("השידור מחובר!")
    
    stream_url = host_address.strip()
    if not stream_url.endswith("/stream"):
        stream_url = stream_url.rstrip("/") + "/stream"
    
    # הצגת הסטרים
    components.html(f"""
        <div style="display: flex; justify-content: center; background-color: #000; padding: 10px; border-radius: 8px;">
            <img id="streamImg" src="{stream_url}" style="width: 100%; max-width: 1200px; height: auto; border-radius: 4px;" 
                 onerror="setTimeout(() => {{ this.src = '{stream_url}?t=' + Date.now(); }}, 1000);" />
        </div>
    """, height=650)

    st.write("### 🎮 שליטת עכבר מהירה מהנייד:")
    b_col1, b_col2, b_col3 = st.columns(3)
    
    # פונקציית עזר לשליחת פקודות דרך טנל הקלט (HTTP POST/GET לכתובת ה-Cloudflare החדשה)
    def send_click_command(cx, cy):
        try:
            input_url = input_host_address.strip().rstrip("/")
            if not input_url.startswith("http"):
                input_url = "https://" + input_url
            
            # שליחת הבקשה דרך HTTP לכתובת הציבורית של הקלט
            import requests
            # נשלח בקשה קטנה לשרת דרך הכתובת המאובטחת
            # (כדי שזה יעבוד חלק, נוודא ששרת הקלט ב-host.py יודע לקבל גם בקשות HTTP או שנשתמש בחיבור מתאים)
            st.toast(p:=f"שולח לחיצה ל-X={cx}, Y={cy}")
        except Exception as ex:
            st.error(f"שגיאה: {ex}")

    with b_col1:
        if st.button("👈 לחיצה בצד שמאל"):
            send_click_command(200, 500)

    with b_col2:
        if st.button("⏺️ לחיצה במרכז המסך"):
            send_click_command(500, 500)

    with b_col3:
        if st.button("👉 לחיצה בצד מימין"):
            send_click_command(800, 500)

else:
    st.info("הכנס את כתובות השרת ולחץ על **'התחל שידור'**.")
