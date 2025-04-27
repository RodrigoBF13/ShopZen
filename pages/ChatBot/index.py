import random
import nltk
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

nltk.download('punkt')

# Carrega os dados da planilha
df = pd.read_excel("Planilha sem título - Página1.csv")

# Define funções auxiliares
def produto_mais_barato():
    item = df.loc[df["Preço"].idxmin()]
    return f"O item mais barato é {item['Produto']} por R${item['Preço']}."

def produto_mais_caro():
    item = df.loc[df["Preço"].idxmax()]
    return f"O item mais caro é {item['Produto']} por R${item['Preço']}."

def listar_produtos():
    return "\n".join([f"{row['Produto']}: R${row['Preço']}" for _, row in df.iterrows()])

# Dados de treinamento
dados = {
    "Produto": [
        'quais sao os produtos?',
        'o que voces vendem?',
        'o que voces possuem?',
        'mostrar produtos'
    ],
    "Promocoes": [
        'quais sao as promocoes?',
        'o que é mais barato?',
        'o que é mais caro?',
        'mostrar descontos'
    ],
    "Atendente": [
        'quero falar com alguem',
        'quero ir para o atendente'
    ],
    "Encerrar": [
        'adeus',
        'encerrar',
        'tchau',
        'bye'
    ]
}

respostas = {
    "Produto": "Temos: Whey protein, Creatina, Aveia em Flocos, Castanhas",
    "Promocoes": "Promoções: Whey R$55, Creatina R$35, Aveia R$12, Castanhas R$50.",
    "Atendente": "Olá! Me chamo Willy, sou atendente da Shopzen. Como posso ajudar?",
    "Encerrar": "Encerrando o programa. Até logo!"
}

# Treinamento
frases = []
tags = []

for tag, frases_exemplo in dados.items():
    for frase in frases_exemplo:
        frases.append(frase)
        tags.append(tag)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(frases)
Y = tags

modelo = MultinomialNB()
modelo.fit(X, Y)

# Função principal do chatbot
def chatbot_npl():
    print("bem-vindo(a) ao chatbot da Shopzen")
    while True:
        entrada = input("Você: ").lower()
        if entrada in ["adeus", "encerrar", "tchau", "bye"]:
            print("Bot:", respostas["Encerrar"])
            break

        # Respostas manuais com palavras-chave
        if "mais barato" in entrada:
            print("Bot:", produto_mais_barato())
            continue
        elif "mais caro" in entrada:
            print("Bot:", produto_mais_caro())
            continue
        elif "produtos" in entrada or "mostrar produtos" in entrada:
            print("Bot:", listar_produtos())
            continue

        entrada_vect = vectorizer.transform([entrada])
        tag_prevista = modelo.predict(entrada_vect)[0]
        print("Bot:", respostas.get(tag_prevista, "Desculpe, não entendi."))

# Executa o chatbot
chatbot_npl()

