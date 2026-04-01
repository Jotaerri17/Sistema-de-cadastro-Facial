import cv2
import face_recognition
import numpy as np
import json
import time
import pygame
from banco import conectar_banco


# Inicializa o sistema de som sem travar o vídeo
pygame.mixer.init()
try:
    som_sucesso = pygame.mixer.Sound('audeos/vai-brasil.mp3')
    som_erro = pygame.mixer.Sound('audeos/nao-vai-nao.mp3')
except:
    print("[AVISO] Arquivos 'vai-brasil.wav' ou 'nao-vai-nao.wav' não encontrados na pasta!")
    som_sucesso, som_erro = None, None

def carregar_usuarios_do_banco():
    print("Buscando usuários cadastrados ...")
    conexao, cursor = conectar_banco()
    usuarios_conhecidos = []
    
    if conexao:
        cursor.execute("SELECT nome, encoding FROM usuarios")
        rows = cursor.fetchall()
        for row in rows:
            nome = row[0]
            # Converte o texto do banco de volta para uma lista de números (numpy array)
            encoding = np.array(json.loads(row[1]))
            usuarios_conhecidos.append({"nome": nome, "encoding": encoding})
        
        cursor.close()
        conexao.close()
    
    return usuarios_conhecidos

def iniciar_reconhecimento():
    usuarios = carregar_usuarios_do_banco()
    encodings_conhecidos = [u["encoding"] for u in usuarios]
    nomes_conhecidos = [u["nome"] for u in usuarios]
    
    video_capture = cv2.VideoCapture(0)
    print(f" Bem-vindo {nomes_conhecidos[0] if nomes_conhecidos else 'usuário'}. Aperte 'q' para encerrar.")

    # Variáveis de controle de tempo para o áudio não repetir loucamente
    ultimo_acesso_liberado = 0
    inicio_desconhecido = None

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        # Redimensiona o frame para 1/4 para processar rápido e evitar lentidão
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Encontra todos os rostos no frame atual
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            nome = "DESCONHECIDO"

            # Usa a menor distância para encontrar o melhor match
            face_distances = face_recognition.face_distance(encodings_conhecidos, face_encoding)
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                tolerancia = 0.4 # Mudei para 0.45 para ficar equilibrado, mas pode voltar para 0.35 se quiser
                
                # Validação rigorosa
                if face_distances[best_match_index] < tolerancia:
                    nome = nomes_conhecidos[best_match_index]

            # Audeo e controle de tempo
            tempo_atual = time.time()

            if nome != "DESCONHECIDO":
                inicio_desconhecido = None 
                
                # Toca o som de sucesso apenas 1 vez a cada 5 segundos
                if tempo_atual - ultimo_acesso_liberado > 3:
                    if som_sucesso: 
                        som_sucesso.play()
                    ultimo_acesso_liberado = tempo_atual
            else:
                # Inicia o timer se for a primeira vez vendo o rosto desconhecido
                if inicio_desconhecido is None:
                    inicio_desconhecido = tempo_atual
                
                # Se for desconhecido por mais de 5 segundos seguidos na tela
                if tempo_atual - inicio_desconhecido > 3:
                    if som_erro: 
                        som_erro.play()
                    inicio_desconhecido = tempo_atual # Reseta para apitar novamente em 5s caso a pessoa não saia

            # ================= DESENHO NA TELA =================
            # Multiplicando por 4 pois reduzimos o frame antes
            top *= 4; right *= 4; bottom *= 4; left *= 4
            cor = (0, 255, 0) if nome != "DESCONHECIDO" else (0, 0, 255)
            
            cv2.rectangle(frame, (left, top), (right, bottom), cor, 2)
            cv2.putText(frame, nome, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        cv2.imshow(' - Reconhecimento Facial - ', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    iniciar_reconhecimento()