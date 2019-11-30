import base64

import cv2
import numpy as np


def get_driver_image(driver, canvas):
    str = """
    try {
        let img = arguments[0].toDataURL('image/png').substring(21);
        return img;
    }
    catch(e) {
        console.log(e);
    }
    """
    canvas_base64 = driver.execute_script(
        str,
        canvas
    )

    cap = base64.b64decode(canvas_base64)
    image = cv2.imdecode(np.frombuffer(cap, np.uint8), 1)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image