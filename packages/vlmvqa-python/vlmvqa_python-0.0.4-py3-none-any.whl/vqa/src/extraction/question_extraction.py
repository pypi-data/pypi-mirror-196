import torch
import numpy as np
from transformers import MT5EncoderModel, T5Tokenizer

class QuestionExtraction():
    def __init__(self) -> None: 
        self.mt5_model = MT5EncoderModel.from_pretrained("google/mt5-base")
        self.tokenizer = T5Tokenizer.from_pretrained("google/mt5-base")

    def question_extraction(self, sentence):
        max_len = 60
        input_ids = self.tokenizer.encode(sentence, add_special_tokens=True)
        padded = np.array([input_ids + [1] * (max_len - len(input_ids))])
        attention_mask = np.where(padded == 1, 0, 1)
        padded = torch.tensor(padded).to(torch.long)
        attention_mask = torch.tensor(attention_mask)
        last_hidden_states = self.mt5_model(input_ids= padded, attention_mask=attention_mask)
        
        v_features = last_hidden_states[0].detach().numpy()[0]
        return v_features
