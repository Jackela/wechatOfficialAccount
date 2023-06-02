import openai
import time

openai.api_key = "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"


class OpenAIChatbot:
    def __init__(self, model_engine="text-davinci-002", max_tokens=50):
        self.model_engine = model_engine
        self.max_tokens = max_tokens

    def generate_response(self, message):
        prompt_text = f"Conversation with OpenAI Chatbot:\nUser: {message}\nAI:"

        response = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt_text,
            max_tokens=self.max_tokens,
            n=1,
            stop=None,
            temperature=0.5,
            headers={'Content-Type': 'application/json'}
        )

        return response.choices[0].text.strip()

if __name__ == "__main__":
    text = b'Hello, how are you?'
    bot = OpenAIChatbot()
    print(bot.generate_response(text.decode("utf-8")))
