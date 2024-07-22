
import random
import sys

class Apple():
    def __init__(self,pos_x,pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    @classmethod
    def random_position(cls,width,height,excluded_positions:list = []):
        x = random.randint(0,width-1)
        y = random.randint(0,height-1)
        while (x,y) in excluded_positions:
            x = random.randint(0,width-1)
            y = random.randint(0,height-1)
        return cls(x,y)

    def get_pos(self):
        return (self.pos_x,self.pos_y)



class Snake():
    def __init__(self,init_body,init_direction) -> None:
        self._body = init_body
        self._direction = Snake.direction_convert(init_direction)

    @staticmethod
    def direction_convert(directionstr):
        direction_map = {
            'UP': (0, 1),
            'DOWN': (0, -1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
        }
        if directionstr in direction_map:
            return direction_map[directionstr]
        else:
            raise ValueError("方向设置错误")

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self,direction):
        self._direction = direction

    def head(self):
        return self._body[-1]

    def take_step(self):
        """
        Returns:
            tuple: 新的头部位置
        """
        # WRONG
        #self._body = self._body[1:].append(self.head_position())
        # RIGHT
        # self._body = self._body[1:]
        # self._body.append(self.head_position())
        new_head_position = self.head_position()
        self._body = self._body[1:] + [new_head_position]
        return new_head_position

    def head_position(self):
        return tuple(map(lambda x,y:x+y,self.direction,self.head()))


class Game():
    def __init__(self,height,width):
        self.width = width
        self.height = height
        self.matrix = self.__board_matrix()
        self.snake = Snake([(0, 0), (0, 1), (0, 2), (0, 3)], 'UP')     #贪吃蛇的初始位置和方向
        self.apple = Apple.random_position(self.width,self.height,excluded_positions=self.snake._body)
    def __board_matrix(self):
        assert self.width > 0, "宽度应为正数"
        assert self.height > 0, "高度应为正数"
        #矩阵外加一圈边界
        return [[None] * (self.width+2) for _ in range(self.height+2)]

    @staticmethod
    def cordinate_mapping(x_logical,y_logical,height):
        """
        将逻辑坐标映射为二维列表中的索引，逻辑坐标中左下角为（0,0），二维列表最外层包含一圈边界
        """
        row_index = height-y_logical
        col_index = x_logical+1
        return (row_index,col_index)

    def init_elements(self):
        matrix = self.matrix
        # true:身体 false 头 "a":苹果
        #添加蛇
        for snakeblock in self.snake._body:
            #坐标映射
            row_index,col_index = Game.cordinate_mapping(*snakeblock,self.height)
            if self.snake._body.index(snakeblock) != len(self.snake._body) - 1:
                matrix[row_index][col_index] = True
            else:
                matrix[row_index][col_index] = False
        #添加苹果
        row_index,col_index =Game.cordinate_mapping(self.apple.pos_x,self.apple.pos_y,self.height)
        matrix[row_index][col_index] = "a"
        self.render()

    def refresh_elements(self):
        matrix = self.matrix
        # WRONG consulting:https://nedbatchelder.com/text/names.html
        # for row in matrix:
        #     for element in row:
        #         if element != "a":
        #             element = None
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] != "a":
                    matrix[i][j] = None

        #添加蛇
        for snakeblock in self.snake._body:
            #坐标映射
            row_index,col_index = Game.cordinate_mapping(*snakeblock,self.height)
            if self.snake._body.index(snakeblock) != len(self.snake._body) - 1:
                matrix[row_index][col_index] = True
            else:
                matrix[row_index][col_index] = False
        self.render()


    def render(self):
        matrix = self.matrix
        print("Snake".center(len(matrix[0])))
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if (i == 0 or i == len(matrix)-1) and (j == 0 or j == len(matrix[0])-1):
                    print("+",end="")
                elif i == 0 or i == len(matrix)-1:
                    print("-",end="")
                elif j == 0 or j == len(matrix[0])-1:
                    print("|",end="")
                elif matrix[i][j] == "a":
                    print("♥",end="")
                elif matrix[i][j] == True:
                    print("o",end="")
                elif matrix[i][j] == False:
                    print("x",end="")

                else:
                    print(" ",end="")
            print("")

    def take_step(self):
        old_pos = self.snake._body
        head_pos = self.snake.take_step()
        #撞墙
        if head_pos[0]<0 or head_pos[0] >= self.width or head_pos[1] < 0 or head_pos[1] >= self.height:
            print("您已撞墙！ 请重新开始游戏")
            sys.exit()
        #吃苹果
        elif head_pos == self.apple.get_pos():
            self.apple = Apple.random_position(self.width,self.height,excluded_positions=self.snake._body)
            row_index,col_index =Game.cordinate_mapping(self.apple.pos_x,self.apple.pos_y,self.height)
            self.matrix[row_index][col_index] = "a"
            self.snake._body = [old_pos[0]] + self.snake._body
        elif head_pos in old_pos:
            print("您撞到了自己！ 请重新开始游戏")
            sys.exit()


#主程序
if __name__ == '__main__':
    myGame = Game(height=10,width=20)
    myGame.init_elements()
    key2direction = {'w':'UP','a':'LEFT','s':'DOWN','d':'RIGHT'}   
    Lastinput = ""
    print("按q可以退出游戏，输入留空将按之前方向移动")
    while True:
        direction = input("请输入w、a、d、s任意一个来移动():")
        if direction == "q":
            break
        elif direction == "":
            direction = Lastinput
            myGame.snake.direction = Snake.direction_convert(key2direction[Lastinput.lower()])
            myGame.take_step()
        elif direction.lower() in key2direction:
            myGame.snake.direction = Snake.direction_convert(key2direction[direction.lower()])
            myGame.take_step()
            Lastinput = direction
        else:
            print("输入错误请输入w、a、d、s中任意一个.")
        myGame.refresh_elements()
        #Lastinput = direction

