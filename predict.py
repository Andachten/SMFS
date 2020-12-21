# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 19:49:23 2020

@author: dell
"""

import torchvision.transforms as transforms
import torch as t
from PIL import Image


def pridict(model):

    device = t.device("cuda" if t.cuda.is_available() else "cpu")
    model = model.to(device)

    model.eval()  # 预测模式

    # 获取测试图片，并行相应的处理
    img = Image.open('cat.jpg')
    transform = transforms.Compose([transforms.Resize(256),  # 重置图像分辨率
                                    transforms.CenterCrop(224),  # 中心裁剪
                                    transforms.ToTensor(), ])
    img = img.convert("RGB")  # 如果是标准的RGB格式，则可以不加
    img = transform(img)
    img = img.unsqueeze(0)
    img = img.to(device)

    with t.no_grad():
        py = model(img)
    _, predicted = t.max(py, 1)  # 获取分类结果
    classIndex_ = predicted[0]

    print('预测结果', classIndex_)


if __name__ == '__main__':
    pridict()