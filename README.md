# 🎬 Sistema de Programações de Filmes

Este projeto implementa um sistema web interativo utilizando **MySQL** como banco de dados relacional e **Streamlit** como framework para a interface gráfica. O sistema permite gerenciar programações de filmes através de operações CRUD (Create, Read, Update, Delete) e inclui funcionalidades avançadas como **triggers** e **consultas SQL não triviais**.

## 📋 Descrição do Projeto

O sistema foi desenvolvido com o objetivo de gerenciar as informações relacionadas a **Filmes**, **Canais** de exibição e **Exibições** de filmes, permitindo ao usuário:

- **Cadastrar novos filmes, canais e exibições**.
- **Consultar** as programações de filmes e suas exibições.
- **Atualizar** informações de filmes ou canais já cadastrados.
- **Remover** dados quando necessário, com a devida aplicação de **integridade referencial**.
- Executar um **gatilho (trigger)** para garantir consistência e automação.

O projeto contempla um **DER** (Diagrama Entidade-Relacionamento) com três tabelas principais: `Filme`, `Canal`, e `Exibição`, todas **normalizadas até a 3ª Forma Normal**.

## 🚀 Funcionalidades Principais

- **CRUD Completo**: Gerenciamento de filmes, canais e exibições.
- **Trigger**: Automatiza uma ação específica após a modificação de dados.
- **Consultas Avançadas**: Utiliza **junções**, **agrupamento** e **agregação** para exibir informações complexas.
- **Integridade Referencial**: Aplica **chaves estrangeiras (FK)** com tratamento para **remoção e atualização em cascata**.

## 🎯 Objetivos do Sistema

- Garantir um sistema funcional que permita a interação completa com o banco de dados.
- Demonstrar a normalização das tabelas até a **3ª Forma Normal**.
- Mostrar a implementação prática de triggers e restrições de integridade.
- Produzir um vídeo explicativo de 15 minutos sobre o projeto e suas funcionalidades.

## 🛠️ Tecnologias Utilizadas

- **MySQL**: Banco de dados relacional utilizado para armazenamento e gestão das tabelas.
- **Streamlit**: Framework em Python para construção da interface gráfica interativa.
- **Python**: Linguagem de programação usada para conectar o banco de dados com a interface.
- **SQL**: Para as consultas ao banco de dados, incluindo **junções**, **agregações** e **filtragens**.
- **Bibliotecas Python**:
  - `mysql-connector-python`: Para conectar o Streamlit com o MySQL.
  - `pandas`: Manipulação e exibição de dados na interface.
  - `streamlit`: Desenvolvimento do front-end.

## 🗂️ Estrutura do Projeto

```bash
├── 📁 scripts_sql       # Contém o script SQL de criação e popular as tabelas
├── 📁 streamlit         # Contém o código-fonte do sistema
│   ├── 📄 app.py        # Arquivo principal do sistema em Streamlit
│   ├── 📄 crud.py       # Operações CRUD no banco de dados
│   └── 📄 db_connect.py # Funções para conexão com o MySQL
├── 📄 README.md         # Este arquivo
└── 📄 requirements.txt  # Dependências do projeto
