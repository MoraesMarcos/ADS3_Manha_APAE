def test_acesso_usuarios_sem_login_redireciona(cliente):
    resposta = cliente.get('/usuarios', follow_redirects=True)
    conteudo = resposta.data.decode('utf-8').lower()
    assert "por favor, faça login" in conteudo

def test_dashboard_bloqueado_para_nao_admin(cliente):
    cliente.post('/login', data={
        'usuario': 'funcionario',
        'senha': 'senha456'
    }, follow_redirects=True)
    resposta = cliente.get('/dashboard', follow_redirects=True)
    conteudo = resposta.data.decode('utf-8').lower()
    assert "acesso restrito" in conteudo
