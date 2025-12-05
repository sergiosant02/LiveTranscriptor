from faster_whisper import WhisperModel
import torch

class ModelProvider:
    
    @staticmethod
    def get_available_models():
        return ["large-v1", "large-v2", "large-v3", "large", "distil-large-v2", "distil-large-v3", "large-v3-turbo", "turbo"]
    
    @staticmethod
    def is_best_device():
        return "cuda" if torch.cuda.is_available() else "cpu"
    
    @staticmethod
    def get_whisper_model(name: str):
        device = ModelProvider.is_best_device()
        return (WhisperModel(name, device), device)