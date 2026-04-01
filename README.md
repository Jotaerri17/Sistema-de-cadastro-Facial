# 🚀 Sistema de Controle de Acesso por Biometria Facial

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red?style=flat-square&logo=opencv&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon_Cloud-336791?style=flat-square&logo=postgresql&logoColor=white)

Este é um projeto universitário de **Visão Computacional e Banco de Dados em Nuvem**, focado na criação de um sistema de controle de acesso inteligente (estilo "catraca virtual"). O sistema é capaz de cadastrar usuários extraindo a biometria facial via webcam e realizar a validação em tempo real consultando um banco de dados Serverless.

## ✨ Funcionalidades

* **Cadastro Biométrico:** Captura o rosto do usuário via webcam e converte as características faciais em um vetor matemático de 128 dimensões (Encoding).
* **Armazenamento Seguro na Nuvem:** Salva os encodings faciais de forma segura no banco de dados **Neon (PostgreSQL)**, sem a necessidade de armazenar imagens pesadas localmente.
* **Reconhecimento em Tempo Real:** Escaneia o feed da webcam em tempo real, comparando os rostos detectados com a base de dados na nuvem para autorizar ou negar o acesso.
* **Segurança de Credenciais:** Utiliza variáveis de ambiente (`.env`) para proteger strings de conexão e dados sensíveis.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Visão Computacional & IA:** `opencv-python`, `face_recognition`, `numpy`
* **Banco de Dados:** PostgreSQL hospedado no [Neon.tech](https://neon.tech/)
* **Integração & Segurança:** `psycopg2-binary`, `python-dotenv`

## ⚙️ Pré-requisitos e Instalação

### 1. Clonar o repositório
```bash
git clone [https://github.com/SEU_USUARIO/Sistema-de-cadastro-Facial.git](https://github.com/SEU_USUARIO/Sistema-de-cadastro-Facial.git)
cd Sistema-de-cadastro-Facial
