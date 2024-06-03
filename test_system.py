import pytest
from app import app, usuarios, hash_senha

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_acessar_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Index Page Content' in rv.data  # Ajuste conforme necessário

def test_fluxo_completo_cadastro_login(client):
    rv = client.post('/cadastrar', data={
        'nome': 'userflow',
        'senha': 'password123',
        'confirmar_senha': 'password123'
    })
    assert rv.status_code == 302

    rv = client.post('/login', data={
        'nome': 'userflow',
        'senha': 'password123'
    })
    assert rv.status_code == 302

    rv = client.post('/perfil/userflow', data={
        'texto': 'Texto de sistema.'
    })
    assert rv.status_code == 302
    assert usuarios['userflow']['texto'] == 'Texto de sistema.'

def test_texto_longo(client):
    usuarios['testuser'] = {'senha': hash_senha('password123'), 'texto': ''}
    texto_longo = 'a' * 501
    rv = client.post('/perfil/testuser', data={
        'texto': texto_longo
    })
    assert b'Erro: O texto não pode ter mais de 500 caracteres.' in rv.data

def test_textos_salvos(client):
    usuarios['testuser'] = {'senha': hash_senha('password123'), 'texto': 'Texto salvo.'}
    rv = client.get('/textos_salvos/testuser')
    assert rv.status_code == 200
    assert b'Texto salvo.' in rv.data

def test_logout(client):
    rv = client.get('/sair')
    assert rv.status_code == 302
