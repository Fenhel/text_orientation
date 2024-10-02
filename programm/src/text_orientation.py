import cv2
import torch
import torch.nn as nn
import warnings
from torchvision.transforms import v2
from torchvision.models import resnet50

warnings.filterwarnings('ignore')

IMG_SIZE = 224
# применяемы трансформации
def prepared_model(state_dict='src/../model/resnet_txt_orientation.pth'):
    ## Подготовим модель
    resnet = resnet50()
    in_features = 2048
    out_features = 4
    resnet.fc = nn.Linear(in_features, out_features)

    resnet.load_state_dict(torch.load(state_dict, weights_only=True, map_location=torch.device('cpu')))
    return resnet.eval()

def evaluate(img_size=IMG_SIZE, img_path='src/../../images/402___96f14679afdb4078bb277152b1b6c215.png'): # нужно убрать дефолтную картинку
    transformer = v2.Compose([
        v2.ToImage(),
        v2.Resize((img_size, img_size))
        ])
    model = prepared_model()
    img = transformer(cv2.imread(img_path))
    result = int(torch.argmax(model(img.unsqueeze(0).float()), 1))
    return result