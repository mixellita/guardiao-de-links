from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista temporária para armazenar os links.
# Cada vez que o app reiniciar, esta lista será zerada.
links_salvos = []

@app.route('/')
def index():
    """ Rota principal que renderiza a página com os links. """
    return render_template('index.html', links=links_salvos)

@app.route('/adicionar', methods=['POST'])
def adicionar_link():
    """ Rota para receber o formulário e adicionar um novo link. """
    url = request.form.get('url_link')
    if url:
        links_salvos.append(url)
    
    # Redireciona o usuário de volta para a página inicial
    return redirect(url_for('index'))

# O Render vai usar o Gunicorn para rodar a aplicação,
# então esta parte abaixo não é estritamente necessária para o deploy,
# mas é essencial para você testar localmente no seu computador.
if __name__ == '__main__':
    # O host='0.0.0.0' permite que o app seja acessível na sua rede local
    # O port=5000 é a porta padrão do Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
