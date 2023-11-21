import { check, sleep } from "k6";
import http from "k6/http";

const BASE_URL = "https://finlearn-api-pds2-production.up.railway.app/v1/network/posts";
const AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkY2U5OGM1OS1iMjljLTQxMmYtYTcyNC01ZTIxYWQ0MDlkYTYiLCJleHAiOjE3MDA1MTI0Mzl9.wxQRQOUNjLhxOlXYPAfUkjGY4xmy6ejybHdthRRTEoY";

export const options = {
    scenarios: {
        constant_request_rate: {
            executor: 'constant-arrival-rate',
            rate: 1000, // Limite de requisição 
            timeUnit: '1m', // iterations por minuto
            duration: '1m', // minutos de duração 
            preAllocatedVUs: 1, // quão grande seria o pool inicial de VUs
            maxVUs: 50, // se as preAllocatedVUs não forem suficientes, podemos inicializar mais
        },
    },
};


const headers = {
    "Content-Type": "application/json",
    Authorization: AUTH_TOKEN,
};

export function setup() {
    console.log("Iniciando execução de testes");
}

export default  function () {

    console.log("Executando requisição");
    let res = http.get(
        `${BASE_URL}`,
        { headers: headers }
    );

    check(res, {
        "status was 200": (r) => r.status == 200,
    });

    if (res.status != 200) {
        console.error(
            `Received HTTP ${res.status} for ${
                res.url
            }, body: ${JSON.stringify(res.body)}`
        );
    }
    console.log(JSON.stringify(res));
    
    check(res, {
      'status was 200': (r) => r.status == 200,
      'status was 400': (r) => r.status == 400,
      'status was 401': (r) => r.status == 401,
      'status was 403': (r) => r.status == 403,
      'status was 429': (r) => r.status == 429,
      'status was 500': (r) => r.status == 500,
      'status was 502': (r) => r.status == 502,
      'status was 503': (r) => r.status == 503,
    });
    
    sleep(1);
}