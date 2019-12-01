import os
import pygame
import time
import sys
import cv2
from pygame.locals import *
import tools.faceu as bd
from aip import AipSpeech

pygame.init()
pygame.mixer.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (32, 27)
pygame.display.set_caption('人脸识别')
screen = pygame.display.set_mode((640, 640))

SLEEP_TIME_LONG = 0
# 初始化摄像头
cap = cv2.VideoCapture(0)

bj = 'images/bg2.png'
mous = 'images/mous.png'
mous = pygame.image.load(mous)  # 拍照
mous1 = 'images/mouse.png'
mous1 = pygame.image.load(mous1)  # 换拍照按钮
nopeople = 'images/nopeople.png'
nopeople = pygame.image.load(nopeople)

class take_photo():
    tk = 'images/nopeople.png'
    al = pygame.image.load(tk)  # 显示信息图片
    filename = "images/test.jpg"  # 照片保存名字
    path = os.path.abspath('')  # 当前路径
    image_msg = path + '/images/test.jpg'  # 绝对路径
    print(image_msg)

    def image(self):
        # cam.saveSnapshot(self.filename, timestamp=3, boldfont=1, quality=75)
        ret, frame = cap.read()
        cv2.imwrite(self.filename, frame)

        # 加载摄像头图像
        image = pygame.image.load(self.filename)
        image_new = pygame.transform.scale(image, (640, 480))
        image_new = pygame.transform.flip(image_new, True, False)
        bg = pygame.image.load(bj)

        # 传送画面
        screen.blit(image_new, (0, 0))  # 画摄像头画面
        screen.blit(bg, (0, 0))  # 画背景图片
        screen.blit(mous, (305, 485))  # 画拍照按钮

    # 显示实时图像，动态
    def show_video(self):
        while True:
            self.image()
            # global n1_y
            pre = pygame.mouse.get_pos()
            if 305 <= pre[0] <= 365 and 485 <= pre[1] <= 545:
                # screen.blit(mous1, (366, 504))
                screen.blit(mous1, (298, 478))
            # 显示图像
            pygame.display.flip()
            # 休眠一下
            time.sleep(SLEEP_TIME_LONG)
            if self.handleEvent():
                break

    # 监测退出事件
    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                cap.release()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and 305 <= event.pos[0] <= 365 and 485 <= event.pos[1] <= 545:
                self.show_image()

            # 拍照后再来一次
            elif event.type == pygame.MOUSEBUTTONDOWN and 235 <= event.pos[0] <= 411 and 382 <= event.pos[1] <= 419:
                self.show_video()

            # 拍照后退出进入游戏
            elif event.type == pygame.MOUSEBUTTONDOWN and 437 <= event.pos[0] <= 645 and 387 <= event.pos[1] <= 432:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                # os.system("python index.py")
                exit()

            # elif event.type == pygame.MOUSEBUTTONDOWN and 335 <= event.pos[0] <= 546 and 274 <= event.pos[1] <= 320:
            #     self.show_video()

    # 显示拍摄的图片,静态
    def show_image(self):
        self.image()
        # 创建实例对象，获取解析的人脸信息
        face = bd.Faceu()
        face.face_detection(self.image_msg)
        analytic_dict = face.face_detection(self.image_msg)
        if analytic_dict:
            igender = analytic_dict['gender']
            iage = analytic_dict['age']
            ibeauty = analytic_dict['beauty']

            if igender == 'male':
                igender = '男'
            else:
                igender = '女'

            # 在画布上写出信息
            TextFont = pygame.font.Font("my_font/font3.ttf", 30)
            infgander1 = TextFont.render('性别：'+igender, True, (255, 255, 255))
            infage1 = TextFont.render('年龄：'+str(iage), True, (255, 255, 255))
            infscore1 = TextFont.render('颜值：'+str(int(ibeauty)), True, (255, 255, 255))
            screen.blit(self.al, (137, 20))  # 显示信息背景图片
            screen.blit(infgander1, (220, 124))
            screen.blit(infage1, (220, 222))
            screen.blit(infscore1, (220, 320))
            pygame.display.update()
        else:
            screen.blit(nopeople, (802, 141))
            TextFont = pygame.font.Font("my_font/font3.ttf", 34)
            war = TextFont.render('未识别到人像', True, (255, 255, 255))
            screen.blit(war, (885, 340))
            TextFont = pygame.font.Font("my_font/font3.ttf", 30)
            war1 = TextFont.render('重新扫描', True, (255, 255, 255))
            screen.blit(war1, (925, 430))
        while True:
            # 显示图像
            pygame.display.flip()
            self.handleEvent()

take = take_photo()
take.show_video()
