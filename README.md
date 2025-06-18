# 🗂️ Sistema de Enquetes Django

Sistema web para criação e gerenciamento de enquetes, desenvolvido em **Python + Django**. Permite criar perguntas com múltiplas opções, controlar data de encerramento das enquetes e gerenciar votos via painel administrativo do Django.

---

## 🚀 Tecnologias Utilizadas
- **Backend:** Python, Django
- **Banco de Dados:** SQLite (padrão) / PostgreSQL (opcional)
- **Admin:** Django Admin para gerenciamento das enquetes

---

## 🏗️ Funcionalidades
- ✅ Cadastro e edição de enquetes via painel administrativo  
- ✅ Adição de múltiplas opções para cada enquete  
- ✅ Controle de data de encerramento para bloquear votos  
- ✅ Visualização de status das enquetes (aberta/encerrada)  

---

## 🚀 Futuras melhorias
- 🚧 Implementar interface web pública para votação  
- 🚧 Criar página de resultados das enquetes  
- 🚧 Adicionar autenticação de usuários comuns  
- 🚧 Melhorar interface com CSS e frameworks front-end  
- 🚧 Migrar banco para PostgreSQL para ambiente de produção  
- 🚧 Implementar testes automatizados  

---

## 📦 Estrutura do Projeto

sistema_enquetes/

├── enquete/ # Aplicação Django para gerenciar enquetes  
│   ├── admin.py # Configuração do painel administrativo  
│   ├── models.py # Modelos Enquete e Opcao  
│   ├── views.py # Views (a implementar)  
│   ├── migrations/ # Migrações do banco de dados  
│   └── templates/ # Templates HTML (a implementar)  

├── sistema_enquetes/ # Configurações do projeto Django  
│   ├── settings.py  
│   ├── urls.py  
│   └── wsgi.py  

├── manage.py # Script para executar comandos Django  

└── venv/ # Ambiente virtual Python  

---

## 🔧 Como rodar o projeto localmente

1️⃣ Clone o repositório  
```bash
git clone <URL_DO_REPOSITORIO>
cd sistema_enquetes
2️⃣ Crie e ative o ambiente virtual

bash
Copiar
Editar
python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# Linux/macOS
source venv/bin/activate
3️⃣ Instale as dependências

bash
Copiar
Editar
pip install django
4️⃣ (Opcional) Configure banco PostgreSQL em sistema_enquetes/settings.py

5️⃣ Execute as migrações

bash
Copiar
Editar
python manage.py migrate
6️⃣ Crie um superusuário para acessar o admin

bash
Copiar
Editar
python manage.py createsuperuser
7️⃣ Inicie o servidor de desenvolvimento

bash
Copiar
Editar
python manage.py runserver
8️⃣ Acesse o painel administrativo
http://127.0.0.1:8000/admin/

👨‍💻 Desenvolvido por
Andre Lima
LinkedIn: André Crisóstomo Nobre Lima


