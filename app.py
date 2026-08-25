import streamlit as st
import streamlit.components.v1 as components
import urllib.request
import json

st.set_page_config(page_title="Remote Desktop Cloud", layout="wide")
st.title("📱 שליטה מרחוק מלאה - פיצ'רים מתקדמים")

API_CONFIG_URL = "https://api.npoint.io/9b001b354d076b04b740"

try:
    req = urllib.request.Request(API_CONFIG_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=3) as response:
        config_data = json.loads(response.read().decode())
        default_video = config_data.get("video_url", "")
        default_input = config_data.get("input_url", "")
except:
    default_video = ""
    default_input = ""

host_address = st.sidebar.text_input("כתובת השרת - וידאו", value=default_video)
input_host_address = st.sidebar.text_input("כתובת השרת - קלט", value=default_input)

if "streaming" not in st.session_state:
    st.session_state.streaming = False
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "mouse_mode" not in st.session_state:
    st.session_state.mouse_mode = "left" # left או right

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("התחל שידור"):
        st.session_state.streaming = True
with col2:
    if st.button("עצור שידור"):
        st.session_state.streaming = False
        st.session_state.authenticated = False

if st.session_state.streaming and host_address:
    stream_url = host_address.strip()
    if not stream_url.endswith("/stream"):
        stream_url = stream_url.rstrip("/") + "/stream"
        
    input_url = input_host_address.strip().rstrip("/")

    if not st.session_state.authenticated:
        st.subheader("🔒 נדרשת סיסמה לכניסה למערכת")
        password_input = st.text_input("הכנס סיסמה למחשב (ברירת מחדל: 1234)", type="password")
        if st.button("התחבר למערכת"):
            try:
                base_host = host_address.strip().replace("/stream", "").rstrip("/")
                auth_url = f"{base_host}/login?pwd={password_input}"
                
                auth_req = urllib.request.Request(auth_url)
                with urllib.request.urlopen(auth_req, timeout=3) as auth_res:
                    res_data = json.loads(auth_res.read().decode())
                    if res_data.get("status") == "ok":
                        st.session_state.authenticated = True
                        st.success("התחברות הצליחה! טוען מערכת...")
                        st.rerun()
                    else:
                        st.error("סיסמה שגויה, נסה שוב.")
            except Exception as e:
                st.error(f"שגיאה בהתחברות לשרת: {e}")
    else:
        st.sidebar.success("השידור מחובר ומאובטח!")

        # בחירת סוג הקליק (שמאל / ימין)
        m_col1, m_col2 = st.sidebar.columns(2)
        with m_col1:
            if st.button("👆 קליק שמאלי"):
                st.session_state.mouse_mode = "left"
        with m_col2:
            if st.button("✌️ קליק ימני"):
                st.session_state.mouse_mode = "right"
        st.sidebar.info(f"מצב עכבר פעיל: **{'ימני' if st.session_state.mouse_mode == 'right' else 'שמאלי'}**")

        # סרגלי כלים מתקדמים (איכות, גלילה, מקשים, הדבקה)
        st.markdown("### 🎛️ כלי שליטה מהירים")
        
        q_col1, q_col2, q_col3, q_col4, q_col5 = st.columns(5)
        with q_col1:
            if st.button("⚡ מהיר"): urllib.request.urlopen(f"{input_url}/set_quality?quality=low")
        with q_col2:
            if st.button("⚖️ מאוזן"): urllib.request.urlopen(f"{input_url}/set_quality?quality=med")
        with q_col3:
            if st.button("💎 איכותי"): urllib.request.urlopen(f"{input_url}/set_quality?quality=high")
        with q_col4:
            if st.button("📜 גלול למעלה"): urllib.request.urlopen(f"{input_url}/scroll?dy=3")
        with q_col5:
            if st.button("📜 גלול למטה"): urllib.request.urlopen(f"{input_url}/scroll?dy=-3")

        # מקשים מיוחדים והדבקה
        k_col1, k_col2, k_col3, k_col4, k_col5 = st.columns(5)
        with k_col1:
            if st.button("↵ Enter"):
                urllib.request.urlopen(urllib.request.Request(f"{input_url}/press_key", data=json.dumps({"key": "enter"}).encode(), headers={'Content-Type': 'application/json'}))
        with k_col2:
            if st.button("⌫ Backspace"):
                urllib.request.urlopen(urllib.request.Request(f"{input_url}/press_key", data=json.dumps({"key": "backspace"}).encode(), headers={'Content-Type': 'application/json'}))
        with k_col3:
            if st.button("📋 הדבק (Ctrl+V)"):
                urllib.request.urlopen(urllib.request.Request(f"{input_url}/press_key", data=json.dumps({"key": "paste"}).encode(), headers={'Content-Type': 'application/json'}))
        with k_col4:
            if st.button("␣ Space"):
                urllib.request.urlopen(urllib.request.Request(f"{input_url}/press_key", data=json.dumps({"key": "space"}).encode(), headers={'Content-Type': 'application/json'}))
        with k_col5:
            if st.button("⎋ Esc"):
                urllib.request.urlopen(urllib.request.Request(f"{input_url}/press_key", data=json.dumps({"key": "esc"}).encode(), headers={'Content-Type': 'application/json'}))

        # הקלדת טקסט חופשי
        t_col1, t_col2 = st.columns([4, 1])
        with t_col1:
            user_text_to_type = st.text_input("הקלד טקסט לשליחה ישירה למחשב:", key="type_box")
        with t_col2:
            st.write("")
            if st.button("שלח טקסט"):
                if user_text_to_type:
                    try:
                        urllib.request.urlopen(urllib.request.Request(
                            f"{input_url}/type_text", 
                            data=json.dumps({"text": user_text_to_type}).encode(), 
                            headers={'Content-Type': 'application/json'}
                        ))
                        st.toast("הטקסט נשלח בהצלחה!")
                    except Exception as e:
                        st.error(f"שגיאה: {e}")

        # כפתורי אבטחה למערכת (כיבוי / הפעלה מחדש)
        with st.expander("⚙️ אפשרויות מתקדמות למערכת (כיבוי ואתחול)"):
            s_col1, s_col2 = st.columns(2)
            with s_col1:
                if st.button("🔄 הפעל מחדש את המחשב"):
                    urllib.request.urlopen(urllib.request.Request(f"{input_url}/system_command", data=json.dumps({"cmd": "restart"}).encode(), headers={'Content-Type': 'application/json'}))
                    st.warning("פקודת הפעלה מחדש נשלחה למחשב!")
            with s_col2:
                if st.button("🔴 כבה את המחשב"):
                    urllib.request.urlopen(urllib.request.Request(f"{input_url}/system_command", data=json.dumps({"cmd": "shutdown"}).encode(), headers={'Content-Type': 'application/json'}))
                    st.error("פקודת כיבוי נשלחה למחשב!")

        # הצגת הסטרים עם אפשרות מסך מלא וקליק שמאלי/ימני דינמי
        current_btn_type = st.session_state.mouse_mode
        components.html(f"""
            <div style="display: flex; flex-direction: column; align-items: center; background-color: #000; padding: 10px; border-radius: 8px;">
                <div style="width: 100%; text-align: left; margin-bottom: 5px;">
                    <button onclick="
                        var img = document.getElementById('streamImg');
                        if (img.requestFullscreen) {{ img.requestFullscreen(); }}
                        else if (img.webkitRequestFullscreen) {{ img.webkitRequestFullscreen(); }}
                    " style="background: #333; color: #fff; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">⛶ מסך מלא</button>
                </div>
                <img id="streamImg" src="{stream_url}" style="width: 100%; max-width: 1200px; height: auto; border-radius: 4px; cursor: crosshair;" 
                     onclick="
                        let rect = this.getBoundingClientRect();
                        let x = Math.round((event.clientX - rect.left) * (this.naturalWidth / rect.width));
                        let y = Math.round((event.clientY - rect.top) * (this.naturalHeight / rect.height));
                        fetch('{input_url}/click?x=' + x + '&y=' + y + '&btn={current_btn_type}', {{method: 'GET', mode: 'no-cors'}});
                     "
                     onerror="setTimeout(() => {{ this.src = '{stream_url}?t=' + Date.now(); }}, 1000);" />
            </div>
        """, height=700)

else:
    st.info("לחץ על **'התחל שידור'** בסיידבר (הכתובות יטענו אוטומטית מהענן).")
