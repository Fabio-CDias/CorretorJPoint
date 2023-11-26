import tkinter as tk
from tkinter import filedialog
import math, os
import json
from config.consts import width, height
from src.util import util
from src.imagem import Imagem

from PIL import ImageTk

# from tk.app import key_pressed
pathRoot = os.path.abspath(__file__)
pathRoot = os.path.dirname(pathRoot)
pathRec = os.path.join(os.path.dirname(pathRoot), "rec")

class Blip:
    def __init__(self, canvas, center: tuple, tam, cor):
        x, y = center

        self.x = x
        self.y = y
        self.tam = tam
        self.visivel = True

        self.canvas = canvas
        self.blip = self.canvas.create_oval(x, y, x+tam, y+tam, fill=cor)
        
    def setVisible(self, status):
        self.visivel = status
        if status:
            self.canvas.itemconfigure(self.blip,state="normal")
        else:
            self.canvas.itemconfigure(self.blip,state="hidden")

    def onMouse(self, x, y):
        halfTam = self.tam // 2
        xb, yb = self.x + halfTam, self.y + halfTam
        return math.sqrt((x - xb)**2 + (y - yb)**2) < (halfTam + 2)

    def move(self, x, y):
        self.x = x - self.tam // 2
        self.y = y - self.tam // 2

        self.canvas.moveto(self.blip, self.x, self.y)

class ScreenMain:
    count_img = 0
    pose = []
    
    def  __init__(self,master):
        global pathRec
        self.master = master

        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        self.default_pathImages = os.path.join("frames","pasta")     # Variable needed due to hardcoding
        self.default_pathJsons  = os.path.join("pose","pasta")       # Variable needed due to hardcoding

        self.tam_blip = 10

        pcores = ["#ff00ff","#0000ff","#00ff00","#ffff00","#ff0000"]
        self.cores = {
            "pose_keypoints_2d": 'blue',
            "hand_left_keypoints_2d": pcores,
            "hand_right_keypoints_2d": pcores
        }
    
        self.count = 0
        self.update()
        self.draw()
        self.gerar_tela()
        self.num_images = self.image_quantity()

    def update(self):
        self.pathJsons =  os.path.join(pathRec,self.default_pathJsons,str(self.count)+"_keypoints.json")
        self.pathImagens =  os.path.join(pathRec,self.default_pathImages,str(self.count)+".jpg")
        self.pathMaoesquerda = os.path.join(pathRec, "maoesquerda.png")
        self.pathMaodreita = os.path.join(pathRec, "maodireita.png")
        self.pathteclas = os.path.join(pathRec, "comandos.png")
        
    # Controls the event of changing images and points back and forth, and update info.  
    def back(self):
        self.canvas.delete("all")
        if self.count > 0: 
            self.count -= 1
        else:
            self.count = self.num_images -1

        self.update()
        self.gerar_tela()
        self.frame_count.config(text=f"Frame: {self.count}")
        
    def next(self):
        self.canvas.delete("all")
        if self.count < self.num_images -1:
            self.count += 1
        else:
            self.count = 0

        self.update()
        self.gerar_tela()
        self.frame_count.config(text=f"Frame: {self.count}")

    def salvar(self,pathJson):
        lista = {}
        for tipo in ["pose_keypoints_2d", "hand_left_keypoints_2d", "hand_right_keypoints_2d"]:
            lista[tipo] = []
            for blip in self.listaBlips[tipo]:
                
                p = util.desconvert_ponto(self.img.point_desconvert((blip.x,blip.y)),(1920,1080))
                lista[tipo].append(p[0]+9)
                lista[tipo].append(p[1])
                lista[tipo].append(1)
        self.data["people"][0]["pose_keypoints_2d"] = lista["pose_keypoints_2d"]
        self.data["people"][0]["hand_left_keypoints_2d"] = lista["hand_left_keypoints_2d"]
        self.data["people"][0]["hand_right_keypoints_2d"] = lista["hand_right_keypoints_2d"]
        with open(pathJson, 'w') as f:
            json.dump(self.data,f)


    #It searches a given directory data (images or points)
    def select_directory(self,images=False,points=False):
        dir = filedialog.askdirectory()
        try:
            if images and len(dir) > 0:
                self.default_pathImages = dir.split(pathRec)[1][1:]
                self.pathImagens = os.path.join(pathRec,self.default_pathImages,"0.jpg")
            elif points and len(dir) > 0:
                self.default_pathJsons = dir.split(pathRec)[1][1:]
                self.pathJsons = os.path.join(pathRec,self.default_pathJsons,"0_keypoints.json")
                
            
            self.canvas.delete("all")
            self.count = 0
            self.num_images = self.image_quantity()
            self.image_directory.config(text=self.default_pathImages)
            self.point_directory.config(text=self.default_pathJsons)
            self.gerar_tela()

        except ValueError:
            raise RuntimeError("Could not load:") from ValueError

    # Set width and height frame values based on its percentage
    def set_width_frame(self, percentage): return width * percentage / 100
    def set_height_frame(self, percentage): return height * percentage / 100
    # Calculates the amount of images of the current directory
    def image_quantity(self): return len(os.listdir(os.path.dirname(self.pathImagens)))
    #Events
    def save_evt(self): self.salvar(os.path.join(pathRec,self.default_pathJsons,f"{self.count}_keypoints.json"))
    def next_evt(self): self.next()
    def prev_evt(self): self.back()
    # Drawing into the screen, based on tkinter frames.
    def draw(self):
        self.font = ("Helvetica", 16)
        self.font2 = ("Helvetica",12)
        self.bg_menu = "#005b96"
        self.bg_color = "#4b86b4"
        self.color_font = "#e7eff6"
        self.bg_display_color = "#2a4d69"

        self.main_frame = tk.Frame(self.master,width=width,height=height,background="white")
        self.main_frame.pack()

        self.menu_frame = tk.Frame(self.main_frame,width=self.set_width_frame(100),height=self.set_height_frame(10),bg=self.bg_menu)
        self.menu_frame.pack(expand=True,fill="x")

        self.prev_button = tk.Button(self.menu_frame,text="◄",command=self.prev_evt,borderwidth=2,font=self.font,bg=self.bg_color,fg=self.color_font)
        self.prev_button.pack(side=tk.LEFT,padx=10,pady=10)

        self.frame_count = tk.Label(self.menu_frame,text= f"Frame: {self.count}",font=self.font,bg=self.bg_menu,fg=self.color_font)
        self.frame_count.pack(side=tk.LEFT,padx=10,pady=10)

        self.next_button = tk.Button(self.menu_frame,text="►",command=self.next_evt,borderwidth=2,font=self.font,bg=self.bg_color,fg=self.color_font)
        self.next_button.pack(side=tk.LEFT,padx=10,pady=10)

        self.save_button = tk.Button(self.menu_frame,text="Salvar",command=self.save_evt,borderwidth=2,font=self.font,bg=self.bg_color,fg=self.color_font)
        self.save_button.pack(side=tk.LEFT,padx=10,pady=10)

        self.load_points_frame = tk.Frame(self.menu_frame,bg=self.bg_menu)
        self.load_points_frame.pack(side=tk.RIGHT,padx=20,pady=10,fill='both')

        self.load_images_frame = tk.Frame(self.menu_frame,bg=self.bg_menu)
        self.load_images_frame.pack(side=tk.RIGHT,padx=20,pady=10,fill='both')
        
        self.image_directory = tk.Label(self.load_images_frame,text=self.default_pathImages,font=self.font2,borderwidth=0)
        self.image_directory.pack(expand=True,fill="both")

        self.load_images_button = tk.Button(self.load_images_frame,text="Load Images",command= lambda: self.select_directory(images=True),font=self.font,borderwidth=2,bg=self.bg_color,fg=self.color_font)
        self.load_images_button.pack(side=tk.RIGHT,expand=True)

        self.point_directory = tk.Label(self.load_points_frame,text=self.default_pathJsons,font=self.font2,borderwidth=0)
        self.point_directory.pack(expand=True,fill="both")

        self.load_points_button = tk.Button(self.load_points_frame,text="Load Points",command= lambda: self.select_directory(points=True),font=self.font,borderwidth=2,bg=self.bg_color,fg=self.color_font)
        self.load_points_button.pack(side=tk.RIGHT,expand=True)

        self.canvas = tk.Canvas(self.main_frame, width=self.set_width_frame(100), height=self.set_height_frame(100))
        self.canvas.pack(expand=False)

        self.footer_frame = tk.Frame(self.main_frame,width=self.set_width_frame(100),height=self.set_height_frame(100),bg=self.bg_menu)
        self.footer_frame.pack(expand=True,fill="y")
    

    def gerar_tela(self):
        #plotar imagem e blips
        try:
            self.img = Imagem(self.canvas, self.pathImagens, (1280//2, 720//2)).plot()
        except FileNotFoundError:
            self.count=0
            self.canvas.delete("all")
            self.gerar_tela()
        
        self.teclas = Imagem(self.canvas, self.pathteclas, (200, 200),ajustar=False).plot()
        #self.mao = Imagem(self.canvas, self.pathMao, (200, 720//2)).plot()

        #obter pontos
        all_pontos = self.getPontosFromJSON(self.pathJsons)

        pontos = {}
        for tipo in ["pose_keypoints_2d", "hand_left_keypoints_2d", "hand_right_keypoints_2d"]:
            pontos[tipo] = []
            if(tipo =="pose_keypoints_2d" ):
                for i in range(0, len(all_pontos[tipo]), 3):
                    p = all_pontos[tipo][i:i+2]

                    pontos[tipo].append(
                        self.img.point_convert(
                            util.convert_ponto(p, (1920, 1080))
                        )
                    )
            else:
                for i in range(0, len(all_pontos[tipo]), 3):
                    p = all_pontos[tipo][i:i+2]

                    pontos[tipo].append(
                        self.img.point_convert(
                            util.convert_ponto(p, (1920, 1080))
                        )
                    )

        self.listaBlips = {}

        #plotar todos os pontos
        for tipo in ["pose_keypoints_2d", "hand_left_keypoints_2d", "hand_right_keypoints_2d"]:
            self.listaBlips[tipo] = []
            i = 0
            for ponto in pontos[tipo]:
                if type(self.cores[tipo]) == list:
                    cor = self.cores[tipo][i]
                    i = (i+1)%len(self.cores[tipo])
                else:
                    cor = self.cores[tipo]
                self.listaBlips[tipo].append(
                    Blip(self.canvas, (ponto[0]-6, ponto[1]), self.tam_blip, cor)
                )
                
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.selBlip)
        self.canvas.bind("<B1-Motion>", self.posMouse)
        self.canvas.bind("<Key>", self.key_pressed)

        # self.canvas.bind("<MouseWheel>", self.scroll)

        self.ponteiroBlip = None
        self.movendo = True

    def showPart(self, grupo):
        for tipo in ["pose_keypoints_2d", "hand_left_keypoints_2d", "hand_right_keypoints_2d"]:
            for blip in self.listaBlips[tipo]:
                blip.setVisible(tipo in grupo)

    def setPontosFronmJSON(self,path):
        with open(path, 'r') as f:
            data = json.loads(f.read())
            return data["people"][0]

    def getPontosFromJSON(self, path):
        with open(path, 'r') as f:
            self.data = json.loads(f.read())
            return self.data["people"][0]

    def key_pressed(self, event):
        global cont, pathRec

        if event.char == 'p': #mostrar pose
            self.showPart("pose_keypoints_2d")
        elif event.char == 'q': #mostrar mao left
            self.showPart("hand_left_keypoints_2d")
            self.mao = Imagem(self.canvas, self.pathMaoesquerda, (1100, 570),ajustar=False).plot()
            #self.teclas = Imagem(self.canvas, self.pathteclas, (100, 200)).plot()
        elif event.char == 'e': #mostrar mao right
            self.showPart("hand_right_keypoints_2d")
            self.mao = Imagem(self.canvas, self.pathMaodreita, (200, 570),ajustar=False).plot()
            #self.teclas = Imagem(self.canvas, self.pathteclas, (100, 200)).plot()
        elif event.char == 'w': #mostrar all
            self.showPart(["pose_keypoints_2d", "hand_left_keypoints_2d", "hand_right_keypoints_2d"])
        elif event.char == 'd': #Move to Next
            self.next_evt()
        elif event.char == 'a': #Move to previous
            self.prev_evt()
        elif event.char == 's': #mostrar all
            self.save_evt()

            print("salvando")

    def selBlip(self, event):
        self.ponteiroBlip = None
        #self.img.zoom((event.x, event.y), True)

    def scroll(self, event):
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

    def posMouse(self, event):
        if self.ponteiroBlip is None:
            for tipo in self.listaBlips:
                for blip in self.listaBlips[tipo]:
                    if blip.onMouse(event.x, event.y) and (blip.visivel) :
                        self.ponteiroBlip = blip
                        break

        if self.ponteiroBlip is None:
            return

        self.ponteiroBlip.move(event.x, event.y)