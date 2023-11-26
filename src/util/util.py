from re import X
from PIL import ImageTk, Image

def ajuste_img(img, tam):
    tw, th = tam
    w, h = img.size

    prop = 1
    if (tw - w) < (th - h):
        new_w = tw // prop
        c = new_w / w
        new_h = h * c
    else:
        new_h = th // prop
        c = new_h / h
        new_w = w * c

    return img.resize((int(new_w), int(new_h)))

def convert_ponto (pontos:tuple,original_size:tuple):
    x = pontos[0]/original_size[0]
    y = pontos[1]/original_size[1]
   
    return x,y 
def desconvert_ponto (pontos:tuple,original_size:tuple):
    x = pontos[0]*original_size[0]
    y = pontos[1]*original_size[1]
    
    return x,y
   
def ajuste_img2(img, tam):
    tw, th = tam
    w, h = img.size

    prop = 1
    if (tw - w) < (th - h):
        new_w = tw // prop
        c = new_w / w
        new_h = h * c
    else:
        new_h = th // prop
        c = new_h / h
        new_w = w * c
    print(new_h)
    print(new_w)
    return img.resize((int(new_w), int(new_h)))

def carregar_img(path, tam=None):
    img = Image.open(path)

    if tam is not None:
       return ajuste_img2(img, tam)

    return img

