
import mysql.connector

#*Arg

def repor_estoque_em_lote(qtd_adicional, *ids_alvo):
    if len(ids_alvo) == 0:
        print("ERRO: Você precisa informar pelo menos um id de livro")
        return
    
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="soul_code", #Coloque a senha configurada na instalação
            database="livraria"
        )
        
        cursor = conexao.cursor()

        print(f"\nIniciando reposição de +{qtd_adicional} unidades para os IDs solicitados...")

        for id_livro in ids_alvo: 
            cursor.execute("SELECT nome FROM livros WHERE id = %s", (id_livro,))
            resultado = cursor.fetchone()

            if not resultado:
                print(f"ERRO: livro com ID {id_livro} não existe no sistema") 
                continue         
            nome_livro = resultado[0]

            cursor.execute("""
                UPDATE livros
                SET quantidade = quantidade + %s
                WHERE id = %s
            """, (qtd_adicional, id_livro))

            print(f"Foram adicionados {qtd_adicional} do seguinte livro: {nome_livro}")
        
        conexao.commit()

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"ERRO FATAL de banco de dados: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()