# Buscadores AdaptaInfra

Este projeto é uma aplicação desenvolvida com Streamlit que integra dois buscadores:

- **Buscador Inteligente**: Pesquisa artigos e publicações acadêmicas usando a API OpenAlex.
- **Buscador de Especialistas**: Pesquisa especialistas (pesquisadores) usando a API ORCID, com filtros para país, área e idioma.

A aplicação oferece um menu central para selecionar o buscador desejado, e cada página preserva suas funcionalidades específicas, permitindo uma navegação simples e intuitiva.

## Funcionalidades

- **Menu Central**: Dois botões que direcionam para o Buscador Inteligente ou para o Buscador de Especialistas.
- **Buscador Inteligente**:
  - Pesquisa artigos na OpenAlex.
  - Exibe título, data de publicação, autores, resumo e link para o artigo.
- **Buscador de Especialistas**:
  - Pesquisa especialistas na API ORCID.
  - Exibe informações detalhadas (nome, biografia, instituição) do especialista.
  - Aplica filtros simulados (país, área e idioma) para refinar os resultados.

## Estrutura do Projeto

O projeto está dividido em três arquivos principais:

- **Artigos.py**: Contém o código do Buscador Inteligente.
- **Especialistas.py**: Contém o código do Buscador de Especialistas.
- **buscadores.py**: Arquivo principal que implementa o menu e realiza a navegação entre os buscadores.

Além disso, o projeto inclui:

- **logo.png**: Imagem utilizada na interface.
- **requirements.txt**: Lista de dependências do projeto.

## Pré-requisitos

Certifique-se de ter o Python (versão 3.7 ou superior) instalado. Você também precisará do [Streamlit](https://streamlit.io/) e da biblioteca [requests](https://pypi.org/project/requests/).

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/SEU_USUARIO/buscadores-adaptainfra.git
   cd buscadores-adaptainfra
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Executando a Aplicação

Para iniciar a aplicação, execute o seguinte comando no terminal:

```bash
streamlit run buscadores.py
```

A aplicação será aberta no navegador, e você poderá navegar entre os dois buscadores através do menu principal.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias ou correções.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---
