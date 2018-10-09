import os
import argparse

from PIL import Image
from torchvision import transforms
from torchvision.transforms import CenterCrop,Scale,Compose
from torch.utils.data.dataset import Dataset
import tqdm
import glob

def is_image_file(filename):
    return any(filename.endswith(extension) for extension in ['.png', '.jpg', '.jpeg', '.JPG', '.JPEG', '.PNG'])


def is_video_file(filename):
    return any(filename.endswith(extension) for extension in ['.mp4', '.avi', '.mpg', '.mkv', '.wmv', '.flv'])


def clculate_valid_crop_size(crop_size,scale):

    return crop_size - (crop_size % scale)


def input_transform(crop_size,scale):

    return Compose([
        CenterCrop(crop_size),
        Scale(crop_size // scale,interpolation=Image.BICUBIC)
    ])

def target_transform(crop_size):

    return Compose([
        CenterCrop(crop_size)
    ])


def generate_dataset(data_dir,crop_size,scale):
    '''
    遍历该文件夹下面的所有图片文件，生成数据集
    :param data_dir:
    :return:
    '''
    sub_dirs = [x[0] for x in os.walk(data_dir)]
    is_root = True

    extends = ['jpg','png','jpeg','bmp']
    filenames = []
    for sub_dir in sub_dirs:

        if is_root:
            is_root = False
            continue
        for extend in extends:
            filenames.extend(glob.glob(os.path.join(sub_dir,"*.",extend)))

    crop_size = clculate_valid_crop_size(crop_size,scale)
    lr_transform = input_transform(crop_size,scale)
    hr_transform = target_transform(crop_size)
    root = './data/'
    if not os.path.exists(root):
        os.makedirs(root)

    input_path = os.path.join(root,'input/SRF_'+str(scale))
    if not os.path.exists(input_path):
        os.makedirs(input_path)

    target_path = os.path.join(root,'input/SRF_'+str(scale))
    if not os.path.exists(target_path):
        os.makedirs(target_path)



    for filename in tqdm.tqdm(filenames,desc='生成放大%s倍数据集,数据来自%s'%(scale,data_dir)):

        image = Image.open(filename)
        target = image.copy()

        image_lr = lr_transform(image)
        image_hr = hr_transform(target)

        image_lr.save(os.path.join(input_path,os.path.basename(filename)))
        image_hr.save(os.path.join(target_path,os.path.basename(filename)))

class DataSetFromFold(Dataset):

    def __init__(self,dataset_dir,scale,input_transform = None,target_transform = None):

        super(Dataset,self).__init__()
        self.image_dir = dataset_dir + '/input/SRF_'+str(scale)+'/'
        self.target_dir = dataset_dir + '/target/SRF_'+str(scale)+'/'
        self.image_name = [os.path.join(self.image_dir,x) for x in os.listdir(self.image_dir)]
        self.target_name = [os.path.join(self.target_dir,x) for x in os.listdir(self.target_dir)]
        self.input_transform = input_transform
        self.target_transform = target_transform

    def __getitem__(self, index):

        image,_,_ = Image.open(self.image_name[index].convert('YCbCr').split())
        targte,_,_ = Image.open(self.target_name[index].convert('YCbCr').split())

        if self.input_transform:
            image = self.input_transform(image)

        if self.target_transform:
            target = self.target_transform(target)

        return image,target

    def __len__(self):
        return len(self.image_name)


if __name__ == '__main__':

    arg = argparse.ArgumentParser(description='生成训练用的数据')
    arg.add_argument('--data_dir',type = str,help = '训练图片的文件夹目录',dest = 'data_dir',required=True)
    arg.add_argument('--scale',default=3,type = int,help = '图片放大的倍数',dest = 'scale')
    arg.add_argument('--crop_size',default=256,type = int,help = '图片裁剪的大小',dest = 'crop_size')
    opt = arg.parse_args()

    scale = opt.scale
    crop_size = opt.crop_size
    data_dir = opt.data_dir
    generate_dataset(data_dir,crop_size,scale)
