import pygame        #导入pygame游戏模块
import time
import sys
from pygame.locals import *

initChessList = []          #保存的是棋盘坐标
initConnect = []            #保存的是棋盘连线
initRole = 1                #1：代表白棋； 2：代表黑棋；11：代表白旗选中状态；12：代表黑棋选中状态
resultFlag = 0              #结果标志
nowclick = 0                #保存选中棋子的参数
class StornPoint():
    def __init__(self,x,y,value):
        '''
        :param x: 代表x轴坐标
        :param y: 代表y轴坐标
        :param value: 当前坐标点的棋子：0:没有棋子 1:白子 2:黑子
        '''
        self.x = x            #初始化成员变量
        self.y = y
        self.value = value

def initChessSquare(x,y):     #初始化棋盘
    for i in range(5):       # 每一行的交叉点坐标
        rowlist = []
        for j in range(7):   # 每一列的交叉点坐标
            pointX = x+ j*99
            pointY = y+ i*98
            if i == 0:
                if j ==6:
                    sp = StornPoint(pointX,pointY,0)
                elif j ==5:
                    sp = StornPoint(10000,10000,0)
                else:
                    sp = StornPoint(pointX,pointY,1)
            elif i == 4:
                if j ==6:
                    sp = StornPoint(pointX,pointY,0)
                elif j == 5:
                    sp = StornPoint(10000,10000,0)
                else:
                    sp = StornPoint(pointX,pointY,2)
            elif i == 1 or i == 3 :
                if j == 6:
                    sp = StornPoint(10000,10000,0)
                else:
                    sp = StornPoint(pointX,pointY,0)
            elif i == 2:
                sp = StornPoint(pointX,pointY,0)
            rowlist.append(sp)
        initChessList.append(rowlist)

#初始化棋盘的各连线
def initChessConnect():
    for i in range(5):
        line = []
        if i == 2:
            for j in range(7):
                line.append([i,j])
        else:
            for j in range(5):
                line.append([i,j])
        initConnect.append(line)
    for i in range(7):
        line = []
        if i < 5:
            for j in range(5):
                line.append([j,i])
        elif i == 5:
            for j in range(1,4):
                line.append([j,i])
        elif i == 6:
            line.append([0,6])
            line.append([2,6])
            line.append([4,6])
        initConnect.append(line)
    for i in range(4):
        line = []
        for j in range(5):
            if i == 0:
                line.append([j,j])
            elif i == 1:
                line.append([4-j,j])
            elif i == 2:
                line.append([j,j+2])
            elif i == 3:
                line.append([j,6-j])
        initConnect.append(line)
    for i in range(2):
        line = []
        for j in range(3):
            if i ==0:
                line.append([j,2-j])
            elif i ==1:
                line.append([j+2,j])
        initConnect.append(line)


#判断是否胜利与是否存在吃棋
def judge(value):
    global initChessList,resultFlag,initConnect
    flag = 2       #1代表挤进葫芦；2代表全部吃掉
    for i in range(18):
        Chess = 0
        for j in range(len(initConnect[i])):
            x = initConnect[i][j][0]
            y = initConnect[i][j][1]
            if initChessList[x][y].value:
                Chess += 1
        if Chess == 3:
            for j in range(len(initConnect[i])-2):
                x = []
                y = []
                for k in range(3):
                    x.append(initConnect[i][j+k][0])
                    y.append(initConnect[i][j+k][1])
                if initChessList[x[0]][y[0]].value == initChessList[x[2]][y[2]].value and initChessList[x[0]][y[0]].value\
                    and initChessList[x[0]][y[0]].value != initChessList[x[1]][y[1]].value and initChessList[x[1]][y[1]].value:
                    for k in range(3):
                        initChessList[x[k]][y[k]].value = value
    ChessC = 0
    for temp in initChessList:
        for point in temp:
            if point.value:
                ChessC = point.value
                break
        if ChessC :
            break 
    for temp in initChessList:
        for point in temp:
            if point.value and point.value != ChessC:
                flag = 0
                break

    if initChessList[2][5].value and initChessList[1][5].value and initChessList[3][5].value:
        isone = initChessList[1][5].value
        if initChessList[3][5].value == isone and initChessList[2][4].value == isone and initChessList[2][6].value == isone\
            and initChessList[2][5].value != isone:
            flag = 1
    if flag:               #如果条件成立，证明游戏结束
        if flag == 1:
            resultFlag = value #获取成立的棋子颜色
            print("白棋赢" if value == 1 else "黑棋赢")
        else:
            resultFlag = value #获取成立的棋子颜色
            print("黑赢" if value == 1 else "白旗赢")

#判断能否移动
def iscanmove(point,nowclick):
    ismove = 0
    pointy = int((point.x-60)/99)
    pointx = int((point.y-40)/98)
    clicky = int((nowclick.x-60)/99)
    clickx = int((nowclick.y-40)/98)
    for i in range(18):
        pointj = 10;clickj = 10
        for j in range(len(initConnect[i])):
            if initConnect[i][j][0] == pointx and initConnect[i][j][1] == pointy:
                pointj = j
            elif initConnect[i][j][0] == clickx and initConnect[i][j][1] == clicky:
                clickj = j
        if pointj < 10 and clickj < 10:
            ismove = 1
        if ismove:
            for j in range(min(pointj,clickj)+1,max(pointj,clickj)):
                if initChessList[initConnect[i][j][0]][initConnect[i][j][1]].value:
                    ismove = 0
        if ismove:
            return ismove

def eventHander():            #监听各种事件
    for event in pygame.event.get():
        global initRole,initRole,nowclick,initConnect,initChessList
        if event.type == QUIT:#事件类型为退出时
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN: #当点击鼠标时
            x,y = pygame.mouse.get_pos()  #获取点击鼠标的位置坐标
            for temp in initChessList:
                for point in temp:
                    if x>=point.x-10 and x<=point.x+10 and y>=point.y-10 and y<=point.y+10 and point.value == initRole \
                        and nowclick.value == 0:
                        nowclick = StornPoint(point.x,point.y,point.value)
                        point.value = 10+point.value
                        if initRole == 1:
                            initRole =2
                        elif initRole == 2:
                            initRole = 1
                        break 
                    elif x>=point.x-10 and x<=point.x+10 and y>=point.y-10 and y<=point.y+10 and point.value == 0 \
                        and nowclick.value:
                        ismove = iscanmove(point,nowclick)
                        if ismove:
                            point.value = nowclick.value
                            for temp1 in initChessList:
                                for point1 in temp1:
                                    if point1.x == nowclick.x and point1.y == nowclick.y:
                                        point1.value = 0
                                        break
                            nowclick.value = 0
                            judge(point.value)
                            break
                    elif x>=point.x-10 and x<=point.x+10 and y>=point.y-10 and y<=point.y+10 and point.value > 10:
                        nowclick = StornPoint(0,0,0)
                        point.value = point.value-10
                        if initRole == 1:
                            initRole =2
                        elif initRole == 2:
                            initRole = 1
                        break


def main():
    global initChessList,resultFlag,initConnect,nowclick 
    initChessSquare(60,40)
    initChessConnect()
    nowclick = StornPoint(0,0,0)
    pygame.init()     # 初始化游戏环境
    screen = pygame.display.set_mode((700,470),0,0)          # 创建游戏窗口 # 第一个参数是元组：窗口的长和宽
    pygame.display.set_caption("五路挑夹棋")                # 添加游戏标题
    background = pygame.image.load("source/background.png")          #加载背景图片
    whiteStorn = pygame.image.load("source/white.png") #加载白棋图片
    blackStorn = pygame.image.load("source/black.png") #加载黑棋图片
    whiteStornnew = pygame.image.load("source/whitenew.png") #加载白棋图片
    blackStornnew = pygame.image.load("source/blacknew.png") #加载黑棋图片
    resultStorn = pygame.image.load("source/win.png")#加载 赢 时的图片
    rect = blackStorn.get_rect()

    while True:
        screen.blit(background,(0,0))
        for temp in initChessList:
            for point in temp:
                if point.value == 1:          #当棋子类型为1时，绘制白棋
                    screen.blit(whiteStorn,(point.x-25,point.y-25))
                elif point.value == 2:        #当棋子类型为2时，绘制黑棋
                    screen.blit(blackStorn,(point.x-25,point.y-25))
                elif point.value == 11:
                    screen.blit(whiteStornnew,(point.x-25,point.y-25))
                elif point.value == 12:
                    screen.blit(blackStornnew,(point.x-25,point.y-25))

        if resultFlag >0:
            initChessList = []                 # 清空棋盘
            initChessSquare(50,50)             # 重新初始化棋盘
            screen.blit(resultStorn,(200,200)) #绘制获胜时的图片
        pygame.display.update()                #更新视图

        if resultFlag >0:
            time.sleep(10)
            resultFlag = 0                     #置空之前的获胜结果
        eventHander()                          #调用之前定义的事件函数
if __name__ == '__main__':
    main()        #调用主函数绘制窗口
    pass

