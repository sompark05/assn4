import tkinter as tk
from assn4_model import Board

TITLE = "Minesweeper"
BTN_WIDTH = 30
BTN_HEIGHT = 30
BORDER_SIZE = 2
OUTTER_PADDING_SIZE = 10
BACKGROUND_COLOR = "#DCDCDC"

# App 클래스
class App(tk.Frame):
    def __init__(self, master, board):
        super(App, self).__init__(master)
        master.title(TITLE)

        # 창을 자동으로 리사이즈 해주는 코드
        master.geometry("")

        # 게임에 사용할 이미지 불러오기
        self.base_icon = tk.PhotoImage(file="imgs/smile.png")
        self.success_icon = tk.PhotoImage(file="imgs/sunglasses.png")
        self.fail_icon = tk.PhotoImage(file="imgs/skull.png")
        self.flag_icon = tk.PhotoImage(file="imgs/flag.png")
        self.bomb_icon = tk.PhotoImage(file="imgs/bomb.png")

        # 기본적인 변수 설정
        self.height = 10
        self.width = 10
        self.numMine = 10
        self.num_flag = 0
        self.board = board
        self.btn_list = []
        self.game = True
        
        self["bg"] = BACKGROUND_COLOR
        self["relief"] = tk.SUNKEN
        self["bd"] = BORDER_SIZE
        self["padx"] = OUTTER_PADDING_SIZE
        self["pady"] = OUTTER_PADDING_SIZE

        # header frame 설정
        head = tk.Frame(self, bg=BACKGROUND_COLOR,
                        relief=tk.SUNKEN, bd=BORDER_SIZE)
        head.grid(row=0, column=0, columnspan=self.width,
                  pady=(0, OUTTER_PADDING_SIZE), sticky='ew')
        
        # start 버튼을 header에 넣어준다
        start_wrapper = tk.Frame(head, width=BTN_WIDTH, height=BTN_HEIGHT)
        start_wrapper.pack_propagate(0)
        start_wrapper.pack(padx=OUTTER_PADDING_SIZE, pady=OUTTER_PADDING_SIZE)
        self.start = tk.Button(start_wrapper, image=self.base_icon, bd=BORDER_SIZE)
        self.start.pack(expand=True, fill='both')
        self.start.config(command= lambda : reset_board(self.numMine, self.height, self.width))
        
        # body frame 설정
        self.body = tk.Frame(self, bg=BACKGROUND_COLOR,
                        relief=tk.SUNKEN, bd=BORDER_SIZE)
        self.body.grid(row=1, column=0, columnspan=self.width)
        
        # 메뉴 바 생성
        menu_bar = tk.Menu(master)
        master.config(menu=menu_bar)

        # 난이도 메뉴 생성
        level_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="난이도", menu=level_menu)

        # 난이도 메뉴에 옵션 추가
        level_menu.add_command(label="Easy", command=lambda: reset_board(10, 10, 10))
        level_menu.add_command(label="Normal", command=lambda: reset_board(30, 15, 15)) 
        level_menu.add_command(label="Hard", command=lambda: reset_board(50, 20, 20))

        # 난이도 설정을 누르면 board를 reset하는 함수
        def reset_board(numMine, height, width):
            # board를 리셋해준다
            self.board.reset(numMine, height, width)
            self.height = height
            self.width = width
            self.numMine = numMine
            self.start["image"] = self.base_icon
            self.game = True
            self.num_flag = 0

            # update 함수 호출
            self.update(self.height, self.width)

        # update 함수 호출
        self.update(self.height, self.width)


    # 좌클릭을 헀을 때 작동하는 함수
    def onLeftClick(self, y, x, btn:tk.Button):

        if self.game == False:
            return

        # # 이미지가 2번째 이미지 (pyimage2) 즉 선글라스 이미지하면 아무것도 하지 않고 리턴한다
        # if self.start["image"] == "pyimage2":
        #     return

        # 이미 밝혀진 패널이거나 깃발이 꽃쳐있으면 아무것도 하지 않고 리턴한다
        if self.board.checkReveal(y, x) or self.board.checkFlag(y, x):
            return
        
        # board의 unveil() 함수를 호출하고 밝혀야할 패널 인덱스를 리스트로 가지고 온다
        result = self.board.unveil(y, x)

        # result가 -1 즉, 지뢰 패널을 눌렀다면 모든 패널을 밝히고, self.game을 False로 바꿔준다
        if result == -1:
            self.game = False
            for row in range(len(self.btn_list)):
                for col in range(len(self.btn_list)):
                    self.board.unveil(row, col)

        # reveal된 panel들을 화면에 표시한다    
        for row in range(len(self.btn_list)):
            for col in range(len(self.btn_list)):
                if self.board.checkReveal(row, col):
                    self.btn_list[row][col].config(state=tk.DISABLED, relief=tk.SUNKEN)
                    mines = self.board.getNumOfNearMines(row, col)

                    # 깃발이 있다면 없애준다
                    if self.btn_list[row][col]["image"] != "":
                        self.btn_list[row][col]["image"] = ""
                        self.num_flag -= 1
                    
                    # 패널이 지뢰하면, 패널을 폭탄 이미지로 바꿔주고, 초기화 버튼의 이미지를 해골로 바꾼다
                    if mines is None:
                        self.btn_list[row][col]["image"] = self.bomb_icon
                        self.start["image"] = self.fail_icon

                    # 패널 주변의 지뢰 개수에 따라 숫자를 적어준다
                    if mines != 0:
                        self.btn_list[row][col]["text"] = mines
                        self.btn_list[row][col]["font"] = ("Arial", 15, "bold")
                        
        # 승리 조건 확인
        if self.board.getNumOfRevealedPanels() == self.height*self.width - self.numMine and self.num_flag == self.numMine:
            self.start["image"] = self.success_icon   
            self.game = False


           
    # 우클릭 했을 때 작동하는 함수
    def onRightClick(self, y, x, btn):
        if self.game == False:
            return
        
        # # 이미지가 2번째 이미지 (pyimage2) 즉 선글라스 이미지하면 아무것도 하지 않고 리턴한다
        # if self.start["image"] == "pyimage2":
        #     return
        
         # 이미 밝혀진 패널이면 아무것도 하지 않는다
        if self.board.checkReveal(y, x):
            pass
        else:
            # 깃발이 있다면 없애준다
            if self.board.checkFlag(y, x):
                btn["image"] = ""
                self.board.toggleFlag(y, x)
                self.num_flag -= 1
            # 깃발이 없다면 깃발을 만든다
            else:
                btn["image"] = self.flag_icon
                self.board.toggleFlag(y, x)
                self.num_flag += 1
        # 만약 모든 EmptyPanel이 밝혀졌고 지뢰 패널 위에 깃발이 있다면 start 버튼 이미지를 success로 바꿔준다
        if self.board.getNumOfRevealedPanels() == self.height*self.width - self.numMine and self.num_flag == self.numMine:
            self.start["image"] = self.success_icon
            self.game = False
               

    # 이벤트가 생길 때마다 업데이트 하는 함수
    def update(self, height, width):
        w = width
        h = height
        self.btn_list = []
        
        # clear all widgets in body frame
        for widget in self.body.winfo_children():
            widget.destroy()

        for row in range(h):
            temp = []
            for col in range(w):
                # 버튼 wrapper 만들어준다
                btn_wrapper = tk.Frame(
                    self.body, width=BTN_WIDTH, height=BTN_HEIGHT)
                btn_wrapper.pack_propagate(0)
                btn_wrapper.grid(row=row, column=col)

                # 버튼을 생성해 준다
                btn = tk.Button(btn_wrapper, bg=BACKGROUND_COLOR, bd=BORDER_SIZE)
                btn.config(command= lambda y=row, x=col, btn=btn: self.onLeftClick(y, x, btn))
                btn.bind("<ButtonRelease-3>", lambda e, y=row, x=col, btn=btn : self.onRightClick(y, x, btn))
                temp.append(btn)
                btn.pack(expand=True, fill='both')
            self.btn_list.append(temp)   
        self.pack()

    
if __name__ == '__main__':
    print("start program")
    root = tk.Tk()
    board = Board(10, 10, 10)
    app = App(root, board)
    app.mainloop()
