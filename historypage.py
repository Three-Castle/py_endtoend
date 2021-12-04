import tkinter as tk

class HistoryPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    
    # 리스트박스가 스크롤바로 되어있어 스크롤하여 이전에 입력한 것을 확인할 수 있다
    self.scrollbar = tk.Scrollbar(self)
    self.scrollbar.pack(side="right", fill="y")

    # 사용자의 history를 보여줌
    playerText = tk.Label(self, background="white", width=15, height=2, text="사용자 history")
    playerText.place(x=135, y=20)

    self.playerlist = tk.Listbox(self, yscrollcommand=self.scrollbar.set, width=25, height=17, font=("Helvetica", 20))
    self.playerlist.pack(side="left")
    self.scrollbar.config(command=self.playerlist.yview)
    controller.setplayerlist(self.playerlist)

    for i in range (len(controller.userhistory)):
      print(controller.userhistory(i))
      self.playerlist.insert(i, dict.keys(controller.userhistory(i)))

    # 컴퓨터의 history를 보여줌
    computerText = tk.Label(self, background="white", width=15, height=2, text="컴퓨터 history")
    computerText.place(x=540, y=20)

    self.computerlist = tk.Listbox(self, yscrollcommand=self.scrollbar.set, width=25, height=17, font=("Helvetica", 20))
    self.computerlist.pack(side="right")
    self.scrollbar.config(command=self.computerlist.yview)
    controller.setcomputerlist(self.computerlist)

    # 시작으로 돌아가는 버튼
    goTostartbutton = tk.Button(self, text="Go to the start page", width=20, height=2, command=lambda: controller.show_frame("StartPage"))
    goTostartbutton.place(x=230, y=650)

    # 창을 닫고 게임을 종료하는 버튼
    endbutton = tk.Button(self, text="End game", width=20, height=2, command=lambda: controller.endGame())
    endbutton.place(x=400, y=650)

    userhistotycheck = tk.Button(self, text="확인", width=10, height=2, command=lambda: controller.usercheck())
    userhistotycheck.place(x = 0 , y = 650)

    comhistorycheck = tk.Button(self, text="확인", width=10, height=2, command=lambda: controller.comcheck())
    comhistorycheck.place(x = 700 , y = 650)
