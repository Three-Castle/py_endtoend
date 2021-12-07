import tkinter as tk          
from tkinter import font as tkfont
import tkinter.messagebox
from gamepage import GamePage
from historypage import HistoryPage
from endpage import EndPage
from startpage import StartPage
from game_turn import playerturn, computerturn

class App(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)

    # 모음-중성
    self.vowels = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ',
           'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

    self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
    self.big_font = tkfont.Font(family='Helvetica', size=30, weight="bold", slant="italic")
    self.title("EndToEnd") # 제목
    self.geometry("800x700") # 화면 크기
    self.configure(bg = 'black') # 배경색 변경
    self.resizable(False, False) # 크기조절 불가
    self.playing = True
    self.history = []
    self.userhistory = []
    self.computerhistory = []
    self.listint = 0
    self.blacklist = ['즘', '틱', '늄', '슘', '퓸', '늬', '뺌', '섯', '숍', '튼', '름', '늠', '쁨']
    self.dict = {}

    self.answord = ''
    self.sword = ''
    self.playerlist=[]
    self.computerlist=[]
    self.WORD = 1
    self.wordOk = True

    #키 발급은 https://krdict.korean.go.kr/openApi/openApiInfo
    self.apikey = 'EC3A8C4A28DC6BE15AF8518696C06CF4'

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
    if page_name == "GamePage":
        frame.restart()
    frame.tkraise()
    
  def setplayerlist(self, set):
    self.playerlist = set

  # 컴퓨터의 history를 가리키게 하기
  def setcomputerlist(self, set):
    self.computerlist = set
  
  # history 내역 받기
  def getuserhistory(self):
    for i in range (len(self.userhistory)):
      print(self.userhistory[i])
      self.playerlist.insert(i, self.userhistory[i])
    for i in range (len(self.computerhistory)):
      print(self.computerhistory[i])
      self.computerlist.insert(i, self.computerhistory[i])
    print(self.dict)

  # 사용자의 history 단어에 대한 뜻을 불러온다.
  def usercheck(self):
    selection = self.playerlist.curselection()
    key = self.playerlist.get(selection[0])
    tkinter.messagebox.showinfo(f"{key}뜻", self.dict[key])

  # 컴퓨터의 history 단어에 대한 뜻을 불러온다.
  def comcheck(self):
    selection = self.computerlist.curselection()
    key = self.computerlist.get(selection[0])
    tkinter.messagebox.showinfo(f"{key}뜻", self.dict[key])
    
  def restart(self, listbox, nextquery):
    # 게임을 다시시작한다.
    print("다시 시작")

    for i in range(listbox.size()):
      listbox.delete(0)
    
    self.playing = True
    self.history = []
    self.userhistory = []
    self.computerhistory = []
    self.listint = 0
    self.dict = {}
    self.answord = ''
    self.sword = ''
    nextquery.configure(text= "입력하세요")

  def get_text(self, nextquery, entry, outputText, Listbox):
    query = entry.get().strip()
    outputText.set("")

    listbox = Listbox
    if self.playing == True:
      query = playerturn(self.WORD, query, listbox, controller=self)
      
      #컴퓨터 턴
      if self.wordOk:
        computerturn(self.WORD, query, listbox, nextquery, controller=self)

  def lose(self, listbox):
    self.playing = False
    listbox.insert(self.listint, 'Player Lose')
    listbox.itemconfig(self.listint, bg="red", fg="white")
    self.listint += 1
    
  def endGame(self):
    # 게임종료
    self.destroy()

  def show_rule(self):
    # 게임 방법을 보여준다
    GAME_RULE = '''
      ========파이썬 끝말잇기==========
      사전 데이터 제공: 국립국어원 한국어기초사전

      - - - - - - - - - 게임 방법 - - - - - - - - - 
      게임시작 버튼을 클릭하여 게임을 시작합니다.
      단어를 입력한 후 입력 버튼을 누르면 해당단어가 유효한지
      검사 후 유효한 단어이면 화면에 뜻과 함께 나타납니다.
      입력창 왼쪽에 컴퓨터가 입력한 단어가 나온것을 확인한 후
      컴퓨터가 입력한 단어의 마지막 글자로 시작하는 단어를
      입력하면 됩니다.

      게임 방법을 다시 읽기 원할 경우 
      오른쪽 게임방법 버튼을 클릭해주세요.
      '다시시작' 버튼을 누르면 그동안의 모든 단어가 
      reset되며 게임이 다시시작 됩니다.
      '졌습니다' 버튼을 누르면
      컴퓨터의 승리로 게임이 종료됩니다.
      '게임종료' 버튼을 누르면 게임이 종료되고,
      다음 페이지로 화면이 넘어갑니다.
      게임 종료 시 나오는 페이지에서는
      히스토리 확인, 첫 페이지로 이동, 게임종료가 가능합니다.
      
      그럼 즐거운 게임 되세요!!

      - - - - - - - - - 게임 규칙 - - - - - - - - -
      1. 사전에 등재된 명사여야 합니다
      2. 적어도 단어의 길이가 두 글자 이상이어야 합니다
      3. 이미 사용한 단어를 다시 사용할 수 없습니다
      4. 두음법칙 적용 가능합니다 (ex. 리->니->이)
      5. 뜻이 다 보이지 않는경우 shift+스크롤을 통해
      확인할 수 있습니다.
      ================================
      '''
    tkinter.messagebox.showinfo("게임 방법", GAME_RULE)

  def setWord(self, count):
    self.WORD = count