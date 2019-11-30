import base64
import time

from selenium import webdriver
import cv2

from adaptive_thresh import adaptiveThresh
from create_image import create_image
from get_driver_image import get_driver_image

try:
    # Disable CORS, chrome may be scared of you downloading pixels from a canvas (they may be malicious)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-web-security')
    driver = webdriver.Chrome(options=chrome_options)

    # After we have the driver, go to the page hosted by server.py
    driver.get("http://localhost:5000/")
    # Get the canvas element
    canvas = driver.find_element_by_id('canvas')

    # Get all the permutations of our greyscale image
    images = adaptiveThresh(get_driver_image(driver, canvas))

    # Now append them to the body of our page, so we can decide which one we like
    for (image, title) in images:
        _, buffer = cv2.imencode('.png', image)
        base64_png = base64.b64encode(buffer).decode()
        create_image(driver, base64_png, title)
    # Sleep so we have time to see our handywork
    time.sleep(30)

except Exception as e:
    driver.close()
    raise e
driver.close()



