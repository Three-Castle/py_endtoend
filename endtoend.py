import pygame

# pip install jamo
from jamo import h2j, j2hcj, j2h

# pip install hangul-utils
from hangul_utils import join_jamos
from pygame import draw

# 모듈 초기화
pygame.init()

# 색
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
YELLOW2 = (255, 192, 0)

# 규칙
RULE = ["========파이썬 끝말잇기==========", "사전 데이터 제공: 국립국어원 한국어기초사전", "사전 데이터 제공: 국립국어원 한국어기초사전", 
"- - - - - - - - - 게임 방법 - - - - - - - - - ", "단어를 입력한 후 '입력' 버튼을 누르면 끝말잇기가 시작됩니다.", "다시시작 버튼을 클릭할 경우 '컴퓨터의 승리'로 게임이 종료되며", 
"게임이 다시 시작됩니다.", "게임종료 버튼을 클릭할 경우 '컴퓨터의 승리'로 게임이 종료됩니다.", "- - - - - - - - - 게임 규칙 - - - - - - - - -", "1. 사전에 등재된 명사여야 합니다.", 
"2. 적어도 단어의 길이가 두 글자 이상이어야 합니다.", "3. 이미 사용한 단어를 다시 사용할 수 없습니다.", "4. 두음법칙 적용 가능합니다 (ex. 리->니->이).", "================================"]

# 자음-초성/종성
cons = {'r':'ㄱ', 'R':'ㄲ', 's':'ㄴ', 'e':'ㄷ', 'E':'ㄸ', 'f':'ㄹ', 'a':'ㅁ', 'q':'ㅂ', 'Q':'ㅃ', 't':'ㅅ', 'T':'ㅆ',
           'd':'ㅇ', 'w':'ㅈ', 'W':'ㅉ', 'c':'ㅊ', 'z':'ㅋ', 'x':'ㅌ', 'v':'ㅍ', 'g':'ㅎ'}
# 모음-중성
vowels = {'k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
           'y':'ㅛ', 'n':'ㅜ', 'nj':'ㅝ', 'np':'ㅞ', 'nl':'ㅟ', 'b':'ㅠ',  'm':'ㅡ', 'ml':'ㅢ', 'l':'ㅣ'}
# 자음-종성
cons_double = {'rt':'ㄳ', 'sw':'ㄵ', 'sg':'ㄶ', 'fr':'ㄺ', 'fa':'ㄻ', 'fq':'ㄼ', 'ft':'ㄽ', 'fx':'ㄾ', 'fv':'ㄿ', 'fg':'ㅀ', 'qt':'ㅄ'}

# 스크린 생성
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

def engkor(text):
  result = ''   # 영 > 한 변환 결과
  
  # 1. 해당 글자가 자음인지 모음인지 확인
  vc = '' 
  for t in text:
    if t in cons :
      vc+='c'
    elif t in vowels:
      vc+='v'
    else:
      vc+='!'
	
  # cvv → fVV / cv → fv / cc → dd 
  vc = vc.replace('cvv', 'fVV').replace('cv', 'fv').replace('cc', 'dd')
	
    
  # 2. 자음 / 모음 / 두글자 자음 에서 검색
  i = 0
  while i < len(text):
    v = vc[i]
    t = text[i]

    j = 1
    # 한글일 경우
    try:
      if v == 'f' or v == 'c':   # 초성(f) & 자음(c) = 자음
        result+=cons[t]

      elif v == 'V':   # 더블 모음
        result+=vowels[text[i:i+2]]
        j+=1

      elif v == 'v':   # 모음
        result+=vowels[t]

      elif v == 'd':   # 더블 자음
        result+=cons_double[text[i:i+2]]
        j+=1
      else:
        result+=t
            
    # 한글이 아닐 경우
    except:
      if v in cons:
        result+=cons[t]
      elif v in vowels:
        result+=vowels[t]
      else:
        result+=t
    
    i += j

  return join_jamos(result)      

def LoadImage():
  # 메인 이미지 로드
  main_image = pygame.image.load("main.png")
  main_image = pygame.transform.scale(main_image, (700, 700))
  pygame.display.set_icon(main_image)
  pygame.display.set_caption("endToend")
  screen.blit(main_image, (50, 0))

def LoadButton(image, wsize, hsize, xpos, ypos):
  # 버튼 로드
  button = pygame.image.load(image)
  button = pygame.transform.scale(button, (wsize, hsize))
  pygame.display.set_icon(button)
  screen.blit(button, (xpos, ypos))

def loadText(text, fontsize, fontcolor, posx, posy):
  # 텍스트 출력
  myFont = pygame.font.SysFont("새굴림", fontsize)
  text_Start = myFont.render(text, True, fontcolor)
  text_Rect = text_Start.get_rect()
  text_Rect.centerx = round(posx)
  text_Rect.y = posy
  screen.blit(text_Start, text_Rect)

def loadText_bold(text, fontsize, fontcolor, posx, posy):
  # 텍스트 출력
  myFont = pygame.font.SysFont("malgungothic", fontsize, True)
  text_Start = myFont.render(text, True, fontcolor)
  text_Rect = text_Start.get_rect()
  text_Rect.centerx = round(posx)
  text_Rect.y = posy
  screen.blit(text_Start, text_Rect)

def loadRect(color, posx, posy, width, height, bold):
  # 사각형 출력
  pygame.draw.rect(screen, color, (posx, posy, width, height), bold)

class mainPage:
  # 메인 페이지
  def __init__(self):
    #print("mainpage")
    self.active = True
    self.drawPage()

  def drawPage(self):
    # 페이지 그리기
    screen.fill(BLACK)
    LoadImage()
    loadText("Game Start", 40, YELLOW, screen_width/2, 660)
    loadRect(WHITE, 275, 645, 250, 70, 2)

  def handle_event(self, event):
    if self.active == True and event.type == pygame.MOUSEMOTION:
      # game start 위치에 마우스를 가져다 댔을 때 
      mouse_pos = pygame.mouse.get_pos()
    
      if mouse_pos[0] in list(range(275, 525)) and mouse_pos[1] in list(range(640, 710)):
        loadText("Game Start", 60, YELLOW, screen_width/2, 660)
      else:
        # game start 크기 복구
        self.drawPage()

    if self.active == True and event.type == pygame.MOUSEBUTTONDOWN:
      # game start 클릭
      mouse_pos = pygame.mouse.get_pos()
      if mouse_pos[0] in list(range(275, 525)) and mouse_pos[1] in list(range(640, 710)):
        # 끝말잇기 게임 설명 페이지를 띄운다
        self.active = False
        gamerulePage # 게임 설명 페이지 띄우기

class gamerulePage:
  # 게임 설명 페이지
  def __init__(self):
    #print("gamerulepage")
    self.active = True
    # 페이지 그리기
    self.drawPage()

  def drawPage(self):
    # 페이지 그리기
    screen.fill(BLACK)

    # 게임 설명
    loadText("게임 규칙", 30, WHITE, screen_width/2, 30)
    y = 120
    for i in range(len(RULE)):
      loadText(RULE[i], 20, WHITE, screen_width/2, y)
      y += 30

    # 다음 페이지로 넘어가는 버튼(next)
    loadText("Next", 40, YELLOW, 600, 660)
    loadRect(WHITE, 500, 645, 200, 70, 2)


  def handle_event(self, event):
    if self.active == True and event.type == pygame.MOUSEMOTION:
    # next 위치에 마우스를 가져다 댔을 때 
      mouse_pos = pygame.mouse.get_pos()
    
      if mouse_pos[0] in list(range(500, 700)) and mouse_pos[1] in list(range(640, 710)):
        # next 텍스트 크기가 커진다
        loadText("Next", 60, YELLOW, 600, 660)
      else:
        # next 크기 복구
        self.drawPage()

    if self.active == True and event.type == pygame.MOUSEBUTTONDOWN:
      # game start 클릭
      mouse_pos = pygame.mouse.get_pos()
      if mouse_pos[0] in list(range(500, 700)) and mouse_pos[1] in list(range(640, 710)):
        # 끝말잇기 게임 실행 페이지를 띄운다
        self.active = False
        gameplayPage # 게임 실행 페이지 띄우기

class inputBox:
  def __init__(self, x, y, w, h):
    self.rect = pygame.Rect(x, y, w, h)
    self.text = ""
    self.posy = self.rect.y+10

  def draw(self, screen):
    pygame.draw.rect(screen, WHITE, self.rect, 0)
    loadText(self.text, 25, BLACK, screen_width / 2 + 15, self.posy)

  def handle_event(self, event):
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RETURN:
        self.text = ''
      elif event.key == pygame.K_BACKSPACE:
        self.text = self.text[:-1]
      else:
        # 영어 -> 한글 변환
        input = engkor(event.unicode)
        
        # 단어 분리
        self.text = j2hcj(h2j(self.text))

        self.text += input
        
        # 글자 결합
        self.text = join_jamos(self.text)

      self.draw(screen)
      print(self.text)
        

class gameplayPage:
  def __init__(self):
    #print("gameplaypage")
    # 게임 실행 페이지
    self.text = ""
    self.active = True
    self.input = inputBox(305, 680, 250, 50)
    self.history = []
    self.playerposy = 600

    # 페이지 그리기
    self.drawPage()

  def drawPage(self):
    # 페이지 그리기
    screen.fill(BLACK)

    # 이전 단어
    loadText("이전단어", 25, YELLOW, 198, 690)
    loadText(" > ", 25, YELLOW, 277, 690)
    
    # 입력창
    self.input.draw(screen)

    # 입력 버튼
    loadText("입력", 25, YELLOW, 608, 690)
    loadRect(WHITE, 567, 679, 80, 50, 2)

    # 게임방법 다시보기
    LoadButton("gamerule.png", 70, 70, 700, 10)

    # 다시시작 버튼
    LoadButton("restart.png", 70, 70, 700, 90)

    # 게임종료 버튼
    LoadButton("endgame.png", 70, 70, 700, 170)


  def restart(self):
    self.active = True
    self.text = ""
    self.drawPage() # 게임 실행 페이지 띄우기

  def gameruleSmall(self):
    # 게임 설명 화면 - 작게
    loadText("게임 규칙", 30, WHITE, screen_width/2, 50)
    y = 140
    for i in range(len(RULE)):
      loadText(RULE[i], 15, WHITE, screen_width/2, y)
      y += 20
      
  def handle_event(self, event, end):
    # 게임을 진행할 수 있는 상황이면 게임 종료 화면은 항상 True이다.
    end.active = True

    if self.active == True and event.type == pygame.MOUSEMOTION:
      mouse_pos = pygame.mouse.get_pos()
      if mouse_pos[0] in list(range(700, 770)) and mouse_pos[1] in list(range(10, 80)):
        # 게임 방법 버튼 크기 커짐
        self.drawPage()
        LoadButton("gamerule.png", 80, 80, 695, 5)
        # 게임 방법 다시보기
        self.gameruleSmall()
      elif mouse_pos[0] in list(range(700, 770)) and mouse_pos[1] in list(range(90, 160)):
        # 다시시작 버튼 크기 커짐
        self.drawPage()
        LoadButton("restart.png", 80, 80, 695, 85)
      elif mouse_pos[0] in list(range(700, 770)) and mouse_pos[1] in list(range(170, 240)):
        # 게임종료 버튼 크기 커짐
        self.drawPage()
        LoadButton("endgame.png", 80, 80, 695, 165)
      elif mouse_pos[0] in list(range(567, 647)) and mouse_pos[1] in list(range(679, 729)):
        # 입력 버튼 크기 커짐
        loadText("입력", 30, YELLOW, 608, 690)
      else:
        # 화면 복구
        screen.fill(BLACK)
        self.drawPage()
    
    if event.type == pygame.KEYDOWN:
      self.input.handle_event(event)

    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_pos = pygame.mouse.get_pos()
      if mouse_pos[0] in list(range(700, 770)) and mouse_pos[1] in list(range(90, 160)):
        # 다시시작 버튼 클릭
        # restart 함수 필요
        self.restart()

      if mouse_pos[0] in list(range(700, 770)) and mouse_pos[1] in list(range(170, 240)):
        # 게임종료 버튼 클릭
        end.win = False
        self.active = False
        gameoverPage # 게임 종료 페이지 띄우기

      if mouse_pos[0] in list(range(567, 647)) and mouse_pos[1] in list(range(679, 729)):
        # 입력 버튼 클릭
        # self.text가 유효한지 체크
        # 단어가 유효하면 띄운다
        print(self.text)
        loadText(self.text, 25, YELLOW, 100, 100)
        

      
        

        
class gameoverPage:
  def __init__(self):
    # print("gameoverpage")
    # 게임 종료 페이지
    self.active = True
    self.win = False

    # 페이지 그리기
    self.drawPage()

  def drawPage(self):
    # 페이지 그리기
    screen.fill(BLACK)
    if win:
      loadText("Player Win!!", 50, WHITE, screen_width/2, screen_height/2)
    else:
      loadText("Player Lose...", 50, WHITE, screen_width/2, screen_height/2)

    # 다시 시작 버튼
    loadRect(YELLOW2, 155, 615, 150, 70, 0)
    loadText_bold("다시시작", 25, WHITE, 230, 630)

    # 게임 종료 버튼
    loadRect(YELLOW2, screen_width/2 - 75, 615, 150, 70, 0)
    loadText_bold("게임종료", 25, WHITE, screen_width/2, 630)

    # 히스토리 확인 버튼
    LoadButton("history.png", 150, 100, screen_width/2 + 95, 600)

  def handle_event(self, event, playPage):
    if self.active == True and event.type == pygame.MOUSEMOTION:
      mouse_pos = pygame.mouse.get_pos()
      if mouse_pos[0] in list(range(325, 475)) and mouse_pos[1] in list(range(615, 685)):
        # 게임종료 글씨 크기 커짐
          self.drawPage()
          loadRect(YELLOW2, 325, 615, 150, 70, 0)
          loadText_bold("게임종료", 35, WHITE, 395, 625)
      elif mouse_pos[0] in list(range(155, 305)) and mouse_pos[1] in list(range(615, 685)):
        # 다시시작 글씨 크기 커짐
          self.drawPage()
          loadRect(YELLOW2, 155, 615, 150, 70, 0)
          loadText_bold("다시시작", 35, WHITE, 225, 625)
      elif mouse_pos[0] in list(range(495, 645)) and mouse_pos[1] in list(range(600, 700)):
        # history 버튼 크기 커짐
        self.drawPage()
        LoadButton("history.png", 160, 110, screen_width/2 + 90, 595)
      else:
        self.drawPage()
    
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_pos = pygame.mouse.get_pos()
      if mouse_pos[0] in list(range(325, 475)) and mouse_pos[1] in list(range(615, 685)):
        # 게임종료 버튼 클릭
        return False # 게임종료
      if mouse_pos[0] in list(range(155, 305)) and mouse_pos[1] in list(range(615, 685)):
        # 다시시작 버튼 클릭
         playPage.restart()
      if mouse_pos[0] in list(range(495, 645)) and mouse_pos[1] in list(range(600, 700)):
        # history 버튼 클릭
        self.active = False
        historyPage() # historyPage로 이동
      
    return True

class historyPage:
  def __init__(self):
    # history를 보여주는 페이지
    self.currentPage = "history"
    self.active = True
    self.drawPage()

  def drawPage(self):
    screen.fill(BLACK)
    
    # 하얀 페이지
    loadRect(WHITE, 20, 100, 760, 680, 0)

    # 상단 history
    loadText_bold("HISTORY", 40, WHITE, screen_width/2, 22)
    
    # 다시시작 버튼
    loadRect(YELLOW2, 560, 22, 100, 60, 0)
    loadText_bold("다시시작", 20, WHITE, 609, 35)

    # 게임종료 버튼
    loadRect(YELLOW2, 680, 22, 100, 60, 0)
    loadText_bold("게임종료", 20, WHITE, 729, 35)

  def handle_event(self, event, playPage):
    if self.active == True and event.type == pygame.MOUSEMOTION:
      mouse_pos = pygame.mouse.get_pos()
      if mouse_pos[0] in list(range(560, 660)) and mouse_pos[1] in list(range(22, 82)):
        # 다시시작 글씨 크기 커짐
          self.drawPage()
          loadRect(YELLOW2, 560, 22, 100, 60, 0)
          loadText_bold("다시시작", 25, WHITE, 609, 32)
      elif mouse_pos[0] in list(range(680, 780)) and mouse_pos[1] in list(range(22, 82)):
        # 게임종료 글씨 크기 커짐
          self.drawPage()
          loadRect(YELLOW2, 680, 22, 100, 60, 0)
          loadText_bold("게임종료", 25, WHITE, 729, 32)
      else:
        self.drawPage()
      

    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_pos = pygame.mouse.get_pos()
      if mouse_pos[0] in list(range(560, 660)) and mouse_pos[1] in list(range(22, 82)):
        # 다시시작 버튼 클릭
        playPage.restart()
      if mouse_pos[0] in list(range(680, 780)) and mouse_pos[1] in list(range(22, 82)):
        # 게임종료 버튼 클릭
        return False # 게임종료

    return True
     

  # FPS 초당 프레임 수
clock = pygame.time.Clock()

# 게임실행 여부
playing = True

# 게임 승패 여부
win = False

# 페이지 생성
main = mainPage()
rule = gamerulePage()
play = gameplayPage()
end = gameoverPage()
history = historyPage()

# 게임 실행
while playing:
  clock.tick(30)

  for event in pygame.event.get():
    # 종료 이벤트 - 창을 닫을 경우 게임이 종료됨
    if event.type == pygame.QUIT:
      playing = False
      break

    if main.active == True:
      main.handle_event(event)
      
    elif rule.active == True:
      rule.handle_event(event)

    elif play.active == True:
      play.handle_event(event, end)

    elif end.active == True:
      playing = end.handle_event(event, play)

    elif history.active == True:
      playing = history.handle_event(event, play)
    

  pygame.display.flip()

pygame.quit()

