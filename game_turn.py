import hgtk
from wordAnalysis import midReturn, midReturn_all, findword, checkexists

def playerturn (count, query, listbox, controller) :
    controller.wordOk = True
    if query == "":
        controller.wordOk = False
        listbox.insert(controller.listint, "단어를 입력해주세요")
        controller.listint += 1
        
    else:
        if not len(controller.history)==0 and not query[0] == controller.sword and not query=='':
            print("두음법칙 적용")
            print("sword: ", controller.sword, ", ", "query: ", query)
            sdis = hgtk.letter.decompose(controller.sword)
            qdis = hgtk.letter.decompose(query[0])
            if sdis[0] == 'ㄹ' and qdis[0] == 'ㄴ':
                listbox.insert(controller.listint, '두음법칙 적용됨')
                listbox.itemconfig(controller.listint, bg="red", fg="white")
                controller.listint += 1
            elif (sdis[0] == 'ㄹ' or sdis[0] == 'ㄴ') and qdis[0] == 'ㅇ' and qdis[1] in controller.vowels: 
                listbox.insert(controller.listint, '두음법칙 적용됨')
                listbox.itemconfig(controller.listint, bg="red", fg="white")
                controller.listint += 1
            else:
                controller.wordOk = False
                listbox.insert(controller.listint, controller.sword + '(으)로 시작하는 단어여야 합니다.')
                listbox.itemconfig(controller.listint, bg="red", fg="white")
                controller.listint += 1
        
        # 잘못된 글자 입력
        if (count == 1 and len(query) == 1) or (count != 1 and len(query) != count):
            print(str(count) + "글자")
            controller.wordOk = False
            listbox.insert(controller.listint, str(count) + '글자가 되어야 합니다.')
            listbox.itemconfig(controller.listint, bg="red", fg="white")
            controller.listint += 1

        # history 안에 있는 단어인지 확인
        if query in controller.history:
            print("중복글자")
            controller.wordOk = False
            listbox.insert(controller.listint, '이미 입력한 단어입니다.')
            listbox.itemconfig(controller.listint, bg="red", fg="white")
            controller.listint += 1

        if query[len(query)-1] in controller.blacklist:
            print("블랙리스트")
            listbox.insert(controller.listint, '아... 좀 심각한데요')
            controller.listint += 1

        if controller.wordOk:
            print("옳은 단어")
            # 단어의 유효성을 체크
            ans = checkexists(query, controller.apikey, controller.history)
            if ans == '':
                controller.wordOk = False
                listbox.insert(controller.listint, '유효한 단어를 입력해 주십시오')
                listbox.itemconfig(controller.listint, bg="red", fg="white")
                controller.listint += 1
            else:
                listbox.insert(controller.listint, query)
                controller.listint += 1
                mean = midReturn(ans, '<definition>', '</definition>')
                listbox.insert(controller.listint, '(' + mean + ')\n')
                controller.dict[query] = mean
                controller.userhistory.append(query)
                controller.listint += 1
    return query

def computerturn (count, query, listbox, nextquery, controller) :
    # 기능1 - 사용자 입력 시 history 단어 추가                
    controller.history.append(query)         
            
    start = query[len(query)-1]
    
    ans = findword(count, start + '*', controller.apikey, controller.history, controller.blacklist)
    
    if ans=='':
        #ㄹ -> ㄴ 검색
        sdis = hgtk.letter.decompose(start)
        if sdis[0] == 'ㄹ':
            newq = hgtk.letter.compose('ㄴ', sdis[1], sdis[2])
            print(start, '->', newq)
            start = newq
            ans = findword(count, newq + '*', controller.apikey, controller.history, controller.blacklist)
            if ans != '':
                listbox.insert(controller.listint, '두음법칙 적용')
                listbox.itemconfig(controller.listint, bg="red", fg="white")
                controller.listint += 1

    if ans=='':
        #(ㄹ->)ㄴ -> ㅇ 검색
        sdis = hgtk.letter.decompose(start)
        if sdis[0] == 'ㄴ' and sdis[1] in controller.vowels:
            newq = hgtk.letter.compose('ㅇ', sdis[1], sdis[2])
            print(start, '->', newq)
            ans = findword(count, newq + '*', controller.apikey, controller.history, controller.blacklist)
        if ans != '':
            listbox.insert(controller.listint, '두음법칙 적용')
            listbox.itemconfig(controller.listint, bg="red", fg="white")
            controller.listint += 1
                
    if ans=='':
        print('당신의 승리!')
        listbox.insert(controller.listint, "Player win!!")
        listbox.itemconfig(controller.listint, bg="yellow", fg="blue")
        nextquery.configure(text= "Winner")
        controller.listint += 1
        controller.playing = False 
    else:
        controller.answord = midReturn(ans, '<word>', '</word>') #단어 불러오기
        ansdef = midReturn(ans, '<definition>', '</definition>') # 품사 불러오기
        
        # 기능1 - 컴퓨터 입력 시 history 단어 추가
        controller.history.append(controller.answord)
        listbox.insert(controller.listint, controller.answord)
        controller.listint += 1
        listbox.insert(controller.listint, ansdef)
        controller.listint += 1
        controller.dict[controller.answord] = ansdef
        controller.computerhistory.append(controller.answord)

        nextquery.configure(text= query + '>'+ controller.answord)

        controller.sword = controller.answord[len(controller.answord)-1]