from .metrics import dice_loss, dice_coef, iou
from tensorflow.keras.utils import CustomObjectScope
import tensorflow as tf
import cv2
import numpy as np
import io
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

""" Global parameters """
H = 512
W = 512

""" Creating a directory """


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def fast_remover(my_image):
    """ Seeding """
    np.random.seed(42)
    tf.random.set_seed(42)

    """ Loading model: DeepLabV3+ """
    with CustomObjectScope({'iou': iou, 'dice_coef': dice_coef, 'dice_loss': dice_loss}):
        model = tf.keras.models.load_model("removebg_app/model/y_model.h5")

    print("Start >>>>>>>>>>>>>>>>>>>")

    """ Read the image """
    # image = cv2.imread(r"D:\photos\freelancer.png", cv2.IMREAD_COLOR)
    image = cv2.imdecode(np.fromstring(my_image.read(), np.uint8), cv2.IMREAD_COLOR)

    h, w, _ = image.shape
    x = cv2.resize(image, (W, H))
    x = x/255.0
    x = x.astype(np.float32)
    x = np.expand_dims(x, axis=0)

    """ Prediction """
    y = model.predict(x)[0]
    y = cv2.resize(y, (w, h))
    y = np.expand_dims(y, axis=-1)
    y = y > 0.5

    photo_mask = y
    background_mask = np.abs(1-y)
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    masked_photo = image * photo_mask
    background_mask = np.concatenate([background_mask, background_mask, background_mask], axis=-1)

    img_float32 = np.float32(background_mask)
    bg_mask = cv2.cvtColor(img_float32, cv2.COLOR_BGR2BGRA)
    final_photo = masked_photo + bg_mask
    # cv2.imwrite("result2.png", final_photo)

    ''' Convert arr into binary image '''
    _, buffer = cv2.imencode(".png", final_photo)
    io_buf = io.BytesIO(buffer)

    return io_buf.read()