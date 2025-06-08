def test_homepage(cliente):
    resposta = cliente.get('/')
    assert resposta.status_code == 200
    conteudo = resposta.data.decode('utf-8').lower()
    assert "login" in conteudo or "inicial" in conteudo
