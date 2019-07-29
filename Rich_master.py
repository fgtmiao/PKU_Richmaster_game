import pygame
import sys
import random
import time

# TODO:
# add music
# 加入新的gamestate:显示玩家拥有的信息和建筑物信息
# 显示电脑损失钱数

#player's dict_val
size = (1080,600)
screen=pygame.display.set_mode(size)
class Building():
    def __init__(self,name,price,payment,location):
        self.name = name
        self.price = price
        self.payment = payment
        self.location = location
        self.wasBought = False                  #  是否被购买
        self.updated_time = 0                   #  被更新重建的次数
        self.owner = 'no'

class Player():
    #判断在哪个建筑中
    def judge_building(self,buildings):
        for building in buildings:
            for pos in building.location:
                if self.position==pos:
                    return building

    def __init__(self, image ,name , isPlayer):
         self.name=name
         self.money = 6000
         self.image=image
         self.position=0
         self.dice_val=0
         self.isPlayer=isPlayer
         self.showtext=[]
         self.ownedBuildings = []
         self.located_building=Building("",0,0,range(2))
         self.state_owned=0         # 表示状态：0为正常，1为破坏王T大附体，2为学霸附体不扣，3为圈地运动是我的了，4为厄运的眷顾

    def show_state(self):
    	for i in range(len(self.ownedBuildings)):
        	print(self.name,self.ownedBuildings[i].name)




    #购买中出现了问题
    def buy_building(self,ispressYES):
        if ispressYES and self.located_building.owner!=self.name:
            self.located_building.owner=self.name
            self.located_building.wasBought=True
            self.ownedBuildings.append(self.located_building)
            self.money-=self.located_building.price
            if self.isPlayer:
                self.showtext=[self.name+"拥有了"+self.located_building.name,'请结束你的回合，给其他同学一个机会']
            else:
                building=self.located_building
                textLine0 = self.name +'扔出了' + '%d'% self.dice_val + '点！'
                textLine1 = self.name +'来到了' + building.name + '!'
                textLine2 = '占领代价：%d' % building.price
                textLine3 = '过路收分：%d' % building.payment
                textline4 = self.name+"拥有了"+self.located_building.name
                textline5 = self.name+'正在结束回合'
                self.showtext = [textLine0,textLine1,textLine2,textLine3,textline4,textline5]
            return True
        #修改了这里
        elif ispressYES==False and self.located_building.owner!=self.name:
            self.showtext=[self.name+"没有买"+self.located_building.name,'请结束你的回合，给其他同学一个机会']
            return False
        else:
            self.showtext=['wrong when buying building']
            return False

    def update_building(self,ispressYES):
        if ispressYES and self.located_building.owner==self.name:
            #print(self.name+"updating"+self.located_building.name)
            self.located_building.updated_time+=1
            #修改
            self.money-=100
            self.showtext=[self.name+"升级了"+self.located_building.name,"现在它的收费是"+str(self.located_building.payment+self.located_building.updated_time*50),'请结束你的回合，给其他同学一个机会']
            return True
            
        elif ispressYES==False and self.located_building.owner==self.name:
            self.showtext=[self.name+"没升级它的"+self.located_building.name,"它的收费还是"+str(self.located_building.payment+self.located_building.updated_time*50),'请结束你的回合，给其他同学一个机会']            
            return False

        else:
            return False

    #这里的返回值是判断是否显示选择对话框，python貌似支持函数的多态
    def move_on(self,buildings,allplayers,dict_v):
        self.dice_val=dict_v
        self.position=(self.position+self.dice_val)%24#map_length

        self.located_building=self.judge_building(buildings)
        
        print(self.name+'now is at',self.position)
        return self.event_in_pos(allplayers)

    def event_in_pos(self,allplayers):
        building=self.located_building
        if building.name!='奇遇':
            if building.wasBought==False:#显示建筑信息
                if self.isPlayer==True:
                    textLine0 = self.name +'扔出了' + '%d'% self.dice_val + '点！'
                    textLine1 = self.name +'来到了' + building.name + '!'
                    textLine2 = '占领代价：%d' % building.price
                    textLine3 = '过路收分：%d' % building.payment
                    textLine4 = '是否购买？'
                    self.showtext = [textLine0,textLine1,textLine2,textLine3,textLine4]

                    return True
                else:
                    self.buy_building(True)
            elif building.owner==self.name:
                #选择update建筑
                print("building is：",building.owner)
                if self.state_owned==1:     #T大附体！破坏
                    textLine0 = self.name + 'T大附体！(╯‵□′)╯︵┻━┻ '
                    textLine1 = '摧毁了自己的'+building.name
                    textLine2 = '我不做人啦！'
                    building.owner = 'no'
                    building.wasBought = False
                    building.updated_time=0
                    self.state_owned=0
                    self.showtext = [textLine0,textLine1,textLine2]

                else:
                    if self.isPlayer==True:
                        textLine0 = self.name + '扔出了' + '%d'% self.dice_val + '点！'
                        textLine1 = '来到了ta的'+ building.name +'!'
                        textLine2 = '可以建设'+building.name 
                        textLine3 = '加盖收费：100'
                        textLine4 = '是否加盖？'
                        self.showtext = [textLine0,textLine1,textLine2,textLine3,textLine4]
                        return True
                    else:
                        self.update_building(False)
            #来到别人的地盘，要交税嗷
            #TODO:find BUG here
            else:
                for player in allplayers:
                    if self.located_building.owner==player.name and player.name!=self.name:
                        if self.state_owned==2:#学霸附体，不扣除GPA
                            textLine0 = self.name + '学霸附体！'
                            textLine1 = '免除扣分%d！' % (building.payment + building.updated_time*50) #扣除钱数#update_money_get
                            self.showtext = [textLine0,textLine1]
                            self.state_owned=0

                        elif self.state_owned==3:
                            textLine0 = self.name + '发起世一大建设运动！'
                            textLine1 = '你的'+building.name+'真棒！'
                            textLine2 = player.name+'的'+building.name + '现在由'+ self.name+'建设！'
                            self.showtext=[textLine0,textLine1,textLine2]
                            self.located_building.owner=self.name
                            self.state_owned=0

                        elif self.state_owned==1:
                            textLine0 = self.name + 'T大附体！(╯‵□′)╯︵┻━┻ '
                            textLine1 = '摧毁了%s的'%building.owner+building.name+'!'
                            textLine2 = '我不做人啦！'
                            self.showtext = [textLine0,textLine1,textLine2]
                            building.owner='no'
                            building.wasBought=False
                            self.state_owned=0
                        #正常状态要被扣分了
                        else:
                            textLine0 = self.name + '扔出了' + '%d'% self.dice_val + '点！'
                            textLine1 = self.name+ '来到了'+ player.name+'的:'+ building.name
                            textLine2 = '你的分很香，但现在是我的啦!'
                            koufen=building.payment+building.updated_time*50#update_money_get
                            if self.state_owned==4:
                                koufen*=2
                                textLine2+='\n哦，厄运的眷顾，双倍扣分！'
                                self.state_owned=0
                            textLine3=self.name+"被扣分%d,so sad!"%koufen
                            #textLine4=self.name+'结束你的回合吧！'
                            self.showtext = [textLine0,textLine1,textLine2,textLine3]
                            self.money-=koufen
                            player.money+=koufen
                        self.showtext.append("请结束你的回合")
        
        #如果是奇遇点，就是获得状态
        else:
            if self.state_owned==0:
                state_get=random.randint(1,4)
                self.state_owned=state_get
                if state_get==1:
                    textLine2="T大的诱惑！"
                    textLine3="下一次摧毁一个地点！"
                elif state_get==2:
                    textLine2='学霸附体！'
                    textLine3="免于下一次扣分！学霸好兄弟"
                elif state_get==3:
                    textLine2='世一大建设卡来了！'
                    textLine3='下一个别人的地盘就给你建设了！'
                elif state_get==4:
                    textLine2='哦，厄运眷顾了你~'
                    textLine3='下次被扣分翻倍，路途多艰'
                textLine0=self.name +'扔出了' +'%d'% self.dice_val + '点！'
                textLine1='来到了奇遇地点！'
                textLine4=self.name+'结束你的回合吧！'
            self.showtext=[textLine0,textLine1,textLine2,textLine3,textLine4]
        #print(self.showtext)

#中心位置我佛了...
class Button(object):
    def __init__(self,before,after,position):
        #self.before=pygame.image.load(before).convert_alpha()
        #self.after=pygame.image.load(after).convert_alpha()
        self.before=before.convert_alpha()
        self.after=after.convert_alpha()
        self.position=position

    def isOver(self):
        point_x,point_y=pygame.mouse.get_pos()
        x,y=self.position
        w,h=self.before.get_size()
        #print('1:',x,y)
        #print('2:',w,h)
        in_x=x- w/2<point_x and point_x<x+ w/2
        in_y=y- h/2<point_y and point_y<y+ h/2
        return in_x and in_y

    def render(self):
        w,h=self.before.get_size()
        x,y=self.position

        if self.isOver():
            screen.blit(self.after,(x-w/2,y-h/2))
        else:
            screen.blit(self.before,(x-w/2,y-h/2))

#带透明度的绘制
def blit_alpha(target,source,location,opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(),source.get_height())).convert()
    temp.blit(target , (-x , -y))
    temp.blit(source,(0,0))
    temp.set_alpha(opacity)
    target.blit(temp,location)

#返回下一个玩家是哪个（index，player）
def update_player(allplayers,tmp_player_idx,all_player_num):
    player_idx=(tmp_player_idx+1)%all_player_num
    return allplayers[player_idx],player_idx


#进入游戏->选择开始游戏人数"1 2 3 4"->如果是4就直接进入游戏->选择电脑人数''->开始游戏
#screen.bilt是显示？
#blit.alpha是透明度的显示？
def main():
    pygame.init()
    clock=pygame.time.Clock()

    #游戏人物
    player_num=1
    silyAI_num=0
    all_player_num=0
    
    #屏幕初始化
    pygame.display.set_caption("P大版大富翁")
    #音乐初始化
    bgm = pygame.mixer.music.load("assets\\bgms\\gamebgm.mp3")
    pygame.mixer.music.play(100)
    #for pos to display pics-8,-10
    Gameposx=[227, 302, 362, 427, 482, 552, 612, 682, 682, 682, 682, 682, 682, 612, 552, 482, 427, 362, 302, 227, 227, 227, 227, 227]
    Gameposy=[135, 135, 135, 135, 135, 135, 135, 135, 205, 260, 320, 380, 450, 450, 450, 450, 450, 450, 450, 450, 380, 320, 260, 205]
    playerbiasx=[-5,-5,5,5]
    playerbiasy=[-5,5,5,-5]

    textColorInMessageBox = (141,146,152)
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    #for font
    fontss=pygame.font.Font('assets\\font\\myfont.ttf',20)
    fonts=pygame.font.Font('assets\\font\\myfont.ttf',30)
    fontb=pygame.font.Font('assets\\font\\myfont.ttf',40)
    #for first
    print("begin load asserts")
    bgAD='assets\\imgs\\background.jpg'
    start1AD=pygame.image.load('assets\\imgs\\start1.png')
    start2AD=pygame.image.load('assets\\imgs\\start2.png')
    staff1AD=pygame.image.load('assets\\imgs\\staff1.png')
    staff2AD=pygame.image.load('assets\\imgs\\staff2.png')
    bg=pygame.image.load(bgAD)
    mymap=pygame.image.load('assets\\imgs\\map.jpg')
    #换用isOver判断？

    #for game
    bigdice_image = pygame.image.load("assets\\imgs\\dice.png").convert_alpha()
    dice_1 = pygame.image.load("assets\\imgs\\dice_1.png")
    dice_2 = pygame.image.load("assets\\imgs\\dice_2.png")
    dice_3 = pygame.image.load("assets\\imgs\\dice_3.png")
    dice_4 = pygame.image.load("assets\\imgs\\dice_4.png")
    dice_5 = pygame.image.load("assets\\imgs\\dice_5.png")
    dice_6 = pygame.image.load("assets\\imgs\\dice_6.png")
    diceimgs=[dice_1,dice_2,dice_3,dice_4,dice_5,dice_6]


    textbox=pygame.image.load("assets\\imgs\\textbg.png")
    showbox=pygame.image.load("assets\\imgs\\showbox.png")
    dices = [dice_1,dice_2,dice_3,dice_4,dice_5,dice_6]
    #add one
    #for judge
    yes1 = pygame.image.load("assets\\imgs\\yes1.png")
    yes2 = pygame.image.load("assets\\imgs\\yes2.png")
    no1 = pygame.image.load("assets\\imgs\\no1.png")
    no2 = pygame.image.load("assets\\imgs\\no2.png")



    turnover = pygame.image.load("assets\\imgs\\turnover.png")
    turnover2=pygame.image.load("assets\\imgs\\turnover2.png")
    
    #for state    
    shuaishen = pygame.image.load("assets\\imgs\\shuaishen.png").convert_alpha()
    tudishen = pygame.image.load("assets\\imgs\\tudishen.png").convert_alpha()
    caishen = pygame.image.load("assets\\imgs\\caishen.png").convert_alpha()
    pohuaishen = pygame.image.load("assets\\imgs\\pohuaishen.png").convert_alpha()    


    #for player
    player1_img= pygame.image.load("assets\\imgs\\player1.png")
    player2_img= pygame.image.load("assets\\imgs\\player2.png")
    player3_img= pygame.image.load("assets\\imgs\\player3.png")
    player4_img= pygame.image.load("assets\\imgs\\player4.png")
    
    AI1_img=pygame.image.load("assets\\imgs\\AI1.png")
    AI2_img=pygame.image.load("assets\\imgs\\AI2.png")
    AI3_img=pygame.image.load("assets\\imgs\\AI3.png")
    AI4_img=pygame.image.load("assets\\imgs\\AI4.png")
    player_number_0_img=pygame.image.load("assets\\imgs\\op0.png")
    player_number_1_img=pygame.image.load("assets\\imgs\\op1.png")
    player_number_2_img=pygame.image.load("assets\\imgs\\op2.png")
    player_number_3_img=pygame.image.load("assets\\imgs\\op3.png")
    player_number_4_img=pygame.image.load("assets\\imgs\\op4.png")


    #选人机/看staff返回上一级
    return_start_image=pygame.image.load("assets\\imgs\\return.png")
    return_start_way="assets\\imgs\\return.png"
    #TODO:load musics
    print("begin set rect")

    #给图片加入rect就算是触发器了（真...方便
    bigdice_rect = bigdice_image.get_rect()
    bigdice_rect.left , bigdice_rect.top = 50 , 450

    yes_rect = yes1.get_rect()
    yes_rect.left , yes_rect.top = 400,350 
    ynw,ynh = yes1.get_size()
    yes_btn_pos=(yes_rect.left+ynw/2, yes_rect.top+ynh/2)
    no_rect = no1.get_rect()
    no_rect.left , no_rect.top =  500,350
    no_btn_pos=(no_rect.left+ynw/2 , no_rect.top+ynh/2)
    yess=Button(yes1,yes2,yes_btn_pos)
    noo =Button(no1,no2,no_btn_pos)

    player_rect=[]
    player_rect.append(player_number_1_img.get_rect())
    player_rect.append(player_number_2_img.get_rect())
    player_rect.append(player_number_3_img.get_rect())
    player_rect.append(player_number_4_img.get_rect())
    for i in range(4):#到4
        player_rect[i].left,player_rect[i].top=i*200+100,400

    AI_rect=[]
    AI_rect.append(player_number_0_img.get_rect())
    AI_rect.append(player_number_1_img.get_rect())
    AI_rect.append(player_number_2_img.get_rect())
    AI_rect.append(player_number_3_img.get_rect())
    for i in range(4):
        AI_rect[i].left,AI_rect[i].top=i*200+100,400
    
    return_rect=return_start_image.get_rect()
    return_rect.left,return_rect.top=900,400
    return_alpha=190
    #回合结束按钮
    turnover_rect = turnover.get_rect()
    turnover_rect.left , turnover_rect.top = 800,485

    #在display的时间，所有按钮失效



    qiyu    =Building("奇遇",1000,400,[0])
    yijiao 	=Building("一教",1000,100,[1,2])
    weiming	=Building("未名湖",300,100,[3,4,5])
    boya  	=Building("博雅塔",1000,300,[6,7])
    erjiao  =Building("二教",1000,300,[8,9,10])
    sanjiao =Building("三教",500,200,[11])
    nongyuan=Building("农园",1000,200,[12,13])
    lijiao	=Building("理教",1000,200,[14,15])
    shaoyuan=Building("勺园",1000,300,[16,17])
    
    baijiang=Building("百讲",1000,200,[18,19])
    tushu   =Building("图书馆",1000,300,[20,21])
    xueyi  	=Building("学一",1000,300,[22,23])


    buildings=[
    qiyu   ,
    yijiao ,
    weiming,
    boya  	,
    erjiao ,
    sanjiao,
    nongyuan,
    lijiao	,
    shaoyuan,
    baijiang,
    tushu  ,
    xueyi  ]



    image_alpha = 255
    button_alpha=[]
    AI_button_alpha=[]

    for i in range(4):
        button_alpha.append(255)
    for i in range(4):
        AI_button_alpha.append(255)
    #0为选择玩家人数，1为选择电脑人数，2为进入正式的游戏界面
    
    
    plimgs=[player1_img,player2_img,player3_img,player4_img]
    plnames=["杰尼龟","可达鸭","蒜头王八","电耗子"]
    AIimgs=[AI1_img,AI2_img,AI3_img,AI4_img]
    #开始实例化
    allplayers=[]
    Game_state=-1#表示游戏进行到哪个界面了
    
    #TODO:BGM set
    #pygame.mixer.music.play(100)  



    #游戏中的变量

    Running=True

    #这里不需要了似乎
    display_tmp_pics=False#打印showtext的状态
    dict_var=0
    #记录退出时的状态，谁赢了或者谁输了
    exit_state=0
    player_now_idx = 0
    press_down_dict_time=0#按下色子的标识符号，为了避免按下时在色子上，离开时在别处？
    added_players=False


    show_text_head=''
    #显示玩家的选择界面
    begin_judge=False

    #玩家的选择,防止直接退出
    choose_yes=False
    choose_no=False

    #是否计算过了，计算过了就可以结束了
    moveon_caled=False
    #玩家更新过了
    player_mode_updated=False

    #按色子中
    player_pressing_dice=False
    #摇过色子了
    player_has_pressed_dict=False
    #按下结束回合
    player_pressed_over=False

    showturnover2=False
    AI_hold_time=0
    start=Button(start1AD,start2AD,(400,320))
    staff=Button(staff1AD,staff2AD,(650,320))
    print("run start")


    AI_showtxt=False
    AI_showcnt=0

    show_player_statue=False
    
    show_player_img1=pygame.image.load("assets\\imgs\\seetmp1.png")
    show_player_img2=pygame.image.load("assets\\imgs\\seetmp2.png")
    show_player_rect=show_player_img1.get_rect()
    spw,sph=show_player_img1.get_size()
    show_player_rect.left,show_player_rect.top=800,0
    show_player_pos=(800+spw/2,0+sph/2)
    show_player_btn=Button(show_player_img1,show_player_img2,show_player_pos)


    fanhui_img1=pygame.image.load("assets\\imgs\\fanhui1.png")
    fanhui_img2=pygame.image.load("assets\\imgs\\fanhui2.png")
    fanhui_rect=fanhui_img1.get_rect()
    fhw,fhh=fanhui_img1.get_size()
    fanhui_rect.left,fanhui_rect.top=500,500
    fanhui_pos=(500+fhw/2,500+fhh/2)
    fanhui_btn=Button(fanhui_img1,fanhui_img2,fanhui_pos)


    game_end_player_state=[]

    while Running:
    	#为了能让人接着玩真麻烦
        if Game_state==-1:

        	#这里不需要了似乎
        	display_tmp_pics=False#打印showtext的状态
        	dict_var=0
        	#记录退出时的状态，谁赢了或者谁输了
        	exit_state=0
        	player_now_idx = 0
        	press_down_dict_time=0#按下色子的标识符号，为了避免按下时在色子上，离开时在别处？
        	added_players=False
        	show_text_head=''
        	#显示玩家的选择界面
        	begin_judge=False
        	#玩家的选择,防止直接退出
        	choose_yes=False
        	choose_no=False
        	#是否计算过了，计算过了就可以结束了
        	moveon_caled=False
        	#玩家更新过了
        	player_mode_updated=False
        	#按色子中
        	player_pressing_dice=False
        	#摇过色子了
        	player_has_pressed_dict=False
        	#按下结束回合
        	player_pressed_over=False
        	showturnover2=False
        	AI_hold_time=0
        	start=Button(start1AD,start2AD,(400,320))
        	staff=Button(staff1AD,staff2AD,(650,320))
        	AI_showtxt=False
        	AI_showcnt=0
        	game_end_player_state=[]





        	screen.blit(bg,(0,0))
        	start.render()
        	staff.render()
        	game_end_player_state.clear()
        	for event in pygame.event.get():
        		if event.type == pygame.QUIT:
        			sys.exit()  
        		if event.type==pygame.MOUSEBUTTONDOWN:
        			if start.isOver():
        				Game_state=0
        			elif staff.isOver():
        				Game_state=-2


        elif Game_state==-2:

        	screen.blit(bg,(0,0))
        	screen.blit(textbox,(240,200))
        	text1=fonts.render("开发人员：李世龙、林丽琪、唐航",True,black,20)
        	text2=fonts.render("				陈印华、黄钰翔、欧夏娴",True,black,20)
        	text3=fonts.render("联系我们：1922903760@qq.com",True,black,20)
        	screen.blit(text1,(300,300))
        	screen.blit(text2,(300,350))
        	screen.blit(text3,(300,400))
        	blit_alpha(screen,return_start_image,(900,400),return_alpha)
        	for event in pygame.event.get():
        		if event.type == pygame.QUIT:
        			sys.exit()              #干净的退出
        		if event.type == pygame.MOUSEMOTION:
        			if return_rect.collidepoint(event.pos):
        				return_alpha=255
        			else:
        				return_alpha=190        			
        		if event.type==pygame.MOUSEBUTTONDOWN:
        			if return_rect.collidepoint(event.pos):
        				Game_state=-1
        				break


        
        #游戏开始之前选择玩家人数界面
        elif Game_state==0:
        	player_num=0
        	silyAI_num=0
        	#如果是空的话会不会出问题？vector...
        	allplayers.clear()
        	for event in pygame.event.get():
        		if event.type == pygame.QUIT:
        			sys.exit()              #干净的退出
        	    
        	    #玩家数目按钮高亮
        		if event.type == pygame.MOUSEMOTION:
        			for i in range(4):
        				if player_rect[i].collidepoint(event.pos):
        					button_alpha[i]=255
        				else:
        					button_alpha[i]=190
        	    
        	    #点击就送
        		if event.type == pygame.MOUSEBUTTONDOWN:
        		    #start a music?
        			for i in range(4):
        				if player_rect[i].collidepoint(event.pos):
        					player_num=i+1
        					if player_num==4:           #达到人数上限，直接开始
        						all_player_num=player_num
        						silyAI_num=0
        						Game_state=2
        						break
        					else:
        						Game_state=1
        						break

        	screen.blit(bg,(0,0))            #start pic and pos
        	btn_img_list=[player_number_1_img,player_number_2_img,player_number_3_img,player_number_4_img]
        	text1=fontb.render("请选择玩家人数：",True,red,50)
        	screen.blit(text1,(50,150))
        	for i in range(4):
        		blit_alpha(screen,btn_img_list[i],(100+200*i,400),button_alpha[i])



        #选择电脑人数
        elif Game_state==1:
       		btn_img_list=[player_number_0_img,player_number_1_img,player_number_2_img,player_number_3_img,player_number_4_img]
        	screen.blit(bg,(0,0))
        	text1=fontb.render("请选择AI人数：",True,black,50)
        	screen.blit(text1,(50,150))
        	blit_alpha(screen,return_start_image,(900,400),return_alpha)
        	if player_num==1:
        		for i in range(1,4):
        			blit_alpha(screen,btn_img_list[i],(100+200*i,400),AI_button_alpha[i])
        	else:
        		for i in range(5-player_num):
        			blit_alpha(screen,btn_img_list[i],(100+200*i,400),AI_button_alpha[i])
        	for event in pygame.event.get():
        		if event.type == pygame.QUIT:
        			sys.exit()              #干净的退出

        		if event.type == pygame.MOUSEMOTION:
        			#只显示这些
        			if return_rect.collidepoint(event.pos):
        				return_alpha=255
        			else:
        				return_alpha=190
        			if player_num==1:
        				for i in range(1,4):
        					if AI_rect[i].collidepoint(event.pos):
        						AI_button_alpha[i]=255
        					else:
        						AI_button_alpha[i]=190
        			else:
        				for i in range(5-player_num):
        					if AI_rect[i].collidepoint(event.pos):
        						AI_button_alpha[i]=255
        					else:
        						AI_button_alpha[i]=190
                
        		if event.type == pygame.MOUSEBUTTONDOWN:
        			if return_rect.collidepoint(event.pos):
        				Game_state=0
        				break
        			print(player_num)
        			iscolide=False
        			if player_num==1:
        				for i in range(1,4):#123
        					if AI_rect[i].collidepoint(event.pos):
        						iscolide=True
        						silyAI_num=i
        						all_player_num=player_num+silyAI_num
        			else:
        				for i in range(5-player_num):#012...
        					if AI_rect[i].collidepoint(event.pos):
        						iscolide=True
        						silyAI_num=i
        						all_player_num=player_num+silyAI_num
        			print(silyAI_num)
        			if iscolide:
	        			Game_state=2
	        			break
        
        
        
        #每一个回合：判断当前是不是电脑->
        #是电脑->电脑random6 move+触发事件->show事件->对外界操作屏蔽且不亮+事件结束后自动更新玩家序列
        #好像不用判断...while本身就可以等待woc
        elif Game_state==2:
            if not added_players:
                for i in range(player_num):
                    allplayers.append(Player(plimgs[i],plnames[i],True))
                for i in range(silyAI_num):
                    allplayers.append(Player(AIimgs[i],"naiveAI"+str(i+1),False))
                added_players=True

            tmp_player=allplayers[player_now_idx]
            screen.blit(mymap,(0,0))
            showbox_pos=(310,210)
            screen.blit(showbox,showbox_pos)
            blit_alpha(screen,bigdice_image,(50,450),image_alpha)#色子透明度
            #show_player_btn.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                	sys.exit() 

                if tmp_player.isPlayer:
                    if event.type == pygame.MOUSEMOTION and player_has_pressed_dict==False and not show_player_statue:
                        if bigdice_rect.collidepoint(event.pos):
                            image_alpha = 255   
                        else:
                            image_alpha = 190
                    #优先级最高的显示
                    if event.type == pygame.MOUSEBUTTONDOWN and show_player_rect.collidepoint(event.pos):
                        show_player_statue=True


                    if event.type == pygame.MOUSEBUTTONDOWN and bigdice_rect.collidepoint(event.pos)\
                     and player_pressing_dice==False and player_has_pressed_dict==False and not show_player_statue:#按色子的持续时间
                        player_pressing_dice=True
                    #按色子抬起
                    if event.type == pygame.MOUSEBUTTONUP and press_down_dict_time!=0 and player_has_pressed_dict==False and not show_player_statue:                     
                        dict_var=(press_down_dict_time*13+random.randint(1,6))%6+1
                        press_down_dict_time=0
                        player_pressing_dice=False
                        player_has_pressed_dict=True



                    if event.type == pygame.MOUSEBUTTONDOWN and turnover_rect.collidepoint(event.pos) and player_has_pressed_dict and player_mode_updated and not show_player_statue:
                    	showturnover2=True
                    	dict_var=0
                    	player_has_pressed_dict=False
                    	player_mode_updated=False
                    	moveon_caled=False

                    #begin choose
                    if event.type == pygame.MOUSEBUTTONDOWN and begin_judge and yes_rect.collidepoint(event.pos) and not show_player_statue:
                        choose_yes=True
                        begin_judge=False

                    if event.type == pygame.MOUSEBUTTONDOWN and begin_judge and no_rect.collidepoint(event.pos) and not show_player_statue:
                        choose_no=True
                        begin_judge=False



                    #end the turn
                    if event.type == pygame.MOUSEBUTTONUP and showturnover2 and not show_player_statue:
                    	showturnover2=False
                    	player_pressed_over=True


                #elif tmp_player.isPlayer==False:
                #	showtext='现在是AI的回合'


            if player_pressing_dice:
            	press_down_dict_time+=1
            if player_has_pressed_dict:
            	screen.blit(diceimgs[dict_var-1],(50,50))

            if showturnover2:
            	screen.blit(turnover2,(800,485))
            else:
            	screen.blit(turnover,(800,485))

            if tmp_player.isPlayer:
                if player_mode_updated==False and dict_var==0:
                    tmp_player.showtext=['现在是'+tmp_player.name+'建设世一大的时间',tmp_player.name+"请摇色子！"]
                    #print(showtext)

                #加锁限制begin judge的变化
                elif player_mode_updated==False:
                    if moveon_caled==False:
                    	begin_judge=tmp_player.move_on(buildings,allplayers,dict_var)
                    	tmp_player.show_state()
                    	moveon_caled=True
                    
                    #选择界面
                    if begin_judge:
                        yess.render()
                        noo.render()

                    #修改,是这里的问题
                    elif choose_yes:
                        if tmp_player.located_building.owner!=tmp_player.name:
                            tmp_player.buy_building(True)
                        else:
                            tmp_player.update_building(True)
                        choose_yes=False
                    elif choose_no:
                        #此处出错
                        if tmp_player.located_building.owner!=tmp_player.name:
                            tmp_player.buy_building(False)
                        else:
                            tmp_player.update_building(False)
                        choose_no=False
                    
                    #无需选择
                    else:
                        player_mode_updated=True
                
                #玩家按下了结束按钮
                if player_pressed_over:
                    tmp_player,player_now_idx=update_player(allplayers,player_now_idx,all_player_num)
                    player_pressed_over=False

                for i in range(len(tmp_player.showtext)):
                	text1=fontss.render(tmp_player.showtext[i],True,black,15)
                	screen.blit(text1,(310,230+20*i))


            elif tmp_player.isPlayer==False:
            	if AI_showtxt==False:
                    tmp_player.move_on(buildings,allplayers,random.randint(1,6))
                    AI_showtxt=True

            	if AI_showtxt:
                    AI_showcnt+=1
                    show_text_head="现在是"+allplayers[player_now_idx].name+"建设世一大的时间！"
                    text1=fontss.render(show_text_head,True,black,15)
                    screen.blit(text1,(310,210))
                    for i in range(len(tmp_player.showtext)):
                    	text1=fontss.render(tmp_player.showtext[i],True,black,15)
                    	screen.blit(text1,(310,230+20*i))

            	if AI_showcnt==400:
                	AI_showcnt=0
                	AI_showtxt=False
                	tmp_player,player_now_idx=update_player(allplayers,player_now_idx,all_player_num)

            #display player pos
            for i in range(len(allplayers)):
            	screen.blit(allplayers[i].image,(Gameposx[allplayers[i].position]+playerbiasx[i],Gameposy[allplayers[i].position]+playerbiasy[i]))
            #print money:
            for i in range(len(allplayers)):
            	player_mes=fonts.render(allplayers[i].name+':',True,black)
            	money_mes =fonts.render(str(allplayers[i].money),True,black)
            	screen.blit(player_mes,(800,50+30*i))
            	screen.blit(money_mes,(950,50+30*i))

            for each in allplayers:
                #懒得查sort了
                if each.money<=0:
                	searched=[]
                	for i in range(len(allplayers)):
                		print()
                		minn=10000
                		tmp=0
                		for j in range(len(allplayers)):
                			if(allplayers[j].money<minn and j not in searched):
                				tmp=j
                				minn=allplayers[j].money
                		searched.append(tmp)
                		game_end_player_state.append(allplayers[tmp])
                		print(allplayers[tmp].name)
                	Game_state=3

        elif Game_state==3:
        	screen.blit(bg,(0,0))
        	screen.blit(textbox,(240,200))
        	blit_alpha(screen,return_start_image,(900,400),return_alpha)
        	txts=[]
        	txts.append('游戏结束！但世一大建设还在继续！')
        	txts.append('无法继续建设的为'+game_end_player_state[0].name)
        	txts.append('其余排名为:')
        	for i in range(1,len(game_end_player_state)):
        		txts.append('第'+str(len(game_end_player_state)-i)+"名："+game_end_player_state[i].name)
        	for i in range(len(txts)):
        		text=fonts.render(txts[i],True,black,20)
        		screen.blit(text,(300,250+50*i))     	
        	for event in pygame.event.get():
        		if event.type == pygame.QUIT:
        			sys.exit()              #干净的退出
        		if event.type == pygame.MOUSEMOTION:
        			if return_rect.collidepoint(event.pos):
        				return_alpha=255
        			else:
        				return_alpha=190        			
        		if event.type==pygame.MOUSEBUTTONDOWN:
        			if return_rect.collidepoint(event.pos):
        				Game_state=-1
        				break


        pygame.display.flip()
        clock.tick(60)

main()      