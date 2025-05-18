import random
import nltk
import pandas as pd
import unicodedata
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

nltk.download('punkt')

# Inicializa cliente OpenAI (você pode usar uma variável de ambiente para a chave)
client = OpenAI(api_key=)
# Função para normalizar texto (remover acentos, lowercase)
def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto

# Função para chamar o ChatGPT
def responder_com_chatgpt(pergunta_usuario):
    try:
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um atendente educado e prestativo da loja Shopzen."},
                {"role": "user", "content": pergunta_usuario}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao conectar com o atendente: {e}"

# Carrega os dados da planilha
df = pd.read_csv(r"C:\Users\thiag\OneDrive\Área de Trabalho\Shopzen.csv")

# Corrige preços: troca vírgula por ponto, e converte para float
df["PREÇO"] = df["PREÇO"].astype(str).str.replace(",", ".")
df["PREÇO"] = pd.to_numeric(df["PREÇO"], errors="coerce")

# Define funções auxiliares
def produto_mais_barato():
    item = df.loc[df["PREÇO"].idxmin()]
    return f"O item mais barato é {item['PRODUTO']} por R${item['PREÇO']:.2f}."

def produto_mais_caro():
    item = df.loc[df["PREÇO"].idxmax()]
    return f"O item mais caro é {item['PRODUTO']} por R${item['PREÇO']:.2f}."

def listar_produtos():
    return "\n".join([f"{row['PRODUTO']}" for _, row in df.iterrows()])

def listar_promocoes():
    promocoes = df[df["PREÇO"] > 0]
    return "\n".join([f"O preço da {row['PRODUTO']} é de R${row['PREÇO']:.2f}" for _, row in promocoes.iterrows()])

def responder_desconto_especial():
    return "Claro que temos descontos!\nNa compra de duas memórias RAM, tudo sai por 350 reais!\nNa compra de dois SSD, tudo sai por 200 reais!"

# Função para buscar o preço de um produto
def buscar_preco_produto(entrada_usuario):
    entrada = normalizar_texto(entrada_usuario)
    for produto in df["PRODUTO"]:
        produto_normalizado = normalizar_texto(produto)
        if produto_normalizado in entrada:
            preco = df[df["PRODUTO"] == produto]["PREÇO"].values[0]
            return f"O preço da {produto} é de R${preco:.2f}."
    return None  # Produto não encontrado

# Dados de treinamento
dados = {
    "Produto": [
        'quais sao os produtos?',
        'quais produtos tem?',
        'mostrar os produtos',
        'me fale sobre os produtos disponíveis'
    ],
    "Promocoes": [
        'quais sao os descontos?',
        'tem descontos?',
        'o que é mais barato?',
        'o que é mais caro?',
        'quais sao os precos?',
        'qual o preco?',
        'quais os preços?'
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

# Treinamento do modelo
frases = []
tags = []

for tag, frases_exemplo in dados.items():
    for frase in frases_exemplo:
        frases.append(normalizar_texto(frase))
        tags.append(tag)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(frases)
Y = tags

modelo = MultinomialNB()
modelo.fit(X, Y)

# Chatbot principal
def chatbot_npl():
    print("Bem-vindo(a) ao chatbot da Shopzen!")
    while True:
        entrada = input("Você: ")
        entrada_normalizada = normalizar_texto(entrada)

        if entrada_normalizada in ["adeus", "encerrar", "tchau", "bye"]:
            print("Bot: Foi um prazer falar contigo! Até logo!")
            break

        # Busca por nome de produto na frase
        resposta_preco_produto = buscar_preco_produto(entrada)
        if resposta_preco_produto:
            print("Bot:", resposta_preco_produto)
            continue

        elif "mais barato" in entrada_normalizada:
            print("Bot:", produto_mais_barato())
            continue

        elif "mais caro" in entrada_normalizada:
            print("Bot:", produto_mais_caro())
            continue

        elif "desconto" in entrada_normalizada or "descontos" in entrada_normalizada:
            print("Bot:", responder_desconto_especial())
            continue

        elif any(p in entrada_normalizada for p in ["preco", "precos", "promocao", "promocoes"]):
            print("Bot:", listar_promocoes())
            continue

        entrada_vect = vectorizer.transform([entrada_normalizada])
        tag_prevista = modelo.predict(entrada_vect)[0]

        if tag_prevista == "Atendente":
            resposta = responder_com_chatgpt(entrada)
            print("Atendente:", resposta)
        elif tag_prevista == "Produto":
            print("Bot:", listar_produtos())
        elif tag_prevista == "Promocoes":
            print("Bot:", listar_promocoes())
        elif tag_prevista == "Encerrar":
            print("Bot: Foi um prazer falar contigo! Até logo!")
            break
        else:
            print("Bot: Desculpe, não entendi. Poderia reformular?")

# Executa o chatbot
chatbot_npl()
