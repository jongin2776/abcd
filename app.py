import streamlit as st
from openai import OpenAI, APIConnectionError, APIStatusError, RateLimitError, AuthenticationError

MODEL = "gpt-4o-mini"
st.set_page_config(page_title="AI 챗봇", page_icon="💬", layout="centered", initial_sidebar_state="expanded")

st.markdown("""
<style>
.block-container { max-width: 900px; padding-top: 2.2rem; padding-bottom: 3rem; }
[data-testid="stChatMessage"] { border-radius: 16px; }
.hero { padding: 1.3rem 1.5rem; border-radius: 20px; margin-bottom: 1.4rem; background: linear-gradient(120deg, rgba(99,102,241,.12), rgba(14,165,233,.10)); border: 1px solid rgba(99,102,241,.15); }
.hero p { color: #64748b; margin: .35rem 0 0; }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("💬 AI 챗봇")
    st.caption(f"사용 모델 · {MODEL}")
    st.divider()
    system_prompt = st.text_area("챗봇 지침", value="당신은 친절하고 정확한 한국어 AI 어시스턴트입니다. 사용자의 질문에 명확하고 도움이 되도록 답변하세요.", height=150, help="대화 전체에 적용할 기본 역할과 답변 방식을 설정합니다.")
    if st.button("대화 지우기", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("API 키는 Streamlit Community Cloud의 Secrets에서 관리합니다.")

st.markdown("""
<div class="hero">
<h1 style="margin:0">무엇이든 물어보세요 👋</h1>
<p>OpenAI와 대화하며 아이디어를 정리하고 궁금한 점을 해결해 보세요.</p>
</div>
""", unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

try:
    api_key = st.secrets.get("OPENAI_API_KEY", "")
except (FileNotFoundError, RuntimeError):
    api_key = ""

if not api_key:
    st.info("시작하려면 Streamlit Community Cloud 앱의 Settings → Secrets에 OPENAI_API_KEY = sk-... 형식으로 API 키를 등록해 주세요.")

if prompt := st.chat_input("메시지를 입력하세요..."):
    if not api_key:
        st.warning("먼저 Community Cloud Secrets에 OpenAI API 키를 등록해 주세요.")
        st.stop()
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response_area = st.empty()
        try:
            client = OpenAI(api_key=api_key)
            stream = client.chat.completions.create(model=MODEL, messages=[{"role": "system", "content": system_prompt}, *st.session_state.messages], stream=True)
            answer = ""
            for chunk in stream:
                text = chunk.choices[0].delta.content
                if text:
                    answer += text
                    response_area.markdown(answer + "▌")
            response_area.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except AuthenticationError:
            st.error("API 키가 올바르지 않습니다. Community Cloud Secrets의 OPENAI_API_KEY 값을 확인해 주세요.")
        except RateLimitError:
            st.error("API 사용 한도에 도달했거나 요청이 너무 많습니다. 잠시 후 다시 시도해 주세요.")
        except APIConnectionError:
            st.error("OpenAI API에 연결하지 못했습니다. 네트워크 상태를 확인한 뒤 다시 시도해 주세요.")
        except APIStatusError as exc:
            st.error(f"OpenAI API 오류가 발생했습니다 (HTTP {exc.status_code}). 잠시 후 다시 시도해 주세요.")
        except Exception:
            st.error("응답을 가져오지 못했습니다. 설정과 연결 상태를 확인한 뒤 다시 시도해 주세요.")
