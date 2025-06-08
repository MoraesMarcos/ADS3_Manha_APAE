# 🏥 Sistema APAE - Gestão de Usuários e Agendamentos

Este é um sistema web desenvolvido com **Flask** para gestão de usuários, agendamentos, feedbacks e controle administrativo. O sistema foi desenvolvido como parte de um projeto educacional com foco em práticas de backend, frontend e testes automatizados.

---

## 🚀 Funcionalidades

- Cadastro completo de usuários com upload de laudo
- Login e controle de sessões
- Perfis de acesso: administrador e funcionário
- Agendamento de consultas
- Envio de feedbacks
- Dashboard com estatísticas
- Exportação de dados para CSV
- Sistema de testes automatizados com `pytest`

---

## 🧪 Testes Automatizados

Os testes estão organizados na pasta `Relatorio de Teste/integracao` e cobrem:

- Página inicial (`/`)
- Login e logout
- Restrições de acesso a rotas protegidas

### ▶️ Executar os testes

para executar os teste:

```bash
python -m pytest Relatorio de Teste/integracao