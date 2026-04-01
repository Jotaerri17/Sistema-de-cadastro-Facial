# 🚀 Sistema de Reconhecimento Facial 

Este é um projeto acadêmico de um sistema de controle de acesso (simulando uma catraca de academia ou portaria) baseado em **Reconhecimento Facial**. Desenvolvido em Python, o sistema é capaz de identificar usuários cadastrados em um banco de dados na nuvem, emitir alertas sonoros de sucesso ou erro e encerrar a sessão automaticamente após a validação.

## ✨ Funcionalidades

* **Reconhecimento Facial Rápido:** Utiliza a biblioteca `face_recognition` (baseada em dlib) para mapear e comparar os pontos faciais.
* **Feedback Sonoro Dinâmico:** Integração com a biblioteca `pygame` para reproduzir áudios de liberação de acesso ou de bloqueio para usuários desconhecidos.
* **Banco de Dados em Nuvem:** Os *encodings* (matrizes matemáticas) dos rostos não ficam salvos em arquivos de texto locais, mas sim serializados (JSON) em um banco de dados remoto (PostgreSQL/Neon), garantindo maior segurança e persistência.
* **Autenticação de Sessão (Face ID Mode):** O sistema não roda em um loop infinito aguardando; ao reconhecer um usuário válido, ele emite o aviso sonoro, libera o acesso e encerra a câmera automaticamente.
* **Sistema Anti-Spam de Áudio:** Lógica de controle de tempo (`time`) para evitar que o alarme de erro toque repetidamente caso uma pessoa não cadastrada permaneça em frente à câmera.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **OpenCV (`cv2`):** Para captura de vídeo e desenho gráfico na tela.
* **Face Recognition:** Para extração e comparação das métricas faciais.
* **NumPy:** Para manipulação rápida de arrays e cálculos de distância vetorial.
* **Pygame:** Para o sistema de áudio assíncrono.
* **Banco de Dados:** PostgreSQL (via Neon) para armazenamento dos dados.

## 📂 Estrutura do Projeto

```text
📦 Sistema-de-cadastro-Facial
 ┣ 📂 audeos/                  # Pasta com os arquivos de som (.mp3 ou .wav)
 ┃ ┣ 📜 vai-brasil.mp3         # Áudio de sucesso/liberado
 ┃ ┗ 📜 nao-vai-nao.mp3        # Áudio de erro/bloqueado
 ┣ 📜 banco.py                 # Script de configuração e conexão com o banco de dados
 ┣ 📜 cadastro.py              # Script para capturar o rosto e salvar no banco
 ┣ 📜 reconhecimento.py        # Script principal da "catraca" (Leitura e Validação)
 ┗ 📜 README.md                # Documentação do projeto
