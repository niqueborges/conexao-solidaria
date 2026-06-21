# História da Arquitetura do Conexão Solidária (2024–2026)

> Documento histórico e vivo da evolução técnica e arquitetural do projeto Conexão Solidária, detalhando as refatorações estratégicas para suportar escalabilidade, múltiplos canais e IA Generativa.

---

## 1. A Arquitetura Original (2024)

O Conexão Solidária nasceu em 2024 com uma arquitetura "Serverless Clássica", fortemente acoplada aos serviços gerenciados da AWS. O propósito sempre foi conectar doadores a instituições sociais, mas a primeira implementação técnica foi construída inteiramente ao redor do **Amazon Lex** como orquestrador principal.

**Fluxo Antigo:**
```text
WhatsApp → Twilio → Lambda Webhook → Amazon Lex → Lambda Fulfillment Code Hook → Regras de Negócio (APIs, BD)
```

**Problema Identificado (Dívida Arquitetural):**
Com o crescimento das integrações (Rekognition para imagens, Polly para voz, ViaCEP), todo o domínio do sistema ficou aprisionado dentro do `FulfillmentCodeHook` do Lex. 
As regras de negócio precisavam interpretar dicionários complexos da AWS, como `event["sessionState"]["intent"]["slots"]`, impossibilitando testes unitários locais e inviabilizando a migração para outros canais (WebChat, Telegram) ou outros motores de IA (OpenAI, Bedrock) sem reescrever 100% do código.

---

## 2. Fase 1: Desacoplamento e Clean Architecture (Início de 2026)

A primeira grande revolução arquitetural foi a extração do Domínio. O objetivo da Fase 1 não foi adicionar funcionalidades, mas **isolar a lógica de negócio**.

### Mudanças Implementadas:
- **Separação de Camadas:** Criação de diretórios `domain/`, `infrastructure/`, `adapters/`.
- **Inversão de Dependência:** O domínio passou a depender de `Protocols` (interfaces) e não mais de `boto3` ou clientes HTTP reais.
- **Adapters e Mappers:** A conversão de `event["sessionState"]` foi isolada no `LexMapper`. As antigas *Intents* (ex: `RegisterIntent`).
- **Testabilidade:** Pela primeira vez, os `Flows` (como `RegistrationFlow`) puderam ser executados e testados 100% em memória (mockados), cobrindo regras de CNPJ e CEP em frações de segundo.

**Resultado da Fase 1:**
A dependência do Lex foi contida. O Domínio se tornou puro e reaproveitável, pronto para ser consumido por qualquer canal.

---

## 3. Fase 2: Conversation Orchestrator e Roteamento Híbrido (Meados de 2026)

Apesar da Fase 1 limpar o domínio, o fluxo do tráfego ainda passava "por dentro" da AWS (o Lex chamava as Lambdas). Na Fase 2, foi implementada a verdadeira inversão de controle no ponto de entrada do sistema: a criação de um **Orquestrador Stateless**.

**O que mudou?**
O Twilio agora bate no Orchestrator (`handlers/twilio.py`), e o Orchestrator decide as rotas. O Lex foi rebaixado: deixou de ser o dono do diálogo e tornou-se um "Microserviço de NLU e Máquina de Estado Temporária".

### Modelo de Estado (State Model)
Para evitar duplicação de estado, o Orchestrator não possui banco de dados e não tenta "entender a conversa". 
- **Orchestrator:** 100% Stateless. Só repassa `message` e `session_id`.
- **Lex (Dialog State):** Mantém a máquina de estado do preenchimento do formulário (*Slot Filling*).
- **Bedrock (LLM):** Atua de forma atômica e Stateless para resolver ambiguidades.
- **Flows (Domínio):** Executam a regra de forma atômica após o Lex extrair os dados.

### Tabela de Decisão de Roteamento (As 3 Únicas Rotas)
O Orchestrator segue regras estritas e determinísticas. Existe **1 chamada por mensagem**, sem loops, garantindo previsibilidade de latência e custo.

| Estado Retornado pelo Lex (`dialog_state`) | Ação do Orchestrator | Rota Escolhida | Racional de Custo |
|---|---|---|---|
| **InProgress / ElicitSlot** | Retorna a mensagem crua gerada pelo Lex. | Volta para o **Usuário** | Lex gerencia a coleta de dados de forma extremamente barata. |
| **ReadyForFulfillment** | Extrai os dados validados (slots) e injeta no Domínio. | Vai para os **Domain Flows** | O Lex cumpriu seu papel de NLU. A lógica real assume. |
| **FallbackIntent** | Repassa a mensagem original crua para o LLM. | Vai para o **BedrockEngine** | Lex falhou ou não há intent. Uso do LLM é acionado apenas sob demanda (controle financeiro). |

### Diagrama Atual (Fase 2)
```text
USER MESSAGE
     ↓
TWILIO WEBHOOK
     ↓
CONVERSATION ORCHESTRATOR
     ↓
LEX recognize_text() (NLU)
     ↓
┌──────────────────────────────┐
│ dialog_state ?               │
└──────────────────────────────┘
     ↓
   [IN_PROGRESS]
        → return LEX ElicitSlot response

   [READY_FOR_FULFILLMENT]
        ↓
   intent valid?
        ↓
   yes → FLOW (Domain Executa a Lógica de Negócio pura)
        ↓
        return response

   no / fallback
        ↓
   BEDROCK_ENGINE fallback (LLM)
        ↓
        return response
```

**Resultado da Fase 2:**
O sistema está pronto para a era da Inteligência Artificial Generativa. O custo do Bedrock/Claude está contido ao fallback (ou intents abertas específicas), enquanto formulários transacionais rodam de graça no Lex. Novos LLMs, como o Amazon Nova ou OpenAI, podem ser substituídos trocando apenas o Engine no Orchestrator, sem quebrar as regras de negócio.

---

## 4. Filosofia e Futuro

O Conexão Solidária consolidou-se sobre os pilares:
- **SOLID e Clean Architecture**
- **Observabilidade** (AWS Powertools Tracer)
- **Otimização de Custos** (Roteamento determinístico antes da inferência Generativa)

Essa fundação madura permitirá integrações futuras avançadas (ex: Bedrock Agents) sem o risco estrutural de transformar a arquitetura em um monólito incontrolável.
