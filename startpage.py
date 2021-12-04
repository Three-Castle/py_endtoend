import tkinter as tk
from PIL import Image, ImageTk

class StartPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    # 배경 이미지 설정
    #img = ImageTk.PhotoImage(Image.open('main.png'))
    # img = tk.PhotoImage(file = "py_endtoend/main.png")
    img = tk.PhotoImage(file = "main.png")
    startPage_label = tk.Label(self, image = img)
    startPage_label.image = img
    startPage_label.place(x = 20, y = 42)

    # 게임 시작 버튼 생성
    startbtn = tk.Button(self, text = "게임시작", background = "white", command=lambda: controller.show_frame("GamePage"))
    startbtn.config(width = 15, height = 2)
    startbtn.config(font = (16))
    startbtn.place(x = 570, y = 300)