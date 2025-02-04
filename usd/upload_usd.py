import streamlit as st
import docker
import os

# Nucleus 서버 정보
NUCLEUS_HOST = "20.*.*.*"
NUCLEUS_PORT = "3009"
NUCLEUS_USER = "omniverse"
NUCLEUS_PASSWORD = "****"

# Docker 클라이언트 설정
client = docker.from_env()

def upload_usd(file_path, destination_path):
    # Nucleus 도구 이미지
    image_name = "nvcr.io/nvidia/omniverse/nucleus-tools:1.2.2"
    
    # 파일 경로와 목적지 경로 설정
    mount_path = os.path.abspath("temp_upload")
    os.makedirs(mount_path, exist_ok=True)
    
    # Docker 컨테이너 실행
    try:
        container = client.containers.run(
            image=image_name,
            command=f"upload /files/ {NUCLEUS_HOST} {destination_path} -u {NUCLEUS_USER} -p {NUCLEUS_PASSWORD}",
            volumes={mount_path: {'bind': '/files', 'mode': 'rw'}},
            environment=["ACCEPT_EULA=Y"],
            detach=True
        )
        
        # 컨테이너 로그 확인
        for line in container.logs(stream=True):
            st.text(line.strip().decode())
        
        container.stop()
        container.remove()
        st.success("파일 업로드가 완료되었습니다.")
    except Exception as e:
        st.error(f"업로드 중 오류가 발생했습니다: {e}")

def main():
    st.title("Nucleus 서버로 USD 파일 업로드")
    
    # 파일 업로드
    uploaded_file = st.file_uploader("업로드할 USD 파일 선택", type=["usd", "usda", "usdc"])
    
    if uploaded_file is not None:
        with open(f"./temp_upload/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        destination_path = st.text_input("업로드할 Nucleus 서버의 목적지 경로", "/Projects/TEST_project_rename")
        
        if st.button("업로드 시작"):
            if destination_path:
                upload_usd(f"./temp_upload/{uploaded_file.name}", destination_path)
            else:
                st.warning("목적지 경로를 입력해주세요.")

if __name__ == "__main__":
    main()
