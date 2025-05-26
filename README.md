# 🧠 Buscadores – Pesquisa Inteligente de Auditorias, Publicações e Especialistas

[![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-red?logo=streamlit)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/database-SQLite-blue?logo=sqlite)](https://sqlite.org)
[![Python](https://img.shields.io/badge/python-3.11+-green?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![image](https://github.com/user-attachments/assets/1dd29a0b-c5a8-472c-b9f4-5c5bc66a3bca)


O **Buscadores** é uma aplicação interativa desenvolvida com [Streamlit](https://streamlit.io/) para facilitar o acesso e a análise de artigos, publicações, ferramentas e especialistas no contexto de auditorias, transparência pública e adaptação às mudanças climáticas na América Latina e Caribe.

## 🚀 Funcionalidades

- 🔎 **Busca inteligente** por artigos e publicações usando análise textual;
- 👤 **Consulta de especialistas** por área de atuação, com base em bases como ORCID e OpenAlex;
- 🛠️ **Ferramentas OLACEFS** integradas via API (`https://datos.olacefs.com`);
- 💬 **Chatbot** com IA para responder perguntas sobre os dados integrados;
- 🧠 **Histórico de buscas e feedbacks** armazenados em banco SQLite;
- 📊 Interface simples, rápida e intuitiva com layout responsivo.

## 📂 Estrutura dos Módulos

```
BUSCADORES/
├── Artigos.py            # Lógica de busca e exibição de artigos
├── Especialistas.py      # Busca e exibição de especialistas
├── Olacefs.py            # Integração com dados e ferramentas OLACEFS
├── Chatbot.py            # Interface com assistente baseado em IA
├── db.py                 # Modelos ORM e conexão com SQLite
├── db_view.py            # Visualização de dados armazenados
├── buscadores.py         # Arquivo principal da aplicação Streamlit
├── uploads/              # Uploads de arquivos e documentos
├── buscadores.db         # Banco de dados local
├── modelo_ia.py          # Vetorização e machine learning (se aplicável)
├── requirements.txt      # Dependências do projeto
└── README.md             # Este arquivo
```

## ⚙️ Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/todydanielm3/buscadores-adaptainfra.git
cd buscadores-adaptainfra
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a aplicação:

```bash
streamlit run buscadores.py
```

Acesse em [http://localhost:8501](http://localhost:8501) no seu navegador.

## 🧠 Requisitos

- Python 3.11+
- Streamlit
- SQLAlchemy
- scikit-learn (para vetorização e clustering)
- Requests, Pandas, entre outras (listadas no `requirements.txt`)

## 📌 Observações Técnicas

- As buscas por artigos e especialistas são processadas localmente e integradas via API.
- O histórico de interações é salvo no banco SQLite (`buscadores.db`) para análise posterior.
- O projeto segue os princípios de [Desenvolvimento Digital Responsável](https://digitalprinciples.org/).

## 🤝 Contribuições

Sinta-se livre para contribuir! Sugestões de melhorias, novos módulos de busca ou integração com novas APIs são bem-vindas.

1. Fork este repositório
2. Crie sua branch: `git checkout -b feature/nova-funcionalidade`
3. Commit suas alterações: `git commit -m 'feat: nova funcionalidade'`
4. Push para a branch: `git push origin feature/nova-funcionalidade`
5. Crie um Pull Request

## Variável de ambiente para o Gemini

> > > export GOOGLE_API_KEY="SUA_CHAVE_AQUI"

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
