# Guia de Contribuição - Conexão Solidária

## Como Contribuir

1. Faça um fork do repositório
2. Crie uma branch para a sua feature (`git checkout -b feature/minha-feature`)
3. Siga o `.editorconfig` para manter o padrão de indentação
4. Faça os commits seguindo o padrão de Commits Semânticos (`feat:`, `fix:`, `docs:`, `test:`, `chore:`)
5. Abra um Pull Request e aguarde a revisão

## Estrutura do Projeto

O projeto é dividido em três componentes principais:
- `website/`: Frontend em Django
- `serverless/`: API Serverless com Serverless Framework e Python (PynamoDB, Powertools)
- `chatbot/backend/`: API Serverless para integração do Twilio com o Amazon Lex

## Padrões de Código
- Use tipagem estática (Type Hints) em funções Python.
- Funções AWS Lambda devem usar os decorators do `aws_lambda_powertools` (Logger, Tracer).
- Qualquer alteração na infraestrutura deve ser refletida no `serverless.yml`.
