import asyncio
from Backend.models.llm_manager import LLMManager  # Adjust import as per your directory

async def main():
    llm_manager = LLMManager(model_name="mistral:latest")
    
    # Test generate_response
    print("Testing generate_response...")
    response = await llm_manager.generate_response("What is AI?")
    print("Response:", response)

    # Test batch_generate
    print("\nTesting batch_generate...")
    prompts = ["Define machine learning.", "Explain neural networks.", "What is deep learning?"]
    batch_responses = await llm_manager.batch_generate(prompts)
    for i, res in enumerate(batch_responses):
        print(f"Response {i+1}:", res)

# Run the async main function
asyncio.run(main())
