import cv2
import face_recognition
import numpy as np
import json
from banco import conectar_banco

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
    print("Bem vindo! Aperte 'q' para encerrar.")

    while True:
        ret, frame = video_capture.read()
        
        # Redimensiona o frame para 1/4 para processar mais rápido (opcional)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Encontra todos os rostos no frame atual
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compara com os rostos que vieram do Neon
            matches = face_recognition.compare_faces(encodings_conhecidos, face_encoding)
            nome = "DESCONHECIDO"

            # Usa a menor distância para encontrar o melhor match
            face_distances = face_recognition.face_distance(encodings_conhecidos, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    nome = nomes_conhecidos[best_match_index]

            # Desenha o quadrado e o nome na tela (multiplicando por 4 pois reduzimos o frame antes)
            top *= 4; right *= 4; bottom *= 4; left *= 4
            cor = (0, 255, 0) if nome != "DESCONHECIDO" else (0, 0, 255)
            
            cv2.rectangle(frame, (left, top), (right, bottom), cor, 2)
            cv2.putText(frame, nome, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        cv2.imshow('Catraca de Academia - Reconhecimento Facial', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    iniciar_reconhecimento()