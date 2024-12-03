# 🚌 Projeto Busão, Ferramenta para Gestão de Campanhas de Transporte

Bem-vindo ao repositório do **Busão - Sistema de Gestão de Campanhas de Transporte**! 🚍 Este projeto foi desenvolvido para facilitar a organização e administração de campanhas envolvendo equipes de transporte, rotas e usuários, com foco na eficiência e na experiência do usuário.

O projeto se encontra na versão 1 (v1), portanto não está finalizado.

---

## ✨ **Principais Funcionalidades**
- **Gestão de Campanhas**: Criação, edição e exclusão de campanhas com informações detalhadas.
- **Gerenciamento de Equipes**: Adição e remoção de administradores, motoristas e auxiliares diretamente vinculados a cada campanha.
- **Rotas Personalizadas**: Organização de itinerários associados às campanhas para maior flexibilidade e controle.
- **Painel Administrativo**: Interface amigável para acompanhar campanhas, equipes e usuários.
- **Login Automatizado**: Registro e autenticação de novos usuários com fluxo ágil e seguro.

---

## 🛠️ **Tecnologias Utilizadas**
- **Back-end**: Django (Python)
- **Banco de Dados**: SQL Server 2016
- **Front-end**: Bootstrap 5 para um design responsivo e moderno
- **Templates**: Django Templates, com personalização utilizando HTML5 e CSS3
- **JSON**: Importação de estados e municípios brasileiros para facilitar o gerenciamento de localizações.

---

## 🚀 **Como Executar o Projeto**
### Pré-requisitos
1. **Python 3.10 ou superior** instalado.
2. **Banco de Dados PostgreSQL** configurado.
3. Clonar este repositório:
   ```bash
   git clone https://github.com/seu-usuario/sistema-campanha-transporte.git
   cd sistema-campanha-transporte
   ```

### Configuração
1. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o banco de dados no arquivo ```settings.py```:
   ```python
   DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": "NomeDoBanco",
        "USER": "sa",
        "PASSWORD": "senha",
        "HOST": "localhost",
        "PORT": "1433",
        "OPTIONS": {"driver": "ODBC Driver 18 for SQL Server",
                    "extra_params": "TrustServerCertificate=yes",
        },
    },
}
   ```

4. Execute o arquivo ```.\env.bat```

5. Carregue os dados de estados e municípios, executando ```.\import.bat```

### Executando
Inicie o servidor: ```.\run.bat```

Acesse o sistema em: [http://localhost:8000](http://localhost:8000)

---

## 🌟 **Destaques**
### 📋 Cadastro e Autenticação
Fluxo simplificado para que usuários possam criar contas e acessar suas campanhas rapidamente.

### 👥 Gestão de Equipe
- Adicione administradores, motoristas ou auxiliares às campanhas.
- Controle funções e permissões facilmente.

### 📍 Organização de Rotas
Defina itinerários detalhados e horários otimizados.

### 📊 Painel Intuitivo
Acompanhe todos os dados de sua campanha em um painel unificado e responsivo.

---

## 📂 **Estrutura do Projeto**
```plaintext
├── controller/              # Configurações do projeto
├── media/                   # Arquivos de midia do usuário
├── static/                  # Arquivos estáticos (CSS, JS, imagens)
├── venv/                    # Gerenciamento de itinerários
├── views/                   # Aplicações do Django
└── manage.py                # Script de gerenciamento do Django
```

---

## 🤝 **Contribuições**
Contribuições são bem-vindas! Se você tiver sugestões ou quiser relatar problemas, sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_.

---

Se gostou deste repositório, não esqueça de dar uma ⭐️! 

**Obrigado pela atenção! 🚀**
