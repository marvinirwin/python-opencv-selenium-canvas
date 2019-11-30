import base64
import time

from selenium import webdriver
import cv2
import numpy as np


def adaptiveThresh(img):
    img = cv2.medianBlur(img, 5)
    ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                cv2.THRESH_BINARY, 11, 2)
    th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 11, 2)
    titles = ['Original Image', 'Global Thresholding (v = 127)',
              'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    images = [img, th1, th2, th3]
    return zip(images, titles)

def create_image(driver, base64png, title):
    str = """
    try {
        debugger;
        const title = document.createElement('h3');
        title.text = arguments[0];
        document.body.appendChild(title);
        
        const img = document.createElement('img');
        img.src = `data:image/jpeg;base64,${arguments[1]}`;
        document.body.appendChild(img);
    }
    catch(e) {
        console.log(e);
    }
    """
    driver.execute_script(
        str,
        title,
        base64png
    )


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
    # Now what do we do with this image?
    # We detect objects inside of it and keep a list of them and their positions on the screen
    # And we draw that list on the screen


try:

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-web-security')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://localhost:5000/")
    canvas = driver.find_element_by_id('canvas')
    images = adaptiveThresh(get_driver_image(driver, canvas))

    # Now I have to iterate through these images, and turn them into html src images
    for (image, title) in images:
        # TODO figure out retval is for
        retval, buffer = cv2.imencode('.png', image)
        base64_png = base64.b64encode(buffer).decode()
        create_image(driver, base64_png, title)
    time.sleep(10)
except Exception as e:
    driver.close()
    raise e
driver.close()



