# **Buscador Inteligente**

Conecta pesquisadores às publicações mais relevantes e a especialistas da área – tudo em uma única interface construída com **Streamlit** e integrada ao **Google Gemini**.

---

## ✨ Funcionalidades

| Módulo               | O que faz                                                                                                                            |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Artigos**          | Pesquisa artigos em bases abertas (OpenAlex). Exibe título, autores, resumo, data e link.                                            |
| **Especialistas**    | Consulta perfis no ORCID. Mostra nome, instituição, biografia resumida e filtros (país, área e idioma) _mockados_ para demonstração. |
| **Chatbot VerichIA** | Assistente virtual que responde em linguagem natural utilizando o modelo **Gemini**.                                                 |

---

🛠️ Pré‑requisitos
• Python ≥ 3.8
• Streamlit
• requests
• Chave de API do Google Gemini

⸻

⚙️ Instalação

Clone este repositório.
cd buscador-inteligente

python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt

# variável de ambiente para o Gemini

export GOOGLE_API_KEY="SUA_CHAVE_AQUI"

⸻

▶️ Executando localmente

streamlit run app.py

A aplicação abrirá em http://localhost:8501.

⸻

🚀 Deploy (opcional)

O arquivo .github/workflows/deploy.yml contém um fluxo básico de CI/CD para implantação em Streamlit Community Cloud.
A única secret necessária é:
• GOOGLE_API_KEY

⸻

📝 Licença

Distribuído sob a licença MIT. Consulte LICENSE para obter mais informações.
