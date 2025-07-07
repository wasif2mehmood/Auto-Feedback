import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

class LLMClient:
    """Handles communication with LLM services"""
    
    def __init__(self, model="gpt-4o-mini"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
    
    def get_feedback(self, prompt):
        """Get feedback from GPT model"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant providing constructive feedback on technical work."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating feedback: {str(e)}"