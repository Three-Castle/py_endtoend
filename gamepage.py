import tkinter as tk          
from tkinter.constants import VERTICAL

# 게임 실행 페이지
class GamePage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    
    # 리스트박스가 스크롤바로 되어있어 스크롤하여 이전에 입력한 것을 확인할 수 있다
    self.scrollbar = tk.Scrollbar(self, orient=VERTICAL)
    self.scrollbar.pack(side="right", fill="y")

    # 리스트 박스를 이용하여 컴퓨터와 사용자가 입력한 단어를 화면에 보인다
    self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set, width=50, height=30, font=("Helvetica", 12))

    self.listbox.pack()
    self.scrollbar.config(command=self.listbox.yview)

    # 입력할 단어의 첫 글자를 나타내는 창
    inputText = tk.Label(self, background="white", width=15, height=2, text="입력")
    inputText.place(x=170, y=609)

    # 단어를 입력하는 
    outputText = tk.StringVar()
    outputText.set("")
    outputEnt = tk.Entry(self, width=30, textvariable=outputText)
    outputEnt.place(x= 290, y = 609, height=35)

    # 입력한 단어를 보내는 버튼
    gamebtn = tk.Button(self, text="입력", background = "white", height=2, width=10, command=lambda: controller.get_text(inputText, outputEnt, outputText, self.listbox))
    gamebtn.place(x=510, y=606)
    
    # 게임을 다시 시작하는 버튼
    replaybtn = tk.Button(self, text="다시시작", background = "white", height=2, width=10, command=lambda: controller.restart(self.listbox, inputText))
    replaybtn.place(x=600, y=578)

    # 졌습니다 버튼
    replaybtn = tk.Button(self, text="졌습니다", background = "white", height=2, width=10, command=lambda: controller.lose(self.listbox))
    replaybtn.place(x=685, y=578)

    # 게임을 종료하는 버튼
    #endbtn = tk.Button(self, text="게임종료", background = "white", height=2, width=10, command=lambda: [controller.restart(self.listbox, inputText), controller.show_frame("EndPage")])
    endbtn = tk.Button(self, text="게임종료", background = "white", height=2, width=10, command=lambda:  controller.show_frame("EndPage"))
    endbtn.place(x=600, y=625)

    # 게임 방법을 보여주는 버튼
    rulebtn = tk.Button(self, text="게임방법", background = "white", height=2, width=10, command=lambda: controller.show_rule())
    rulebtn.place(x=650, y=300)


  