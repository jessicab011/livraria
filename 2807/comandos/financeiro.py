import mysql.connector
import datetime

def aplicar_promocao():
    print("\n--- PROMOÇÕES ---")
    print("'1' = Desconto em 1 livro específico")
    print("'2' = Desconto em TODO o acervo")
    
    try:
        tipo_promo = int(input("Digite o tipo de promoção: "))
    except ValueError:
        print("ERRO: O tipo de promoção deve ser um número.")
        return
    
    try:
        conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="livraria")
        cursor = conexao.cursor()


        if tipo_promo == 1:
            try:
                porcentagem = float(input("Qual a porcentagem(%) do desconto: "))
                id_produto = int(input("Digite o [ID] do livro: "))
            except ValueError:
                print("ERRO: Porcentagem e ID devem ser números válidos.")
                return
            

            fator_desconto = (100 - porcentagem) / 100

            cursor.execute("UPDATE livros SET preco = ROUND(preco * %s, 2) WHERE id = %s", (fator_desconto, id_produto))
            conexao.commit() 
            print("Desconto aplicado com sucesso!!!! :)")

        elif tipo_promo == 2:
            try:
                porcentagem = float(input("Digite a pocentagem(%) que deseja aplicar no acervo: "))
            except ValueError:
                print("ERRO: procentagem(%) invalida")
                return

            fator_desconto = (100 - porcentagem) / 100
            cursor = conexao.cursor()
            cursor.execute("UPDATE livros SET preco = ROUND(preco * %s, 2)", (fator_desconto,))
            conexao.commit()
            print("Desconto aplicado com sucesso!!!! :)")

        else:
            print("Comando invalido")

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Motivo tecnico: {erro}")
        print("Promoção não aplicada.")
    
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()







def exibir_nota_fiscal():
    print("\n=====NOTA FISCAL===============")

    try:
        conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="livraria")
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT vendas.id, vendas.horario, livros.nome, vendas.quantidade, vendas.valor_total
            FROM vendas
            INNER JOIN livros ON vendas.id_livro = livros.id      
        """)
        
        historico = cursor.fetchall()
        if len(historico) == 0:
            print("Não foi realizado nenhuma venda ainda")
        else:
            for venda in historico:
                print(f"[{venda[0]}] Data/Hora: {venda[1]} | {venda[2]} x{venda[3]} | Total venda R$ {venda[4]:.2f}")
   
    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Motivo tecnico: {erro}")

    
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()  




def exibir_painel_bi():
    print("\n===================PAINEL DE BUSINESS INTELLIGENCE===============")

    try:
        conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="livraria")
        cursor = conexao.cursor()

        cursor.execute("SELECT COUNT(*) FROM vendas")

        if cursor.fetchone()[0] == 0:
            print("Sem dados de vendas, nenhuma venda realizada ainda.")
            return
        
        cursor.execute("SELECT SUM(valor_total) FROM vendas")
        faturamento = cursor.fetchone()[0]
        print(f"Historico de faturamente Bruto: R$ {faturamento:.2f}")

        cursor.execute("SELECT AVG(valor_total) FROM vendas")
        ticket_medio = cursor.fetchone()[0]
        print(f"====Ticket Médio por venda: R$ {ticket_medio:.2f}==========")

        cursor.execute("""
            SELECT livros.nome, SUM(vendas.quantidade)
            FROM vendas
            INNER JOIN livros ON vendas.id_livro = livros.id
            GROUP BY livros.nome
            ORDER BY SUM(vendas.quantidade) DESC
            LIMIT 1
        """)

        produto_campeao, maior_qtd = cursor.fetchone()
        print(f" -> LIVRO MAIS VENDIDO: {produto_campeao} ({maior_qtd}) exemplares vendidos")
 
    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Motivo tecnico: {erro}")
    
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()






def exportar_relatorio_txt():
    print("\n Gerando relatorio de fechamento...")

    try:
        conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="livraria")
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT vendas.horario, livros.nome, vendas.quantidade, vendas.valor_total
            FROM vendas
            INNER JOIN livros ON vendas.id_livro = livros.id
            ORDER BY vendas.id ASC
        """)
        
        vendas = cursor.fetchall()

        if not vendas:
            print("Nenhuma venda registrada")
            return
        
        cursor.execute("SELECT SUM(valor_total) FROM vendas")
        faturamento_total = cursor.fetchone()[0]

        nome_arquivo = f"Fechamento_Caixa_{datetime.datetime.now().strftime('%y_%m_%d___%H__%M__%S')}.txt"

        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write("=========================================\n")
            arquivo.write("           RELATORIO DE VENDAS             \n")
            arquivo.write("======================================\n\n")

            for venda in vendas:
                linha = f"DATA: {venda[0]} | Livro: {venda[1]} | Qtd: {venda[2]} | Subtotal: R$ {venda[3]:.2f}\n"
                arquivo.write(linha)
            
            arquivo.write(f"Faturamento Total de hoje: R$ {faturamento_total:.2f}")
        
        print(f"SUCESSO! Arquivo '{nome_arquivo}' foi criado na sua pasta")


    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Motivo tecnico: {erro}")

    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()




