# Arquitetura do Sistema

## API Serverless (CRUD de Instituições)

A API principal expõe operações CRUD protegidas por AWS WAF e CloudFront, utilizando o DynamoDB para persistência de dados.

```mermaid
flowchart TD
    Client[Cliente / Website] --> CF[CloudFront]
    CF -->|X-Origin-Verify| WAF[AWS WAF]
    WAF --> APIGW[API Gateway]
    APIGW --> Lambda[AWS Lambda]
    Lambda --> DDB[(DynamoDB)]
    Lambda --> Bedrock[Amazon Bedrock]
    Lambda --> Rek[Amazon Rekognition]
```

## Chatbot (Lex + Twilio)

O Chatbot recebe requisições do Twilio ou do Proxy Web, e integra com o Amazon Lex para PLN. Em caso de cadastros com áudios, há conversão de texto em voz via Polly e armazenamento no S3.

```mermaid
flowchart TD
    User[Usuário] --> WhatsApp[WhatsApp]
    WhatsApp --> Twilio[Twilio]
    Twilio --> APIGW2[API Gateway]
    WebProxy[Website Chat] --> APIGW2
    APIGW2 --> LambdaLex[Lex Handler Lambda]
    LambdaLex <--> Lex[Amazon Lex V2]
    LambdaLex --> Polly[Amazon Polly]
    Polly --> S3[(S3 Bucket)]
    LambdaLex --> ServerlessAPI[Serverless API]
```
