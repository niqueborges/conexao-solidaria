import http from 'k6/http';
import { check, sleep } from 'k6';

// Executar com: k6 run k6_load_test.js
// Obs: Substitua a variável de ambiente URL pela URL do seu CloudFront

export const options = {
  stages: [
    { duration: '30s', target: 50 },  // Ramp-up para 50 VUs
    { duration: '1m', target: 500 },  // Pico simulando tráfego médio
    { duration: '30s', target: 1000 }, // Stress Test para disparar o Rate Limit do WAF (500 requisições num período curto de 5 mins)
    { duration: '30s', target: 0 },   // Ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% das requisições devem ser < 2s
  },
};

export default function () {
  const BASE_URL = __ENV.API_URL || 'https://example-cloudfront.net';

  // 1. Teste de Fluxo Normal
  const res = http.get(`${BASE_URL}/api/v1/institutions`, {
    headers: { 'User-Agent': 'K6-LoadTest' }
  });

  check(res, {
    'status 200 (Sucesso)': (r) => r.status === 200,
    // Se o Rate Limit atuar, devemos começar a ver 429 ou 403 dependendo de como o WAF responde
    'status 403 (Bloqueado por WAF/Rate Limit)': (r) => r.status === 403, 
    'status 429 (Too Many Requests)': (r) => r.status === 429,
  });

  // 2. Teste de Injeção Maliciosa (Validação de Segurança)
  // Esse payload deve invocar o AWSManagedRulesCommonRuleSet e ser bloqueado instantaneamente (403)
  const malicousPayload = JSON.stringify({
    bucket: "test-bucket",
    image_key: "image.png' OR 1=1 --"
  });

  const resSec = http.post(`${BASE_URL}/api/v1/scan`, malicousPayload, {
    headers: { 
      'Content-Type': 'application/json',
      'User-Agent': 'K6-SecurityTest' 
    }
  });

  check(resSec, {
    'status 403 (Bloqueado por SQLi/XSS)': (r) => r.status === 403,
  });

  sleep(1);
}
