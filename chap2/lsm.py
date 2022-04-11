import numpy as np
from PIL import Image, ImageDraw


def get_featurepoint_list(image):
    l = []
    width, height = image.size
    print(width, height)

    r_thresh = 170
    g_thresh = 110
    b_thresh = 110

    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            if r > r_thresh and g < g_thresh and b < b_thresh:
                l.append((x, y))

    return l


def plot_feature_points(image: Image, fplist, filename):
    im_work = image.copy()
    draw = ImageDraw.Draw(im_work)
    size = 2
    for x, y in fplist:
        pos = (x-size, y-size, x+size, y+size)
        draw.ellipse(pos, fill=(255, 0, 0))

    im_work.save(filename)
    print("save to ", filename)

def main():
    im = Image.open("../data/chap2/mami1.png")
    im_fplist = get_featurepoint_list(im)
    print("feature points:", len(im_fplist))
    plot_feature_points(im, im_fplist, '../result/chap2/fp_mami1.png')



if __name__ == '__main__':
    main()