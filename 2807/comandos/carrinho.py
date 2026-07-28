import datetime
import mysql.connector

def realizar_venda():
    print("\n=======CARRINHO DE COMPRAS (SQLITE)=========")
    carrinho = [] 

    while True:
        try:
            id_venda = int(input("digite o [ID] do produto: (-1 pra concluir compra -2 pra cancelar)"))
        except ValueError:
            print("ERRO: ID DEVE SER UM NUMERO INTEIRO")
            continue
        if id_venda == -1:
            break
        elif id_venda == -2:
            print("COMPRA CANCELADA")
            carrinho = []
            return
        
        conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="livraria")
        cursor = conexao.cursor()
        

        cursor.execute("SELECT nome, preco, quantidade FROM livros WHERE id = %s", (id_venda,))
        
        livro_encontrado = cursor.fetchone()

        cursor.close()
        conexao.close()



        if not livro_encontrado:
            print("ERRO: ID INVALIDO. Esse livro não existe no sistema")
            continue

        nome_livro, preco_livro, estoque_real = livro_encontrado

        try:
            qtd = int(input(f"Quantos exemplares do '{nome_livro}' você deseja adicionar?"))
        except ValueError:
            print("ERRO: quantidade invalida")
            continue

        qtd_ja_no_carrinho = sum(item['qtd'] for item in carrinho if item['id'] == id_venda)  
        estoque_disponivel = estoque_real - qtd_ja_no_carrinho

        if qtd <= 0:
            print("ERRO: QUANTIDADE INVALIDA")
        elif qtd > estoque_disponivel:
            print(f"ESTOQUE INSUFICIENTE. Vocã ja tem {qtd_ja_no_carrinho} no carrinho, o estoque total é {estoque_real}. ")
        else:
            carrinho.append({
                "id": id_venda,
                "nome": nome_livro,
                "preco": preco_livro,
                "qtd": qtd,
                "subtotal": qtd * preco_livro
            })
            print(f"-> {qtd}x '{nome_livro}' adicionado ao carrinho. ")

    if len(carrinho) > 0:
        total_compra = sum(item['subtotal'] for item in carrinho)
        print(f"\n ========FECHAMENTO DE CAIXA=======")
        print(f"Total a pagar: R$ {total_compra:.2f}")
        confirmar = input("Confirmar pagamento e registrar a venda? (s/n): ").strip().lower()

        if confirmar == "s":
            conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="livraria")
            cursor = conexao.cursor()
            
            try:
                for item in carrinho:
                    cursor.execute("""
                        UPDATE livros
                        SET quantidade = quantidade - %s
                        WHERE id = %s                   
                    """, (item['qtd'], item['id']))

                    cursor.execute("""
                        INSERT INTO vendas (horario, id_livro, quantidade, valor_total)
                        VALUES (%s, %s, %s, %s)         
                    """, (
                        datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S"),
                        item['id'],
                        item['qtd'],
                        item['subtotal']
                    ))
                conexao.commit()
                print("VENDA CONCLUIDA COM SUCESSO!!!! :) ")


            except mysql.connector.Error as erro:
                conexao.rollback()
                print("\nERRO FATAL NO BANCO DE DADOS: Transação cancelada.")
                print(f"Motivo tecnico: {erro}")
                print("O estoque foi restaurado e nenhuma nota fiscal corrompida foi gerada.")
            
            finally:
                if 'conexao' in locals() and conexao.is_connected(): 
                    cursor.close()
                    conexao.close() 

        else:
            print("VENDA NÃO FINALIZADA")










        




