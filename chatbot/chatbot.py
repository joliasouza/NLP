import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def chatbot_gpt(prompt):
    resposta = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": prompt}]
    )

    return resposta.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        input_usuario = input("Você: ")

        resposta = chatbot_gpt(input_usuario)
        print("Chatbot: ", resposta)
