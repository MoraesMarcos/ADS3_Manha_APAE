# 🧪 Testes Automatizados com Selenium – Projeto APAE

Este documento descreve os testes automatizados de interface realizados com **Selenium WebDriver** no sistema APAE. Os testes visam validar o funcionamento de funcionalidades essenciais através da automação de ações no navegador.

---

## 🔧 Ferramentas Utilizadas

- **Python 3.11**
- **Selenium**
- **WebDriver Manager**
- **Google Chrome (v137+)**
- **VS Code**
- **Ambiente:** [http://localhost:5000](http://localhost:5000)  
- **Data:** 08/0562025 

---

## 📋 Funcionalidades Testadas

| Funcionalidade         | Descrição                                                                 | Resultado |
|------------------------|---------------------------------------------------------------------------|-----------|
| Login                  | Acesso ao sistema com credenciais válidas                                 | ✅ Sucesso |
| Dashboard              | Verificação de acesso à página inicial após login                         | ✅ Sucesso |
| Envio de Feedback      | Acesso à página de feedback e envio de sugestão automática                 | ✅ Sucesso |
| Cadastro de Usuário    | Preenchimento do formulário com dados de usuário fictício                  | ⚠️ Parcial (campos de e-mail e telefone com problemas de interação) |
| Logout                 | Encerramento da sessão e retorno à tela de login                          | ⚠️ Não executado devido à falha anterior |

---

## ⚠️ Problemas Detectados

- `element not interactable`: Campo de e-mail presente no DOM, mas não interagível.
- `not visible`: Campo de telefone residencial não visível ao WebDriver.
- `UnexpectedAlertPresentException`: Um alerta JavaScript foi disparado (e-mail inválido), mas estava fechado no momento da captura.
- Possível lógica dinâmica ocultando campos do formulário.

---

## 📝 Sugestões de Correção

- Verificar se os campos do formulário estão **habilitados** e **visíveis** antes da interação.
- Inserir `waits` adicionais para elementos que aparecem após ações do usuário (ex: seleção de sexo).
- Validar o HTML e scripts da página de cadastro para evitar `display: none`, `readonly` ou `disabled` sem necessidade.

---

## ▶️ Como Executar os Testes

```bash
# Instale as dependências
pip install selenium webdriver-manager

# Execute o script de teste
python teste_apae_selenium.py
