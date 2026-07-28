
import mysql.connector

def alterar_preco():
    try:
        id_produto = int(input("Digite o [ID] do livro: "))
    except ValueError:
        print("ERRO: O ID deve ser um número.")
        return
    
    try:
        conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="livraria")
        cursor = conexao.cursor()

        cursor.execute("SELECT nome, preco FROM livros WHERE id = %s", (id_produto,))
        livro = cursor.fetchone()
        if not livro:
            print("ERRO: ID INVALIDO, LIVRO N ENCONTRADO")
            return
        try:
            novo_preco = float(input(f"Digite o novo preço para o livro '{livro[0]}' (preço atual: R$ {livro[1]}): "))
        except ValueError:
            print("ERRO: O preço deve ser o valor numerico")
            return
        
        cursor.execute("UPDATE livros SET preco = %s WHERE id = %s", (novo_preco, id_produto) )
        conexao.commit()
        print("Preço atualizado com sucesso!!!!!! :)")

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Motivo tecnico: {erro}")
        print("Valor não alterado.")
    
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()








def repor_estoque():
    try:
        id_produto = int(input("Digite o [ID] do livro: "))
    except ValueError:
        print("ERRO: O ID deve ser um número.")
        return

    try:
        conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="livraria")
        cursor = conexao.cursor()
        
        cursor.execute("SELECT nome, quantidade FROM livros WHERE id = %s", (id_produto,)) 
        livro = cursor.fetchone()   

        if not livro:
            print("ERRO: ID INVALIDO")
            return

        try:
            qtd_reposicao = int(input(f"Quantas unidades de '{livro[0]}' você deseja repor? [Atual: {livro[1]}]: " ))
        except ValueError:
            print("Quantidade deve ser um numero inteiro")
            return

        if qtd_reposicao <= 0:
            print("ERRO: QUANTIDADE INVALIDA")
        else:
            cursor = conexao.cursor()
            cursor.execute("UPDATE livros SET quantidade = quantidade + %s WHERE id = %s", (qtd_reposicao, id_produto))
            conexao.commit()
            print("ESTOQUE ATUALIZADO COM SUCESSO!!!! :)")

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Motivo tecnico: {erro}")
        print("Valor não alterado.")
    
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()










def exibir_relatorios_expressos():
    print("\n======RELATORIOS EXPRESOS============")
    print("Livros em ALERTA DE ESTOQUE (menos que 5): ")
    try:
        conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="livraria")
        cursor = conexao.cursor()
        cursor = conexao.cursor()
        cursor.execute("SELECT nome FROM livros WHERE quantidade < 5")  
        estoque_baixo = [linha[0] for linha in cursor.fetchall()]

        if len(estoque_baixo) == 0:
            print("Nenhum livro com estoque baixo")
        else:
            print(", ".join(estoque_baixo))  

        print("Livros populares abaixo de R$ 40,00: ")
        cursor.execute("SELECT nome FROM livros WHERE preco <= 40.0")
        estoque_baratos = [linha[0] for linha in cursor.fetchall()]

        if len(estoque_baratos) == 0:
            print("Nenhum livro barato")
        else:
            print(", ".join(estoque_baratos))

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Motivo tecnico: {erro}")
        print("Valor não alterado.")
    
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()


    

def desativar_livro():
    while True:    
        print("\n=======DESATIVAR LIVRO DO CATALÓGO (Soft delete)========")
        try:
            id_produto = int(input("Digite o [ID] do livro(Ou 0 pra voltar ao menu): "))
        except ValueError:
            print("ERRO: O ID deve ser um número.")
            return
        
        if id_produto == 0:
            break
        try:
            conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="livraria")
            cursor = conexao.cursor()

            cursor.execute("SELECT nome FROM livros WHERE id = %s AND ativo = 1", (id_produto,))
            livro = cursor.fetchone()

            if not livro:
                print("ERRO: livro não encontrado ou já foi desativado.")
                return

            print("(Digite 0 pra cancelar e voltar ao menu)")
            confirmar = input(f"Tem certeza que deseja excluir o livro '{livro[0]}'? (Historico de vendas sera mantido. (s/n:) )").strip().lower()

            if confirmar == '0':
                break
            
            elif confirmar == 's':
                cursor.execute("UPDATE livros SET ativo = 0 WHERE id = %s", (id_produto,))
                conexao.commit()
                print("Livro desativado do catalago com sucesso!!!!!")
                break
            else:
                continue
        except mysql.connector.Error as erro:
            conexao.rollback()
            print(f"Motivo tecnico: {erro}")
            print("Valor não alterado.")
        
        finally:
            if 'conexao' in locals() and conexao.is_connected(): 
                cursor.close()
                conexao.close()
        




def alterar_informacoes_livro():
    print("\n=====ALTERAR DADOS CADASTRAIS DO LIVRO========")

    try:
        id_produto = int(input("Digite o [ID] do livro: "))
    except ValueError:
        print("ERRO: O ID deve ser um número.")
        return
    
    try:
        conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="livraria")
        cursor = conexao.cursor()


        cursor.execute("SELECT nome, autor, ano, categoria FROM livros WHERE id = %s", (id_produto,))
        livro = cursor.fetchone()

        if not livro:
            print("ERRO: Livro não encontrado")
            return
        print(f"\nEditando livro: {livro[0]} | Autor: {livro[1]} | ano: {livro[2]}")
        print("(Se não quiser alterar algum elemento, deixe em branco e aperte enter)")

        novo_nome = input(f"Alterar nome do livro [{livro[0]}]  para: ").strip() or livro[0]
        novo_autor = input(f"Alterar nome do autor [{livro[1]}] para: ").strip() or livro[1]
        novo_genero = input(f"Alterar o genero [{livro[3]}] para: ").strip() or livro[3]


        novo_ano_str = input(f"Alterar ano de publicação[{livro[2]}] para: ").strip()

        try:
            novo_ano = int(novo_ano_str) if novo_ano_str else livro[2]

        except ValueError:

            print("ERRO: O ANO PRECISA SER NUMERICO, alteração cancelada")
            return

        cursor.execute("""
        UPDATE livros
        SET nome = %s, autor = %s, ano = %s, categoria = %s
        WHERE id = %s
        """, (novo_nome, novo_autor, novo_ano, id_produto, novo_genero))

        conexao.commit()
        print(f"\nAlterado com sucesso!!!!!")

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Motivo tecnico: {erro}")
        print("Valor não alterado.")
    
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()



