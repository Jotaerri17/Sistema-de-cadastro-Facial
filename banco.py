import psycopg2
import os
from dotenv import load_dotenv

# Carrega as senhas do arquivo .env
load_dotenv()

# Pega a URL que está escondida lá
URL_NEON = os.getenv("URL_NEON")

def conectar_banco():
    try:
        # Tenta estabelecer a conexão
        conexao = psycopg2.connect(URL_NEON)
        cursor = conexao.cursor()
        print("[SUCESSO] Conectado ao Neon!")
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                encoding TEXT NOT NULL
            );
        ''')
        conexao.commit() 
        print("[SUCESSO] Tabela verificada/criada com sucesso.")
        
        return conexao, cursor

    except Exception as e:
        print(f"[ERRO] Não foi possível conectar ao banco: {e}")
        return None, None

# Testando a conexão
if __name__ == "__main__":
    conexao, cursor = conectar_banco()
    if conexao:
        cursor.close()
        conexao.close()
        print("Conexão encerrada.")