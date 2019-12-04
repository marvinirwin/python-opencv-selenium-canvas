import math
import time

from selenium import webdriver
import cv2

from adaptive_thresh import adaptiveThresh
from draw_bbs_on_canvas import draw_bbs_on_canvas, cent_stats_boxes, Box
from get_driver_image import get_driver_image

CONNECTIVITY = 4


def euclid_distance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def intersection(a: Box, b: Box):
    x1 = max(min(a.x1, a.x2), min(b.x1, b.x2))
    y1 = max(min(a.y1, a.y2), min(b.y1, b.y2))
    x2 = min(max(a.x1, a.x2), max(b.x1, b.x2))
    y2 = min(max(a.y1, a.y2), max(b.y1, b.y2))
    if x1 < x2 and y1 < y2:
        return True


# This will fill indexTypeMap with mappings from each index to a type
# def typify_elements(indexTypeMap, centroids, stats):

# This should return a map of index -> vectors representing the way each thing is moving
# Maybe it should keep track of the player's movement?
# Maybe it wont have to
# I'll probably have to look up how they do this, I imagine you check whose bounding boxes overlap
# If a bounding box doesn't overlap with anything else the original object has disappeared
# Above is a hack, but it will probably work?  Maybe I'll have to make the bounding box bigger
# It will return a list of new centroids and stats, and a list of the deleted ones
# What if more than two bounding boxes overlap?
# I guss they all become the same object?
# There's probably a better way to do motion tracking?  Or is there?
# So what if 3+ things overlap?
# What if there is one thing which now overlaps with two bounding boxes?
# Screw it, I'll take the closest one as bounding box, tiebreaking by taking the first one
def track_motion(cent_stats_boxes_1, cents_stats_boxes_2, diff):
    # There's probably a really cool way of searching through the bounding boxes I could be near
    # But I don't know it
    # Returns a list of objects in the frame and how fast they are moving
    centroidsStillHere = []
    centroidsDeleted = []
    a = []
    for (centroid2, stat2, box2) in cents_stats_boxes_2:
        # Ge the bounding rect
        x2, y2, w2, h2 = cv2.boundingRect(centroid2)
        # Find the corresponding centroid
        # TODO make this more efficient than O(n*m)
        for (centroid1, stat1, box1) in cent_stats_boxes_1:
            if intersection(box2, box1):
                # Now take the euclidian distance between x and y
                # Get the ratio between the diff (milliseconds) and one second
                distRatio = 1000 / diff
                # Get the unscaled vector, representing the movement of your thing every one second
                vec = (
                    (centroid2[0] - centroid1[0]) * distRatio,
                    (centroid2[1] - centroid1[1]) * distRatio
                )

                a.append((centroid2, stat2, box2, vec))
                # Break from the forLoop, we've found our thing
                # Also I should really make a class for these progressively larger tuples
                break

    return a


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
    threshed = adaptiveThresh(get_driver_image(driver, canvas))
    # Get the connected components, these are the things we'll recognize as objects
    _, _, stats, centroids = cv2.connectedComponentsWithStats(threshed, CONNECTIVITY, cv2.CV_32S)
    centroidStats = cent_stats_boxes(centroids, stats)
    draw_bbs_on_canvas(centroidStats, driver)

    # So now we have a single thing, but we need multiple things
    # How do we do this?
    # Easy, we take a recording of diep.io and make it a gif

    # Sleep so we have time to see our handywork
    time.sleep(30)



except Exception as e:
    driver.close()
    raise e
driver.close()
