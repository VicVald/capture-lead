# Projeto Capturação de Leads - Victor Hugo

---

O projeto consiste em um fluxo de trabalho com agentes de IA que permitem uma captura de leads de forma consistente e rápida.

### 👨‍💻 Autor

---

**Victor Hugo Kawano Monteiro**

[
    ![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/victor-hugo-kawano-monteiro-b236152b6) [![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:victorhugokawano@gmail.com) [![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/5514997500603)

### 📚 Sobre o Projeto

---

Neste projeto foi utilizado técnicas de extração de dados e agentes para captura de informações onlines para compor a tabela de leads para contato, bem como utilização de modelos de linguagem para expor essas informações de maneira resumida auxiliando o usuário em uma análise de oportunidades.

Para melhor interação do usuário foi utilizado o Gradio para criação de uma interface web que recebe os inputs necessários e retorna a planilha com os resultados encontrados.

### 🗂️ Estrutura do Projeto

---

```
capture-lead/
├── README.md                   # Documentação do projeto
├── Dockerfile                  # Construção do container Docker
├── .env                        # Variáveis de ambiente
├── requirements.txt            # Dependências do projeto
├── src/
│   ├── agent/
│   │   ├── __init__.py         # Inicialização do módulo de agentes
│   │   ├── nodes.py            # Definição dos nós de agentes
│   │   └── state.py            # Definição do estado do agente
│   ├── utils/
│   │   └── locations.json      # Base de dados de localizações
│   └── app.py                  # Script principal para execução do projeto
```

### 🐳 Como usar com Docker

---

1. Clonar o respositório

   ```
   https://github.com/VicVald/capture-lead.git
   cd lead-capture
   ```
2. Configure as variáveis de ambiente

   ```
   cp .env.example .env
   ```
3. Coloque suas chaves de API

   ```
   SERPAPI_KEY = sua_chave_serpapi | https://serpapi.com/manage-api-key
   TAVILY_API_KEY = sua_chave_tavily | https://app.tavily.com/home
   GROQ_API_KEY = sua_chave_groq | https://console.groq.com/keys
   ```
4. Construa sua imagem Docker

   ```
   docker build -t lead-capture .
   ```
5. Execute o container

   ```
   docker run -p 7860:7860 lead-capture
   ```

### 🛠️ Como utilizar

---

Após iniciar a aplicação com no navegador adicione as informações da sua busca:

- Niche: Palavra-chave para fazer a busca de empresas
- Locations: Lista de cidades para fazer a busca
- Role: Sua função do produto (Exemplo: Web Developer caso você queira prospectar clientes para oferece-los serviços dessa área)

Vai ser gerada uma prévia da sua tabela e o arquivo para baixá-la no final da página.

### 💻 Implementações Futuras

---

- Mensagens personalizadas para cada cliente ou tentativas de comunicação

Desenvolvido por: Victor Hugo Kawano Monteiro
