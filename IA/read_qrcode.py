# Importando as libs
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import pygame

# Construir o analisador de argumentos e analisar os argumentos
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="resultado.csv") # esse é o arquivo que vai ser salvo com os dados que foram lidos.
args = vars(ap.parse_args())

# Iniciar a stream (iniciar a webcam) e permitir que o sensor da câmera aqueça
print("[INFO] Iniciando o stream e o arquivo .CSV")
vs = VideoStream(src=0).start()

time.sleep(2)

csv = open(args["output"], "a")
found = set()

# loop sobre a stream
while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=800)

    barcodes = pyzbar.decode(frame)

    # loop sobre os códigos de barras detectados
    for barcode in barcodes:
        # extrair o local da caixa delimitadora do código de barras e desenhar
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # desenha os dados do código de barras e o tipo de código de barras na imagem
        text = "{} ({})".format(barcodeData,barcodeType)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # não expõe os dados
        # text = "{}".format(barcodeData, barcodeType)
        # cv2.putText(frame, '', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # csv.write("{},{}\n".format(datetime.datetime.now(), barcodeData))

        if barcodeData not in found:
            print(barcodeData)
            csv.write("{}\n".format(barcodeData))
            csv.flush()

            found.clear()
            found.add(barcodeData)

    # Título do Frame
    cv2.imshow("Scanner QRCode", frame)
    key = cv2.waitKey(1) & 0xFF

    # A letra q encerra 
    if key == ord("q"):
        break

# fecha o arquivo CSV
print("[INFO] Finalizando a stream e fechando o arquivo CSV...")
csv.close()
cv2.destroyAllWindows()
vs.stop()