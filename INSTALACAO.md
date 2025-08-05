# 🚀 Guia de Instalação - OLASIS Menu Moderno

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

### 1. **Instalar Dependências**

```bash
# Instalar o Streamlit e outras dependências
pip install streamlit pandas numpy
pip install google-generativeai python-dotenv
pip install langchain langchain-community langchain-google-genai
pip install faiss-cpu scikit-learn
pip install requests beautifulsoup4
```

### 2. **Configurar Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
GOOGLE_API_KEY=sua_chave_da_api_gemini_aqui
```

### 3. **Executar o Sistema**

```bash
# Navegar para a pasta app
cd app

# Executar o Streamlit
streamlit run main.py
```

## 🎨 Funcionalidades do Novo Design

### ✨ **Melhorias Visuais**
- [x] Header moderno com efeito de vidro
- [x] Logo interativo OLASIS
- [x] Barra de busca elegante
- [x] Botões com gradientes
- [x] Chatbot redesenhado
- [x] Animações suaves
- [x] Design 100% responsivo

### 🌐 **Responsividade**
- [x] Mobile (≤ 768px)
- [x] Tablet (769px - 1024px)  
- [x] Desktop (≥ 1200px)

### 🎯 **Interatividade**
- [x] Busca com Enter
- [x] Hover effects
- [x] Toggle do chatbot
- [x] Animações de entrada

## 📱 Como Testar

### **Desktop**
1. Abra o navegador
2. Acesse `http://localhost:8501`
3. Teste todos os botões e interações

### **Mobile**
1. Use o modo desenvolvedor do navegador
2. Simule dispositivos móveis
3. Teste responsividade

### **Funcionalidades**
- Clique no logo OLASIS
- Teste a barra de busca
- Clique nos botões principais
- Abra/feche o chatbot
- Teste navegação

## 🎨 Paleta de Cores

```css
Azul Principal:    #004FA5
Azul Secundário:   #0072BB
Azul Ativo:        #00ACEC
Texto:             #333333
Fundo:             #FFFFFF
Cinza Claro:       #f8f9fa
Cinza Médio:       #e9ecef
Cinza Escuro:      #6c757d
```

## 📂 Estrutura de Arquivos

```
app/
├── main.py                 # 🎯 Arquivo principal com novo design
├── artigos.py             # 📚 Módulo de artigos
├── especialistas.py       # 👥 Módulo de especialistas  
├── olacefs.py            # 🔧 Módulo OLACEFS
├── chatbot.py            # 💬 Chatbot modernizado
├── db_view.py            # 📊 Visualização de dados
└── assets/
    ├── logo.png           # 🖼️ Logo principal
    ├── VerichIA.png       # 🤖 Avatar do chatbot
    └── modern_styles.css  # 🎨 Estilos CSS separados
```

## 🐛 Resolução de Problemas

### **Módulo não encontrado**
```bash
pip install nome_do_modulo
```

### **Streamlit não inicia**
```bash
# Verificar se está na pasta correta
cd app
streamlit run main.py
```

### **Estilos não carregam**
- Verificar conexão com internet (Google Fonts)
- Limpar cache do navegador
- Testar em modo incógnito

### **Responsividade não funciona**
- Testar em navegadores diferentes
- Verificar media queries no código
- Usar ferramentas de desenvolvedor

## 📈 Performance

### **Otimizações Aplicadas**
- CSS inline para elementos críticos
- Transições GPU-accelerated
- Lazy loading quando possível
- Minificação automática pelo Streamlit

### **Métricas Esperadas**
- Tempo de carregamento: < 2s
- First Paint: < 1s
- Interatividade: Imediata

## 🔄 Atualizações Futuras

### **Próximas Versões**
- [ ] PWA (Progressive Web App)
- [ ] Tema escuro completo
- [ ] Mais animações
- [ ] Cache avançado
- [ ] Offline support

### **Melhorias de UX**
- [ ] Feedback tátil
- [ ] Sounds effects
- [ ] Micro-interações avançadas
- [ ] Personalização de temas

## 📞 Suporte

### **Problemas Técnicos**
1. Verificar logs do terminal
2. Consultar documentação do Streamlit
3. Verificar versões das dependências

### **Problemas de Design**
1. Consultar `VISUAL_UPDATES.md`
2. Verificar CSS no navegador
3. Testar em diferentes dispositivos

## 🎉 Pronto para Usar!

Após seguir estes passos, você terá:
- ✅ Sistema funcionando
- ✅ Design moderno
- ✅ Responsividade completa
- ✅ Animações suaves
- ✅ UX otimizada

**Comando final:**
```bash
cd app && streamlit run main.py
```

---
*Última atualização: 29 de julho de 2025*
