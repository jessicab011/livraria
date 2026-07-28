import mysql.connector

def cadastrar_livro():
    print("\n------ CADASTRAR NOVO LIVRO ----------")
    novo_nome = input("Qual o nome do livro? ").strip()
    novo_autor = input("Qual o autor do livro? ").strip()
    
    try:
        novo_ano = int(input("Qual o ano de lançamento? "))
        novo_preco = float(input("Qual o preço de venda? "))
        nova_qtd = int(input("Qual a quantidade inicial do estoque? "))
        novo_genero = input("Qual o genero do livro? ")
    except ValueError:
        print("ERRO: Ano, preço e quantidade devem ser valores numéricos válidos.")
        return

    try:
        conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="livraria")
        cursor = conexao.cursor()

        cursor.execute("""
                       
            INSERT INTO livros (nome, autor, ano, preco, quantidade, categoria)
            VALUES (%s, %s, %s, %s, %s, %s)
                       
        """, (novo_nome, novo_autor, novo_ano, novo_preco, nova_qtd, novo_genero))

        conexao.commit()
        print(f"Livro '{novo_nome}' salvo com sucesso.")

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Motivo tecnico: {erro}")
        print("Valor não alterado.")
    
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()