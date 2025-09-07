import sqlite3 # Biblioteca para interagir com o SQLite
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- Configuração do Banco de Dados ---

DATABASE_FILE = 'database.db'

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE_FILE)
    # Isso faz com que os resultados do banco de dados venham como dicionários,
    # o que é mais fácil de trabalhar. Ex: {'id': 1, 'url': 'http...'}
    conn.row_factory = sqlite3.Row
    return conn

def init_db( ):
    """Função para criar a tabela do banco de dados se ela não existir."""
    with app.app_context():
        conn = get_db_connection()
        # O 'with' garante que a conexão será fechada mesmo se der erro.
        with conn:
            conn.execute(
                'CREATE TABLE IF NOT EXISTS links ('
                '  id INTEGER PRIMARY KEY AUTOINCREMENT,'
                '  url TEXT NOT NULL'
                ');'
            )
        conn.close()

# --- Rotas da Aplicação ---

@app.route('/')
def index():
    """ Rota principal que busca os links do banco de dados e renderiza a página. """
    conn = get_db_connection()
    # Busca todos os links da tabela, ordenando pelos mais recentes primeiro.
    links_do_banco = conn.execute('SELECT * FROM links ORDER BY id DESC').fetchall()
    conn.close()
    
    # A variável 'links' agora contém os dados vindos do banco de dados.
    return render_template('index.html', links=links_do_banco)

@app.route('/adicionar', methods=['POST'])
def adicionar_link():
    """ Rota para receber o formulário e salvar o novo link no banco de dados. """
    url = request.form.get('url_link')
    if url:
        conn = get_db_connection()
        # O '?' é um placeholder para evitar injeção de SQL, uma boa prática de segurança.
        conn.execute('INSERT INTO links (url) VALUES (?)', (url,))
        conn.commit() # Confirma (salva) a transação no banco de dados.
        conn.close()
    
    return redirect(url_for('index'))

# --- Inicialização ---

# Chama a função para criar o banco de dados assim que o app inicia.
init_db()

# O resto do código para rodar localmente permanece o mesmo.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
