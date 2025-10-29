# API Flask - Sistema de Autenticação

Uma API REST simples desenvolvida em Flask para gerenciamento de usuários com sistema de autenticação.

## 📋 Funcionalidades

- ✅ Sistema de login/logout com sessões
- ✅ CRUD completo de usuários
- ✅ **Sistema de roles/permissões** (user, admin, master)
- ✅ **Criptografia de senhas** com bcrypt
- ✅ Autenticação obrigatória para operações sensíveis
- ✅ **Controle de acesso baseado em roles**
- ✅ Validações de dados e segurança avançadas
- ✅ Banco de dados SQLite com SQLAlchemy
- ✅ **Timestamps automáticos** (created_at, updated_at)

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
- ✅ **Senha é verificada com hash bcrypt**
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
- 🛡️ **Requer permissão de admin** (role admin ou master)
- ✅ Verifica se existem usuários no banco

**Respostas:**
- `200`: Lista de usuários retornada
- `403`: Usuário sem permissão de admin
- `404`: Nenhum usuário encontrado
- `401`: Usuário não autenticado

**Exemplo de resposta:**
```json
[
    {
        "id": 1,
        "username": "admin",
        "role": "master"
    },
    {
        "id": 2,
        "username": "usuario2",
        "role": "user"
    }
]
```

#### POST `/create_user`
Cria um novo usuário no sistema.

**Requisição:**
```json
{
    "username": "string",
    "password": "string",
    "role": "string (opcional - apenas para masters)"
}
```

**Validações:**
- 🔒 Requer autenticação (`@login_required`)
- 🛡️ **Requer permissão de admin** (role admin ou master)
- ✅ Campos `username` e `password` são obrigatórios
- ✅ **Senha é automaticamente criptografada** com bcrypt
- ✅ Username deve ser único (não pode existir)
- 🎭 **Role padrão é 'user'** (apenas masters podem definir roles)
- ✅ Dados devem ser válidos

**Respostas:**
- `201`: Usuário criado com sucesso
- `400`: Username já existe ou dados inválidos
- `403`: Usuário sem permissão de admin
- `401`: Usuário não autenticado

#### PUT `/update_user/<int:user_id>`
Atualiza dados de um usuário existente.

**Requisição:**
```json
{
    "username": "string (opcional)",
    "password": "string (opcional)",
    "role": "string (opcional - apenas para masters)"
}
```

**Validações:**
- 🔒 Requer autenticação (`@login_required`)
- ✅ ID deve ser um número inteiro
- ✅ Usuário deve existir no banco
- 🛡️ **Usuários comuns só podem atualizar o próprio perfil**
- 🚫 **Regra especial**: Usuário logado não pode alterar o próprio username
- ✅ **Senha é automaticamente criptografada** com bcrypt
- 🎭 **Apenas masters podem alterar roles**
- ✅ Pelo menos um campo deve ser fornecido

**Respostas:**
- `200`: Usuário atualizado com sucesso
- `400`: Tentativa de alterar próprio username
- `403`: Sem permissão para alterar usuário/role
- `404`: Usuário não encontrado
- `401`: Usuário não autenticado

#### DELETE `/delete_user/<int:user_id>`
Remove um usuário do sistema.

**Validações:**
- 🔒 Requer autenticação (`@login_required`)
- 🛡️ **Requer permissão de admin** (role admin ou master)
- ✅ ID deve ser um número inteiro
- ✅ Usuário deve existir no banco
- 🚫 **Usuário não pode deletar a própria conta**
- 🎭 **Apenas masters podem deletar outros admins/masters**

**Respostas:**
- `200`: Usuário deletado com sucesso
- `400`: Tentativa de deletar própria conta
- `403`: Sem permissão para deletar usuário
- `404`: Usuário não encontrado
- `401`: Usuário não autenticado

---

## 🛡️ Sistema de Segurança

### Autenticação
- Utiliza **Flask-Login** para gerenciamento de sessões
- Middleware `@login_required` protege rotas sensíveis
- Sistema de cookies para manter sessão ativa

### 🎭 Sistema de Roles (Novo!)

#### Hierarquia de Permissões:
1. **`user`** - Usuário comum
   - ✅ Pode visualizar próprio perfil
   - ✅ Pode atualizar próprio perfil
   - ❌ Não pode criar/deletar usuários
   - ❌ Não pode listar todos os usuários

2. **`admin`** - Administrador
   - ✅ Todas as permissões de `user`
   - ✅ Pode criar novos usuários (apenas role 'user')
   - ✅ Pode listar todos os usuários
   - ✅ Pode deletar usuários comuns
   - ❌ Não pode alterar roles
   - ❌ Não pode deletar outros admins/masters

3. **`master`** - Super Administrador
   - ✅ Todas as permissões de `admin`
   - ✅ Pode criar usuários com qualquer role
   - ✅ Pode alterar roles de qualquer usuário
   - ✅ Pode deletar qualquer usuário (exceto própria conta)

### 🔐 Criptografia de Senhas (Novo!)
- **bcrypt**: Todas as senhas são hasheadas com salt
- **Segurança**: Senhas nunca são armazenadas em texto plano
- **Verificação**: Login usa comparação segura de hash

### Validações Implementadas

1. **Autenticação Obrigatória**: Todas as rotas exceto `/login` requerem usuário autenticado
2. **Controle de Acesso por Role**: Operações sensíveis verificam permissões
3. **Validação de Dados**: Verifica se campos obrigatórios estão presentes
4. **Unicidade de Username**: Impede criação de usuários duplicados
5. **Proteção de Autoedição**: Usuário logado não pode alterar próprio username
6. **Proteção de Autodeleção**: Usuário não pode deletar própria conta
7. **Hierarquia de Roles**: Admins não podem deletar outros admins
8. **Criptografia Automática**: Senhas são automaticamente hasheadas
9. **Existência de Recursos**: Verifica se usuário existe antes de operações

### Headers Necessários
```
Content-Type: application/json
```

## 🗄️ Banco de Dados

- **Tipo**: SQLite (`api.db`)
- **ORM**: SQLAlchemy
- **Usuário Padrão**: admin/admin (role: master, criado automaticamente)

### Estrutura da Tabela User
```sql
- id: INTEGER (Primary Key)
- username: VARCHAR (Unique)
- password: VARCHAR (Hash bcrypt)
- role: VARCHAR (user/admin/master)
- created_at: DATETIME (Timestamp automático)
- updated_at: DATETIME (Atualização automática)
```

## 📦 Dependências

Principais bibliotecas utilizadas:
- **Flask 3.1.2**: Framework web
- **Flask-Login 0.6.3**: Gerenciamento de autenticação
- **Flask-SQLAlchemy 3.1.1**: ORM para banco de dados
- **SQLAlchemy 2.0.44**: Toolkit SQL
- **bcrypt**: Criptografia de senhas (Nova dependência)

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

### 3. Criar Novo Usuário (como Admin/Master)
```bash
curl -X POST http://localhost:5000/create_user \
  -H "Content-Type: application/json" \
  -d '{"username": "novo_usuario", "password": "senha123", "role": "user"}' \
  -b cookies.txt
```

### 4. Atualizar Usuário (alterar role - apenas master)
```bash
curl -X PUT http://localhost:5000/update_user/2 \
  -H "Content-Type: application/json" \
  -d '{"role": "admin"}' \
  -b cookies.txt
```

### 5. Fazer Logout
```bash
curl -X GET http://localhost:5000/logout \
  -b cookies.txt
```

## ⚠️ Observações Importantes

- ✅ **Segurança Melhorada**: Implementação com bcrypt e sistema de roles
- 🎭 **Sistema de Permissões**: Controle granular de acesso
- 🔐 **Senhas Seguras**: Hash bcrypt com salt automático
- ⚠️ **Para Produção**: Ainda recomendamos:
  - HTTPS obrigatório
  - Validação mais robusta de entrada
  - Rate limiting
  - Tokens JWT ou OAuth2
  - Logs de auditoria

- 📝 **Desenvolvimento**: O modo debug está ativado (`debug=True`)
- 🔑 **Secret Key**: Altere a `SECRET_KEY` em produção

## 🆕 Changelog - Novas Funcionalidades

### v2.0 - Sistema de Roles e Segurança Avançada
- ✅ **Sistema de Roles**: user, admin, master
- ✅ **Criptografia bcrypt**: Senhas hasheadas com salt
- ✅ **Controle de Acesso**: Permissões baseadas em roles
- ✅ **Timestamps**: created_at e updated_at automáticos
- ✅ **Validações Avançadas**: Proteção contra auto-deleção e hierarquia de roles
- ✅ **Usuário Master**: admin/admin com role master por padrão

## 📄 Licença

Este projeto é apenas para fins educacionais.