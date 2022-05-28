

from tkinter import *
from PIL import Image, ImageTk
import tkinter.messagebox


class Chess:
    @staticmethod
    def center(window, w, h): #establecemos el tamaño  el centro de la ventana
        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        window.geometry("{:.0f}x{:.0f}+{:.0f}+{:.0f}".format(w, h, x, y))

    def is_win(self):
        for i, j in self.seq_list:
            color = self.matrix_flag[i][j]
            if j <= 10:
                for col in range(j + 1, j + 5): #juicio horizontal
                    if self.matrix_flag[i][col] != color:
                        break
                else:
                    tkinter.messagebox.showinfo("rápido", "¡Ajedrez negro, ganaste!" if color == 1 else "¡Ajedrez blanco, ganaste!" )
                    return
            if i <= 10:
                for row in range(i + 1, i + 5): #sentencia vertical
                    if self.matrix_flag[row][j] != color:
                        break
                else:
                    tkinter.messagebox.showinfo("rápido", "¡Ajedrez negro, ganaste!" if color == 1 else "¡Ajedrez blanco, ganaste!" )
                    return
            if i <= 10 and j <= 10:
                for row, col in zip([x for x in range(i + 1, i + 5)], [y for y in range(j + 1, j + 5)]): #jUICIO DIAGONAL
                    if self.matrix_flag[row][col] != color:
                        break
                else:
                    tkinter.messagebox.showinfo("Rápido", "¡Ajedrez negro, ganaste!" if color == 1 else "¡Ajedrez blanco, ganaste!")
                    return

    def undo(self, event):  #Lamentar
        if self.seq_list:
            i, j = self.seq_list.pop()
            self.canvas.delete(self.matrix_img[i][j])
            self.matrix_img[i][j] = None
            self.matrix_flag[i][j] = 0
        else:
            tkinter.messagebox.showwarning("consideración", "¡No hay mas peones!")

    def callback(self, event):  #Lousy
        x, y = event.x - 20, event.y - 20
        res_x, res_y = x // 40,  y // 40
        div_x, div_y = x % 40, y % 40
        flag_x = flag_y = False #La distribución juzga si las coordenadas de xey están alrededor de la intersección
        i = j = 0
        if div_x <= 10:
            flag_x = True
            x = res_x * 40
            j = res_x
        elif 30 <= div_x:
            flag_x = True
            x = (res_x + 1) * 40
            j = res_x + 1
        if div_y <= 10:
            flag_y = True
            y = res_y * 40
            i = res_y
        elif 30 <= div_y:
            flag_y = True
            y = (res_y + 1) * 40
            i = res_y + 1

        if flag_x and flag_y and not self.matrix_flag[i][j]:
            self.matrix_img[i][j] = self.canvas.create_image(x + 20, y + 20, image=self.img_black)
            self.img_black, self.img_white = self.img_white, self.img, self.img_black #intercambio en blanco y negro
            self.matrix_flag[i][j] = self.count % 2 + 1 #Hei Zi es 1 Blanco Zi es 2
            self.count += 1
            self.seq_list.append((i, j))
            self.is_win() #Determina si quieres llegar a cinco

    def __init__(self):
        self.row, self.column = 15, 15
        self.matrix_flag = [[0 for _ in range(self.row)] for _ in range(self.column)]
        self.matrix_img = [[None for _ in range(self.row)] for _ in range(self.column)]
        self.count = 0
        self.seq_list = []
        self.root = Tk()
        self.root.resizable(width=False, height=False) #Configurar la ventana para que no se acerque
        self.root.title("A jugar!!")
        self.center(self.root, 600, 600)
        self.canvas = Canvas(self.root, bg="pink", bd=0)
        self.canvas.pack(fill='both', expand='Yes')
        self.img_black = ImageTk.PhotoImage(Image.open("heart.jpg")) #cargar ajedrez negro
        self.img_white = ImageTk.PhotoImage(Image.open("rose.png")) #cargar ajedrez blanco
        self.draw_grid()

        self.canvas.bind("<Button-1>", self.callback) #Lousy
        self.canvas.bind("<Button-3>", self.undo) #Lamentar

        self.root.mainloop()

    def draw_grid(self): #Dibujar cuadrícula
        start = [(20, i) for i in range(20, 580, 40)] + [(i, 20) for i in range(20, 580, 40)] + [(20, 580), (580, 20)]
        end = [(580, i) for i in range(20, 580, 40)] + [(i, 580) for i in range(20, 580, 40)] + [(580, 580), (580, 580 )]
        for i in range(len(start)):
            self.canvas.create_line((start[i], end[i]), width=2)

if __name__ == '__main__':
    Chess()
