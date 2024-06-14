import cv2
import mediapipe

# Inicializar a webcam
webcam = cv2.VideoCapture(0)

# Inicializar o reconhecedor de rostos do MediaPipe
face_detection = mediapipe.solutions.face_detection.FaceDetection()

while True:
    # Ler o frame da webcam
    ret, frame = webcam.read()

    if not ret:
        break

    # Processar o frame para detecção de rostos
    result = face_detection.process(frame)

    # Verificar se foram detectados rostos
    if result.detections:
        for detection in result.detections:
            # Desenhar o retângulo ao redor do rosto
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                   int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(frame, bbox, (0, 255, 0), 2)

            # Exibir uma mensagem para o usuário
            cv2.putText(frame, "Pessoa Detectada. Cadastrar? (s/n)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Mostrar o frame com as detecções
            cv2.imshow("Rostos na Webcam", frame)

            # Aguardar pela entrada do usuário
            key = cv2.waitKey(0)

            # Se o usuário pressionar 's', a pessoa é cadastrada
            if key == ord('s'):
                print("Pessoa cadastrada!")
                # Adicione o código para cadastrar a pessoa aqui

            # Se o usuário pressionar 'n', a pessoa não é cadastrada
            elif key == ord('n'):
                print("Pessoa não cadastrada!")

    # Quando 'ESC' é pressionado, sair do loop
    if cv2.waitKey(1) == 27:
        break

# Liberar recursos
webcam.release()
cv2.destroyAllWindows()
