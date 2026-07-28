import mysql.connector


def inicializar_banco():
    """
    Prepara terreno, cria um arquivo e desenha as tabelas

    """
    try:
        conexao = mysql.connector.connect(host="localhost", user="root", password="soul_code", database="livraria")
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(255) NOT NULL,
                autor VARCHAR(255) NOT NULL,
                ano INT NOT NULL,
                preco DECIMAL(10, 2) NOT NULL,
                quantidade INT NOT NULL,
                ativo INT DEFAULT 1,
                categoria VARCHAR(50) DEFAULT 'Geral'                                              
            )
        """)

        cursor.execute("""
            
            CREATE TABLE IF NOT EXISTS vendas (                    
                id INT PRIMARY KEY AUTO_INCREMENT,
                horario DATETIME NOT NULL,
                id_livro INT NOT NULL,
                quantidade INT NOT NULL,
                valor_total DECIMAL(10, 2) NOT NULL,  
                FOREIGN KEY (id_livro) REFERENCES livros (id)                                                 
            )             
        """)

        cursor.execute("SELECT COUNT(*) FROM livros")
        
        if cursor.fetchone()[0] == 0:
            livros_iniciais = [
                ("O alquimista", "Paulo Coelho", 1988, 45.00, 15),
                ("Dom Casmurro", "Machado de Assis", 1899, 35.00, 20),
            ]

            cursor.executemany("""
                INSERT INTO livros (nome, autor, ano, preco, quantidade)
                VALUES (%s, %s, %s, %s, %s)
            """, livros_iniciais)
        

        conexao.commit()

    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
    
    finally:

        if 'conexao' in locals() and conexao.is_connected(): 
            cursor.close()
            conexao.close()







