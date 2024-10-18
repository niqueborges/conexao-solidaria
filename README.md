# Conexão Solidária

## Descrição

**Conexão Solidária** é um chat interativo que facilita a comunicação entre doadores e Instituições, fornecendo uma plataforma simples para listagem e cadastro de Instituições. O projeto utiliza a moderação de imagens e textos para garantir a qualidade do conteúdo. A ideia é criar um ambiente seguro e organizado para conectar essas duas partes, promovendo ações solidárias de forma acessível e segura.

## Arquitetura base

O projeto utiliza diversos serviços da AWS para garantir escalabilidade, acessibilidade e facilidade de uso. Abaixo está uma visão geral dos principais componentes:

<!-- ### **Componentes Principais:** -->
- **Amazon Lex**: Chatbot que gerencia interações via WhatsApp para doadores e Instituições.
- **Twilio**: Integração com o WhatsApp para permitir a comunicação entre o chatbot e os usuários.
- **Amazon Polly**: Converte respostas do Bot em aúdio.
- **Amazon S3**: Armazena as imagens enviadas pelas instituições.
- **Amazon Rekognition**: Modera imagens enviadas pelas Instituições para verificar conteúdos inadequados.
- **Amazon Bedrock**: Analisa descrições de texto fornecidas pelas Instituições para garantir linguagem apropriada.
- **API ViaCEP**: Verifica a existência de endereços fornecidos pelas intituições.
- **AWS Lambda**: Backend serverless que processa cadastro, listagem e moderação de conteúdo.
- **Amazon DynamoDB**: Banco de dados NoSQL que armazena informações sobre as Instituições.

### **Diagrama da Arquitetura**
![Arquitetura do Conexão Solidária](./assets/img/architecture.png)

### **Banco de Dados**
A tabela de armazenamento dos dados das Instituições no DynamoDB terá a seguinte estrutura:
![Banco de dados](./assets/img/database.png)


<!-- - **Tabela de Instituições**:
  - **CNPJ** (String): Chave primária, usada para identificar a ONG.
  - **Nome** (String): Nome da ONG.
  - **Email** (String): Email de contato da ONG.
  - **Telefone** (String): Telefone de contato da ONG.
  - **CEP** (String): Localização da ONG (baseado no código postal).
  - **Descricao** (String): Descrição da ONG, incluindo suas atividades e área de atuação.
  - **Status de Verificação** (Boolean): Indica se a ONG foi aprovada ou contém conteúdo inadequado. -->

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

**Conexão Solidária** propõe uma solução simples e segura para conectar doadores e Instituições, utilizando serviços robustos da AWS para garantir escalabilidade e confiabilidade. Com a moderação automática de conteúdo e uma arquitetura serverless eficiente, o projeto visa promover ações solidárias de forma acessível, transparente e segura, criando um ambiente confiável para todos os envolvidos.

---

## Estrutura do Diretórios

```
conexao_solidaria/
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
|
├── lex/
|   └── backend/
|
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
