from deep_translator import GoogleTranslator
import ollama
import re


def split_sentences(text):
    # 使用正则表达式按照句子结束符分割文本
    sentences = re.split(r'(?<=[.!?]) +', text)
    return sentences

def translate_and_print(text):
    translated_text = GoogleTranslator(source='auto', target='zh-CN').translate(text)
    print(translated_text)

def chat_with_llm():
    while True:
        user_input = input('>>>')

        if user_input in ['退出', '再见']:
            break

        # 将用户输入的中文翻译成英文
        translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)

        # 发送翻译后的英文输入给模型
        stream = ollama.chat(
            model='tinyllama',
            messages=[{'role': 'user', 'content': translated_input}],
            stream=True,
        )

        sentence_buffer = ""
        # 逐步接收和处理响应数据块
        for chunk in stream:
            text = chunk['message']['content']
            sentence_buffer += text
            
            # 检查是否形成了完整的句子
            sentences = split_sentences(sentence_buffer)
            for sentence in sentences[:-1]:
                translate_and_print(sentence)
            
            # 保留最后一个可能不完整的句子
            sentence_buffer = sentences[-1]

        # 处理剩余的句子
        if sentence_buffer:
            translate_and_print(sentence_buffer)



if __name__ == "__main__":
    chat_with_llm()