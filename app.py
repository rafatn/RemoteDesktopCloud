import streamlit as st
import streamlit.components.v1 as components
import socket

st.set_page_config(page_title="Remote Desktop Cloud", layout="wide")
st.title("📱 שליטה מרחוק מלאה - שידור חי יציב")

# שדה להזנת כתובת השרת (כולל https:// ו- /stream)
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
    
    # שימוש ישיר בכתובת המלאה שהוזנה, תוך וידוא שהיא מסתיימת ב-/stream
    stream_url = host_address.strip()
    if not stream_url.endswith("/stream"):
        stream_url = stream_url.rstrip("/") + "/stream"
    
    # חילוץ הכתובת הבסיסית או ה-IP עבור שליחת פקודות קלט (עכבר/מקלדת)
    # במידה ומשתמשים ב-Cloudflare Tunnel, שליחת קלט דרך TCP חיצוני דורשת כתובת מתאימה, 
    # אך לצורך הדוגמה נשתמש בחילוץ ה-hostname או נשמור על תאימות
    clean_host = host_address.replace("https://", "").replace("http://", "").split("/")[0]

    # הצגת הסטרים בתוך נגן HTML חלק ויציב עם מנגנון רענון אוטומטי במקרה של ניתוק
    components.html(f"""
        <div style="display: flex; justify-content: center; background-color: #000; padding: 10px; border-radius: 8px;">
            <img id="streamImg" src="{stream_url}" style="width: 100%; max-width: 1200px; height: auto; border-radius: 4px;" 
                 onerror="setTimeout(() => {{ this.src = '{stream_url}?t=' + Date.now(); }}, 1000);" />
        </div>
    """, height=700)

    if st.button("שלח לחיצה שמאלית במרכז המסך"):
        try:
            # הערה: שליחת קלט דרך TCP דורשת חיבור ישיר (למשל דרך Tailscale IP עבור פקודות),
            # לכן אם משתמשים ב-Cloudflare עבור וידאו, כדאי לוודא לאן שולחים את פקודות ה-TCP.
            temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_sock.settimeout(3)
            # אם מוזנת כתובת Cloudflare, פקודות TCP ישירות לא יעברו דרכה אלא אם יש טנל נפרד לפקודות.
            # נשאיר את החיבור הבסיסי לפי הפורט המוגדר:
            target_ip = clean_host.split(":")[0] # ניקוי פורטים במידה וקיימים
            temp_sock.connect((target_ip if not "trycloudflare.com" in target_ip else "localhost", int(input_port)))
            temp_sock.sendall(b"CLICK,500,500,left")
            temp_sock.close()
            st.toast("הפקודה נשלחה בהצלחה!")
        except Exception as ex:
            st.error(f"שגיאה בשליחת קלט: {ex}")
else:
    st.info("הכנס את כתובת השרת ולחץ על **'התחל שידור'**.")
