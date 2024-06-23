import pyttsx3


def speak_text(text):
    # 初始化pyttsx3引擎
    engine = pyttsx3.init()

    # 设置语速 (可选)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 200)  # 调整语速为150字/分钟

    # 设置音量 (可选)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 1.0)  # 调整音量为最大值

    # 设置声音类型 (可选)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # 选择不同的声音（例如，voices[1]为女性声音）

    # 朗读文字
    engine.say(text)

    # 等待朗读完成
    engine.runAndWait()


def read_and_speak(file_path):
    # 初始化pyttsx3引擎
    engine = pyttsx3.init()

    # 设置语速 (可选)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 150)  # 调整语速为150字/分钟

    # 设置音量 (可选)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 1.0)  # 调整音量为最大值

    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 朗读文字
    engine.say(text)

    # 等待朗读完成
    engine.runAndWait()


def main():
    # 使用函数朗读文字
    text_to_read = "你好，这是一个文本到语音的示例。"
    speak_text(text_to_read)

    # file_path = "output.txt"
    # # 朗读文件内容
    # read_and_speak(file_path)

if __name__ == "__main__":
    main()