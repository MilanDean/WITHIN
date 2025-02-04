import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class LLMRouteSummarizer:
    def __init__(self, model_name="Qwen/Qwen2.5-3B-Instruct"):
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
        elif torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")
        print(f"Using device: {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
        self.model = self.model.to(self.device)

    def summarize_route(self, route_description: str) -> str:
        input_text = "summarize: " + route_description
        # Tokenize the input and move it to MPS or GPU.
        input_ids = self.tokenizer.encode(
            input_text, return_tensors="pt", max_length=512, truncation=True
        ).to(self.device)

        if self.device.type == "mps":
            print("MPS detected: Forcing generation on CPU as a workaround for unsupported ops.")
            self.model = self.model.to("cpu")
            summary_ids = self.model.generate(
                input_ids.to("cpu"),
                max_length=150,
                min_length=40,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True
            )
            self.model = self.model.to(self.device)
        else:
            summary_ids = self.model.generate(
                input_ids,
                max_length=150,
                min_length=40,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True
            )

        # Decode and return the summary.
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary