from flask import Flask, render_template, request, redirect, url_for
import hashlib

app = Flask(__name__)

# Dicionário para simular o armazenamento dos usuários e seus textos
usuarios = {}


@app.route('/')
def index():
    return render_template('index.html')


def hash_senha(senha):
    # Usando SHA-256 para hash da senha
    return hashlib.sha256(senha.encode()).hexdigest()


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    senha = request.form['senha']
    confirmar_senha = request.form['confirmar_senha']

    if senha != confirmar_senha:
        return "Erro: As senhas não coincidem."

    if nome in usuarios:
        return "Erro: Usuário já cadastrado."

    usuarios[nome] = {'senha': hash_senha(senha), 'texto': ''}
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        if nome in usuarios and usuarios[nome]['senha'] == hash_senha(senha):
            return redirect(url_for('perfil', nome=nome))
        else:
            return "Erro: Usuário ou senha incorretos."

    return render_template('login.html')


@app.route('/perfil/<nome>', methods=['GET', 'POST'])
def perfil(nome):
    if request.method == 'POST':
        texto = request.form['texto']
        if len(texto) > 500:
            return "Erro: O texto não pode ter mais de 500 caracteres."
        usuarios[nome]['texto'] = texto
        return redirect(url_for('textos_salvos', nome=nome))

    return render_template('perfil.html', nome=nome, texto=usuarios[nome]['texto'])


@app.route('/textos_salvos/<nome>')
def textos_salvos(nome):
    texto = usuarios[nome]['texto']
    return render_template('textos_salvos.html', nome=nome, texto=texto)


@app.route('/sair')
def sair():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
