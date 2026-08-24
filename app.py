import streamlit as st
import streamlit.components.v1 as components
import socket

st.set_page_config(page_title="Remote Desktop Cloud", layout="wide")
st.title("📱 שליטה מרחוק מלאה - שידור חי יציב")

# שדה להזנת כתובת השרת
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

    # קליטת קואורדינטות במידה ונשלחו מה-HTML
    if "click_x" in st.query_params and "click_y" in st.query_params:
        try:
            cx = int(st.query_params["click_x"])
            cy = int(st.query_params["click_y"])
            temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_sock.settimeout(2)
            temp_sock.connect((target_ip, int(input_port)))
            temp_sock.sendall(f"CLICK,{cx},{cy},left".encode('utf-8'))
            temp_sock.close()
            st.toast(f" בוצעה לחיצה בקוורדינטות: X={cx}, Y={cy}")
        except Exception as ex:
            pass

    # הצגת הסטרים בתוך נגן HTML המאפשר ללחוץ על התמונה
    components.html(f"""
        <div style="display: flex; justify-content: center; background-color: #000; padding: 10px; border-radius: 8px;">
            <img id="streamImg" src="{stream_url}" style="width: 100%; max-width: 1200px; height: auto; border-radius: 4px; cursor: crosshair;" 
                 onclick="let rect = this.getBoundingClientRect(); let x = Math.round((event.clientX - rect.left) * (this.naturalWidth / rect.width)); let y = Math.round((event.clientY - rect.top) * (this.naturalHeight / rect.height)); window.location.href = '?click_x=' + x + '&click_y=' + y;"
                 onerror="setTimeout(() => {{ this.src = '{stream_url}?t=' + Date.now(); }}, 1000);" />
        </div>
    """, height=700)

else:
    st.info("הכנס את כתובת השרת ולחץ על **'התחל שידור'**.")
