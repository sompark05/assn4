import random
import tkinter as tk

x_pos = [-1, 0, 1]
y_pos = [-1, 0, 1]
integrated_list = [[j, i] for j in y_pos for i in x_pos]

# 패널 클래스
class Panel:
    def __init__(self):
        """
        패널 초기화
        1. isRevealed : False
        2. hasFlag : False
        """
        self.isRevealed = False
        self.hasFlag = False
        
    # 깃발을 토글하는 함수
    def toggleFlag(self):
        """
        깃발을 토글한다.
        현재 True라면, 실행 후 False
        현재 False라면, 실행 후 True
        """
        if self.hasFlag:
            self.hasFlag = False
        else:
            self.hasFlag = True

    # 패널을 오픈하는 함수
    def unveil(self):
        """
        패널을 오픈한다.
        """
        self.isRevealed = True

# EmptyPanel 클래스, Panel 클래스를 상속 받는다 
class EmptyPanel(Panel):
    def __init__(self):
        super().__init__()
        self.near_mines = 0

    # 주변 지뢰 개수를 1 증가시키는 함수
    def addNumOfNearMines(self):
        """
        주변 지뢰 개수를 1 증가시킨다.
        """
        self.near_mines += 1

    # 패널을 오픈하는 함수
    def unveil(self):
        """
        패널을 오픈한다.
        부모인 P anel 의 unveil 을 수행하고 이때 인접한 mine 의 수를
r eturn 합니다
        """
        super().unveil()
        return self.near_mines

# MinePanel 클래스, Panel 클래스를 상속 받는다
class MinePanel(Panel):
    def __init__(self):
        super().__init__()

    # 패널을 오픈하는 함수
    def unveil(self):
        """
        패널을 오픈한다.
        부모인 P anel 의 unveil 을 수행하고 -1을 return합니다.
        """
        super().unveil()
        return -1

# Board 클래스
class Board:
    # 생성자
    def __init__(self, numMine, height, width):
        self.panels = []
        self.height = height
        self.width = width

        # board height와 width에 따라 가능한 모든 좌표를 가지고 있는 list를 만든다
        board_index_list = [[j, i] for i in range(self.width) for j in range(self.height)]
        
        # board_inex_list에서 지뢰 개수만큼 랜덤하게 가져온다
        mine_loc_list = random.sample(board_index_list, k=numMine)

        # mine_loc_list에 있는 지뢰 위치를 바탕으로 panels 리스트를 만든다
        for x in range(width):
            temp = []
            for y in range(height):
                if [x, y] in mine_loc_list:
                    temp.append(MinePanel())
                else:
                    temp.append(EmptyPanel())
            self.panels.append(temp)

        # panels를 돌며, 각 패널의 주변의 지뢰를 계산하고 addNumOfNearMines() 함수로 값을 더해준다
        for y in range(len(self.panels)):
                for x in range(len(self.panels[y])):
                    num_of_near_mines = self.getNumOfNearMines(y, x)
                    if num_of_near_mines is not None:
                        for _ in range(num_of_near_mines):
                            self.panels[y][x].addNumOfNearMines()

    # panels를 초기화하는 함수
    def reset(self, numMine, height, width):
        """
        Board를 초기화한다.
        1. panels를 초기화한다.
        2. 중복 없이 numMine개의 지뢰를 랜덤하게 배치한다.
        3. 나머지 패널들을 EmptyPanel로 초기화한다.
        """
        # 생성자에 있는 코드와 같은 로직이다
        self.panels = []
        self.height = height
        self.width = width
        board_index_list = [[j, i ]for i in range(self.width) for j in range(self.height)]
        mine_loc_list = random.sample(board_index_list, k=numMine)

        for x in range(width):
            temp = []
            for y in range(height):
                if [x, y] in mine_loc_list:
                    temp.append(MinePanel())
                else:
                    temp.append(EmptyPanel())
            self.panels.append(temp)

        for y in range(len(self.panels)):
            for x in range(len(self.panels[y])):
                num_of_near_mines = self.getNumOfNearMines(y, x)
                if num_of_near_mines is not None:
                    for _ in range(num_of_near_mines):
                        self.panels[y][x].addNumOfNearMines()

    # 오픈된 패널의 개수를 반환하는 함수
    def getNumOfRevealedPanels(self):
        """
        오픈된 패널의 개수를 반환한다.
        """
        result = 0
        for row in self.panels:
            for panel in row:
                if panel.isRevealed:
                    result += 1
        
        return result

    # y, x 위치의 패널을 오픈한다
    def unveil(self, y, x):
        """
        y, x 위치의 패널을 오픈한다.
        """
        # index out of range일 때 return
        if y < 0 or y >= self.height or x < 0 or x >= self.width:
            return
        
        # 패널의 주변 지뢰 개수가 0이 아닐 때
        if self.panels[y][x].unveil() == -1:  
            return self.panels[y][x].unveil()
        
        if self.panels[y][x].unveil() != 0:
            return

        # 패널의 주변 지뢰가 없을 떄
        if self.panels[y][x].unveil() == 0:
            # 주변 8개의 패널을 돈다
            for next in range(len(integrated_list)):
                # 5번째는 자기 자신이므로 continue
                if next == 4:
                    continue
                try:
                    # 이미 밝혀진 패널이라면 continue
                    if self.panels[y + integrated_list[next][0]][x + integrated_list[next][1]].isRevealed:
                        continue
                except:
                    pass
                # unveil_recursive를 해 준다
                self.unveil(y + integrated_list[next][0], x + integrated_list[next][1])
        return
        

    def toggleFlag(self, y, x):
        """
        y, x 위치의 패널의 깃발을 토글한다.
        """
        self.panels[y][x].toggleFlag()

    def checkReveal(self, y, x):
        """
        y, x 위치의 패널이 오픈되었는지 확인한다.
        """
        if self.panels[y][x].isRevealed:
            return True
        return False

    def checkFlag(self, y, x):
        """
        y, x 위치의 패널에 깃발이 꽂혀있는지 확인한다.
        """
        if self.panels[y][x].hasFlag:
            return True
        return False

    def checkMine(self, y, x):
        """
        y, x 위치의 패널이 지뢰인지 확인한다.
        """
        if type(self.panels[y][x]) is MinePanel:
            return True
        return False

    def getNumOfNearMines(self, y, x):
        """
        y, x 위치의 패널의 주변 지뢰 개수를 반환한다.
        """
        if type(self.panels[y][x]) is not EmptyPanel:
            return 
        left = max(0, x-1)
        right = min(self.width-1, x+1)
        top = max(0, y-1)
        bottom = min(self.height-1, y+1)
        result = 0
        for i in range(left, right+1):
            for j in range(top, bottom+1):
                if self.checkMine(j, i):
                    result += 1
        return result
        