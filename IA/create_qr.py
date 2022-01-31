import qrcode
url = {"modelo":"DELL I5243","marca":"DELL","fabricacao":"12/09/2021"}
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit = True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("qr.jpeg")