import base64
import qrcode
from io import BytesIO


def Generate_qrcode(data: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_byte_array = BytesIO()
    img.save(img_byte_array)

    base64_image = base64.b64encode(img_byte_array.getvalue()).decode("utf-8")
    return base64_image
