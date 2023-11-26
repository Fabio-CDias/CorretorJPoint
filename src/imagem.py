from cgi import print_environ
from re import X
from config.consts import width, height
from src.util import util


from PIL import ImageTk,Image

class Imagem:
    def __init__(self, canvas, path,pos,ajustar=True):
        self.path = path
        self.img = Image.open(path)
        if ajustar:
            self.img = self.ajuste_img(self.img,(width,height))
        self.tamX, self.tamY = self.img.size
        self.limX, self.limY = self.tamX, self.tamY
        #self.posx, self.posy = width//2, height//2
        self.posx = pos[0]
        self.posy = pos[1]
        # print(self.img.size)

        #zoom
        self.x = 0
        self.qtdZoom = 100
        self.id = None
        self.canvas = canvas

    def point_convert(self,prop:tuple):
        x = self.tamX*prop[0]
        y = self.tamY*prop[1]
        
        x += self.posx-(self.tamX//2)
        y += self.posy-(self.tamY//2)
        return x,y


    def point_desconvert (self, prop:tuple):
        x = prop[0] - (self.posx-(self.tamX//2))
        y = prop[1] - (self.posy-(self.tamY//2))
        x /= self.tamX
        y /= self.tamY
        
        return x,y

    def ajuste_img(self,img,tam):
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

    def photoImg(self):
        return ImageTk.PhotoImage(self.img)

    def plot(self, anchor='center'):
        self.photo = self.photoImg()

        if self.id is not None:
            self.canvas.delete(self.id)

        self.id = self.canvas.create_image((self.posx, self.posy), image=self.photo, anchor=anchor)
        return self

    def move(self):
        pass

    def zoom(self, pos, aumento):
        #resetar para o original
        if not aumento and self.x - 1 <= 0:
            self.img = util.carregar_img(self.path, (width, height))
            self.x = 0
            return self.plot(pos=(width//2, height//2))

        pX, pY = pos #mouse
        pIX, pIY = self.posx - (self.tamX / 2), self.posy - (self.tamY / 2) #pos imagem na origem

        #pos do mouse relativa a imagem
        pX = pIX if pX < pIX else pX
        pX = pIX + self.tamX if pX > pIX + self.tamX else pX

        pY = pIY if pY < pIY else pY
        pY = pIY + self.tamY if pY > pIY + self.tamY else pY

        #usado para os blips
        pcX = (pX - pIX) / self.tamX
        pcY = (pY - pIY) / self.tamY

        #tam zoom
        tamX = self.tamX + self.qtdZoom if aumento else self.tamX - self.qtdZoom
        tamY = self.tamY + self.qtdZoom if aumento else self.tamY - self.qtdZoom

        self.img = self.img.resize((tamX, tamY))

        pIX, pIY = self.posx - (tamX / 2), self.posy - (tamY / 2)





        self.canvas.moveto(self.id, 0, 0)

        
        
        '''
        if event.delta > 0:
            self.tamX += 100
            self.tamY += 100
        else:
            if self.tamX > self.limX and self.tamY > self.limY:
                self.tamX -= 100
                self.tamY -= 100

        self.img = self.img.resize((self.tamX, self.tamY))
        self.photoImg = ImageTk.PhotoImage(self.img)

        self.canvas.itemconfigure(self.mainImg, image=self.photoImg)

        mx, my = 0, 0

        if event.delta > 0:
            if event.x < self.posx:
                mx = min((self.posx - event.x) / 10, 100)
            else:
                mx = max((self.posx - event.x) / 10, -100)

            if event.y < self.posy:
                my = min((self.posy - event.y) / 10, 100)
            else:
                my = max((self.posy - event.y) / 10, -100)
        else:
            if width//2 > self.posx:
                mx = min(width//2 - self.posx, 50)
            else:
                mx = max(width//2 - self.posx, -50)

            if height//2 > self.posy:
                my = min(height//2 - self.posy, 50)
            else:
                my = max(height//2 - self.posy, -50)

        self.posx += mx
        self.posy += my

        self.canvas.move(self.mainImg, mx, my)
        '''