import os
import openai
from dotenv import load_dotenv

def useGPT(content) :

    # .env 파일 활성화
    load_dotenv()

    # OpenAI API 키 설정
    openai.api_key = os.getenv('OPENAI_API_KEY')


    # ChatGPT 모델에 요청 보내기
    response = openai.ChatCompletion.create(
        model="gpt-4", # 사용할 모델 선택
        messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": content}
            ],
        max_tokens=500,  # 필요한 토큰 수에 따라 조정
        temperature=0.7,  # 창의적인 응답을 위한 온도 설정
        
    )

    # 응답 출력
    print(response)
    print(response['choices'][0]['message']['content'])

    return response['choices'][0]['message']['content']

