
import math

PI = 3.14159265359
class CBlock:
    def __init__(self, angle, pos, color):
        self.ULEN = 50
        self.m_angle = angle
        self.m_pos = pos
        self.m_color = color
        self.m_points = []

    # 围绕原点旋转点
    # 参数：pp为需要旋转的POINT指针，angle为旋转角度
    def _rotatePoint(self, pp, angle):
        radian = PI / 180 * (-angle)	        # 旋转弧度（逆时针），为符合直觉改为顺时针
        x = pp[0] * math.cos(radian) - pp[1] * math.sin(radian)
        y = pp[0] * math.sin(radian) + pp[1] * math.cos(radian)
        return (x, y)

    def rotateBlock(self, angle):
        self.m_angle = angle
        # 根据板块angle，重新计算旋转后各点坐标(原点保持不动)
        for i in range(1, len(self.m_points)):
            self.m_points[i] = self._rotatePoint(self.m_points[i], angle)

    def moveBlock(self, pos):
        m_pos = pos
        # 根据板块偏移量offx/offy，重新计算偏移后各点坐标
        for i in range(len(self.m_points)):
            x = self.m_points[i][0] + (m_pos[0] * self.ULEN)
            y = self.m_points[i][1] + (m_pos[1] * self.ULEN)
            self.m_points[i] = (x, y)

    def setColor(self, color):
        self.m_color = color

    def draw(self, pos):
        # 按照给定的pos,对所有板块顶点进行位移
        pts = []
        for point in self.m_points:
            # 四舍五入取整操作延迟到最后环节进行，以保证计算的精度
            x = round(pos[0] + point[0])
            y = round(pos[1] + point[1])
            # 调整y轴方向朝上
            y = screen.get_height() - y
            pts.append((x, y))
        pygame.draw.polygon(screen, self.m_color, pts)

# 小三角形◣，左下角为原点，边长 1 - 1 - sqrt(2)
class CTriangleS(CBlock):
    def __init__(self, angle, pos, color):
        super().__init__(angle, pos, color)
        self.m_points.append((0.0, 0.0))
        self.m_points.append((0.0, 1.0 * self.ULEN))
        self.m_points.append((1.0 * self.ULEN, 0))
        self.rotateBlock(self.m_angle)
        self.moveBlock(self.m_pos)

# 中三角形◣，左下角为原点，边长 sqrt(2) - sqrt(2) - 2
class CTriangleM(CBlock):
    def __init__(self, angle, pos, color):
        super().__init__(angle, pos, color)
        self.m_points = [(0.0, 0.0) for _ in range(3)]
        self.m_points[0] = (0.0, 0.0)
        self.m_points[1] = (0.0, math.sqrt(2) * self.ULEN)
        self.m_points[2] = (math.sqrt(2) * self.ULEN, 0.0)
        self.rotateBlock(self.m_angle)
        self.moveBlock(self.m_pos)

# 大三角形◣，左下角为原点，边长 2 - 2 - 2*sqrt(2)
class CTriangleL(CBlock):
    def __init__(self, angle, pos, color):
        super().__init__(angle, pos, color)
        self.m_points = [(0.0, 0.0) for _ in range(3)]
        self.m_points[0] = (0.0, 0.0)
        self.m_points[1] = (0.0, 2.0 * self.ULEN)
        self.m_points[2] = (2.0 * self.ULEN, 0.0)
        self.rotateBlock(self.m_angle)
        self.moveBlock(self.m_pos)

# 正方形■，左下角为原点，边长 1 - 1 - 1 - 1
class CSquare(CBlock):
    def __init__(self, angle, pos, color):
        super().__init__(angle, pos, color)
        self.m_points = [(0.0, 0.0) for _ in range(4)]
        self.m_points[0] = (0.0, 0.0)
        self.m_points[1] = (0.0, 1.0 * self.ULEN)
        self.m_points[2] = (1.0 * self.ULEN, 1.0 * self.ULEN)
        self.m_points[3] = (1.0 * self.ULEN, 0.0)
        self.rotateBlock(self.m_angle)
        self.moveBlock(self.m_pos)


# 右向平行四边形◢■◤，左下角为原点，边长sqrt(2) - 1 - sqrt(2) - 1
class CParallelogramR(CBlock):
    def __init__(self, angle, pos, color):
        super().__init__(angle, pos, color)
        self.m_points = [(0.0, 0.0) for _ in range(4)]
        self.m_points[0] = (0.0, 0.0)
        self.m_points[1] = (2.0 * math.sqrt(0.5) * self.ULEN, 0)
        self.m_points[2] = (3.0 * math.sqrt(0.5) * self.ULEN, math.sqrt(0.5) * self.ULEN)
        self.m_points[3] = (math.sqrt(0.5) * self.ULEN, math.sqrt(0.5) * self.ULEN)
        self.rotateBlock(self.m_angle)
        self.moveBlock(self.m_pos)

# 左向平行四边形◥■◣，左下角为原点，边长sqrt(2) - 1 - sqrt(2) - 1
class CParallelogramL(CBlock):
    def __init__(self, angle, pos, color):
        super().__init__(angle, pos, color)
        self.m_points = [(0.0, 0.0) for _ in range(4)]
        self.m_points[0] = (0.0, 0.0)
        self.m_points[1] = (2.0 * math.sqrt(0.5) * self.ULEN, 0)
        self.m_points[2] = (math.sqrt(0.5) * self.ULEN, math.sqrt(0.5) * self.ULEN)
        self.m_points[3] = (-math.sqrt(0.5) * self.ULEN, math.sqrt(0.5) * self.ULEN)
        self.rotateBlock(self.m_angle)
        self.moveBlock(self.m_pos)


class CTangram:
    def __init__(self, blocks) -> None:
        self.m_blocks = blocks

    def draw(self, pos):
        # 七巧板每个板块采用统一函数绘制
        for i in range(len(self.m_blocks)):
            self.m_blocks[i].draw(pos)

import pygame
from pygame.color import THECOLORS
# 初始化
pygame.init()
screen = pygame.display.set_mode((800, 600))
screen.fill((0, 0, 0))  # 清屏

arrhouse = [
	CTriangleS(-45, (-math.sqrt(2) / 2, -math.sqrt(2) / 2), THECOLORS['brown']),
	CTriangleS(-135, (-math.sqrt(2) / 2, -math.sqrt(2) / 2), THECOLORS['yellow']),
	CTriangleM(180, (math.sqrt(2), 0), THECOLORS['blue']),
	CTriangleL(135, (-(math.sqrt(2) - 1), math.sqrt(2)), THECOLORS['red']),
	CTriangleL(135, (0, 0), THECOLORS['cyan']),
	CSquare(0, (0, 1), THECOLORS['green']),
	CParallelogramR(45, (0, 1), THECOLORS['magenta']),
]

arrbox = [
	CTriangleS(135, (0, 0), THECOLORS['brown']),
	CTriangleS(-135, ( -math.sqrt(2) / 2, math.sqrt(2) / 2 ), THECOLORS['yellow']),
	CTriangleM(0, (-math.sqrt(2), -math.sqrt(2)), THECOLORS['blue']),
	CTriangleL(-45, (0, 0), THECOLORS['red']),
	CTriangleL(45, (0, 0), THECOLORS['cyan']),
	CSquare(-135, (0, 0), THECOLORS['green']),
	CParallelogramL(0, (0, -math.sqrt(2)), THECOLORS['magenta'])
]

arrturtle = [
	CTriangleS(135, (0, 0), THECOLORS['yellow']),
	CTriangleS(135, (2, 0), THECOLORS['brown']),
	CTriangleM(-135, (3, 1), THECOLORS['blue']),
	CTriangleL(0, (0, 0), THECOLORS['cyan']),
	CTriangleL(180, (2, 2), THECOLORS['red']),
	CSquare(0, (-2, 1), THECOLORS['green']),
	CParallelogramL(45, (-1, 1), THECOLORS['magenta'])
]

arrfish = [
	CTriangleS(0, (0, 0.5), THECOLORS['brown']),
	CTriangleS(90, (0, -0.5), THECOLORS['yellow']),
	CTriangleM(45, (1, 0.5), THECOLORS['blue']),
	CTriangleL(-90, (0, 0), THECOLORS['cyan']),
	CTriangleL(180, (0, 0), THECOLORS['red']),
	CSquare(0, (0, -0.5), THECOLORS['green']),
	CParallelogramL(45, (1, -0.5), THECOLORS['magenta'])
]

arrcat = [
	CTriangleS(45, (0, 0), THECOLORS['brown']),
	CTriangleS(-135, (0, 0), THECOLORS['yellow']),
	CTriangleM(-90, (0.5 * math.sqrt(2), -2 * math.sqrt(2)), THECOLORS['blue']),
	CTriangleL(-135, (1.5 * math.sqrt(2), -math.sqrt(2)), THECOLORS['cyan']),
	CTriangleL(-90, (1.5 * math.sqrt(2), -(2 + math.sqrt(2))), THECOLORS['red']),
	CSquare(135, (0, 0), THECOLORS['green']),
	CParallelogramR(-30, (1.5 * math.sqrt(2), -2 * math.sqrt(2)), THECOLORS['magenta'])
]

arrbird = [
	CTriangleS(135, (-0.5 * math.sqrt(2), (1 + 0.5 * math.sqrt(2))), THECOLORS['brown']),
	CTriangleS(135, (0, -2), THECOLORS['yellow']),
	CTriangleM(135, (1, -1), THECOLORS['blue']),
	CTriangleL(180, (0, 0), THECOLORS['cyan']),
	CTriangleL(90, (0, 0), THECOLORS['red']),
	CSquare(-90, (0, 0), THECOLORS['green']),
	CParallelogramL(-45, (2, -1), THECOLORS['magenta'])
]

arrduck = [
	CTriangleS(135, (-math.sqrt(2), math.sqrt(2)), THECOLORS['brown']),
	CTriangleS(135, (1.8, math.sqrt(0.5)), THECOLORS['yellow']),
	CTriangleM(-45, (math.sqrt(2) - 1, -math.sqrt(2) - 1), THECOLORS['blue']),
	CTriangleL(-45, (math.sqrt(2), -math.sqrt(2)), THECOLORS['cyan']),
	CTriangleL(135, (0, 0), THECOLORS['red']),
	CSquare(-45, (-math.sqrt(0.5), math.sqrt(0.5) ), THECOLORS['green']),
	CParallelogramL(-90, (0, 0), THECOLORS['magenta'])
]

arrshirt = [
	CTriangleS(90, (0, 0), THECOLORS['brown']),
	CTriangleS(180, (2, -1), THECOLORS['yellow']),
	CTriangleM(135, (1, 0), THECOLORS['blue']),
	CTriangleL(180, (1, -1), THECOLORS['cyan']),
	CTriangleL(0, (-1, -3), THECOLORS['red']),
	CSquare(180, (0, 0),  THECOLORS['green']),
	CParallelogramR(-45, (-2, -2), THECOLORS['magenta'])
]

arrwindmill = [
	CTriangleS(-135, (0, 0), THECOLORS['brown']),
	CTriangleS(135, (1.5 * math.sqrt(2), -0.5 * math.sqrt(2)), THECOLORS['yellow']),
	CTriangleM(0, (0, -math.sqrt(2)), THECOLORS['blue']),
	CTriangleL(-45, (0, 0), THECOLORS['cyan']),
	CTriangleL(45, (0.5 * math.sqrt(2), 0.5 * math.sqrt(2)), THECOLORS['red']),
	CSquare(45, (0.5 * math.sqrt(2), -0.5 * math.sqrt(2)), THECOLORS['green']),
	CParallelogramL(-90, (0, -math.sqrt(2)), THECOLORS['magenta'])
]

tg = CTangram(arrduck)
tg.draw((200,200))
pygame.display.flip()  # 更新屏幕

#clock = pygame.time.Clock()
running = True
while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 按键检测
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # draw frame
    # pygame.display.flip()  # 更新屏幕
    # clock.tick(60)  # 帧率控制

pygame.quit()

