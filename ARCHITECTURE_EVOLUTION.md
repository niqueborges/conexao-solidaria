````markdown
# História da Arquitetura do Conexão Solidária (2024–2026)

> Documento histórico da evolução técnica e arquitetural do projeto Conexão Solidária.

## Origem do Projeto (2024)

O Conexão Solidária nasceu em 2024 como um projeto voltado para conectar instituições sociais e potenciais doadores através de uma plataforma digital.

A proposta original era relativamente simples:

- Cadastro de instituições.
- Consulta de instituições por região.
- Divulgação de necessidades e campanhas.
- Interface web para os usuários.
- Atendimento via WhatsApp utilizando Amazon Lex.

Desde o início, a arquitetura foi construída sobre serviços da AWS, seguindo a cultura cloud-native incentivada pelo programa da Compass UOL.

---

# Primeira Arquitetura (2024)

A primeira versão utilizava:

- Amazon Lex V2
- AWS Lambda
- API Gateway
- DynamoDB
- Amazon S3
- Amazon Polly
- Amazon Rekognition
- Twilio WhatsApp

Fluxo:

```text
WhatsApp
    ↓
Twilio
    ↓
Lambda Webhook
    ↓
Amazon Lex
    ↓
Lambda Handler
    ↓
API Gateway
    ↓
Backend
    ↓
DynamoDB
```

Essa arquitetura funcionava bem para conversas estruturadas.

Exemplos:

- Cadastro de instituições.
- Busca por região.
- Coleta de dados em etapas.

---

# Crescimento do Projeto

Com a expansão das funcionalidades, surgiram novos componentes:

## Moderação de imagens

Foi incorporado:

- Amazon Rekognition

para validar imagens enviadas durante o cadastro.

---

## Síntese de voz

Foi integrado:

- Amazon Polly

permitindo respostas em áudio.

---

## Consulta de CEP

Passou a existir integração com:

- ViaCEP

para preenchimento automático de endereços.

---

## Backend Serverless

O backend foi estruturado com:

- Python
- AWS Lambda
- Serverless Framework

seguindo o modelo:

```text
Controller
↓
Service
↓
Repository
↓
DynamoDB
```

---

# Problema Arquitetural Descoberto (2026)

Durante revisões de arquitetura realizadas em 2026, foi identificado um problema importante.

As regras de negócio do chatbot estavam fortemente acopladas ao formato interno do Amazon Lex.

Exemplo:

```python
event["sessionState"]["intent"]["slots"]
```

As classes:

- RegisterIntent
- ListIntent

misturavam:

- Validação de CNPJ.
- Validação de e-mail.
- Chamada da API.
- Integração com Rekognition.
- Consulta ao ViaCEP.
- Manipulação dos eventos do Lex.

Isso criava uma dependência direta entre o domínio do sistema e o mecanismo de conversação.

Caso o Lex fosse substituído por:

- Amazon Bedrock;
- OpenAI;
- Anthropic Claude;
- outro canal de atendimento;

grande parte da lógica precisaria ser reescrita.

---

# Revisão Arquitetural de 2026

Foi adotada uma estratégia evolutiva.

A decisão foi:

**não reescrever o sistema do zero.**

Em vez disso, a arquitetura passou por um processo gradual de desacoplamento.

---

# Fase 1 — Clean Architecture

Objetivo:

Separar transporte e domínio.

Nova estrutura:

```text
chatbot/backend/

domain/
    schemas.py
    services/
        validators.py
        registration_flow.py
        list_flow.py
        tips_flow.py

adapters/
    lex_mapper.py

intents/
    register.py
    list.py
    tips.py
```

---

## Domain

Passou a conter:

### Schemas

Modelos de dados independentes.

Exemplos:

- RegistrationRequest
- ValidationResult

---

### Validators

Funções puras:

```python
validate_cnpj()

validate_email()

validate_phone()
```

Sem dependência da AWS.

---

### Flows

Regras de negócio:

- RegistrationFlow
- ListFlow
- TipsFlow

Os serviços passaram a funcionar independentemente do Lex.

---

## Adapters

Foi criado:

```text
adapters/lex_mapper.py
```

Responsável por converter:

```python
event["sessionState"]["intent"]["slots"]
```

em objetos simples consumidos pelo domínio.

---

## Intents

As antigas Intents foram transformadas em adaptadores.

Elas passaram a:

1. Receber eventos do Lex.
2. Chamar o domínio.
3. Traduzir respostas do domínio para eventos do Lex.

---

# Resultado da Fase 1

A camada de domínio tornou-se completamente independente.

Buscas por:

- sessionState
- slots

retornaram zero ocorrências dentro de:

```text
chatbot/backend/domain/
```

Toda a dependência do Lex ficou concentrada nos adaptadores.

---

# Testabilidade

Com o desacoplamento, tornou-se possível testar o domínio sem acessar a AWS.

Foram criados testes unitários para:

- validação de CNPJ;
- validação de e-mail;
- fluxo de cadastro;
- busca por região;
- geração de dicas.

Todos os testes passaram com sucesso.

Exemplo:

```text
6 passed in 1.10s
```

---

# Arquitetura Atual (2026)

```text
WhatsApp
     ↓
Twilio
     ↓
Lambda Webhook
     ↓
Amazon Lex
     ↓
Lex Adapters
     ↓
Domain Flows
     ↓
Infrastructure
     ↓
API Gateway
     ↓
Backend
     ↓
DynamoDB
```

O domínio já não depende do Lex.

---

# Próxima Evolução Planejada

## Fase 2 — Conversation Orchestrator

Introduzir uma camada intermediária:

```text
ConversationOrchestrator
```

Fluxo:

```text
WhatsApp
    ↓
Twilio
    ↓
Conversation Orchestrator
         ↓
         ├── LexEngine
         │
         ├── BedrockEngine
         │
         └── FallbackEngine
```

Responsabilidades:

- roteamento por intenção;
- controle de custos;
- fallback;
- governança.

---

# Abstração dos Engines

Planeja-se utilizar uma interface única:

```python
class ConversationEngine(Protocol):

    def process(
        self,
        message: str,
        session_id: str
    ) -> ConversationResponse:
        ...
```

Implementações possíveis:

```python
LexEngine

ClaudeEngine

TitanEngine

NovaEngine

OpenAIEngine

FallbackEngine
```

Dessa forma, modelos podem ser substituídos sem alterar o domínio.

---

# Filosofia Adotada

O propósito do sistema é conectar doadores e instituições.

Tecnologias como:

- Lex;
- Bedrock;
- OpenAI;
- Twilio;
- Polly;
- Rekognition;

são apenas detalhes de implementação.

A arquitetura passou a seguir princípios de:

- SOLID;
- Clean Architecture;
- Inversão de Dependência;
- AWS Well-Architected Framework;
- Otimização de custos;
- Evolução incremental.

---

# Situação Atual

Em 2026, o Conexão Solidária deixou de ser apenas um chatbot baseado em Amazon Lex.

Ele se tornou uma plataforma preparada para múltiplos canais e múltiplos modelos de IA, preservando as regras de negócio e permitindo evolução gradual, sem reescritas massivas.

A ideia original de conectar pessoas e instituições continua a mesma.

O que mudou foi a maturidade da arquitetura construída ao redor dela.
````
