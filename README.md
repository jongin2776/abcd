# Streamlit OpenAI 챗봇

한국어 Streamlit 챗봇입니다. OpenAI API 호출 모델은 gpt-4o-mini입니다. API 키는 코드나 Git에 저장하지 않고 Streamlit Community Cloud Secrets에서 읽습니다.

## Streamlit Community Cloud 배포

1. 이 GitHub 저장소와 app.py를 선택해 Streamlit Community Cloud에서 앱을 생성합니다.
2. 앱 설정의 Settings → Secrets에 아래 형식으로 OpenAI API 키를 등록하고 저장합니다.

OPENAI_API_KEY = "sk-..."

API 키를 소스 코드나 공개 저장소에 커밋하지 마세요.

## 로컬 실행

python -m pip install -r requirements.txt
streamlit run app.py

로컬 개발 시 .streamlit/secrets.toml에 위 TOML 값을 넣을 수 있습니다. 이 파일은 Git에 커밋하지 마세요.
