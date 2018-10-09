from os import listdir
import numpy as np
import torch
from PIL import Image
from torch.autograd import Variable
from torchvision.transforms import ToTensor
import cv2
from scipy.misc import imresize
from .utils import  is_image_file
from .model import Net
import os

#BASE_DIR = os.path.dirname()

#不同放大倍数的模型文件
checkpoint_dict = {
    2:'epoch_2_100.pt',
    3:'epoch_3_100.pt',
    4:'epoch_4_100.pt',
    8:'epoch_8_100.pt',
}

def build_model(checkpoint,scale):
    '''
    加载pytorch模型
    :param checkpoint:
    :return:
    '''
    model = Net(scale)

    if torch.cuda.is_available():
        model = model.cuda()
    
    model.load_state_dict(torch.load(os.path.join(checkpoint,checkpoint_dict[scale]).replace('\\','/')))
    print('model load')
    return model


def generate_image(model,image):
    '''
    图片清晰度提升
    :param image:
    :param model:
    :return:
    '''
    img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).convert('YCbCr')
#    img = cv2.cvtColor(image,cv2.COLOR_RGB2YCrCb)

#    y,cr,cb = img.split()
    y,cb,cr = img.split()
    image = Variable(ToTensor()(y)).view(1, -1, y.size[1], y.size[0])
    if torch.cuda.is_available():
        image = image.cuda()

    out = model(image)
    out = out.cpu()
    out_img_y = out.data[0].numpy()
    out_img_y *= 255.
    out_img_y = out_img_y.clip(0,255)
    
#    # out_img_y = Image.fromarray(np.uint8(out_img_y[0]),model = 'L')
#    out_img_cb = imresize(cb,out_img_y.size(),interp='bicubic')
#    out_img_cr = imresize(cr,out_img_y.size(),interp='bicubic')
#    # out_img = Image.merge('YCbCr',[out_img_y,out_img_cb,out_img_cr]).convert('RGB')
#    out_img = np.concatenate((out_img_y,out_img_cr,out_img_cb))
#    out_img = cv2.cvtColor(out_img,cv2.COLOR_YCrCb2BGR)
    
    
    out_img_y = Image.fromarray(np.uint8(out_img_y[0]), mode='L')
    out_img_cb = cb.resize(out_img_y.size, Image.BICUBIC)
    out_img_cr = cr.resize(out_img_y.size, Image.BICUBIC)
    out_img = Image.merge('YCbCr', [out_img_y, out_img_cb, out_img_cr]).convert('RGB')
    out_img = cv2.cvtColor(np.asarray(out_img), cv2.COLOR_RGB2BGR)
    return out_img