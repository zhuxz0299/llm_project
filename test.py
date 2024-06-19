import ollama
from text_to_voice import speak_text
from voice_to_text import recognize_speech_from_mic
import re

def clean_markdown(text):
    # 去掉Markdown格式符号
    clean_text = re.sub(r'[*_~`]', '', text)  # 去掉*、_、~、`符号
    clean_text = re.sub(r'\[.*?\]\(.*?\)', '', clean_text)  # 去掉链接
    clean_text = re.sub(r'!\[.*?\]\(.*?\)', '', clean_text)  # 去掉图片链接
    # 去掉表情符号
    clean_text = re.sub(r'[^\w\s,.!?]', '', clean_text)
    return clean_text

def chat_with_llm():
    while True:
        user_input = recognize_speech_from_mic()
        print(user_input)

        if user_input in ['退出', '再见']:
            break

        stream = ollama.chat(
            model='llama3:8b',
            messages=[{'role': 'user', 'content': user_input}],
            stream=True,
        )

        buffer = ''
        # 逐步接收和处理响应数据块
        for chunk in stream:
            text = chunk['message']['content']
            text = clean_markdown(text)
            buffer += text
            print(text, end='', flush=True)
            
            # 如果缓冲区中有完整的句子，则朗读它们
            sentences = re.split(r'([.!?])', buffer)
            
            # sentences[-1] 是不完整的句子部分，因此不朗读它
            for i in range(0, len(sentences) - 1, 2):
                complete_sentence = sentences[i] + sentences[i + 1]
                speak_text(complete_sentence)
            
            # 更新缓冲区，只保留不完整的句子部分
            buffer = sentences[-1]

if __name__ == "__main__":
    chat_with_llm()