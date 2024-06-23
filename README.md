### Install Python Environment
Run the following command in the terminal:

```bash
conda env create -f environment.yaml
```

### Large Language Model Interaction
Voice Interaction Mode:

```bash
python run_llm.py
```

Text Interaction Mode:

```bash
python run_llm_text.py
```
In both modes, you can choose different models for interaction by modifying the model parameter in:

```python
stream = ollama.chat(
    model='tinyllama',
    messages=[{'role': 'user', 'content': translated_input}],
    stream=True,
)
```
Simply change model to the desired model name. Note that if the selected model is available in ollama, it will be downloaded automatically. However, if you wish to use your own model, you need to quantize it using ollama and place it in the local ollama model storage path.

### Speculative Decoding for Model Acceleration
```bash
python decoding.py
```
Before running the code, download the required model from Huggingface to a local folder and change the model path to the local path.