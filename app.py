import streamlit as st
import socket
import struct
import cv2
import numpy as np
import threading

st.set_page_config(page_title="Remote Desktop Cloud", layout="wide")

st.title("📱 שליטה מרחוק מלאה - צפייה ושליטה")

# הגדרת כתובות ופורטים (למשל דרך הצינור של Cloudflare)
host_address = st.sidebar.text_input("כתובת השרת (Host / Domain)", value="0.tcp.ngrok.io")
video_port = st.sidebar.number_input("פורט וידאו", value=5000, step=1)
input_port = st.sidebar.number_input("פורט קלט (עכבר/מקלדת)", value=5001, step=1)

connect_btn = st.sidebar.button("התחבר למחשב")

if connect_btn:
    st.sidebar.success(f"מתחבר אל השרתים...")
    frame_slot = st.empty()
    
    # משתנים גלובליים לשמירת הסוקטים
    global input_sock
    input_sock = None

    def run_viewer():
        global input_sock
        try:
            # חיבור לערוץ הוידאו
            v_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            v_sock.connect((host_address, int(video_port)))
            
            # חיבור לערוץ הקלט
            input_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            input_sock.connect((host_address, int(input_port)))
            st.toast("התחבר בהצלחה לערוצי הווידאו והקלט!")

            data = b""
            payload_size = struct.calcsize(">L")

            while True:
                while len(data) < payload_size:
                    packet = v_sock.recv(4096)
                    if not packet: break
                    data += packet
                if not data: break

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack(">L", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += v_sock.recv(4096)

                frame_data = data[:msg_size]
                data = data[msg_size:]

                frame = np.frombuffer(frame_data, dtype=np.uint8)
                image = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                if image is not None:
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    frame_slot.image(image_rgb, channels="RGB", use_container_width=True)
                    
        except Exception as e:
            st.error(f"שגיאה בחיבור: {e}")

    threading.Thread(target=run_viewer, daemon=True).start()

    # דוגמה לשליחת פקודת עכבר ידנית או כפתורי שליטה מהירים דרך הממשק
    st.subheader("בקרת שליטה מהירה")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("שלח לחיצה שמאלית במרכז המסך"):
            if 'input_sock' in globals() and input_sock:
                # שליחת פקודת קליק לדוגמה
                cmd = "CLICK,500,500,left".encode('utf-8')
                input_sock.sendall(cmd)
