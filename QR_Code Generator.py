import qrcode

# Input for a QR-Code Creation
website_link = input("What website do you want a code for?: ")

# Creating the QR-Code
qr = qrcode.QRCode(version = 1, box_size = 10, error_correction=qrcode.ERROR_CORRECT_L, border = 5)
qr.add_data(website_link)
qr.make()

# Saving the QR-Code
img = qr.make_image(fill_color = 'black', back_color = 'white')
img.save('custom_qr2.png')