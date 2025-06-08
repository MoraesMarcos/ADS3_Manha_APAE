def test_login_com_sucesso(cliente):
    resposta = cliente.post('/login', data={
        'usuario': 'admin',
        'senha': 'senha123'
    }, follow_redirects=True)
    assert resposta.status_code == 200
    assert "bem-vindo" in resposta.data.decode('utf-8').lower()

def test_login_falha(cliente):
    resposta = cliente.post('/login', data={
        'usuario': 'admin',
        'senha': 'senha_errada'
    }, follow_redirects=True)
    assert "usuário ou senha incorretos" in resposta.data.decode('utf-8').lower()

def test_logout(cliente):
    cliente.post('/login', data={
        'usuario': 'admin',
        'senha': 'senha123'
    }, follow_redirects=True)
    resposta = cliente.get('/logout', follow_redirects=True)
    assert "login" in resposta.data.decode('utf-8').lower()
