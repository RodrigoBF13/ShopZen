def linhas():
    print('-=' * 10)

# FUNÇÃO PRINCIPAL DO CHATBOT
def chatbot(nome=''):
    while True:
        linhas()
        print("Olá, bem-vindo(a) ao chatbot da Shopzen! " + nome)
        linhas()
        print("""
OPÇÕES: ESCOLHA UMA:


[1] - Ver produtos
[2] - Ver promoções
[3] - Falar com um atendente
[4] - Encerrar programa
""")

        # Entrada do usuário
        escolha = input("Escolha uma das opções de 1 a 5: ").strip().lower()

        # Listas e strings
        produtos = ('Whey protein', 'Creatina', 'Aveia em Flocos', 'Castanhas')
        promocoes = ('Whey - R$55.00', 'Creatina - R$35.00', 'Aveia em flocos (pacote) - R$12.00', 'Castanhas (KG) - R$50.00')
        atendente = 'Olá, me chamo Willy e sou atendente do Shopzen. Como posso te ajudar hoje?'

        if escolha == "1":
            linhas()
            for item in produtos:
                print(item)
            linhas()

        elif escolha == "2":
            linhas()
            for item in promocoes:
                print(item)
            linhas()

        elif escolha == "3":
            linhas()
            for item in atendente:
                print(item)
            linhas()

        elif escolha == "4":
            print("Encerrando o programa. Até logo!")
            break
        else:
            print("Opção inválida, tente novamente.")
            continue
chatbot()

