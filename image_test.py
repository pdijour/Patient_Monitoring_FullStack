import base64
import io
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from skimage.io import imsave


def read_file_as_b64(image_path):
    with open(image_path, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def b64_string_to_file(b64_string, filename):
    image_bytes = base64.b64decode(b64_string)
    with open(filename, "wb") as out_file:
        out_file.write(image_bytes)
    return None


def view_b64_image(base64_string):
    image_bytes = base64.b64decode(base64_string)
    image_buf = io.BytesIO(image_bytes)
    i = mpimg.imread(image_buf, format='JPG')
    plt.imshow(i, interpolation='nearest')
    plt.show()
    return


def save_b64_image(base64_string):
    image_bytes = base64.b64decode(base64_string)
    with open("new-img.jpg", "wb") as out_file:
        out_file.write(image_bytes)
    return


def b64_to_ndarray(b64):
    image_bytes = base64.b64decode(b64)
    image_buf = io.BytesIO(image_bytes)
    img_ndarray = mpimg.imread(image_buf, format='JPG')
    return img_ndarray


if __name__ == "__main__":
    b64 = read_file_as_b64("/Users/michael.tian/Desktop/"
                           "BME 547/class_repos/final-project"
                           "-spooky-dookie/images/test_image.jpg")
    view_b64_image(b64)
    b64_string_to_file(b64, "test_image_output.jpg")
    nd = b64_to_ndarray(b64)
    print(nd[0][0:5])
    print(b64[0:20])
