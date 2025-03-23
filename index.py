import nltk
from nltk.chat.util import Chat, reflections

# Baixar recursos necessários do NLTK
nltk.download('punkt')

# Definindo os pares de perguntas e respostas
pares = [
    (r"oi|olá|oii", ["Olá, como posso te ajudar hoje?", "Oi! Em que posso te ajudar?"]),
    (r"como você está?", ["Estou bem, obrigado! E você?", "Estou ótimo! Como você está?"]),
    (r"qual é o sato)", ["De nada!", "Fico feliz em ajudar!"]),
    (r"(tchau|até logo|bye)eu nome?", ["Eu sou um chatbot simples, criado para te ajudar.", "Meu nome é ChatBot!"]),
    (r"(obrigado|valeu|gr", ["Tchau! Até mais!", "Foi bom falar com você!"]),
    (r"(.*)", ["Desculpe, não entendi. Pode reformular sua pergunta?"]),
]

# Criando o chatbot com os padrões definidos
chatbot = Chat(pares, reflections)

# Função para iniciar a conversa
def conversar():
    print("Oi! Eu sou um chatbot. Como posso te ajudar? (Digite 'tchau' para sair)")
    while True:
        # Recebendo a entrada do usuário
        entrada_usuario = input("Você: ")

        # Se o usuário digitar 'tchau', o bot encerra
        if entrada_usuario.lower() in ["tchau", "até logo", "bye"]:
            print("ChatBot: Até logo! Fique bem!")
            break

        # Obtendo a resposta do chatbot
        resposta = chatbot.respond(entrada_usuario)

        # Caso não haja uma resposta definida, o bot avisa que não entendeu
        if resposta:
            print(f"ChatBot: {resposta}")
        else:
            print("ChatBot: Desculpe, não entendi. Pode reformular sua pergunta?")

# Iniciar a conversa
conversar()

