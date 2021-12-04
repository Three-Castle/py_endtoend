import tkinter as tk          
from tkinter import ttk      
from tkinter import font as tkfont
from tkinter.constants import HORIZONTAL, VERTICAL  
from PIL import Image, ImageTk
import tkinter.messagebox
import time
import requests, hgtk, random


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
    self.remaintime = 5
    self.count = 0
    self.playing = True
    self.history = []
    self.userhistory = []
    self.computerhistory = []
    self.listint = 0
    self.blacklist = ['즘', '틱', '늄', '슘', '퓸', '늬', '뺌', '섯', '숍', '튼', '름', '늠', '쁨']
    self.dict = {}
    self.answord = ''
    self.sword = ''

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
    frame.tkraise()
    

  def restart(self, listbox, nextquery):
    # 게임을 다시시작한다.
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


  #지정한 두 개의 문자열 사이의 문자열을 리턴하는 함수
  #string list에서 단어, 품사와 같은 요소들을 추출할때 사용됩니다
  def midReturn(self, val, s, e):
    if s in val:
      val = val[val.find(s)+len(s):]
      if e in val: val = val[:val.find(e)]
    return val

  #지정한 두 개의 문자열 사이의 문자열 여러개를 리턴하는 함수
  #string에서 XML 등의 요소를 분석할때 사용됩니다
  def midReturn_all(self, val, s, e):
    if s in val:
      tmp = val.split(s)
      val = []
      for i in range(0, len(tmp)):
        if e in tmp[i]: val.append(tmp[i][:tmp[i].find(e)])
    else:
      val = []
    return val

  def findword(self, query):
    url = 'https://krdict.korean.go.kr/api/search?key=' + self.apikey + '&part=word&pos=1&q=' + query
    response = requests.get(url)
    ans = []
    
    #단어 목록을 불러오기
    words = self.midReturn_all(response.text,'<item>','</item>')
    for w in words:
      # 기능1 - history 단어 확인
      #이미 쓴 단어가 아닐때
      if not (w in self.history):           
        #한글자가 아니고 품사가 명사일때
        word = self.midReturn(w,'<word>','</word>')
        pos = self.midReturn(w,'<pos>','</pos>')
        
        # 기능5 - blacklist
        if len(word) > 1 and pos == '명사' and not word in self.history and not word[len(word)-1] in self.blacklist:
          ans.append(w)
    if len(ans)>0:
      return random.choice(ans)
    else:
      return ''


  def checkexists(self, query):
    url = 'https://krdict.korean.go.kr/api/search?key=' + self.apikey + '&part=word&sort=popular&num=100&pos=1&q=' + query
    response = requests.get(url)
    ans = ''

    #단어 목록을 불러오기
    words = self.midReturn_all(response.text,'<item>','</item>')
    for w in words:
      #이미 쓴 단어가 아닐때
      if not (w in self.history):           
        #한글자가 아니고 품사가 명사일때
        word = self.midReturn(w,'<word>','</word>')
        pos = self.midReturn(w,'<pos>','</pos>')
        if len(word) > 1 and pos == '명사' and word == query: ans = w

    if len(ans)>0:
      return ans
    else:
      return ''


  def get_text(self, nextquery, entry, outputText, listbox):
    query = entry.get().strip()
    outputText.set("")
  
    if self.playing == True:
      wordOK = True
      if query == "":
        wordOK = False
        listbox.insert(self.listint, "단어를 입력해주세요")
        listbox.itemconfig(self.listint, bg="black", fg="white")
        self.listint += 1
        
      else:
        if not len(self.history)==0 and not query[0] == self.sword and not query=='':
          print("두음법칙 적용")
          print("sword: ", self.sword, ", ", "query: ", query)
          sdis = hgtk.letter.decompose(self.sword)
          qdis = hgtk.letter.decompose(query[0])
          if sdis[0] == 'ㄹ' and qdis[0] == 'ㄴ':
            listbox.insert(self.listint, '두음법칙 적용됨')
            listbox.itemconfig(self.listint, bg="black", fg="white")
            self.listint += 1
          elif (sdis[0] == 'ㄹ' or sdis[0] == 'ㄴ') and qdis[0] == 'ㅇ' and qdis[1] in self.vowels: 
            listbox.insert(self.listint, '두음법칙 적용됨')
            listbox.itemconfig(self.listint, bg="black", fg="white")
            self.listint += 1
          else:
            wordOK = False
            listbox.insert(self.listint, self.sword + '(으)로 시작하는 단어여야 합니다.')
            listbox.itemconfig(self.listint, bg="black", fg="white")
            self.listint += 1
          
        # 잘못된 글자 입력
        if len(query) == 1:
          print("한글자")
          wordOK = False
          listbox.insert(self.listint, '적어도 두 글자가 되어야 합니다.')
          listbox.itemconfig(self.listint, bg="black", fg="white")
          self.listint += 1

        # history 안에 있는 단어인지 확인
        if query in self.history:
          print("중복글자")
          wordOK = False
          listbox.insert(self.listint, '이미 입력한 단어입니다.')
          listbox.itemconfig(self.listint, bg="red", fg="white")
          self.listint += 1

        if query[len(query)-1] in self.blacklist:
          print("블랙리스트")
          listbox.insert(self.listint, '아... 좀 선넘네요...')
          self.listint += 1

        if wordOK:
          print("옳은 단어")
          # 단어의 유효성을 체크
          ans = self.checkexists(query)
          if ans == '':
            wordOK = False
            listbox.insert(self.listint, '유효한 단어를 입력해 주십시오')
            listbox.itemconfig(self.listint, bg="black", fg="white")
            self.listint += 1
          else:
            listbox.insert(self.listint, query)
            self.listint += 1
            mean = self.midReturn(ans, '<definition>', '</definition>')
            listbox.insert(self.listint, '(' + mean + ')\n')
            self.dict[query] = mean
            self.userhistory.append(query)
            self.listint += 1

      if wordOK:
        # 기능1 - 사용자 입력 시 history 단어 추가                
        self.history.append(query)         
              
        start = query[len(query)-1]
        ans = self.findword(start + '*')
        if ans=='':
          #ㄹ -> ㄴ 검색
          sdis = hgtk.letter.decompose(start)
          if sdis[0] == 'ㄹ':
            listbox.insert(self.listint, '두음법칙 적용')
            listbox.itemconfig(self.listint, bg="black", fg="white")
            self.listint += 1
            newq = hgtk.letter.compose('ㄴ', sdis[1], sdis[2])
            print(start, '->', newq)
            start = newq
            ans = self.findword(newq + '*')

        elif ans=='':
          #(ㄹ->)ㄴ -> ㅇ 검색
          sdis = hgtk.letter.decompose(start)
          listbox.insert(self.listint, '두음법칙 적용')
          listbox.itemconfig(self.listint, bg="black", fg="white")
          self.listint += 1
          if sdis[0] == 'ㄴ' and sdis[1] in self.vowels:
            newq = hgtk.letter.compose('ㅇ', sdis[1], sdis[2])
            print(start, '->', newq)
            ans = self.findword(newq + '*')
              
        if ans=='':
          print('당신의 승리!')
          listbox.insert(self.listint, "Player win!!")
          listbox.itemconfig(self.listint, bg="yellow", fg="blue")
          nextquery.configure(text= "Winner")
          self.listint += 1
          self.playing = False 
        else:
          self.answord = self.midReturn(ans, '<word>', '</word>') #단어 불러오기
          ansdef = self.midReturn(ans, '<definition>', '</definition>') # 품사 불러오기
          
          # 기능1 - 컴퓨터 입력 시 history 단어 추가
          self.history.append(self.answord)
          listbox.insert(self.listint, self.answord)
          self.listint += 1
          listbox.insert(self.listint, ansdef)
          self.listint += 1
          self.dict[self.answord] = ansdef
          self.computerhistory.append(self.answord)

          nextquery.configure(text= query + '>'+ self.answord)
          self.sword = self.answord[len(self.answord)-1]

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

  # def countdown(self):
  #   # 타이머
  #   timer = tk.Label(self, text=self.remaintime, background = "white", height=2, width=10)
  #   timer.place(x = 650, y = 500)
  #   for i in range(5):
  #     time.sleep(1)
  #     self.remaintime -= 1
  #     timer.configure(text=self.remaintime)

  #   self.remaintime = 5


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
    self.remaintime = 5
    
    # 리스트박스가 스크롤바로 되어있어 스크롤하여 이전에 입력한 것을 확인할 수 있다
    self.scrollbar = tk.Scrollbar(self, orient=VERTICAL)
    self.scrollbar.pack(side="right", fill="y")

    # 리스트 박스를 이용하여 컴퓨터와 사용자가 입력한 단어를 화면에 보인다
    self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set, width=50, height=30, font=("Helvetica", 12))

    self.listbox.pack()
    self.scrollbar.config(command=self.listbox.yview)

    # 타이머
    # Clock()

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
    endbtn = tk.Button(self, text="게임종료", background = "white", height=2, width=10, command=lambda: [controller.restart(self.listbox, inputText), controller.show_frame("EndPage")])
    endbtn.place(x=600, y=625)

    # 게임 방법을 보여주는 버튼
    rulebtn = tk.Button(self, text="게임방법", background = "white", height=2, width=10, command=lambda: controller.show_rule())
    rulebtn.place(x=650, y=300)

class Clock():
  def __init__(self):
    self.label = tk.Label(text="", font=('Helvetica', 48), fg='red')
    self.label.pack()
    self.update_clock()
    
  def update_clock(self):
    now = time.strftime("%H:%M:%S")
    self.label.configure(text=now)
    self.after(1000, self.update_clock)

# game 종료 페이지
class EndPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    # 게임 종료 표시
    endlabel = tk.Label(self, text="Game Over", font=controller.big_font)
    endlabel.place(x=290, y=300)

    # 히스토리 확인버튼
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

    for i in range (len(controller.userhistory)):
      print(controller.userhistory(i))
      self.playerlist.insert(i, dict.keys(controller.userhistory(i)))

    # 컴퓨터의 history를 보여줌
    computerText = tk.Label(self, background="white", width=15, height=2, text="컴퓨터 history")
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