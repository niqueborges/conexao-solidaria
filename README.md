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
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" width="100" height="30"/>
</p>


---

## **👥 Desenvolvedores**

| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/97261564?v=4" width="100" alt="Gusttavo Felipe">](https://github.com/gusttavofelipe) <br>[Gusttavo Felipe](https://github.com/gusttavofelipe) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/95103547?v=4" width="100" alt="Monique da Silva Borges">](https://github.com/niqueborges) <br>[Monique da Silva Borges](https://github.com/niqueborges) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/154631421?v=4" width="100" alt="Pedro Nunes">](https://github.com/PedroNunesBH) <br>[Pedro Nunes](https://github.com/PedroNunesBH) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/167145673?v=4" width="100" alt="Roger Dev">](https://github.com/Rogerdev02) <br>[Roger Dev](https://github.com/Rogerdev02) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/114765722?v=4" width="100" alt="Silvio CMJ">](https://github.com/SilvioCMJ) <br>[Silvio CMJ](https://github.com/SilvioCMJ) |
|:---:|:---:|:---:|:---:|:---:|

---

## **📜 Descrição**

Este projeto **Conexão Solidária** tem como objetivo criar uma plataforma de comunicação entre doadores e instituições, com suporte a um chatbot multicanal e integração com AWS. A plataforma utiliza Django para o backend e frontend, Docker para a execução do chatbot, e diversas soluções AWS para melhorar a experiência do usuário.

---

## **📑 Índice**

- [✨ Funcionalidades, Arquitetura e Fluxo de Trabalho](#funcionalidades-arquitetura-e-fluxo-de-trabalho)
- [📦 Como Rodar a Aplicação](#como-rodar-a-aplicação)
- [💻 Tecnologias Utilizadas](#tecnologias-utilizadas)
- [🗄️ Banco de Dados](#banco-de-dados)
- [📂 Estrutura de Diretórios](#estrutura-de-diretórios)
- [📅 Metodologia de Desenvolvimento](#metodologia-de-desenvolvimento)
- [😿 Principais Dificuldades](#principais-dificuldades)
- [📜 Termos de Uso](#termos-de-uso)

---

## **✨ Funcionalidades, Arquitetura e Fluxo de trabalho ⚙️**


O repositório é dividido em três áreas principais:

- **Backend (Chatbot)**: Implementação da lógica do chatbot, com integrações ao Amazon Lex, Twilio e outros serviços AWS.
- **Backend (Infraestrutura AWS)**: Configurações utilizando o Serverless Framework para gerenciar recursos AWS, como S3, Polly e Rekognition.
- **Frontend (Website)**: Aplicação Django que fornece a interface para os usuários, incluindo páginas para busca de instituições e integração com o backend.

---

O projeto segue uma arquitetura serverless na AWS. Principais passos incluem:

1. **Chatbot Multicanal**: Interação integrada via **Amazon Lex** e **Twilio** para WhatsApp.
2. **Armazenamento**: **DynamoDB** para persistência de dados, **AWS Lambda** para processamento.
3. **Moderação Inteligente**: Utiliza **Amazon Rekognition** e **Bedrock** para moderação de imagens e textos.
4. **Acessibilidade Avançada**: Conversão de texto para áudio com **Amazon Polly**.
5. **Suporte Avançado**: Transcrição de áudio para texto usando **Amazon Transcribe**.
6. **Geolocalização e Endereços**: Consulta eficiente via **API ViaCEP**.
7. **Diagrama da Arquitetura**
   ![Arquitetura](./assets/img/architecture.png)

---

## **📦 Como Rodar a Aplicação**

### Requisitos

Certifique-se de ter os seguintes pré-requisitos instalados:

- [Python 3.9+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/products/docker-desktop) (opcional para rodar o chatbot)
- [AWS CLI](https://aws.amazon.com/cli/)
- [Serverless Framework](https://www.serverless.com/framework/docs/getting-started/)
- [Node.js](https://nodejs.org/en/download/)

### **Clonando o Repositório**

Clone o repositório em sua máquina:

```bash
git clone https://github.com/Compass-pb-aws-2024-JUNHO/sprints-9-10-pb-aws-junho.git grupo-1
cd grupo-1
```

Antes de realizar o deploy, configure suas credenciais AWS e o ambiente:

#### **Definindo Credenciais AWS**

Configure o AWS CLI para que os serviços possam ser acessados corretamente:

```bash
aws configure
```

Defina manualmente as variáveis de ambiente, se necessário:

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=your_region
```

#### **Configurando o Serverless Framework**

Certifique-se de ter o **Serverless Framework** instalado e configurado. Para instalar, execute:

```bash
npm install -g serverless
```

Navegue até o diretório `serverless/` e instale as dependências do projeto:

```bash
cd serverless
npm install
```

#### **Realizando o Deploy**

Com as dependências instaladas, execute o seguinte comando para realizar o deploy dos recursos AWS:

```bash
serverless deploy
```

O comando acima criará os seguintes recursos:

- Funções Lambda
- Buckets S3 para armazenamento
- Tabelas DynamoDB
- Serviços como Amazon Polly, Rekognition e Transcribe

Ao final, o Serverless fornecerá os endpoints necessários para acessar as APIs e o chatbot.

---

## **Backend**

### **Chatbot**

O chatbot interage com usuários via WhatsApp e site, utilizando Amazon Lex para compreensão de intenções e Twilio para envio de mensagens.

#### **Instalação das Dependências**

Navegue até o diretório do chatbot e instale as dependências:

```bash
cd chatbot
pip install -r requirements.txt
```

#### **Deploy com Serverless Framework**

Realize o deploy das funções AWS Lambda e recursos:

```bash
serverless deploy
```

---

### **Infraestrutura AWS**

Os serviços AWS, como S3 e Polly, são configurados no diretório `serverless/infra/`. Após configurar o `serverless.yml`, faça o deploy:

```bash
cd serverless
serverless deploy
```

---

## **Frontend**

A aplicação Django fornece a interface de usuário do projeto.

### **1. Instalação das Dependências**

No diretório `website`, instale os pacotes necessários:

```bash
cd website
pip install -r requirements.txt
```

#### **2. Configuração do Banco de Dados**

Aplique as migrações para configurar o banco de dados SQLite:

```bash
python manage.py migrate
```

#### **3. Executando o Servidor Local**

Para rodar o servidor Django localmente:

```bash
python manage.py runserver
```

Acesse o site em [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## **Execução com Docker**

Caso prefira rodar o chatbot em um ambiente isolado, siga as etapas abaixo:

#### **1. Criar a Imagem Docker**

No diretório do chatbot:

```bash
docker build -t conexao-solidaria .
```

#### **2. Rodar o Contêiner Docker**

Execute o contêiner:

```bash
docker run -p 80:80 conexao-solidaria
```
---

**Verificação e Testes**

Após o deploy, teste os seguintes itens:

- **Backend**:
  - Verifique os endpoints fornecidos pelo Serverless.
  - Teste as funções Lambda para garantir que estão funcionando corretamente.

- **Frontend**:
  - Certifique-se de que a aplicação web está acessível no navegador.
  - Verifique a integração com os serviços backend, como o chatbot e os recursos AWS.

- **Chatbot**:
  - Teste a interação com o chatbot via WhatsApp (ou outro canal configurado).

---

### **Acesse o chatbot via WhatsApp ou a aplicação web no URL fornecido**

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
- **Docker**  
- **Python**  
- **Twilio**


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
│       ├── architecture.png            # Imagem representando a arquitetura do projeto
│       └── database.png                # Imagem representando o design do banco de dados
├── chatbot/                            # Diretório principal do chatbot
│   ├── backend/                        # Backend do chatbot
│   ├── handlers/                       # Manipuladores para as interações do chatbot
│   │   ├── health.py                   # Verificação de saúde do serviço
│   │   ├── lex.py                      # Manipulação de integração com o Amazon Lex
│   │   └── twilio.py                   # Manipulação de integração com o Twilio
│   ├── intents/                        # Intenções definidas para o chatbot
│   │   ├── list.py                     # Intenção de listagem
│   │   ├── register.py                 # Intenção de registro
│   │   └── tips.py                     # Intenção de dicas
│   ├── services/                       # Serviços auxiliares para o chatbot
│   │   ├── api.py                      # Serviço para chamada de APIs externas
│   │   ├── aws.py                      # Integração com serviços AWS
│   │   ├── lex.py                      # Serviço para integração com o Amazon Lex
│   │   ├── s3.py                       # Serviço para integração com o Amazon S3
│   │   └── via_cep_api.py              # Serviço para integração com a API ViaCEP
│   ├── utils/                          # Funções utilitárias e auxiliares
│   │   ├── content_type.py             # Funções relacionadas ao tipo de conteúdo
│   │   ├── decode.py                   # Função para decodificação de dados
│   │   ├── download_media.py           # Função para download de mídia
│   │   ├── get_twilio_phone.py         # Função para obtenção do número de telefone do Twilio
│   │   ├── responses.py                # Funções para manipulação de respostas do chatbot
│   │   └── slots.py                    # Funções para manipulação de slots do chatbot
│   ├── requirements.txt                # Dependências Python do projeto
│   ├── serverless.yml                  # Arquivo de configuração do Serverless
│   └── __init__.py                     # Inicializador de pacote Python
├── serverless/                         # Configurações do Serverless Framework
│   ├── api/                            # Diretório de APIs do Serverless
│   │   ├── v1/                         # Versão 1 da API
│   │   │   └── __init__.py          
│   │   └── __init__.py              
│   ├── core/                            # Lógica central e configurações
│   │   ├── config.py                    # Arquivo de configurações
│   │   ├── exceptions.py                # Exceções personalizadas
│   │   └── __init__.py              
│   ├── domain/                          # Lógica de negócio
│   │   ├── services/
│   │   │   ├── institution.py           # Serviço para gerenciar instituições
│   │   │   └── __init__.py          
│   │   └── __init__.py              
│   ├── infra/                           # Serviços de infraestrutura (AWS)
│   │   ├── aws/                         # Módulos específicos para integração com AWS
│   │   │   ├── bedrock.py               # Integração com o Amazon Bedrock
│   │   │   ├── polly.py                 # Integração com o Amazon Polly
│   │   │   ├── rekognition.py           # Integração com o Amazon Rekognition
│   │   │   ├── s3.py                    # Integração com o Amazon S3
│   │   │   ├── transcribe.py            # Integração com o Amazon Transcribe
│   │   │   └── __init__.py         
│   │   └── __init__.py              
│   ├── models/                          
│   │   ├── institutions.py              # Modelo de dados para instituições
│   │   └── __init__.py              
│   ├── schemas/                         
│   │   ├── bedrock.py                   # Esquema de validação para o Amazon Bedrock
│   │   ├── base.py                      # Esquema de validação base
│   │   ├── institutions.py              # Esquema de validação para instituições
│   │   ├── rekognition.py               # Esquema de validação para o Amazon Rekognition
│   │   └── __init__.py              
│   ├── utils/                           # Funções utilitárias
│   │   ├── build.py                     # Script para compilar o projeto
│   │   └── __init__.py                  
│   ├── requirements.txt                 # Dependências Python do backend
│   └── serverless.yml                   # Configuração principal do Serverless para o backend
├── website/                             # Diretório principal do website
│   ├── app/                             # Aplicativo principal Django do website
│   │   ├── templates/                   # Templates HTML para o website
│   │   │   └── base.html                # Template base HTML
│   │   ├── __init__.py                 
│   │   ├── asgi.py                      # Configuração ASGI para deploy
│   │   ├── settings.py                  # Configurações do Django
│   │   ├── urls.py                      # URLs principais do website
│   │   └── wsgi.py                      # Configuração WSGI para deploy
│   ├── institutions/                    # Aplicativo Django para instituições
│   │   ├── templates/                   # Templates específicos de instituições
│   │   │   ├── detail_institution.html  # Detalhes de uma instituição
│   │   │   ├── institutions.html        # Listagem de instituições
│   │   │   └── terms_of_use.html        # Página de Termos de Uso
│   │   ├── __init__.py              
│   │   ├── admin.py                     # Configuração de administração do Django
│   │   ├── apps.py                      # Configuração do aplicativo Django
│   │   ├── models.py                    # Modelos de dados das instituições
│   │   ├── tests.py                     # Testes do aplicativo de instituições
│   │   ├── urls.py                      # URLs específicas do aplicativo instituições
│   │   └── views.py                     # Views do aplicativo de instituições
│   ├── static/                          # Arquivos estáticos do website
│       ├── assets/                      # Arquivos de mídia e imagens
│       │   └── img/
│       │       ├── img1.png             # Imagem de exemplo 1
│       │       └── solidarity.png       # Imagem de solidariedade
│       └── css/                         
│           ├── base.css                 # Estilos básicos
│           ├── detail_institution.css   # Estilos para detalhe de instituições
│           ├── institutions.css         # Estilos para listagem de instituições
│           └── terms_of_use.css         # Estilos para página de Termos de Uso
├── .gitignore                           # Arquivo para ignorar arquivos/desnecessários no Git
├── .pre-commit-config.yaml              # Configuração de hooks de pré-commit
├── Makefile                             # Script de automação de tarefas
├── package.json                         # Dependências e scripts do Node.js
└── README.md                            # Documentação principal do projeto
```


```

---

## **📅 Metodologia de Desenvolvimento**

Adotamos a metodologia **Ágil**, com **Sprints** curtas, **Daily Meetings** e **Code Reviews** para garantir a qualidade e agilidade no desenvolvimento.

---

## **😿 Principais Dificuldades**

1. **Integração de múltiplos serviços AWS**: A configuração de vários serviços como **Lex**, **Rekognition** e **Polly** envolveu um desafio técnico considerável.
2. **Moderação de conteúdo**: Encontrar a melhor combinação de serviços para moderação eficiente de imagens e textos foi complexo.
3. **Gerenciamento de estado do chatbot**: Manter a continuidade das conversas no **Amazon Lex** foi um desafio técnico.


---

## **📜 Termos de Uso**

Os **Termos de Uso** podem ser acessados em [termos de uso](https://conexao-solidaria-termos.s3.amazonaws.com/termos.html).

---

Este README segue as melhores práticas, conforme recomendado no Programa de Bolsas Compass UOL e AWS.

