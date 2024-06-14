import cv2

# Inicializa o classificador de detecção de rosto
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Lista de rostos conhecidos e seus nomes
known_faces = []
known_names = []

# Inicializa a webcam
video_capture = cv2.VideoCapture(0)

# Define a resolução desejada
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    # Captura um quadro da câmera
    ret, frame = video_capture.read()

    # Redimensiona o quadro para melhor desempenho
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Converte o quadro para escala de cinza
    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

    # Detecta rostos na imagem
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Desenha retângulos ao redor dos rostos detectados
    for (x, y, w, h) in faces:
        # Verifica se o rosto está dentro de uma margem de erro das coordenadas dos rostos conhecidos
        is_known = any(abs(x - known_x) < 50 and abs(y - known_y) < 50 and abs(w - known_w) < 50 and abs(h - known_h) < 50 for (known_x, known_y, known_w, known_h) in known_faces)
        
        # Desenha retângulo verde se o rosto é conhecido, senão desenha em vermelho
        color = (0, 255, 0) if is_known else (0, 0, 255)
        cv2.rectangle(small_frame, (x, y), (x+w, y+h), color, 2)

        # Se o rosto é desconhecido e ainda não foi nomeado
        if not is_known and (x, y, w, h) not in known_faces:
            # Prompt para inserir o nome do rosto conhecido
            cv2.putText(small_frame, "Pressione 's' para adicionar o nome", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Se 's' for pressionado, adiciona o rosto detectado à lista de rostos conhecidos
            if cv2.waitKey(1) & 0xFF == ord('s'):
                name = input("Digite o nome do rosto conhecido: ")
                known_faces.append((x, y, w, h))
                known_names.append(name)
                print("Rosto adicionado à lista de rostos conhecidos com o nome:", name)

        # Se o rosto é conhecido, exibe o nome sobre o retângulo delimitador
        elif is_known:
            index = known_faces.index((x, y, w, h))
            name = known_names[index]
            cv2.putText(small_frame, name, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Exibe o quadro
    cv2.imshow('Video', small_frame)

    # Se 'q' for pressionado, sai do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a captura de vídeo e fecha a janela
video_capture.release()
cv2.destroyAllWindows()
