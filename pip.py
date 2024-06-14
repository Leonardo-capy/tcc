import cv2

xml_haar_cascade = 'haarcascade_frontalface_alt2.xml'

classificador_de_faces = cv2.CascadeClassifier(xml_haar_cascade)

# Iniciar a câmera
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

known_faces = {}  # Dicionário para armazenar os rostos conhecidos com seus respectivos nomes

while not cv2.waitKey(10) & 0xFF == 27:
    ret, frame_color = capture.read()

    gray = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)

    faces = classificador_de_faces.detectMultiScale(gray)

    for x, y, w, h in faces:
        # Verifica se o rosto está na lista de rostos conhecidos
        is_known = False
        for name, (known_x, known_y, known_w, known_h) in known_faces.items():
            if abs(x - known_x) < 50 and abs(y - known_y) < 50 and abs(w - known_w) < 50 and abs(h - known_h) < 50:
                is_known = True
                cv2.putText(frame_color, f"Rosto conhecido ({name})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                break
        
        # Se o rosto não for conhecido, exibe um prompt para inserir um nome
        if not is_known:
            name = input("Rosto desconhecido. Insira um nome: ")
            known_faces[name] = (x, y, w, h)
            cv2.putText(frame_color, f"Rosto adicionado como '{name}'", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Desenha o retângulo ao redor do rosto
        cv2.rectangle(frame_color, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('color', frame_color)
