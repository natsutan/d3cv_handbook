import math
import os
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

class ConvInfo:
    def __init__(self, img):
        w, h = img.size
#        self.f0 = min(w, h)
        self.f0 = 1.0
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
        arr = np.array([x * x, 2 * x * y, y * y, 2 * f0 * x, 2 * f0 * y, f0 * f0])
        xi = arr.reshape(-1, 1)
        return xi


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

def plot_result(image: Image, fplist, elist, filename):
    im_work = image.copy()
    draw = ImageDraw.Draw(im_work)

    #eclipse
    size = 2
    for x, y in elist:
        pos = (x - size, y - size, x + size, y + size)
        draw.ellipse(pos, fill=(125, 125, 255))

    # feature point
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


def convert_logical_to_image(conv:ConvInfo, llist):
    result = []
    for xy in llist:
        x = xy[0, 0]
        y = xy[0, 1]
        im_xy = conv.logical_to_pixel(x, y)
        result.append(im_xy)

    return result



def matrixM(conv:ConvInfo, plist):
    N = len(plist)
    M = np.zeros((6, 6))
    for x, y in plist:
        eta = conv.eta(x, y)
        tmp = np.dot(eta, eta.T)
        M = M + tmp

    M = M / N

    rank = np.linalg.matrix_rank(M)
    print("rank M:", rank)
    print(M)

    return M

def infer_theta(M):
    w, v = np.linalg.eig(M)
    print("w ", w)
    print("v ", v)

    theta = v[:,5]
    print('theta ', theta)
    print("norm ", np.linalg.norm(theta))
    return theta


# Thanks to Daily Tech Blog
# https://daily-tech.hatenablog.com/entry/2018/04/13/084734
def getEllipseProperty(A, B, C, D, E, F):
    if A < 0:
        A = -A
        B = -B
        C = -C
        D = -D
        E = -E
        F = -F

        # Spectral Decomposition
    M = np.matrix([[A, B / 2], [B / 2, C]])
    lamdas, v = np.linalg.eigh(M)

    # Diagonalize Coeffs Matrix
    DiagA = v.T * M * v

    # Apply translation for 1st order term.
    tmp = np.matrix([D, E]) * v

    # Calculate coefficient in rotated coords
    AA = DiagA[0, 0]
    BA = DiagA[0, 1] + DiagA[1, 0]
    CA = DiagA[1, 1]
    DA = tmp[0, 0]
    EA = tmp[0, 1]
    scale = F - DA ** 2 / (4 * AA) - EA ** 2 / (4 * CA)

    # Normalize coeffs wrt to constant term.
    AA = AA / abs(scale)
    BA = BA / abs(scale)
    CA = CA / abs(scale)
    DA = DA / abs(scale)
    EA = EA / abs(scale)
    FA = abs(scale) / abs(scale)

    # Ellipse Property Extraction
    a = 1 / math.sqrt(abs(lamdas[0] / scale))
    b = 1 / math.sqrt(abs(lamdas[1] / scale))

    T = np.matrix([[v[0, 0], v[0, 1]], [v[1, 0], v[1, 1]]])
    trans = v.T * np.matrix([[-DA / (2 * AA)], [-EA / (2 * CA)]])

    valid = True
    if AA * CA < 0:
        valid = False

    return valid, np.matrix([[a], [b]]), trans, T


# Thanks to Daily Tech Blog
# https://daily-tech.hatenablog.com/entry/2018/04/13/084734
def generateVecFromEllipse(axis, center, T, rng=[0, 2 * math.pi], num=601):
    t = np.linspace(rng[0], rng[1], num)
    t = np.reshape(t, (t.shape[0], 1))

    xVec = np.zeros((t.shape))
    yVec = np.zeros((t.shape))
    for i in range(t.shape[0]):
        xVec[i] = axis[0, 0] * math.cos(t[i])
        yVec[i] = axis[1, 0] * math.sin(t[i])

    dataTmp = np.concatenate((xVec, yVec), axis=1)
    dataTmp = T * dataTmp.T
    dataTmp = dataTmp.T
    dataTmp[:, 0] = dataTmp[:, 0] + center[0, 0]
    dataTmp[:, 1] = dataTmp[:, 1] + center[1, 0]

    return dataTmp


def plotData(dataEst):
    fig, ax = plt.subplots(ncols=1, figsize=(10, 10))
#    plt.xlim(-10, 10)
#    plt.ylim(-10, 10)
    ax.plot(dataEst[:, 0], dataEst[:, 1])
    plt.show()

def main():
    file_base = "mami1"

    im = Image.open(os.path.join("../data/chap2/", file_base +".png"))
    im_fplist = get_featurepoint_list(im)
    print("feature points:", len(im_fplist))

    plot_feature_points(im, im_fplist, os.path.join("../result/chap2/", "fp_" + file_base + ".png"))

    conv_info = ConvInfo(im)
    print("f0 = ", conv_info.f0)
    log_fplist = convert_fplist_to_logical(conv_info, im_fplist)
    mat_M = matrixM(conv_info, log_fplist)
    theta = infer_theta(mat_M)

    A = theta[0]
    B = 2 * theta[1]
    C = theta[2]
    D = 2 * conv_info.f0 * theta[3]
    E = 2 * conv_info.f0 * theta[4]
    F = conv_info.f0 * conv_info.f0 * theta[5]

    valid, axis, centerEst, Rest = getEllipseProperty(A, B, C, D, E, F)
    dataEst = generateVecFromEllipse(axis, centerEst, Rest)
    im_ellipse = convert_logical_to_image(conv_info, dataEst)

    plot_result(im, im_fplist, im_ellipse, os.path.join("../result/chap2/", "lsm_" + file_base + ".png"))

if __name__ == '__main__':
    main()