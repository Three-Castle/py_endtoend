import tkinter as tk          
from tkinter import ttk      
from tkinter import font as tkfont  
from PIL import Image, ImageTk
import tkinter.messagebox

class App(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)

    self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
    self.big_font = tkfont.Font(family='Helvetica', size=30, weight="bold", slant="italic")
    self.title("EndToEnd") # 제목
    self.geometry("800x700") # 화면 크기
    self.configure(bg = 'black') # 배경색 변경
    self.resizable(False, False) # 크기조절 불가

    container = tk.Frame(self)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)


    self.frames = {}
    for F in (StartPage, GamePage, EndPage, HistoryPage):
      page_name = F.__name__
      frame = F(parent=container, controller=self)
      self.frames[page_name] = frame

      frame.grid(row=0, column=0, sticky="nsew")

    # 시작화면을 띄운다
    self.show_frame("StartPage")

  def show_frame(self, page_name):
    # 화면을 전환한다
    frame = self.frames[page_name]
    frame.tkraise()

  def restart(self):
    # 게임을 다시시작한다.
    print("다시 시작")

  def get_text(self, entry):
    # 입력받은 텍스트를 불러와서 유효성 여부를 테스트한다.
    txt = entry.get().strip()
    print(txt)
    
  def endGame(self):
    # 게임종료
    self.destroy()

  def show_rule(self):
    # 게임 방법을 보여준다
    GAME_RULE = '''
      ========파이썬 끝말잇기==========
      사전 데이터 제공: 국립국어원 한국어기초사전

      - - - - - - - - - 게임 방법 - - - - - - - - - 
      단어를 입력한 후 '입력' 버튼을 누르면 
      끝말잇기가 시작됩니다.
      다시시작 버튼을 클릭할 경우 '컴퓨터의 승리'로 게임이 
      종료되며 게임이 다시 시작됩니다.
      게임종료 버튼을 클릭할 경우 '컴퓨터의 승리'로 
      게임이 종료됩니다.
      
      - - - - - - - - - 게임 규칙 - - - - - - - - -
      1. 사전에 등재된 명사여야 합니다
      2. 적어도 단어의 길이가 두 글자 이상이어야 합니다
      3. 이미 사용한 단어를 다시 사용할 수 없습니다
      4. 두음법칙 적용 가능합니다 (ex. 리->니->이)
      ================================
      '''
    tkinter.messagebox.showinfo("게임 방법", GAME_RULE)


class StartPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    # 배경 이미지 설정
    #img = ImageTk.PhotoImage(Image.open('main.png'))
    img = tk.PhotoImage(file = "main.png")
    startPage_label = tk.Label(self, image = img)
    startPage_label.image = img
    startPage_label.place(x = 20, y = 42)

    # 게임 시작 버튼 생성
    startbtn = tk.Button(self, text = "게임시작", background = "white", command=lambda: controller.show_frame("GamePage"))
    startbtn.config(width = 15, height = 2)
    startbtn.config(font = (16))
    startbtn.place(x = 570, y = 300)


# 게임 실행 페이지
class GamePage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    
    # 리스트박스가 스크롤바로 되어있어 스크롤하여 이전에 입력한 것을 확인할 수 있다
    self.scrollbar = tk.Scrollbar(self)
    self.scrollbar.pack(side="right", fill="y")

    # 리스트 박스를 이용하여 컴퓨터와 사용자가 입력한 단어를 화면에 보인다
    self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set, width=30, height=17, font=("Helvetica", 20))

    self.listbox.pack()
    self.scrollbar.config(command=self.listbox.yview)

    # 입력할 단어의 첫 글자를 나타내는 창
    inputText = tk.Label(self, background="white", width=15, height=2, text="입력")
    inputText.place(x=180, y=609)

    # 단어를 입력하는 창
    outputEnt = tk.Entry(self, width=30)
    outputEnt.place(x= 290, y = 609, height=35)

    # 입력한 단어를 보내는 버튼
    gamebtn = tk.Button(self, text="입력", background = "white", height=2, width=10, command=lambda: controller.get_text(outputEnt))
    gamebtn.place(x=510, y=606)
    
    # 게임을 다시 시작하는 버튼
    replaybtn = tk.Button(self, text="다시시작", background = "white", height=2, width=10, command=lambda: controller.restart())
    replaybtn.place(x=600, y=578)

    # 게임을 종료하는 버튼
    endbtn = tk.Button(self, text="게임종료", background = "white", height=2, width=10, command=lambda: controller.show_frame("EndPage") )
    endbtn.place(x=600, y=625)

    # 게임 방법을 보여주는 버튼
    rulebtn = tk.Button(self, text="게임방법", background = "white", height=2, width=10, command=lambda: controller.show_rule())
    rulebtn.place(x=650, y=300)

    
# game 종료 페이지
class EndPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    # 게임 종료 표시
    endlabel = tk.Label(self, text="Game Over", font=controller.big_font)
    endlabel.place(x=290, y=300)

    # 시작으로 돌아가는 버튼
    historybutton = tk.Button(self, text="Check History", width=20, height=2, command=lambda: controller.show_frame("HistoryPage"))
    historybutton.place(x=325, y=370)

    # 시작으로 돌아가는 버튼
    goTostartbutton = tk.Button(self, text="Go to the start page", width=20, height=2, command=lambda: controller.show_frame("StartPage"))
    goTostartbutton.place(x=325, y=420)

    # 창을 닫고 게임을 종료하는 버튼
    endbutton = tk.Button(self, text="End game", width=20, height=2, command=lambda: controller.endGame())
    endbutton.place(x=325, y=470)


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

    # 컴퓨터의 history를 보여줌
    computerText = tk.Label(self, background="white", width=15, height=2, text="사용자 history")
    computerText.place(x=540, y=20)

    self.computerlist = tk.Listbox(self, yscrollcommand=self.scrollbar.set, width=25, height=17, font=("Helvetica", 20))
    self.computerlist.pack(side="right")
    self.scrollbar.config(command=self.computerlist.yview)

    # 시작으로 돌아가는 버튼
    goTostartbutton = tk.Button(self, text="Go to the start page", width=20, height=2, command=lambda: controller.show_frame("StartPage"))
    goTostartbutton.place(x=230, y=650)

    # 창을 닫고 게임을 종료하는 버튼
    endbutton = tk.Button(self, text="End game", width=20, height=2, command=lambda: controller.endGame())
    endbutton.place(x=400, y=650)


# 창 실행
if __name__ == "__main__":
  app = App()
  app.mainloop()