import streamlit as st
import streamlit.components.v1 as components
import socket

st.set_page_config(page_title="Remote Desktop Cloud", layout="wide")
st.title("📱 שליטה מרחוק מלאה - שידור חי יציב")

host_address = st.sidebar.text_input(
    "כתובת השרת (Cloudflare URL)", 
    value="https://purchasing-lovers-ebook-bbs.trycloudflare.com/stream"
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
    
    clean_host = host_address.replace("https://", "").replace("http://", "").split("/")[0]
    target_ip = clean_host.split(":")[0]
    if "trycloudflare.com" in target_ip:
        target_ip = "localhost"

    # הצגת הסטרים
    components.html(f"""
        <div style="display: flex; justify-content: center; background-color: #000; padding: 10px; border-radius: 8px;">
            <img id="streamImg" src="{stream_url}" style="width: 100%; max-width: 1200px; height: auto; border-radius: 4px;" 
                 onerror="setTimeout(() => {{ this.src = '{stream_url}?t=' + Date.now(); }}, 1000);" />
        </div>
    """, height=650)

    st.write("### 🎮 שליטת עכבר מהירה מהנייד:")
    b_col1, b_col2, b_col3 = st.columns(3)
    
    with b_col1:
        if st.button("👈 לחיצה בצד שמאל"):
            try:
                temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                temp_sock.settimeout(2)
                temp_sock.connect((target_ip, int(input_port)))
                temp_sock.sendall(b"CLICK,200,500,left")
                temp_sock.close()
                st.toast("נשלחה לחיצה שמאלית")
            except Exception as ex:
                st.error(f"שגיאה: {ex}")

    with b_col2:
        if st.button("⏺️ לחיצה במרכז המסך"):
            try:
                temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                temp_sock.settimeout(2)
                temp_sock.connect((target_ip, int(input_port)))
                temp_sock.sendall(b"CLICK,500,500,left")
                temp_sock.close()
                st.toast("נשלחה לחיצה מרכזית")
            except Exception as ex:
                st.error(f"שגיאה: {ex}")

    with b_col3:
        if st.button("👉 לחיצה בצד מימין"):
            try:
                temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                temp_sock.settimeout(2)
                temp_sock.connect((target_ip, int(input_port)))
                temp_sock.sendall(b"CLICK,800,500,left")
                temp_sock.close()
                st.toast("נשלחה לחיצה ימנית")
            except Exception as ex:
                st.error(f"שגיאה: {ex}")

else:
    st.info("הכנס את כתובת השרת ולחץ על **'התחל שידור'**.")
