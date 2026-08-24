import streamlit as st
import streamlit.components.v1 as components
import socket

st.set_page_config(page_title="Remote Desktop Cloud", layout="wide")
st.title("📱 שליטה מרחוק מלאה - שידור חי יציב")

# שדה להזנת כתובת ה-Tailscale IP
host_address = st.sidebar.text_input("כתובת השרת (Tailscale IP)", value="area-loop-councils-scenarios.trycloudflare.com")
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
    
    # ניקוי הכתובת מרווחים מיותרים או פרוטוקולים
    clean_host = host_address.strip().replace("https://", "").replace("http://", "").split("/")[0]
    stream_url = f"http://{clean_host}:{video_port}/stream"
    
    # הצגת הסטרים בתוך נגן HTML חלק ויציב עם מנגנון רענון אוטומטי במקרה של ניתוק
    components.html(f"""
        <div style="display: flex; justify-content: center; background-color: #000; padding: 10px; border-radius: 8px;">
            <img id="streamImg" src="{stream_url}" style="width: 100%; max-width: 1200px; height: auto; border-radius: 4px;" 
                 onerror="setTimeout(() => {{ this.src = '{stream_url}?t=' + Date.now(); }}, 1000);" />
        </div>
    """, height=700)

    if st.button("שלח לחיצה שמאלית במרכז המסך"):
        try:
            temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_sock.settimeout(3)
            temp_sock.connect((clean_host, int(input_port)))
            temp_sock.sendall(b"CLICK,500,500,left")
            temp_sock.close()
            st.toast("הפקודה נשלחה בהצלחה!")
        except Exception as ex:
            st.error(f"שגיאה בשליחת קלט: {ex}")
else:
    st.info("הכנס את כתובת השרת ולחץ על **'התחל שידור'**.")
