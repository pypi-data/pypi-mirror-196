import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import torch
import pandas as pd
import copy
import os
from paddleocr import PaddleOCR
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Add, BatchNormalization, Conv2D, Dense, Flatten, Input, LeakyReLU, PReLU, Lambda
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg19 import VGG19
from PIL import Image

LR_SIZE = 24
HR_SIZE = 96
import numpy as np
import tensorflow as tf


DIV2K_RGB_MEAN = np.array([0.4488, 0.4371, 0.4040]) * 255

def resolve(model, lr_batch):
    lr_batch = tf.cast(lr_batch, tf.float32)
    sr_batch = model(lr_batch)
    sr_batch = tf.clip_by_value(sr_batch, 0, 255)
    sr_batch = tf.round(sr_batch)
    sr_batch = tf.cast(sr_batch, tf.uint8)
    return sr_batch
def resolve_single(model, lr):
    return resolve(model, tf.expand_dims(lr, axis=0))[0]



# ---------------------------------------
#  Normalization
# ---------------------------------------


def normalize(x, rgb_mean=DIV2K_RGB_MEAN):
    return (x - rgb_mean) / 127.5


def denormalize(x, rgb_mean=DIV2K_RGB_MEAN):
    return x * 127.5 + rgb_mean


def normalize_01(x):
    """Normalizes RGB images to [0, 1]."""
    return x / 255.0


def normalize_m11(x):
    """Normalizes RGB images to [-1, 1]."""
    return x / 127.5 - 1


def denormalize_m11(x):
    """Inverse of normalize_m11."""
    return (x + 1) * 127.5


# ---------------------------------------
#  Metrics
# ---------------------------------------



# ---------------------------------------
#  See https://arxiv.org/abs/1609.05158
# ---------------------------------------


def pixel_shuffle(scale):
    return lambda x: tf.nn.depth_to_space(x, scale)
def load_image(path):
    return np.array(Image.open(path))

def plot_sample(lr, sr):
    plt.figure(figsize=(20, 10))

    images = [lr, sr]
    titles = ['LR', f'SR (x{sr.shape[0] // lr.shape[0]})']

    for i, (img, title) in enumerate(zip(images, titles)):
        plt.subplot(1, 2, i+1)
        plt.imshow(img)
        plt.title(title)
        plt.xticks([])
        plt.yticks([])


def upsample(x_in, num_filters):
    x = Conv2D(num_filters, kernel_size=3, padding='same')(x_in)
    x = Lambda(pixel_shuffle(scale=2))(x)
    return PReLU(shared_axes=[1, 2])(x)


def res_block(x_in, num_filters, momentum=0.8):
    x = Conv2D(num_filters, kernel_size=3, padding='same')(x_in)
    x = BatchNormalization(momentum=momentum)(x)
    x = PReLU(shared_axes=[1, 2])(x)
    x = Conv2D(num_filters, kernel_size=3, padding='same')(x)
    x = BatchNormalization(momentum=momentum)(x)
    x = Add()([x_in, x])
    return x


def sr_resnet(num_filters=64, num_res_blocks=16):
    x_in = Input(shape=(None, None, 3))
    x = Lambda(normalize_01)(x_in)

    x = Conv2D(num_filters, kernel_size=9, padding='same')(x)
    x = x_1 = PReLU(shared_axes=[1, 2])(x)

    for _ in range(num_res_blocks):
        x = res_block(x, num_filters)

    x = Conv2D(num_filters, kernel_size=3, padding='same')(x)
    x = BatchNormalization()(x)
    x = Add()([x_1, x])

    x = upsample(x, num_filters * 4)
    x = upsample(x, num_filters * 4)

    x = Conv2D(3, kernel_size=9, padding='same', activation='tanh')(x)
    x = Lambda(denormalize_m11)(x)

    return Model(x_in, x)


gan_generator=sr_resnet()
p=pd.__file__[:-18]
gan_generator.load_weights(p+"dettag/gan_generator.h5")
model=torch.hub.load('ultralytics/yolov5','custom',path=p+"dettag/best.pt",force_reload=True)
ocr=PaddleOCR(lang='en')




def resolve_(img):
    if(type(img))==str:
        img=load_image(img)
    gan_sr = resolve_single(gan_generator, img)
    return gan_sr
def getTags(img,path_to_csv=""):
    hr=resolve_(img)
    img_temp=copy.copy(hr.numpy())
    img=hr.numpy()
    result=model(img_temp)
    img_cords=[]
    for i in result.xyxy:
        img_cords+=i.tolist()
    imgs=[img[int(i[1]):int(i[3]),int(i[0]):int(i[2]),:] for i in img_cords]
    Text={}
    for im in imgs:
        r=ocr.ocr(im)
        txts = [line[1][0] for line in r[0]]
        for i in txts:
            i=i.upper()
            if i in Text:
                Text[i]+=1
            else:
                Text[i]=1
    Text=[[i,Text[i]]for i in Text]
    df=pd.DataFrame(Text)
    df.to_csv(path_to_csv + "/Tags.csv")
    return Text,df
