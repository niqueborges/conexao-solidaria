# Documentação da API (Conexão Solidária)

A API do projeto foi construída usando **AWS API Gateway** e **AWS Lambda** (através do Serverless Framework).

Todos os endpoints estão hospedados na URL base do API Gateway fornecida pelo deploy do CloudFormation.

## Segurança e Rate Limit

- **Segurança (Header)**: Todas as requisições requerem o cabeçalho `X-Custom-Auth` para validar a origem da requisição e previnir abusos (implementado no WAF e API Gateway).
- **Tokens Privados**: Endpoints de modificação (`PUT`, `DELETE`) de uma instituição requerem que a requisição passe o `token` de criação da mesma nos Headers ou Body (a depender da implementação do client).
- **Rate Limit**: A API é protegida por regras do AWS WAF e possui um limite padrão de 500 requisições a cada 5 minutos por IP (RateLimitRule).

---

## Endpoints

### 1. Criar Instituição

- **Método**: `POST`
- **Path**: `/institutions`
- **Descrição**: Cadastra uma nova instituição no banco de dados.

**Body (JSON)**:
```json
{
  "cnpj": "12345678000199",
  "name": "ONG Esperança",
  "email": "contato@ongesperanca.org",
  "phone_number": "11999999999",
  "cep": "01000000",
  "region": "Sudeste",
  "state": "SP",
  "address": "Rua Exemplo",
  "address_number": "123",
  "city": "São Paulo",
  "neighborhood": "Centro",
  "site": "https://ongesperanca.org",
  "about": "Ajudamos pessoas em vulnerabilidade.",
  "image": "s3://bucket/image.jpg",
  "confirmation_audio": "s3://bucket/audio.mp3"
}
```

**Retorno (201 Created)**: Retorna a instituição criada **incluindo o `token`** de edição. *Este token deve ser salvo pelo cliente (chatbot), pois não será exposto novamente nas buscas públicas.*

---

### 2. Listar Instituições

- **Método**: `GET`
- **Path**: `/institutions`
- **Descrição**: Retorna todas as instituições com paginação.

**Query Params**:
- `limit` (opcional, int): Número máximo de resultados (padrão: 1000).
- `last_evaluated_key` (opcional, string JSON): Chave de paginação.

**Retorno (200 OK)**:
```json
{
  "institutions": [
    {
      "cnpj": "12345678000199",
      "id": "uuid",
      "name": "ONG Esperança",
      // (Nota: o campo 'token' é omitido por segurança)
      "verified": false,
      ...
    }
  ],
  "last_evaluated_key": null
}
```

---

### 3. Consultar Instituição (Específica)

- **Método**: `GET`
- **Path**: `/institutions/{cnpj}`
- **Descrição**: Retorna os detalhes públicos de uma única instituição.

**Retorno (200 OK)**: Objeto da instituição.

---

### 4. Filtrar Instituições (Região ou Estado)

- **Método**: `GET`
- **Path**: `/institutions/filter`
- **Descrição**: Busca instituições com base na Região ou Estado.

**Query Params**:
- `region` (opcional, string): Nome da região (Ex: 'Nordeste').
- `state` (opcional, string): UF do Estado (Ex: 'BA').
- `limit` (opcional, int)
- `last_evaluated_key` (opcional, string JSON)

---

### 5. Atualizar Instituição

- **Método**: `PUT`
- **Path**: `/institutions/{cnpj}`
- **Descrição**: Atualiza dados da instituição (requer autorização/token).

---

### 6. Excluir Instituição

- **Método**: `DELETE`
- **Path**: `/institutions/{cnpj}`
- **Descrição**: Remove a instituição (requer autorização/token).
