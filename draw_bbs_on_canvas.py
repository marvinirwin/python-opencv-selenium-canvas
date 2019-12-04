import cv2


def draw_bbs_on_canvas(centroidStats, driver):
    # Let's draw the things we think we see
    for (centroid, stat, box) in centroidStats:
        # Remove tiny entities, they don't matter
        if stat[cv2.CC_STAT_AREA] < 20:
            continue
        if stat[cv2.CC_STAT_AREA] > 2000:
            continue

        width = int(stat[cv2.CC_STAT_WIDTH])
        height = int(stat[cv2.CC_STAT_HEIGHT])
        driver.execute_script("""
            const [index, canvasx, canvasy, canvaswidth, canvasheight, centx, centy, width, height] = arguments;
            const el = document.createElement('div');
            el.style.position = 'absolute';
            el.style.left = `${canvasx + centx}px`;
            el.style.top = `${canvasy + centy}px`;
            el.style.zIndex = 100;
            el.style.backgroundColor = '6a0dad';
            el.style.opacity = 0.5;
            el.style.width = width + 'px';
            el.style.height = height + 'px';
            // el.style.borderRadius = '20px';
            el.style.backgroundColor = 'green';
            el.style.border = '2px solid #ccc';
            document.body.appendChild(el);
        """, '', 0, 0, 1000, 514,
                              centroid[0] - (width / 2),
                              centroid[1] - (height / 2),
                              width,
                              height
                              )


def cent_stats_boxes(cents, stats):
    a = []
    # TODO avoid the double zip
    for c, s in zip(cents, stats):
        a.append([c, s, get_box_from_centroid_and_stat(c, s)])
    return a


def get_box_from_centroid_and_stat(c, s):
    width = s[cv2.CC_STAT_WIDTH]
    height = s[cv2.CC_STAT_HEIGHT]
    top_x = c[0] - (width / 2)
    top_height = c[1] - (height / 2)
    return Box(
        top_x,
        top_height,
        top_x + width,
        top_height + height
    )


class Box:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.y2 = y2
        self.x2 = x2