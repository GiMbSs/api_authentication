# API Flask - Sistema de Autenticação

Uma API REST simples desenvolvida em Flask para gerenciamento de usuários com sistema de autenticação.

## 📋 Funcionalidades

- ✅ Sistema de login/logout com sessões
- ✅ CRUD completo de usuários
- ✅ Autenticação obrigatória para operações sensíveis
- ✅ Validações de dados e segurança
- ✅ Banco de dados SQLite com SQLAlchemy

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.7+
- pip

### Instalação
```bash
# Clone o repositório
git clone git@github.com:GiMbSs/api_authentication.git
cd API_Flask

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
```

A API estará disponível em: `http://localhost:5000`

## 📚 Documentação das Rotas

### 🔐 Autenticação

#### POST `/login`
Realiza login do usuário no sistema.

**Requisição:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Validações:**
- ✅ Campos `username` e `password` são obrigatórios
- ✅ Credenciais devem existir no banco de dados
- ✅ Verifica se usuário já está logado

**Respostas:**
- `200`: Login realizado com sucesso
- `403`: Credenciais inválidas
- `200`: Usuário já está logado

**Exemplo:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'
```

#### GET `/logout`
Realiza logout do usuário autenticado.

**Validações:**
- 🔒 Requer autenticação (`@login_required`)

**Respostas:**
- `200`: Logout realizado com sucesso
- `401`: Usuário não autenticado

---

### 👥 Gerenciamento de Usuários

#### GET `/users/<int:user_id>`
Busca um usuário específico pelo ID.

**Validações:**
- 🔒 Requer autenticação (`@login_required`)
- ✅ ID deve ser um número inteiro
- ✅ Usuário deve existir no banco

**Respostas:**
- `200`: Usuário encontrado
- `404`: Usuário não encontrado
- `401`: Usuário não autenticado

**Exemplo de resposta:**
```json
{
    "id": 1,
    "username": "admin"
}
```

#### GET `/users/all`
Lista todos os usuários cadastrados.

**Validações:**
- 🔒 Requer autenticação (`@login_required`)
- ✅ Verifica se existem usuários no banco

**Respostas:**
- `200`: Lista de usuários retornada
- `404`: Nenhum usuário encontrado
- `401`: Usuário não autenticado

**Exemplo de resposta:**
```json
[
    {
        "id": 1,
        "username": "admin"
    },
    {
        "id": 2,
        "username": "usuario2"
    }
]
```

#### POST `/create_user`
Cria um novo usuário no sistema.

**Requisição:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Validações:**
- 🔒 Requer autenticação (`@login_required`)
- ✅ Campos `username` e `password` são obrigatórios
- ✅ Username deve ser único (não pode existir)
- ✅ Dados devem ser válidos

**Respostas:**
- `201`: Usuário criado com sucesso
- `400`: Username já existe ou dados inválidos
- `401`: Usuário não autenticado

#### PUT `/update_user/<int:user_id>`
Atualiza dados de um usuário existente.

**Requisição:**
```json
{
    "username": "string (opcional)",
    "password": "string (opcional)"
}
```

**Validações:**
- 🔒 Requer autenticação (`@login_required`)
- ✅ ID deve ser um número inteiro
- ✅ Usuário deve existir no banco
- 🚫 **Regra especial**: Usuário logado não pode alterar o próprio username
- ✅ Pelo menos um campo deve ser fornecido

**Respostas:**
- `200`: Usuário atualizado com sucesso
- `400`: Tentativa de alterar próprio username
- `404`: Usuário não encontrado
- `401`: Usuário não autenticado

#### DELETE `/delete_user/<int:user_id>`
Remove um usuário do sistema.

**Validações:**
- 🔒 Requer autenticação (`@login_required`)
- ✅ ID deve ser um número inteiro
- ✅ Usuário deve existir no banco
- ✅ Usuário a ser deletado deve ser diferente do logado

**Respostas:**
- `200`: Usuário deletado com sucesso
- `404`: Usuário não encontrado
- `401`: Usuário não autenticado

---

## 🛡️ Sistema de Segurança

### Autenticação
- Utiliza **Flask-Login** para gerenciamento de sessões
- Middleware `@login_required` protege rotas sensíveis
- Sistema de cookies para manter sessão ativa

### Validações Implementadas

1. **Autenticação Obrigatória**: Todas as rotas exceto `/login` requerem usuário autenticado
2. **Validação de Dados**: Verifica se campos obrigatórios estão presentes
3. **Unicidade de Username**: Impede criação de usuários duplicados
4. **Proteção de Autoedição**: Usuário logado não pode alterar próprio username
5. **Existência de Recursos**: Verifica se usuário existe antes de operações

### Headers Necessários
```
Content-Type: application/json
```

## 🗄️ Banco de Dados

- **Tipo**: SQLite (`api.db`)
- **ORM**: SQLAlchemy
- **Usuário Padrão**: admin/admin (criado automaticamente)

### Estrutura da Tabela User
```sql
- id: INTEGER (Primary Key)
- username: VARCHAR (Unique)
- password: VARCHAR
```

## 📦 Dependências

Principais bibliotecas utilizadas:
- **Flask 3.1.2**: Framework web
- **Flask-Login 0.6.3**: Gerenciamento de autenticação
- **Flask-SQLAlchemy 3.1.1**: ORM para banco de dados
- **SQLAlchemy 2.0.44**: Toolkit SQL

## 🧪 Testando a API

### 1. Fazer Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}' \
  -c cookies.txt
```

### 2. Listar Usuários (com cookies)
```bash
curl -X GET http://localhost:5000/users/all \
  -b cookies.txt
```

### 3. Criar Novo Usuário
```bash
curl -X POST http://localhost:5000/create_user \
  -H "Content-Type: application/json" \
  -d '{"username": "novo_usuario", "password": "senha123"}' \
  -b cookies.txt
```

### 4. Fazer Logout
```bash
curl -X GET http://localhost:5000/logout \
  -b cookies.txt
```

## ⚠️ Observações Importantes

- ⚠️ **Segurança**: Esta é uma implementação básica para estudos. Em produção, use:
  - Hash das senhas (bcrypt, scrypt, etc.)
  - HTTPS obrigatório
  - Validação mais robusta de entrada
  - Rate limiting
  - Tokens JWT ou OAuth2

- 📝 **Desenvolvimento**: O modo debug está ativado (`debug=True`)
- 🔑 **Secret Key**: Altere a `SECRET_KEY` em produção

## 📄 Licença

Este projeto é apenas para fins educacionais.