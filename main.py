import streamlit as st
from PIL import Image
import pandas as pd
import tempfile
import os
import io
import time
import datetime

# 데이터 저장 함수
def save_data(new_data):
    try:
        existing_data = pd.read_excel("survey_new3.xlsx")
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    except FileNotFoundError:
        updated_data = new_data

    updated_data.to_excel("survey_new3.xlsx", index=False)
    st.success("설문 응답이 저장되었습니다. 참여 감사드립니다!!!")

# 엑셀 파일 다운로드를 위한 함수
def download_excel():
    filename = 'survey_new3.xlsx'
    with open(filename, "rb") as file:
        btn = st.download_button(
                label="설문 결과 다운로드",
                data=file,
                file_name=filename,
                mime="application/vnd.ms-excel"
            )

admin_key = os.getenv('ADMIN')

def app():

    image = Image.open('survey01.png')
    image = image.resize((130, 130))
    st.image(image)
    st.write(":parachute: 느낀점을 솔직히 써주세요!:yum:")
    
    # 사용자 입력 양식
    with st.form(key='survey_form'):
        satisfaction = st.slider(":one: 답변만족도 점수는? (10만족, 5보통)", 0, 10, 7)
        st.write("")
        positive_feedback = st.text_area(":two: 어떤 점이 마음에 들었죠?")
        st.write("")
        improvement_feedback = st.text_area(":three: 어떤 점을 개선하면 좋을까요?")
        st.write("")
        st.write(":smile::smile::smile:아래 '저장하기' 클릭!")
        submit_button = st.form_submit_button(label='저장하기')

        # 제출 버튼이 눌렸을 때의 처리
        if submit_button:
            current_time = datetime.datetime.now() 
            new_data = pd.DataFrame({
                "만족도": [satisfaction],
                "좋았던 점": [positive_feedback],
                "개선하고 싶은 점": [improvement_feedback],
                "응답 시간": [current_time] 
            })
            # 파일에 데이터 저장
            save_data(new_data)        

    # 엑셀 다운로드
    password = st.text_input(":lock: 관리자", type="password")
    if password:
        if password == admin_key:
            # 비밀번호가 맞으면 다운로드 버튼 표시
            st.success("비밀번호 확인 완료")
            download_excel()
        else:
            st.error("에러")

if __name__ == "__main__":
    app()
