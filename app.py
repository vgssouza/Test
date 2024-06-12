from flask import Flask, render_template, request, redirect, url_for, session, g, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from azure.storage.blob import BlobServiceClient
from encrypt_decrypt import encrypt_file, decrypt_file
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
import sqlite3
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'supersecretkey'

DATABASE = 'users.db'

# Função para conectar ao banco de dados


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Função para inicializar o banco de dados


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL)''')
    print("Banco de dados inicializado.")

# Formulário de Registro


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80)])

# Formulário de Login


class LoginForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80)])

# Rota para registro


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(
            password, method='pbkdf2:sha256')

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
                conn.commit()
                flash('Registro realizado com sucesso!', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Nome de usuário já existe. Escolha outro nome.', 'danger')

    return render_template('register.html', form=form)

# Rota para login


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash('Credenciais inválidas. Tente novamente.', 'danger')

    return render_template('login.html', form=form)

# Verifica se o usuário está logado antes de acessar determinadas rotas


@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect(url_for('login'))


# Conexão com o Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(
    app.config['AZURE_STORAGE_CONNECTION_STRING'])
container_client = blob_service_client.get_container_client(
    app.config['AZURE_STORAGE_CONTAINER_NAME'])

# Rota para a página inicial


@app.route('/')
def index():
    blobs = container_client.list_blobs()
    return render_template('index.html', blobs=blobs)

# Rota para upload de arquivos


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'username' not in session:
        return redirect(url_for('login'))

    if 'file' not in request.files:
        return redirect('/')

    file = request.files['file']
    if file.filename == '':
        return redirect('/')

    file_path = os.path.join('static/uploads', file.filename)
    file.save(file_path)
    print(f"File saved locally: {file_path}")  # Debug message

    encrypt_file(file_path)

    blob_client = blob_service_client.get_blob_client(
        container=app.config['AZURE_STORAGE_CONTAINER_NAME'], blob=file.filename)
    with open(file_path, 'rb') as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"File uploaded to Azure: {file.filename}")  # Debug message

    os.remove(file_path)
    print(f"Local file removed: {file_path}")  # Debug message

    return redirect('/')

# Rota para download de arquivos


@app.route('/download/<filename>')
def download_file(filename):
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        file_path = os.path.join('static/uploads', filename)
        print(f"Attempting to download file: {filename}")  # Debug message

        blob_client = blob_service_client.get_blob_client(
            container=app.config['AZURE_STORAGE_CONTAINER_NAME'], blob=filename)
        print(f"Blob client created for file: {filename}")  # Debug message

        with open(file_path, 'wb') as data:
            data.write(blob_client.download_blob().readall())
            print(f"File {filename} downloaded successfully")  # Debug message

        decrypt_file(file_path)
        print(f"File {filename} decrypted successfully")  # Debug message

        return send_from_directory('static/uploads', filename, as_attachment=True)
    except Exception as e:
        print(f"Error downloading file {filename}: {e}")  # Debug message
        return str(e)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
