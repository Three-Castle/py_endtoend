import tkinter as tk

class StartPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    # 배경 이미지 설정
    #img = ImageTk.PhotoImage(Image.open('main.png'))
    img = tk.PhotoImage(file = "py_endtoend/main.png")
    # img = tk.PhotoImage(file = "main.png")
    startPage_label = tk.Label(self, image = img)
    startPage_label.image = img
    startPage_label.place(x = 20, y = 42)

    # 게임 시작 버튼 생성
    startbtn = tk.Button(self, text = "자유 글자수", background = "white", command=lambda: [controller.setWord(1), controller.show_frame("GamePage")])
    startbtn.config(width = 15, height = 2)
    startbtn.config(font = (16))
    startbtn.place(x = 570, y = 200)

    # 2낱말 버튼
    twowordbtn = tk.Button(self, text = "2낱말ver.", background = "white", command=lambda: [controller.setWord(2), controller.show_frame("GamePage")])
    twowordbtn.config(width = 15, height = 2)
    twowordbtn.config(font = (10))
    twowordbtn.place(x = 570, y = 300)

    # 3낱말 버튼
    threewordbtn = tk.Button(self, text = "3낱말ver.", background = "white", command=lambda: [controller.setWord(3), controller.show_frame("GamePage")])
    threewordbtn.config(width = 15, height = 2)
    threewordbtn.config(font = (10))
    threewordbtn.place(x = 570, y = 400)

    # 4낱말 버튼
    fourwordbtn = tk.Button(self, text = "4낱말ver.", background = "white", command=lambda: [controller.setWord(4), controller.show_frame("GamePage")])
    fourwordbtn.config(width = 15, height = 2)
    fourwordbtn.config(font = (10))
    fourwordbtn.place(x = 570, y = 500)