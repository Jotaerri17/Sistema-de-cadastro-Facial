import cv2
import face_recognition
import json
from banco import conectar_banco 

def cadastrar_usuario(nome):
    print(f"Preparando para cadastrar: {nome}")
    print("Olhe para a câmera e aperte 's' para tirar a foto ou 'q' para sair.")
    
    # Inicia a webcam
    video_capture = cv2.VideoCapture(0)

    while True:
        # Lê um frame da câmera
        ret, frame = video_capture.read()

        if not ret or frame is None:
            print("[ERRO] Não foi possível acessar a câmera. Verifique as permissões do macOS!")
            break
        
        # Mostra a imagem numa janela
        cv2.imshow('Cadastro de Usuario - Aperte S para salvar', frame)

        # Espera uma tecla ser pressionada
        tecla = cv2.waitKey(1) & 0xFF
        
        if tecla == ord('q'):
            print("Cadastro cancelado.")
            break
            
        elif tecla == ord('s'):
            print("Processando a imagem...")
            # O OpenCV usa BGR, mas o face_recognition precisa de RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Procura rostos na imagem
            rostos = face_recognition.face_encodings(rgb_frame, num_jitters=10)
            
            if len(rostos) > 0:
                # Pega o primeiro rosto encontrado (caso tenha mais de uma pessoa na tela)
                encoding = rostos[0]
                
                # Transforma a lista de 128 números em um texto (JSON) para salvar no banco
                encoding_texto = json.dumps(encoding.tolist())
                
                # Salva no banco de dados Neon
                conexao, cursor = conectar_banco()
                if conexao:
                    try:
                        cursor.execute(
                            "INSERT INTO usuarios (nome, encoding) VALUES (%s, %s)", 
                            (nome, encoding_texto)
                        )
                        conexao.commit()
                        print(f"[SUCESSO] Rosto de {nome} cadastrado no Banco!")
                    except Exception as e:
                        print(f"[ERRO] Falha ao salvar no banco: {e}")
                    finally:
                        cursor.close()
                        conexao.close()
                break 
            else:
                print("[ERRO] Nenhum rosto detectado! Tente novamente em um local mais iluminado.")

    # Desliga a câmera e fecha a janela
    video_capture.release()
    cv2.destroyAllWindows()

# Executa o cadastro
if __name__ == "__main__":
    nome_aluno = input("Digite o nome do novo usuário: ")
    cadastrar_usuario(nome_aluno)