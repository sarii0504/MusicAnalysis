# -*- coding: utf-8 -*-
import pygame
import sys
from pygame.locals import *
import pyaudio, wave
import time #为了给录音文件命名
import threading
from global_variable import *
import win32ui

print(flag)


#字符串资源列表
background_image_filename='./source/background.png'

button_readMidi_focus_filename='./source/button_readMidi_focus.png'
button_readMidi_hover_filename='./source/button_readMidi_hover.png'
button_readMidi_normal_filename='./source/button_readMidi_normal.png'

button_readWav_focus_filename='./source/button_readWav_focus.png'
button_readWav_hover_filename='./source/button_readWav_hover.png'
button_readWav_normal_filename='./source/button_readWav_normal.png'

button_record_end_focus_filename='./source/button_record_end_focus.png'
button_record_end_hover_filename='./source/button_record_end_hover.png'
button_record_end_normal_filename='./source/button_record_end_normal.png'

button_record_start_focus_filename='./source/button_record_start_focus.png'
button_record_start_hover_filename='./source/button_record_start_hover.png'
button_record_start_normal_filename='./source/button_record_start_normal.png'

button_score_focus_filename='./source/button_score_focus.png'
button_score_hover_filename='./source/button_score_hover.png'
button_score_normal_filename='./source/button_score_normal.png'

image_calculate_filename='./source/image_calculate.png'
image_recording_filename='./source/image_recording.png'
image_result_filename='./source/image_result.png'


pygame.init()
screen= pygame.display.set_mode((800,500))
pygame.display.set_caption('Music Analysis')
background_image = pygame.image.load(background_image_filename)#加载图片
calculate_image=pygame.image.load(image_calculate_filename)
recording_image=pygame.image.load(image_recording_filename)
result_image=pygame.image.load(image_result_filename)




FPS = 60


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORDING = False
#录音函数
def record_thread(fileName, stream, p):
    
    waveFile = wave.open(fileName, "wb")
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    while RECORDING:
        #print(stream.read(CHUNK))
        waveFile.writeframes(stream.read(CHUNK))
    waveFile.close()

def recordGenerator():#生成器
    global RECORDING
    RECORDING=False
    p=pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
        channels=CHANNELS, rate=RATE,
        input=True, frames_per_buffer=CHUNK)
            
    while 1:
        if flag==0:#非录制状
            return
        else:#开始录制
            RECORDING=True
            fileName=time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))+".wav"
            fileName='./record/'+fileName
            global wavFileName
            wavFileName=fileName
            t = threading.Thread(target=record_thread, args=(fileName, stream, p))
            t.setDaemon(True)
            t.start()
            return

class recordButton(object):#开始录音
    def __init__(self,button_record_end_focus_filename,button_record_end_hover_filename,button_record_end_normal_filename,button_record_start_focus_filename,button_record_start_hover_filename,button_record_start_normal_filename,position):
        self.imageEndFocus = pygame.image.load(button_record_end_focus_filename).convert_alpha()
        self.imageEndHover = pygame.image.load(button_record_end_hover_filename).convert_alpha()
        self.imageEndNormal = pygame.image.load(button_record_end_normal_filename).convert_alpha()
        self.imageStartFocus = pygame.image.load(button_record_start_focus_filename).convert_alpha()
        self.imageStartHover = pygame.image.load(button_record_start_hover_filename).convert_alpha()
        self.imageStartNormal = pygame.image.load(button_record_start_normal_filename).convert_alpha()
        self.position = position

    def isOver(self):
        point_x,point_y = pygame.mouse.get_pos()
        x, y = self. position
        w, h = self.imageEndFocus.get_size()
        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y
	
    def isPressed(self):#判断是否按下
        point_x,point_y=pygame.mouse.get_pos()
        x, y = self.position
        w, h = self.imageEndFocus.get_size()
        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2		
        click=pygame.mouse.get_pressed()
        return in_x and in_y and click[0]

	
    def render(self):#绘制
        global flag
        flag=flag
        w, h = self.imageEndFocus.get_size()
        x, y = self.position
        global end_record
        global clock#新建计时器
        global time_passed
        if self.isPressed():#按下
            if flag==0:#非录制状态->开始录制,文字：结束录制
                #self.record_button_flag=1
                flag=1
                clock=pygame.time.Clock()
                end_record=0
                global result
                result=0
                time_passed=0
                print('click')
                recordGenerator()
                print("test1")
                global midiFileName
                print(midiFileName)
                playMidi(midiFileName)
                screen.blit(self.imageEndFocus,(x-w/2,y-h/2))
            else:#录制状态->结束录制，文字：开始录制
                #self.record_button_flag=0
                flag=0
                end_record=1
               
                recordGenerator()
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.stop()
                screen.blit(self.imageStartFocus,(x-w/2,y-h/2))
        elif self.isOver():
            if flag==0:
                screen.blit(self.imageStartHover,(x-w/2,y-h/2))
            else:#录制状态
                screen.blit(self.imageEndHover,(x-w/2,y-h/2))
                screen.blit(recording_image,(300,200))
                font=pygame.font.SysFont('arial',50)
                time_passed=time_passed+clock.tick()
                temp=("%.2f" % (time_passed/1000))
                text_surface=font.render(str(temp),True,(0,0,0),None)
                screen.blit(text_surface, (350,250)) 
        else:
            if flag==0:#非录制状态  
                screen.blit(self.imageStartNormal,(x-w/2,y-h/2))
            else:#录制状态
                screen.blit(self.imageEndNormal,(x-w/2,y-h/2))
                screen.blit(recording_image,(300,200))
                font=pygame.font.SysFont('arial',50)
                time_passed=time_passed+clock.tick()
                temp=("%.2f" % (time_passed/1000))
                text_surface=font.render(str(temp),True,(0,0,0),None)
                screen.blit(text_surface, (350,250)) 
record_button = recordButton(button_record_end_focus_filename,button_record_end_hover_filename,button_record_end_normal_filename,button_record_start_focus_filename,button_record_start_hover_filename,button_record_start_normal_filename,(100,180))

class readWavButton(object):#读取录音文件
    def __init__(self,imageFocus,imageHover,imageNormal,position): 
        self.imageFocus = pygame.image.load(imageFocus).convert_alpha()
        self.imageHover=pygame.image.load(imageHover).convert_alpha()
        self.imageNormal=pygame.image.load(imageNormal).convert_alpha()
        self.position = position
 
    def isOver(self):
        point_x,point_y = pygame.mouse.get_pos()
        x, y = self. position
        w, h = self.imageFocus.get_size()

        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y

    def isPressed(self):#判断是否按下
        point_x,point_y=pygame.mouse.get_pos()
        x, y = self.position
        w, h = self.imageFocus.get_size()
        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2		
        click=pygame.mouse.get_pressed()
        return in_x and in_y and click[0]
    
    def render(self):
        w, h = self.imageFocus.get_size()
        x, y = self.position
        if self.isPressed():
            screen.blit(self.imageFocus,(x-w/2,y-h/2))
        elif self.isOver():
            screen.blit(self.imageHover,(x-w/2,y-h/2))
        else:
            screen.blit(self.imageNormal,(x-w/2,y-h/2))
        if self.isPressed():
            dlg= win32ui.CreateFileDialog(1)# 1表示打开文件对话框  
            dlg.SetOFNInitialDir('C:/')# 设置打开文件对话框中的初始显示目录   
            dlg.DoModal()    
            filename= dlg.GetPathName()# 获取选择的文件名称
            global wavFileName
            wavFileName=filename
            global wavFile
            if wavFileName:
                wavFile=wave.open(filename,"rb")#获取wav文件		
                print("wavfilename")				
                print(filename)  
read_wav_button=readWavButton(button_readWav_focus_filename,button_readWav_hover_filename,button_readWav_normal_filename,(100,260))

class readMidiButton(object):#选择Midi文件
    def __init__(self,imageFocus,imageHover,imageNormal,position):
        self.imageFocus = pygame.image.load(imageFocus).convert_alpha()
        self.imageHover=pygame.image.load(imageHover).convert_alpha()
        self.imageNormal=pygame.image.load(imageNormal).convert_alpha()
        self.position = position
 
    def isOver(self):
        point_x,point_y = pygame.mouse.get_pos()
        x, y = self. position
        w, h = self.imageFocus.get_size()

        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y

    def isPressed(self):#判断是否按下
        point_x,point_y=pygame.mouse.get_pos()
        x, y = self.position
        w, h = self.imageFocus.get_size()
        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2		
        click=pygame.mouse.get_pressed()
        return in_x and in_y and click[0]
    
    def render(self):
        w, h = self.imageFocus.get_size()
        x, y = self.position
        if self.isPressed():
            screen.blit(self.imageFocus,(x-w/2,y-h/2))
        elif self.isOver():
            screen.blit(self.imageHover,(x-w/2,y-h/2))
        else:
            screen.blit(self.imageNormal,(x-w/2,y-h/2))
        if self.isPressed():
            dlg= win32ui.CreateFileDialog(1)# 1表示打开文件对话框  
            dlg.SetOFNInitialDir('C:/')# 设置打开文件对话框中的初始显示目录   
            dlg.DoModal()    
            filename= dlg.GetPathName()# 获取选择的文件名称
            global midiFileName#存储midi文件名称
            print(filename)
            midiFileName=filename
            if midiFileName:
                #midiFile=wave.open(filename,"rb")#获取midi文件
                #打开的midi文件
                
                
                
                print("midifilename")			
                print(filename)  
read_midi_button=readMidiButton(button_readMidi_focus_filename,button_readMidi_hover_filename,button_readMidi_normal_filename,(100,100))

class scoreButton(object):#计算得分
    def __init__(self,imageFocus,imageHover,imageNormal,position):
        self.imageFocus = pygame.image.load(imageFocus).convert_alpha()
        self.imageHover=pygame.image.load(imageHover).convert_alpha()
        self.imageNormal=pygame.image.load(imageNormal).convert_alpha()
        self.position = position
 
    def isOver(self):
        point_x,point_y = pygame.mouse.get_pos()
        x, y = self. position
        w, h = self.imageFocus.get_size()

        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y

    def isPressed(self):#判断是否按下
        point_x,point_y=pygame.mouse.get_pos()
        x, y = self.position
        w, h = self.imageFocus.get_size()
        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2		
        click=pygame.mouse.get_pressed()
        return in_x and in_y and click[0]
    
    def render(self):
        w, h = self.imageFocus.get_size()
        x, y = self.position
        global result_clock
        global time_passed2
        global _score
        if self.isPressed():
            screen.blit(self.imageFocus,(x-w/2,y-h/2))
        elif self.isOver():
            screen.blit(self.imageHover,(x-w/2,y-h/2))
        else:
            screen.blit(self.imageNormal,(x-w/2,y-h/2))
        if self.isPressed():
            _score=str(score())#调用计算得分的函数
            result_clock=pygame.time.Clock()#新建计时器
            global result
            result=1
            time_passed2=0
        if end_record==1 and result==1:
            time_passed2=time_passed2+result_clock.tick()
            #print(time_passed2)
            if(time_passed2/1000<5):
                screen.blit(calculate_image,(300,150))
                font=pygame.font.SysFont('arial',50)
                text_surface=font.render(str(5-int(time_passed2/1000)),True,(0,0,0),None)
                screen.blit(text_surface, (350,250)) 
            else:#经过5s之后
                #print("true")
                screen.blit(result_image,(300,150))
                font=pygame.font.SysFont('arial',50)
                text_surface=font.render(_score,True,(0,0,0),None)
                screen.blit(text_surface, (350,250))  

score_button=scoreButton(button_score_focus_filename,button_score_hover_filename,button_score_normal_filename,(100,340))


def score():







    return 88


pygame.mixer.init()  
# 设置及播放背景音乐  
pygame.mixer.music.set_volume(0.2)  # 设置音量  

def playMidi(fileName):  
    print(fileName)
    pygame.mixer.music.load(fileName)
    print("Music file %s loaded!" % fileName)
    pygame.mixer.music.play()

j=0
while True:#主循环
    for event in pygame.event.get():
        if event.type ==QUIT:
            pygame.quit()
            sys.exit()
    
    screen.blit(background_image,(0,0))#背景
    record_button.render()
    read_midi_button.render()
    read_wav_button.render()
    score_button.render()
    #pygame.draw.rect(screen,[255,0,0],[250,150,300,200],0)
    pygame.display.update()
    pygame.time.Clock().tick(FPS)