def exibir_menu_e_estoque(caixa_atual, estoque_atual):
    """
    Função dedicada a imprimir o menu e estoque na tela

    """
    print(f"""
    ==================================================
                   LIVRARIA SOUL 
       Caixa Acumulado Histórico: R$ {caixa_atual:.2f}
    ==================================================
    """)
    print("ACERVO DISPONIVEL: ")

    for livro in estoque_atual:
        print(f"[{livro[0]}] {livro[1]} ({livro[3]}) | Autor: {livro[2]} | Genero {livro[7]} | R$ {livro[4]:.2f} | Estoque: {livro[5]}")

    print("""--------------------------------------------------
        '1' = Carrinho de compras
        '2' = Cadastrar Novo Livro
        '3' = Sair do Sistema
        '4' = Alterar Preço
        '5' = Repor Estoque
        '6' = Pesquisar por Nome/Autor
        '7' = PROMOÇÕES
        '8' = Nota Fiscal (Vendas da Sessão)
        '9' = PAINEL DE ESTATÍSTICAS E BALANÇO
        '10' = Ordenar catalogo
        '11' = Relatorio Expressos
        '12' = Desativar venda
        '13' = Editar Informações do Livro
        '14' = Exportar relatorio
        '15' = Repor estoque em lote
        =====================================================\n""")

    




