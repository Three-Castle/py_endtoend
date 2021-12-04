import tkinter as tk   

# game 종료 페이지
class EndPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    # 게임 종료 표시
    endlabel = tk.Label(self, text="Game Over", font=controller.big_font)
    endlabel.place(x=290, y=300)

    # 히스토리 확인버튼
    historybutton = tk.Button(self, text="Check History", width=20, height=2, command=lambda: [controller.show_frame("HistoryPage"), controller.getuserhistory()])
    historybutton.place(x=325, y=370)

    # 시작으로 돌아가는 버튼
    goTostartbutton = tk.Button(self, text="Go to the start page", width=20, height=2, command=lambda: controller.show_frame("StartPage"))
    goTostartbutton.place(x=325, y=420)

    # 창을 닫고 게임을 종료하는 버튼
    endbutton = tk.Button(self, text="End game", width=20, height=2, command=lambda: controller.endGame())
    endbutton.place(x=325, y=470)