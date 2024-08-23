import os
import openai
from dotenv import load_dotenv

def useGPT() :

    # .env 파일 활성화
    load_dotenv()

    # OpenAI API 키 설정
    openai.api_key = os.getenv('OPENAI_API_KEY')


    # ChatGPT 모델에 요청 보내기
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 사용할 모델 선택
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
    )

    # 응답 출력
    print(response)
    print(response['choices'][0]['message']['content'])

