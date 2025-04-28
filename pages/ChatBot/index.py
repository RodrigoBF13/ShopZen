import random
import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

nltk.download('punkt')

# Carrega os dados da planilha
df = pd.read_csv("FRUTAS.csv")

# Define funções auxiliares
def produto_mais_barato():
    item = df.loc[df["Preço"].idxmin()]
    return f"O item mais barato é {item['Produto']} por R${item['Preço']}."

def produto_mais_caro():
    item = df.loc[df["Preço"].idxmax()]
    return f"O item mais caro é {item['Produto']} por R${item['Preço']}."

def listar_produtos():
    return "\n".join([f"{row['Produto']}: R${row['Preço']}" for _, row in df.iterrows()])

def listar_promocoes():
    # Suponha que você tenha uma coluna "Desconto" ou similar para promoções
    return "\n".join([f"{row['Preço']} com desconto de R${row['Preço']}!" for _, row in df[df["Preço"] > 0].iterrows()])

# Dados de treinamento (frases exemplo baseadas nos dados do Excel)
dados = {
    "Produto": [
        'quais sao os produtos?',
        'o que voces vendem?',
        'quais produtos tem?',
        'mostrar os produtos',
        'me fale sobre os produtos disponíveis'
    ],
    "Promocoes": [
        'quais sao as promocoes?',
        'tem descontos?',
        'o que é mais barato?',
        'o que é mais caro?',
        'mostrar as promoções',
        'produtos com desconto'
    ],
    "Atendente": [
        'quero falar com alguem',
        'quero falar com o atendente',
        'quero ir para o atendente'
    ],
    "Encerrar": [
        'adeus',
        'tchau',
        'encerrar',
        'bye'
    ]
}

# Treinamento
frases = []
tags = []

for tag, frases_exemplo in dados.items():
    for frase in frases_exemplo:
        frases.append(frase)
        tags.append(tag)

vectorizer = TfidfVectorizer()  # Usar TfidfVectorizer para melhorar as predições
X = vectorizer.fit_transform(frases)
Y = tags

modelo = MultinomialNB()
modelo.fit(X, Y)

# Funções de resposta do chatbot baseadas em dados do Excel
def responder_produto():
    return listar_produtos()

def responder_promocao():
    return listar_promocoes()

def responder_atendente():
    return "Olá! Eu sou Willy, atendente virtual da Shopzen. Como posso te ajudar hoje?"

def chatbot_npl():
    print("Bem-vindo(a) ao chatbot da Shopzen!")
    while True:
        entrada = input("Você: ").lower()

        # Encerra a conversa
        if entrada in ["adeus", "encerrar", "tchau", "bye"]:
            print("Bot: Foi um prazer falar contigo! Até logo!")
            break

        # Respostas baseadas no conteúdo do Excel
        if "mais barato" in entrada:
            print("Bot:", produto_mais_barato())
            continue
        elif "mais caro" in entrada:
            print("Bot:", produto_mais_caro())
            continue
        elif "produtos" in entrada or "mostrar produtos" in entrada:
            print("Bot:", responder_produto())
            continue
        elif "promocoes" in entrada or "desconto" in entrada:
            print("Bot:", responder_promocao())
            continue

        # Previsão baseada no modelo
        entrada_vect = vectorizer.transform([entrada])
        tag_prevista = modelo.predict(entrada_vect)[0]

        if tag_prevista == "Atendente":
            print("Bot:", responder_atendente())
        elif tag_prevista == "Encerrar":
            print("Bot: Foi um prazer falar contigo! Até logo!")
            break
        else:
            print("Bot: Desculpe, não entendi. Poderia reformular?")

# Executa o chatbot
chatbot_npl()
