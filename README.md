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

1. **Chatbot Interativo**: Usa **Amazon Lex** integrado ao **WhatsApp** via **Twilio**.
2. **Moderação de Conteúdo**: **Amazon Rekognition** e **Amazon Bedrock** para moderação de imagens e textos.
3. **Conversão de Texto para Áudio**: Com **Amazon Polly**.
4. **Transcrição de Áudio**: Via **Amazon Transcribe**.
5. **Verificação de Endereços**: Integração com **API ViaCEP**.

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
- **Serverless Framework**
- **Credenciais AWS**

### **Passos**:

1. Clone o repositório:
   ```bash
   git clone https://github.com/Compass-pb-aws-2024-JUNHO/sprints-9-10-pb-aws-junho.git
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
4. Execute o deploy:
   ```bash
   serverless deploy
   ```
5. Utilize o chatbot via WhatsApp.

---

## **🚀 Deploy**

O deploy utiliza **Serverless Framework** para orquestrar os serviços AWS.

---

## **💻 Tecnologias Utilizadas**

- **Amazon Lex**
- **Twilio**
- **Amazon Polly**
- **Amazon Transcribe**
- **Amazon S3**
- **Amazon Rekognition**
- **Amazon Bedrock**
- **API ViaCEP**
- **AWS Lambda**
- **Amazon DynamoDB**
- **Python**

---

## **🗄️ Banco de Dados**

A estrutura de armazenamento das Instituições em **DynamoDB** segue o modelo abaixo:
![Banco de Dados](./assets/img/database.png)

---

## **📂 Estrutura de Diretórios**

```
conexao_solidaria/
│
├── api/
│   └── v1/
│       └── handlers/
├── application/
│   └── core/
├── infra/
│   └── aws/
│   └── schemas/
├── interfaces/
├── lex/
│   └── backend/
├── utils/
├── serverless.yml
├── .gitignore
├── .pre-commit-config.yaml
├── package.json
├── README.md
└── requirements.txt
```

---

## **📅 Metodologia de Desenvolvimento**

Adotamos a metodologia **Ágil**, com **Sprints** curtas, **Daily Meetings** e **Code Reviews** para garantir a qualidade e agilidade no desenvolvimento.

---

## **😿 Principais Dificuldades**

- Dificuldade com a mudança nas datas de entrega gerando confusão no gerenciamento de tempo.
- Configuração da moderação com **Amazon Rekognition**.
- Análise de texto com **Amazon Bedrock**.

---

## **📜 Termos de Uso**

Os **Termos de Uso** podem ser acessados em [termos de uso](https://conexao-solidaria-termos.s3.amazonaws.com/termos.html).

---

Este README segue as melhores práticas, conforme recomendado no Programa de Bolsas Compass UOL e AWS.

