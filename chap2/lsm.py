import numpy as np
from PIL import Image, ImageDraw


class ConvInfo:
    def __init__(self, img):
        w, h = img.size
        self.f0 = min(w, h)
        self.x_offset = int(w/2)
        self.y_offset = int(h/2)

    def pixel_to_logical(self, x, y):
        return x - self.x_offset, y - self.y_offset

    def logical_to_pixel(self, x, y):
        px = int(x + self.x_offset)
        py = int(y + self.y_offset)
        return px, py

    def eta(self, x, y):
        f0 = self.f0
        return np.array([x * x, 2 * x * y, y * y, 2 * f0 * x, 2 * f0 * y, f0 * f0])


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


def convert_fplist_to_logical(conv:ConvInfo, fplist):
    result = []
    for x, y in fplist:
        logical_xy = conv.pixel_to_logical(x, y)
        result.append(logical_xy)

    return result


def matrixM(conv:ConvInfo, plist):
    N = len(plist)
    M = np.zeros((6, 6))
    for x, y in plist:
        eta = conv.eta(x, y)
        M = M + np.dot(eta, eta.T)

    M = M / N

    return M

def main():
    im = Image.open("../data/chap2/mami1.png")
    im_fplist = get_featurepoint_list(im)
    print("feature points:", len(im_fplist))
    conv_info = ConvInfo(im)
    print("f0 = ", conv_info.f0)
    log_fplist = convert_fplist_to_logical(conv_info, im_fplist)
    mat_M = matrixM(conv_info, log_fplist)
    print(mat_M)

if __name__ == '__main__':
    main()