import pytest
from app import app, usuarios

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_cadastrar_usuario(client):
    rv = client.post('/cadastrar', data={
        'nome': 'testuser',
        'senha': 'password123',
        'confirmar_senha': 'password123'
    })
    assert rv.status_code == 302
    assert 'testuser' in usuarios

def test_cadastrar_senhas_diferentes(client):
    rv = client.post('/cadastrar', data={
        'nome': 'testuser2',
        'senha': 'password123',
        'confirmar_senha': 'password456'
    })
    assert b'Erro: As senhas não coincidem.' in rv.data

def test_login_usuario(client):
    usuarios['testuser'] = {'senha': hash_senha('password123'), 'texto': ''}
    rv = client.post('/login', data={
        'nome': 'testuser',
        'senha': 'password123'
    })
    assert rv.status_code == 302

def test_login_falha(client):
    rv = client.post('/login', data={
        'nome': 'testuser',
        'senha': 'wrongpassword'
    })
    assert b'Erro: Usuário ou senha incorretos.' in rv.data

def test_adicionar_texto(client):
    usuarios['testuser'] = {'senha': hash_senha('password123'), 'texto': ''}
    rv = client.post('/perfil/testuser', data={
        'texto': 'Este é um texto de teste.'
    })
    assert rv.status_code == 302
    assert usuarios['testuser']['texto'] == 'Este é um texto de teste.'
