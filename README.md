🗂️ Gerenciador de Projetos
Sistema de gerenciamento de projetos desenvolvido em Python + Flask, com banco de dados MySQL, que permite cadastrar projetos, ambientes, materiais e mobiliários. Suporte a múltiplos usuários, com autenticação e gerenciamento completo via API RESTful.

🚀 Tecnologias Utilizadas
Backend: Python, Flask, Flask-CORS
Banco de Dados: MySQL
Segurança: Bcrypt para hash de senhas
Arquitetura: RESTful + Blueprints (modular)
🏗️ Funcionalidades
✅ Autenticação de usuários (login e cadastro)
✅ Criação e gerenciamento de projetos
✅ Adição de membros aos projetos
✅ Gerenciamento de ambientes dentro dos projetos
✅ Cadastro de materiais e mobiliários para cada ambiente
✅ Operações completas de CRUD:
Projetos
Ambientes
Materiais
Mobiliários
✅ Validação de dados e segurança nas operações
🛠️ melhorias aplicadas

✅ Resolvi o problema de N+1 querys na rota de projetos

🛠️ Futuras melhorias

🚧 Integração com frontend (React, Vue ou outro)

🚧 Deploy na nuvem (Render)

🚧 Implementação de autenticação via JWT

🚧 Logs e tratamento de erros mais robusto

🚧 Testes automatizados

📦 Estrutura do Projeto
gerenciador/

├── main.py # Arquivo principal para iniciar a aplicação

├── db_config.py # Configuração e conexão com o banco de dados

├── blueprints/ # Rotas organizadas em blueprints

│ ├── init.py

│ ├── login.py # Rotas relacionadas a login e autenticação

│ ├── materiais.py # Rotas para gerenciamento de materiais

│ ├── mobiliarios.py # Rotas para gerenciamento de mobiliários

│ ├── projetos.py # Rotas para gerenciamento de projetos

│ └── usuarios.py # Rotas para gerenciamento de usuários

├── imagens/ # Diretório para armazenar imagens dos materiais

└── requirements.txt # Dependências do projeto

🔗 Principais Rotas da API
🔐 Autenticação
Método	Endpoint	Descrição
POST	/cadastro	Cadastro de usuário
POST	/login	Login de usuário
📁 Projetos
Método	Endpoint	Descrição
GET	/projetos	Listar todos os projetos
POST	/projetos	Criar um novo projeto
PUT	/projetos/:id	Atualizar um projeto
DELETE	/projetos/:id	Deletar um projeto
🏢 Ambientes
Método	Endpoint	Descrição
GET	/ambientes	Listar ambientes
POST	/ambientes	Criar ambiente
PUT	/ambientes/:id	Atualizar ambiente
DELETE	/ambientes/:id	Deletar ambiente
🏗️ Materiais
Método	Endpoint	Descrição
GET	/materiais	Listar materiais
POST	/materiais	Criar material
PUT	/materiais/:id	Atualizar material
DELETE	/materiais/:id	Deletar material
🪑 Mobiliários
Método	Endpoint	Descrição
GET	/mobiliarios	Listar mobiliários
POST	/mobiliarios	Criar mobiliário
PUT	/mobiliarios/:id	Atualizar mobiliário
DELETE	/mobiliarios/:id	Deletar mobiliário
🔧 Como rodar o projeto localmente
1️⃣ Clone o repositório
git clone https://github.com/seu-usuario/gerenciador.git
cd gerenciador

2️⃣ Crie e ative um ambiente virtual
bash
Copiar
Editar
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
3️⃣ Instale as dependências
bash
Copiar
Editar
pip install -r requirements.txt
4️⃣ Configure o banco de dados
Crie um banco de dados MySQL chamado gerenciador.

Configure as credenciais no arquivo db_config.py.

5️⃣ Execute o projeto
bash
Copiar
Editar
python app.py
O servidor estará rodando em:
➡️ http://localhost:5000

---

👨‍💻 Desenvolvido por
Andre Lima
 LinkedIn: André Crisóstomo Nobre Lima 
