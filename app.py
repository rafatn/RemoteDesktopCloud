import streamlit as st
import streamlit.components.v1 as components
import socket

st.set_page_config(page_title="Remote Desktop Cloud", layout="wide")
st.title("📱 שליטה מרחוק בענן - שידור חי")

# שדה להזנת כתובת ה-Ngrok או ה-IP החיצוני
host_address = st.sidebar.text_input("כתובת השרת (Ngrok URL / IP)", value="100.94.213.104")
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
    st.sidebar.success("השידור מחובר לענן!")
    
    # בניית כתובת הסטרים (אם משתמשים ב-Ngrok, הם מספקים HTTPS ישיר)
    if "ngrok" in host_address:
        # ב-Ngrok אין צורך בציון הפפורט כי הכתובת מובילה ישירות לפורט 5000
        clean_url = host_address.replace("https://", "").replace("http://", "")
        stream_url = f"https://{clean_url}/stream"
    else:
        stream_url = f"http://{host_address}:{video_port}/stream"
    
    # הצגת הסטרים בתוך נגן HTML חלק ויציב
    components.html(f"""
        <div style="display: flex; justify-content: center; background-color: #000; padding: 10px; border-radius: 8px;">
            <img src="{stream_url}" style="width: 100%; max-width: 1200px; height: auto; border-radius: 4px;" />
        </div>
    """, height=700)

    if st.button("שלח לחיצה שמאלית במרכז המסך"):
        try:
            temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_sock.connect((host_address.replace("https://", "").replace("http://", ""), int(input_port)))
            temp_sock.sendall("CLICK,500,500,left".encode('utf-8'))
            temp_sock.close()
            st.toast("הפקודה נשלחה בהצלחה!")
        except Exception as ex:
            st.error(f"שגיאה בשליחת קלט: {ex}")
else:
    st.info("הכנס את כתובת השרת ולחץ על **'התחל שידור'**.")
