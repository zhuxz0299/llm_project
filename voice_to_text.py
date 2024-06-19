import speech_recognition as sr

def recognize_speech_from_mic():
    # 初始化识别器
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("请开始说话...")
        audio = recognizer.listen(source)

    try:
        print("正在识别...")
        text = recognizer.recognize_google(audio, language='zh-CN')  # 选择适当的语言代码
        return text
    except sr.UnknownValueError:
        return "无法识别语音"
    except sr.RequestError:
        return "无法连接到语音识别服务"
    
def main():
    text = recognize_speech_from_mic()
    print(text)

if __name__ == "__main__":
    main()