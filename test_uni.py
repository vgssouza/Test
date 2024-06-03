import pytest
from app import hash_senha, usuarios

def test_hash_senha():
    senha = "password123"
    hash_result = hash_senha(senha)
    assert hash_result == hashlib.sha256(senha.encode()).hexdigest()

def test_hash_senha_diferente():
    senha1 = "password123"
    senha2 = "password456"
    hash1 = hash_senha(senha1)
    hash2 = hash_senha(senha2)
    assert hash1 != hash2

def test_usuarios_dicionario_vazio():
    assert usuarios == {}

def test_adicionar_usuario():
    usuarios['testuser'] = {'senha': hash_senha('password123'), 'texto': ''}
    assert 'testuser' in usuarios

def test_remover_usuario():
    usuarios['testuser'] = {'senha': hash_senha('password123'), 'texto': ''}
    del usuarios['testuser']
    assert 'testuser' not in usuarios