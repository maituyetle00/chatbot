import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs

# Hàm trích xuất ID từ URL YouTube
def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    elif 'youtube.com' in parsed_url.hostname:
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    return None

# Hàm lấy transcript từ video ID
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['vi', 'en'])
        text = " ".join([item['text'] for item in transcript])
        return text
    except TranscriptsDisabled:
        return "Video này đã tắt chức năng transcript."
    except NoTranscriptFound:
        return "Không tìm thấy transcript cho video này."
    except Exception as e:
        return f"Lỗi: {str(e)}"

# Giao diện Streamlit
st.title("🎥 Chuyển video YouTube sang văn bản")

url = st.text_input("Nhập URL video YouTube:")

if url:
    video_id = extract_video_id(url)
    if video_id:
        with st.spinner("Đang xử lý..."):
            transcript = get_transcript(video_id)
        st.subheader("📄 Nội dung văn bản:")
        st.write(transcript)
    else:
        st.error("URL không hợp lệ!")