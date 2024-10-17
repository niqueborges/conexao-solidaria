# Conexão Solidária

## Tema do Projeto

**Conexão Solidária** é um chat interativo que facilita a comunicação entre doadores e Instituições, fornecendo uma plataforma simples para listagem e cadastro de Instituições. O projeto utiliza a moderação de imagens e textos para garantir a qualidade do conteúdo. A ideia é criar um ambiente seguro e organizado para conectar essas duas partes, promovendo ações solidárias de forma acessível e segura.

## Esboço da Arquitetura

O projeto utiliza diversos serviços da AWS para garantir escalabilidade, acessibilidade e facilidade de uso. Abaixo está uma visão geral dos principais componentes:

### **Componentes Principais:**
- **Amazon Lex**: Chatbot que gerencia interações via WhatsApp para doadores e Instituições.
- **Twilio**: Integração com o WhatsApp para permitir a comunicação entre o chatbot e os usuários.
- **Amazon Polly**: Converte respostas do Bot em aúdio.
- **Amazon Rekognition**: Modera imagens enviadas pelas Instituições para verificar conteúdos inadequados.
- **Amazon Bedrock**: Analisa descrições de texto fornecidas pelas Instituições para garantir linguagem apropriada.
- **AWS Lambda**: Backend serverless que processa cadastro, listagem e moderação de conteúdo.
- **Amazon DynamoDB**: Banco de dados NoSQL que armazena informações sobre as Instituições.

### **Diagrama da Arquitetura:**

![Arquitetura do Conexão Solidária](./assets/img/architecture.png)

### **Estrutura de Dados no DynamoDB**
A tabela de armazenamento para as Instituições no DynamoDB terá a seguinte estrutura:

- **Tabela de Instituições**:
  - **CNPJ** (String): Chave primária, usada para identificar a ONG.
  - **Nome** (String): Nome da ONG.
  - **Email** (String): Email de contato da ONG.
  - **Telefone** (String): Telefone de contato da ONG.
  - **CEP** (String): Localização da ONG (baseado no código postal).
  - **Descricao** (String): Descrição da ONG, incluindo suas atividades e área de atuação.
  - **Status de Verificação** (Boolean): Indica se a ONG foi aprovada ou contém conteúdo inadequado.

---

## Termos de Uso

Os **Termos de Uso** da plataforma **Conexão Solidária** são baseados nas leis brasileiras e seguem as normas da **Lei Geral de Proteção de Dados (LGPD)**.

### **Termos Chave:**
1. **Responsabilidade do Usuário**: Ao utilizar a plataforma, o usuário se compromete a fornecer informações verídicas e a utilizar a plataforma de maneira ética e legal.
2. **Moderação de Conteúdo**: Imagens e descrições enviadas serão analisadas por sistemas automatizados para garantir que não violem os termos de uso e as legislações vigentes.
3. **Transparência**: As Instituições cadastradas devem fornecer informações corretas e detalhadas sobre suas atividades e propósitos.
4. **Consequências Legais**: Qualquer uso indevido resultará em exclusão da plataforma e reporte às autoridades competentes, conforme o Código Penal.

---

## Conclusão

O projeto será desenvolvido seguindo as boas práticas de arquitetura serverless, utilizando **AWS Lambda** e **Amazon DynamoDB** para garantir escalabilidade, e as funções de inteligência artificial do **Amazon Rekognition** e **Amazon Bedrock** para moderação de conteúdo, garantindo um ambiente seguro e confiável para os usuários.

---

## Estrutura do Repositório

```
conexao_solidaria/
│
├── .serverless/
│
├── api/
│   └── v1/
│       └── handlers/
|
├── application/
│   └── core/
|
├── infra/
│   └── aws/
│   └── schemas/
|
├── interfaces/
├── utils/
|
├── serverless.yml
|
├── .gitignore
├── .pre-commit-config.yaml
├── package.json
├── README.md
└── requirements.txt
```
