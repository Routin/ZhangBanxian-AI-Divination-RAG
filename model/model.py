from typing import Any
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

device = "cuda"  # the device to load the model onto

class LLM():
    def __init__(self, use_quantization: bool = False) -> None:
        self.system_prompt = '''
        你是一个会解卦的半仙，你姓张，人送外号阴阳先生张半仙。
        你能通过别人给出的问题和卦象进行解卦，为人排忧解难。
        在提供解卦的时候，请你先把卦象变卦等原始信息列出，再进行解卦，因为用户并不知道所提供的卦象信息。
        你会分析用户提供给你的卦象，尤其重点分析其中的动爻来解答用户让你解卦的问题。
        你说话的时候语气比较古风虚玄，经常喜欢用比较文言和每句七个字的诗文来表达你的观点。
        '''
        self.history = [{"role": "system", "content": self.system_prompt}]
        
        self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-7B-Instruct")

        if use_quantization:
            self.model = AutoModelForCausalLM.from_pretrained(
                "Qwen/Qwen2-7B-Instruct",
                torch_dtype=torch.float16,
                device_map="auto",
                load_in_8bit=True  # Use 8-bit quantization provided by bitsandbytes
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                "Qwen/Qwen2-7B-Instruct",
                torch_dtype="auto",
                device_map="auto"
            )
    
    def clean_history(self):
        self.history = [{"role": "system", "content": self.system_prompt}]
    
    def assemble_messages(self, user_content):
        messages = self.history
        messages.append({"role": "user", "content": user_content})
        self.history = messages
        return messages
    
    def __call__(self, inputs) -> Any:
        messages = self.assemble_messages(inputs)
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(device)

        generated_ids = self.model.generate(
            model_inputs.input_ids,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        self.history.append({"role": "assistant", "content": response})
        return response

