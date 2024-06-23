from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time

device = "cuda" if torch.cuda.is_available() else "cpu"

def gpu_memory_usage():
    if device == "cuda":
        print("Initial memory allocated:", torch.cuda.memory_allocated() / 1024 ** 2, "MB")
        # print("Initial memory reserved:", torch.cuda.memory_reserved() / 1024 ** 2, "MB")

def speculatively_decode():
    # 模型路径
    tinyllama_model_dir = "./tinyllama"
    litellama_model_dir = "./litellama"

    # 加载 tokenizer
    tokenizer = AutoTokenizer.from_pretrained(tinyllama_model_dir)

    # 准备输入
    prompt = "What is the tallest mountain in the world?"
    formatted_prompt = f"### Human: {prompt}### Assistant:"
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(device)

    # 检查 input_ids 是否在词汇表范围内
    vocab_size = tokenizer.vocab_size
    input_ids = inputs['input_ids']
    if torch.max(input_ids) >= vocab_size:
        raise ValueError("Input contains token id out of vocabulary range.")

    # 加载大模型 TinyLlama
    model = AutoModelForCausalLM.from_pretrained(tinyllama_model_dir).to(device)
    print("Large model loaded")
    model.config.use_cache = True

    # 加载小模型 LiteLlama
    assistant_model = AutoModelForCausalLM.from_pretrained(litellama_model_dir).to(device)
    assistant_model.config.use_cache = True
    print("Small model loaded")

    # # 原生解码
    # print("###Native Decoding Starts...\n")
    # start = time.time()
    # outputs = model.generate(**inputs, max_new_tokens=64)  # 减少 max_new_tokens 以减少显存占用
    # end = time.time()
    # print(tokenizer.batch_decode(outputs, skip_special_tokens=True))
    # print("Time: ", end - start)

    # 辅助解码
    print("###TinyLlama Assisted Decoding Starts...\n")
    start = time.time()
    outputs = model.generate(**inputs, assistant_model=assistant_model, max_new_tokens=64)  # 减少 max_new_tokens 以减少显存占用
    end = time.time()
    print(tokenizer.batch_decode(outputs, skip_special_tokens=True))
    print("Time: ", end - start)

    gpu_memory_usage()

def only_tinyllama():
    # 模型路径
    tinyllama_model_dir = "./tinyllama"

    # 加载 tokenizer
    tokenizer = AutoTokenizer.from_pretrained(tinyllama_model_dir)

    # 准备输入
    prompt = "What is the tallest mountain in the world?"
    formatted_prompt = f"### Human: {prompt}### Assistant:"
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(device)

    # 检查 input_ids 是否在词汇表范围内
    vocab_size = tokenizer.vocab_size
    input_ids = inputs['input_ids']
    if torch.max(input_ids) >= vocab_size:
        raise ValueError("Input contains token id out of vocabulary range.")

    # 加载大模型 TinyLlama
    model = AutoModelForCausalLM.from_pretrained(tinyllama_model_dir).to(device)
    print("Large model loaded")
    model.config.use_cache = True

    # 原生解码
    print("###Native Decoding Starts...\n")
    start = time.time()
    outputs = model.generate(**inputs, max_new_tokens=64)  # 减少 max_new_tokens 以减少显存占用
    end = time.time()
    print(tokenizer.batch_decode(outputs, skip_special_tokens=True))
    print("Time: ", end - start)

    gpu_memory_usage()


if __name__ == "__main__":
    speculatively_decode()
    # only_tinyllama()