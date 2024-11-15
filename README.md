# Conexão Solidária

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" width="100" height="30"/>
  <img src="https://img.shields.io/badge/Amazon%20Lex-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" width="100" height="30"/>
  <img src="https://img.shields.io/badge/Twilio-F22F46?style=for-the-badge&logo=twilio&logoColor=white" width="100" height="30"/>
  <img src="https://img.shields.io/badge/Amazon%20Polly-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" width="100" height="30"/>
  <img src="https://img.shields.io/badge/Amazon%20S3-569A31?style=for-the-badge&logo=amazonaws&logoColor=white" width="100" height="30"/>
  <img src="https://img.shields.io/badge/Amazon%20Rekognition-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" width="100" height="30"/>
  <img src="https://img.shields.io/badge/Amazon%20Bedrock-00A3E0?style=for-the-badge&logo=amazonaws&logoColor=white" width="100" height="30"/>
  <img src="https://img.shields.io/badge/API%20ViaCEP-0072C6?style=for-the-badge&logo=postman&logoColor=white" width="100" height="30"/>
  <img src="https://img.shields.io/badge/AWS%20Lambda-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" width="100" height="30"/>
  <img src="https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=amazonaws&logoColor=white" width="100" height="30"/>
  <img src="https://img.shields.io/badge/Amazon%20Transcribe-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" width="100" height="30"/>
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" width="100" height="30"/>
</p>


---

## **👥 Desenvolvedores**

| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/97261564?v=4" width="100" alt="Gusttavo Felipe">](https://github.com/gusttavofelipe) <br>[Gusttavo Felipe](https://github.com/gusttavofelipe) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/95103547?v=4" width="100" alt="Monique da Silva Borges">](https://github.com/niqueborges) <br>[Monique da Silva Borges](https://github.com/niqueborges) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/154631421?v=4" width="100" alt="Pedro Nunes">](https://github.com/PedroNunesBH) <br>[Pedro Nunes](https://github.com/PedroNunesBH) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/167145673?v=4" width="100" alt="Roger Dev">](https://github.com/Rogerdev02) <br>[Roger Dev](https://github.com/Rogerdev02) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/114765722?v=4" width="100" alt="Silvio CMJ">](https://github.com/SilvioCMJ) <br>[Silvio CMJ](https://github.com/SilvioCMJ) |
|:---:|:---:|:---:|:---:|:---:|

---

## **📜 Descrição**

**Conexão Solidária** é um chat interativo que conecta doadores a Instituições de caridade, com moderação de conteúdo para garantir segurança e qualidade. O sistema utiliza tecnologias AWS, incluindo **Amazon Lex**, **Amazon Rekognition**, e **Amazon Bedrock**, para criar um ambiente de confiança.

---

## **📑 Índice**

- [✨ Funcionalidades](#✨-funcionalidades)
- [⚙️ Arquitetura e Fluxo de Trabalho](#⚙️-arquitetura-e-fluxo-de-trabalho)
- [📦 Como Rodar a Aplicação](#📦-como-rodar-a-aplicação)
- [🚀 Deploy](#🚀-deploy)
- [💻 Tecnologias Utilizadas](#💻-tecnologias-utilizadas)
- [🗄️ Banco de Dados](#🗄️-banco-de-dados)
- [📂 Estrutura de Diretórios](#📂-estrutura-de-diretórios)
- [📅 Metodologia de Desenvolvimento](#📅-metodologia-de-desenvolvimento)
- [😿 Principais Dificuldades](#😿-principais-dificuldades)
- [📜 Termos de Uso](#📜-termos-de-uso)

---

## **✨ Funcionalidades**

1. **Chatbot Multicanal**: Interação integrada via **Amazon Lex** e **Twilio** para WhatsApp.
2. **Moderação Inteligente**: Utiliza **Amazon Rekognition** e **Bedrock** para moderação de imagens e textos.
3. **Acessibilidade Avançada**: Conversão de texto para áudio com **Amazon Polly**.
4. **Suporte Avançado**: Transcrição de áudio para texto usando **Amazon Transcribe**.
5. **Geolocalização e Endereços**: Consulta eficiente via **API ViaCEP**.

---

## **⚙️ Arquitetura e Fluxo de Trabalho**

O projeto segue uma arquitetura serverless na AWS. Principais passos incluem:

1. **Interação via Chatbot**: Usuários interagem através de **Amazon Lex** no WhatsApp.
2. **Moderação de Conteúdo**: Imagens e textos são moderados utilizando **Amazon S3**, **Rekognition** e **Bedrock**.
3. **Armazenamento**: **DynamoDB** para persistência de dados, **AWS Lambda** para processamento.
4. **Diagrama da Arquitetura**
   ![Arquitetura](./assets/img/architecture.png)

---

## **📦 Como Rodar a Aplicação**

### **Pré-requisitos**:  
- Python 3.13  
- Credenciais AWS configuradas  
- Serverless Framework instalado  

### **Passos**:

```bash
git clone https://github.com/Compass-pb-aws-2024-JUNHO/sprints-9-10-pb-aws-junho.git grupo-1
cd grupo-1

   ```  
2. Instale as dependências:  
   ```bash  
   pip install -r requirements.txt  
   ```  
3. Configure as variáveis de ambiente:  
   ```bash  
   export AWS_ACCESS_KEY_ID=your_access_key  
   export AWS_SECRET_ACCESS_KEY=your_secret_key  
   ```  
4. Execute a aplicação localmente:  
   ```bash  
   python manage.py runserver  
   ```  

---  

## **🚀 Deploy**  

### **Passos**:  
1. Configure o arquivo `serverless.yml` com suas credenciais AWS.  
2. Realize o deploy com o Serverless Framework:  
   ```bash  
   serverless deploy  
   ```  
3. Acesse o chatbot via WhatsApp ou a aplicação web no URL fornecido pelo Serverless.  

---


## **💻 Tecnologias Utilizadas**

- **Amazon Bedrock**  
- **Amazon DynamoDB**  
- **Amazon Lex**  
- **Amazon Polly**  
- **Amazon Rekognition**  
- **Amazon S3**  
- **Amazon Transcribe**  
- **API ViaCEP**  
- **AWS Lambda**  
- **Django**  
- **Python**  
- **Twilio**

--- 

---

## **🗄️ Banco de Dados**

A estrutura de armazenamento das Instituições em **DynamoDB** segue o modelo abaixo:
![Banco de Dados](./assets/img/database.png)

---

## **📂 Estrutura de Diretórios**

Este repositório contém o código-fonte do projeto **Conexão Solidária**, com a divisão entre backend, integração com AWS, e o frontend da aplicação. Abaixo está a estrutura principal do repositório:

```plaintext
Sprints-9-10-PB-AWS-JUNHO/
├── assets/
│   └── img/
│       ├── architecture.png         # Imagem representando a arquitetura do projeto
│       └── database.png             # Imagem representando o design do banco de dados
├── chatbot/                         # Diretório principal do chatbot
│   ├── backend/                     # Backend do chatbot
│   ├── handlers/                    # Manipuladores para as interações do chatbot
│   │   ├── health.py                # Verificação de saúde do serviço
│   │   ├── lex.py                   # Manipulação de integração com o Amazon Lex
│   │   └── twilio.py                # Manipulação de integração com o Twilio
│   ├── intents/                     # Intenções definidas para o chatbot
│   │   ├── list.py                  # Intenção de listagem
│   │   ├── register.py              # Intenção de registro
│   │   └── tips.py                  # Intenção de dicas
│   ├── services/                    # Serviços auxiliares para o chatbot
│   │   ├── api.py                   # Serviço para chamada de APIs externas
│   │   ├── aws.py                   # Integração com serviços AWS
│   │   ├── lex.py                   # Serviço para integração com o Amazon Lex
│   │   ├── s3.py                    # Serviço para integração com o Amazon S3
│   │   └── via_cep_api.py           # Serviço para integração com a API ViaCEP
│   ├── utils/                       # Funções utilitárias e auxiliares
│   │   ├── content_type.py          # Funções relacionadas ao tipo de conteúdo
│   │   ├── decode.py                # Função para decodificação de dados
│   │   ├── download_media.py        # Função para download de mídia
│   │   ├── get_twilio_phone.py      # Função para obtenção do número de telefone do Twilio
│   │   ├── responses.py             # Funções para manipulação de respostas do chatbot
│   │   └── slots.py                 # Funções para manipulação de slots do chatbot
│   ├── requirements.txt             # Dependências Python do projeto
│   ├── serverless.yml               # Arquivo de configuração do Serverless
│   └── __init__.py                  # Inicializador de pacote Python
├── serverless/                      # Configurações do Serverless Framework
│   ├── api/                         # Diretório de APIs do Serverless
│   │   ├── v1/                      # Versão 1 da API
│   │   │   └── __init__.py          # Inicializador de pacote Python para a versão 1
│   │   └── __init__.py              # Inicializador de pacote Python para APIs
│   ├── core/                        # Lógica central e configurações
│   │   ├── config.py                # Arquivo de configurações
│   │   ├── exceptions.py            # Exceções personalizadas
│   │   └── __init__.py              # Inicializador de pacote Python
│   ├── domain/                      # Lógica de negócio
│   │   ├── services/
│   │   │   ├── institution.py       # Serviço para gerenciar instituições
│   │   │   └── __init__.py          # Inicializador de pacote Python
│   │   └── __init__.py              # Inicializador de pacote Python
│   ├── infra/                       # Serviços de infraestrutura (AWS)
│   │   ├── aws/                     # Módulos específicos para integração com AWS
│   │   │   ├── bedrock.py           # Integração com o Amazon Bedrock
│   │   │   ├── polly.py             # Integração com o Amazon Polly
│   │   │   ├── rekognition.py       # Integração com o Amazon Rekognition
│   │   │   ├── s3.py                # Integração com o Amazon S3
│   │   │   ├── transcribe.py        # Integração com o Amazon Transcribe
│   │   │   └── __init__.py          # Inicializador de pacote Python
│   │   └── __init__.py              # Inicializador de pacote Python
│   ├── models/                      # Modelos de dados compartilhados
│   │   ├── institutions.py          # Modelo de dados para instituições
│   │   └── __init__.py              # Inicializador de pacote Python
│   ├── schemas/                     # Esquemas de validação de dados
│   │   ├── bedrock.py               # Esquema de validação para o Amazon Bedrock
│   │   ├── base.py                  # Esquema de validação base
│   │   ├── institutions.py          # Esquema de validação para instituições
│   │   ├── rekognition.py           # Esquema de validação para o Amazon Rekognition
│   │   └── __init__.py              # Inicializador de pacote Python
│   ├── utils/                       # Funções utilitárias
│   │   ├── build.py                 # Script para compilar o projeto
│   │   └── __init__.py              # Inicializador de pacote Python
│   ├── requirements.txt             # Dependências Python do backend
│   └── serverless.yml               # Configuração principal do Serverless para o backend
├── website/                         # Diretório principal do website
│   ├── app/                         # Aplicativo principal Django do website
│   │   ├── templates/               # Templates HTML para o website
│   │   │   └── base.html            # Template base HTML
│   │   ├── __init__.py              # Inicializador de pacote Python
│   │   ├── asgi.py                  # Configuração ASGI para deploy
│   │   ├── settings.py              # Configurações do Django
│   │   ├── urls.py                  # URLs principais do website
│   │   └── wsgi.py                  # Configuração WSGI para deploy
│   ├── institutions/                # Aplicativo Django para instituições
│   │   ├── templates/               # Templates específicos de instituições
│   │   │   ├── detail_institution.html  # Detalhes de uma instituição
│   │   │   ├── institutions.html        # Listagem de instituições
│   │   │   └── terms_of_use.html        # Página de Termos de Uso
│   │   ├── __init__.py              # Inicializador de pacote Python
│   │   ├── admin.py                 # Configuração de administração do Django
│   │   ├── apps.py                  # Configuração do aplicativo Django
│   │   ├── models.py                # Modelos de dados das instituições
│   │   ├── tests.py                 # Testes do aplicativo de instituições
│   │   ├── urls.py                  # URLs específicas do aplicativo instituições
│   │   └── views.py                 # Views do aplicativo de instituições
│   ├── static/                      # Arquivos estáticos do website
│       ├── assets/                  # Arquivos de mídia e imagens
│       │   └── img/
│       │       ├── img1.png         # Imagem de exemplo 1
│       │       └── solidarity.png   # Imagem de solidariedade
│       └── css/                     # Arquivos CSS para estilos do website
│           ├── base.css             # Estilos básicos
│           ├── detail_institution.css  # Estilos para detalhe de instituições
│           ├── institutions.css        # Estilos para listagem de instituições
│           └── terms_of_use.css        # Estilos para página de Termos de Uso
├── .gitignore                       # Arquivo para ignorar arquivos/desnecessários no Git
├── .pre-commit-config.yaml          # Configuração de hooks de pré-commit
├── Makefile                         # Script de automação de tarefas
├── package.json                     # Dependências e scripts do Node.js
└── README.md                        # Documentação principal do projeto
```


```

---

## **📅 Metodologia de Desenvolvimento**

Adotamos a metodologia **Ágil**, com **Sprints** curtas, **Daily Meetings** e **Code Reviews** para garantir a qualidade e agilidade no desenvolvimento.

---

## **😿 Principais Dificuldades**

1. **Integração de múltiplos serviços AWS**: A configuração de vários serviços como **Lex**, **Rekognition** e **Polly** envolveu um desafio técnico considerável.
2. **Moderação de conteúdo**: Encontrar a melhor combinação de serviços para moderação eficiente de imagens e textos foi complexo.
3. **Gerenciamento de estado do chatbot**: Manter a continuidade das conversas no **Amazon Lex** foi um desafio técnico, exigindo uma solução de armazenamento de estado.


---

## **📜 Termos de Uso**

Os **Termos de Uso** podem ser acessados em [termos de uso](https://conexao-solidaria-termos.s3.amazonaws.com/termos.html).

---

Este README segue as melhores práticas, conforme recomendado no Programa de Bolsas Compass UOL e AWS.

