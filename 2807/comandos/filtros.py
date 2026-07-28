import mysql.connector

def buscar_livro():
    print("\n========BUSCAR LIVRO ========")

    termo_busca = input("Digite o nome do livro ou autor: ").strip().lower()  

    try:
        conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="livraria")
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome, autor, ano, preco, quantidade, categoria
            FROM livros
            WHERE ativo = 1 AND (
                LOWER(nome) LIKE %s OR
                LOWER(autor) LIKE %s OR
                LOWER(categoria) LIKE %s OR
                CAST(ano AS CHAR)  LIKE %s                                
            )
        """, (f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%"), f"%{termo_busca}%")  


        resultados = cursor.fetchall()

        cursor.close()
        conexao.close()


        if len(resultados) == 0:
            print("Nenhum resultado encontrado :(")
        else:
            for livro in resultados:
                print(f"[{livro[0]}] {livro[1]} ({livro[3]}) | Autor: {livro[2]} | Genero {livro[6]} | R$ {livro[4]:.2f} | Estoque: {livro[5]}")

    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE CONEXÃO COM O BANCO")
        
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()




        




def exibir_catalogo_ordenado():
    while True:
        print("\n--- CATÁLOGO ORDENADO---")

        print("1. Ordem Alfabética")
        print("2. Mais Baratos Primeiro")
        print("3. Mais Caros Primeiro")
        print("4. Maior Estoque Primeiro") # Nova opção de organização adicionada
        print("0. Voltar pro Menu")

        ordem = input("Escolha a ordenação: ")

        if ordem == "0":
            break

        query_base = "SELECT nome, preco, quantidade FROM livros WHERE ativo = 1"
        
        if ordem == "1":
            query_base = f"{query_base} ORDER BY LOWER(nome) ASC"
        elif ordem == "2":
            query_base = f"{query_base} ORDER BY preco ASC"
        elif ordem == "3":
            query_base = f"{query_base} ORDER BY preco DESC"
        elif ordem == "4":
            query_base = f"{query_base} ORDER BY quantidade DESC"
        else:
            print("Opção invalida")
            continue
        try:
            conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="livraria")
            cursor = conexao.cursor()

            cursor.execute(query_base)
            estoque_ordenado = cursor.fetchall()


            for livro in estoque_ordenado:
                print(f"={livro[0]:<20} | R$ {livro[1]:.2f} | Qtd: {livro[2]}")


        except mysql.connector.Error as erro:
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO")
        
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()




