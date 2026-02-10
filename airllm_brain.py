import os
import sys
import threading
import time

class AirLLMBrain:
    """
    Bankoo AirLLM Bridge.
    Enables layer-wise inference for massive models on local hardware.
    """
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.is_loading = False
        self.current_model_path = None
        self._lock = threading.Lock()

    def initialize_model(self, model_id="unsloth/Llama-3-70B-Instruct-bnb-4bit"):
        """
        Initializes AirLLM with the specified model.
        This will download sharded layers if not present.
        """
        try:
            from airllm import AirLLMLlama
            
            print(f"🧬 [AirLLM] Initializing Layer-wise Engine for: {model_id}")
            self.is_loading = True
            
            # Note: AirLLM handles the sharding and memory management
            self.model = AirLLMLlama(model_id)
            self.current_model_path = model_id
            self.is_loading = False
            
            return True
        except ImportError:
            print("❌ [AirLLM] Library 'airllm' not found. Please install it.")
            return False
        except Exception as e:
            print(f"❌ [AirLLM] Initialization Error: {e}")
            self.is_loading = False
            return False

    def ask(self, prompt, max_new_tokens=128):
        """
        Runs inference across model layers. 
        Note: This is slow but memory-efficient.
        """
        if not self.model:
            return "AirLLM Engine is not initialized. Please load a model first."

        try:
            print(f"🧠 [AirLLM] Streaming Inference across layers...")
            input_tokens = self.model.tokenizer(
                [prompt], 
                return_tensors="pt", 
                return_attention_mask=False
            ).input_ids.cuda()

            # AirLLM inference loop
            output = self.model.generate(
                input_tokens, 
                max_new_tokens=max_new_tokens,
                use_cache=True,
                return_dict_in_generate=True
            )
            
            response = self.model.tokenizer.decode(output.sequences[0], skip_special_tokens=True)
            return response
        except Exception as e:
            return f"Inference Error: {e}"

# Singleton instance
air_brain = AirLLMBrain()
