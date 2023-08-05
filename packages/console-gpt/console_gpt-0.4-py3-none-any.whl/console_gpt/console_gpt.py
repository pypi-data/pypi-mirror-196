__Author__ = "Pranav Chandran"
__Date__ = "08/03/2023"
__FileName__ = "main.py"

"""
This is the code for connecting to ChatbotGPT and getting the response
Set up your OpenAI API credentials: To use the ChatGPT API, you will need 
to set up your OpenAI API credentials.
"""
import openai


class ChatbotGPT:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    @staticmethod
    def get_response(prompt):
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.5,
        )
        text = response.choices[0].text.strip()
        return text.replace('\\n', '\n')

    def ask(self):
        #  ask the user to give input
        prompt = input("You: ")
        return self.get_response(prompt)


if __name__ == "__main__":
    # Set up your OpenAI API credentials
    key = "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"
    chatbot = ChatbotGPT(key)
    while True:
        print("Chatbot: ", chatbot.ask())




