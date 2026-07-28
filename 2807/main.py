import mysql.connector

from banco_dados import inicializar_banco
from interface import exibir_menu_e_estoque

#arquivos da pasta comando

from comandos.carrinho import realizar_venda
from comandos.cadastro import cadastrar_livro
from comandos.estoque_cmd import alterar_preco, repor_estoque, exibir_relatorios_expressos, desativar_livro, alterar_informacoes_livro
from comandos.filtros import buscar_livro, exibir_catalogo_ordenado
from comandos.financeiro import aplicar_promocao, exibir_nota_fiscal, exibir_painel_bi, exportar_relatorio_txt
from comandos.novo import repor_estoque_em_lote

inicializar_banco()

while True:

    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="soul_code", #Coloque a senha configurada na instalação
        database="livraria"
    )
    
    cursor = conexao.cursor()

    cursor.execute("SELECT SUM(valor_total) FROM vendas")
    resultado_caixa = cursor.fetchone()[0]
    caixa = resultado_caixa if resultado_caixa is not None else 0.0

    cursor.execute("SELECT * FROM livros WHERE ativo = 1")
    estoque = cursor.fetchall()

    cursor.close()
    conexao.close()


    exibir_menu_e_estoque(caixa, estoque)

    try:
        comando = int(input("Digite o comando: "))
    except ValueError:
        print("ERRO: COMANDO DEVE SER UM NUMERO INTEIRO: ")
    

    if comando == 3:
        print(f"Encerrando sistema. Total geral em caixa: R$ {caixa:.2f}")
        break

    elif comando == 1:
        caixa = realizar_venda()

    elif comando == 2:
        cadastrar_livro()

    elif comando == 4:
        alterar_preco()

    elif comando == 5:
        repor_estoque()

    elif comando == 6:
        buscar_livro()

    elif comando ==7:
        aplicar_promocao()

    elif comando == 8:
        exibir_nota_fiscal()

    elif comando == 9:
        exibir_painel_bi()

    elif comando == 10:
        exibir_catalogo_ordenado()

    elif comando == 11:
        exibir_relatorios_expressos()
    
    elif comando == 12:
        desativar_livro()
        
    elif comando == 13:
        alterar_informacoes_livro()
    
    elif comando == 14:
        exportar_relatorio_txt()
    
    elif comando == 15:
        print("\nREPOSIÇÃO DE ESTOQUE EM LOTE")
        try:
            qtd = int(input("Qual a quantidade recebida para CADA livro do lote: "))
            entrada_ids = input("Digite os [IDs] dos livros separados por virgula: ")
            lista_ids = [int(numero.strip()) for numero in entrada_ids.split(', ')]

            repor_estoque_em_lote(qtd, *lista_ids)

        except ValueError:
            print("ERRO DE DIGITAÇÃO: Você digitou letras ou deixou o formato errado")


    # --- BLOCO DE PAUSA ---
    print("\n-----------------------------------------")
    print("[1] Fechar sistema")
    print("[2] Voltar ao menu principal")
    try:
        acao_pos_comando = int(input("O que deseja fazer agora? "))
        if acao_pos_comando == 1:
            print(f"Encerrando o sistema. Total geral em caixa: R$ {caixa:.2f}")
            break
    except ValueError:
        pass



