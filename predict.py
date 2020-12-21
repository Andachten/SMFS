# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 19:49:23 2020

@author: dell
"""

import torchvision.transforms as transforms
import torch as t
from PIL import Image


def predict(model,imgdir):

    device = t.device("cuda" if t.cuda.is_available() else "cpu")
    model = model.to(device)

    model.eval()  # 预测模式

    # 获取测试图片，并行相应的处理
    img = Image.open(imgdir)
    transform = transforms.Compose([transforms.Resize(224),  # 重置图像分辨率
                                    transforms.ToTensor(), ])
    img = transform(img)
    img = img.unsqueeze(0)
    img = img.to(device)

    with t.no_grad():
        py = model(img)
    _, predicted = t.max(py, 1)  # 获取分类结果
    classIndex_ = predicted[0]
    return classIndex_.item()
