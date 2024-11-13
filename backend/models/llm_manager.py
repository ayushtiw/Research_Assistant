import ollama
from typing import List
from .logger import setup_logger

class LLMManager:
    def __init__(self, model_name: str = "mistral:latest"):
        self.model_name = model_name
        self.logger = setup_logger(__name__)
        self.logger.info(f"Initialized LLMManager with model: {model_name}")

    async def generate_response(self, prompt: str) -> str:
        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            if 'response' in response:
                self.logger.info(f"Successfully generated response for prompt: {prompt[:50]}...")
                return response['response']
            else:
                self.logger.error(f"Response key not found in the output: {response}")
                return ""
        except Exception as e:
            self.logger.error(f"Error generating response for prompt '{prompt[:50]}...': {e}")
            return ""

    async def batch_generate(self, prompts: List[str]) -> List[str]:
        responses = []
        for prompt in prompts:
            response = await self.generate_response(prompt)
            responses.append(response)
            self.logger.info(f"Generated response for batch prompt: {prompt[:50]}...")
        self.logger.info("Completed batch generation.")
        return responses
