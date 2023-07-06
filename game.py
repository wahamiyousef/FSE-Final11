from pygame import *

#icon window
iconImg=image.load("images/icon.png")
display.set_caption("1v1 Arena")
display.set_icon(iconImg)

font.init()
width,height=800,450
screen=display.set_mode((width,height))
familyFont=font.SysFont("Arial",25)
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE = (255,255,255)

#variables
jumpSpeed=-20
gravity=1.5
ground=height
bottom=ground
playerSpeed=5
bullSpeed=5
rapid1=60
rapid2=60

X=0
Y=1
W=BOT=2
H=SX=3
ROW=4
COL=5
HP=6
SCORE=7
v=[0,0,bottom]
Ev=[0,0,bottom]

jump1=False
jump2=False


    #   x   y   w  h row col HP
player1=[ 50,320,30,40,0,0, 100,0]

player2=[750,320,30,40,0,0, 100,0]


bg1=image.load("images/bg1.png").convert() #level 1
bg2=image.load("images/bg2.png").convert() #level 2
picon1=image.load("images/picon1.png").convert_alpha() #player icon 1
picon2=image.load("images/picon2.png").convert_alpha() #player icon 2
Erock=image.load("anims/Erock.png").convert_alpha() #Enemy rock 
rock=image.load("anims/rock.png").convert_alpha() #player rock

backg=image.load("images/backg.png").convert() #background for menu,etc.

plats1=[Rect(40,225,180,10),Rect(320,265,180,10),Rect(600,230,180,10),Rect(235,305,60,10),Rect(225,385,60,10),Rect(140,345,60,10),Rect(500,310,60,10),Rect(470,405,60,10)]
plats2=[Rect(260,225,225,10),Rect(240,285,115,10),Rect(15,305,115,10),Rect(125,382,115,10),Rect(390,340,115,10),Rect(570,385,115,10),Rect(600,300,115,10)]

pups=[]

bullets=[]
Ebullets=[]


def drawScene(screen,player1,picList1,player2,picList2,bull1,bull2,bg):
    #screen.fill(0)
    
    #offset=v[SX]-player1[X]
    screen.blit(bg,(0,0))
    #for plat in plats:
        #plat=plat.move(offset,0)
        #draw.rect(screen,WHITE,plat)
    for b in bull1:
        brect1=Rect(b[X],b[Y],10,10)
        #draw.rect(screen,BLUE,brect1)
        screen.blit(rock,(brect1))
    for b in bull2:
        brect2=Rect(b[X],b[Y],10,10)
        #draw.rect(screen,RED,brect2)
        screen.blit(Erock,(brect2))

    #player 1's HP bar
    h1rect=Rect(50,50,player1[HP]*2,20)
    draw.rect(screen,RED,h1rect)
    draw.rect(screen,BLACK,Rect(50,50,200,20),2)
    screen.blit(picon1,(10,7))

    #player 2's HP bar
    h2rect=Rect(550,50,player2[HP]*2,20)
    draw.rect(screen,BLUE,h2rect)
    draw.rect(screen,BLACK,Rect(550,50,200,20),2)
    screen.blit(picon2,(730,7))

    #display score
    score=familyFont.render(str(player2[SCORE])+"                            "+str(player1[SCORE]),True,BLACK)
    screen.blit(score,(300,45))
        

    #player 1
    row1=player1[ROW]
    col1=int(player1[COL])
    pic1=picList1[row1][col1]

    screen.blit(pic1,([player1[0],player1[1],player1[2],player1[3]]))
    #draw.rect(screen,BLUE,[player1[0],player1[1],player1[2],player1[3]],2)

    #player 2
    row2=player2[ROW]
    col2=int(player2[COL])
    pic2=picList2[row2][col1]

    screen.blit(pic2,([player2[0],player2[1],player2[2],player2[3]]))
    #draw.rect(screen,RED,[player2[0],player2[1],player2[2],player2[3]],2)

    display.flip()

def addPics(name,start,end):
    mypics=[]
    for i in range(start,end+1):
        mypics.append(image.load("anims/%s%03d.png" %(name,i)))
    
    return mypics

#first player movement WASD
def movePlayer1(player,playerSpeed,bullSpeed):
    global jump1,rapid1

    keys=key.get_pressed() #get key inputs
    v[X]=0 #set X to 0

    if rapid1<60: #add until rapid1 is 60
        rapid1+=1

    if keys[K_e] and rapid1==60: #if rapid1 is 60 and hit E key
        bullets.append([player[X],player[Y],bullSpeed,bullSpeed]) #add bullet to list
        rapid1=0 #reset rapid1
    elif keys[K_q] and rapid1==60: #if rapid1 is 60 and hit Q key
        bullets.append([player[X],player[Y],-bullSpeed,bullSpeed]) #add bullet (with negative speed, goes Left) to list
        rapid1=0 #reset rapid1
    
    if keys[K_w] and v[Y]==0: #if w (to jump) and 0 Y velocity
        player[ROW]=3 #animate jump row
        v[Y]=jumpSpeed #jump player
        player[COL]=0 #set column to 0 to loop animation
        jump1=True #jumping is true

    elif keys[K_d] and player[X]<770: #go right
        if jump1==False: #if not jumping
            player[ROW]=1 #animate running right
        v[X]+=playerSpeed #add speed
        
    elif keys[K_a] and player[X]>0: #go left
        if jump1==False: #if not jumping
            player[ROW]=2 #animate running left
        v[X]-=playerSpeed #add speed (left)
        
    elif jump1==False: #if not jumping
        player[ROW]=0 #idle animation

    player[X]+=v[X] #moving L/R
    v[Y]+=gravity #adding gravity 

    #this loops animation
    player[COL]=player[COL]+0.2 #frames every 0.2 for animation
    if player[COL]>=7: #if column reaches index 7,
        player[COL]=0 #reset col to 0

    

#second player movement (IJKL)
def movePlayer2(player,playerSpeed,bullSpeed):
    global jump2,rapid2
    '''this function moves the player
    It also adjusts the "row" and "column" values
    to ensure the correct picture is drawn (in the drawScene function)
    '''
    keys=key.get_pressed()
    Ev[X]=0

    if rapid2<60: #add until rapid1 is 60
        rapid2+=1

    if keys[K_o] and rapid2==60: #if rapid1 is 60 and hit E key
        Ebullets.append([player[X],player[Y],bullSpeed,bullSpeed]) #add bullet to list
        rapid2=0 #reset rapid1
    elif keys[K_u] and rapid2==60: #if rapid1 is 60 and hit Q key
        Ebullets.append([player[X],player[Y],-bullSpeed,bullSpeed]) #add bullet (with negative speed, goes Left) to list
        rapid2=0 #reset rapid1
    
    if keys[K_i] and Ev[Y]==0:
        player[ROW]=3
        Ev[Y]=jumpSpeed
        player[COL]=0
        jump2=True

    elif keys[K_l] and player[X]<770: #go right
        if jump2==False:
            player[ROW]=1 #animate
        Ev[X]+=playerSpeed #add speed
        
    elif keys[K_j] and player[X]>0: #go left
        if jump2==False:
            player[ROW]=2
        Ev[X]-=playerSpeed
        
    elif jump2==False:
        player[ROW]=0 #idle animation

    player[X]+=Ev[X] #moving L/R
    Ev[Y]+=gravity #adding gravity 


    player[COL]=player[COL]+0.2 #frames every 0.2 for animation
    if player[COL]>=7:
        player[COL]=0
        

'''
def powerUps(player1,player2,pups):
    for pup in pups:
        if player1.colliderect(pup):
            v[X]=2
        if player2.colliderect(pup):
            Ev[X]=2
'''


def checkAttack(bull1,player1,bull2,player2): #check attack with bullets, players
    for b in bull1:
        brect1=Rect(b[0],b[1],10,10)
        p2=Rect(player2[X],player2[Y],player2[W],player2[H])
        if brect1.colliderect(p2):
            player2[HP]-=25
            bull1.remove(b)
            print("player 2 hit")
            break
        
    for b in bull2:
        brect=Rect(b[0],b[1],10,10)
        p1=Rect(player1[X],player1[Y],player1[W],player1[H])
        if brect.colliderect(p1):
            player1[HP]-=25
            bull2.remove(b)
            print("player 1 hit")
            break

def moveBullets(bull1,bull2): #moves bullets with coordinated values
    for b in bull1:
        b[0]+=b[2] #left/right
        #b[1]+=b[3] #up/down, which isnt needed
        if b[0]>800 or b[0]<0: #if out of screen
            bull1.remove(b) #delete bullet
    for b in bull2:
        b[0]+=b[2] #left/right
        #b[1]+=b[3] #up/down, which isnt needed
        if b[0]>800 or b[0]<0: #if out of screen
            bull2.remove(b) #delete bullet


def checkScore(player1,player2): #check the players score
    hp1=player1[HP]# set variables 
    hp2=player2[HP]
    if hp1<=0: #if hp reaches 0
        player1[SCORE]+=1 #add score
        player1[HP]=100 #reset position, and HP back to full health
        player2[HP]=100 
        player1[X]=50
        player1[Y]=320
        player2[X]=750
        player2[Y]=320
    if hp2<=0:
        player2[SCORE]+=1
        player1[HP]=100
        player2[HP]=100
        player1[X]=50
        player1[Y]=320
        player2[X]=750
        player2[Y]=320

 
    if player1[SCORE]==3: #if player 1 gets 3 scores
        leadFile=open("leaderboard.txt","w")
        leadFile.write(str(player1[SCORE])+","+str(player2[SCORE]))
        leadFile.close()
        gameReset(player1,player2)
        page = "board" 
        
    if player2[SCORE]==1: #if player 2 gets 3 scores
        leadFile=open("leaderboard.txt","w")
        leadFile.write(str(player1[SCORE])+","+str(player2[SCORE]))
        leadFile.close()
        #gameReset(player1,player2)
        page = "board"
        return "board"
        
        #make "recent winner" screen
##    if player2[SCORE]==3:
##        winner()


##def winner():
##    running=True
##    #inst=image.load("images/howtoplay.png")
##    #screen.blit(inst,(0,0))
##    leadFile=open("leaderboard.txt","r")
##    #leadlist=leadFile.readlines()
##    while running:
##        for evt in event.get():
##            if evt.type==QUIT:
##                running=False
##                
##        print("aaa",player1[SCORE])
##        if player1[SCORE]==3:
##            screen.fill(RED)
##            leadFile.write("Player 1:"+str(player1[SCORE])+","+"Player 2:"+str(player2[SCORE])+"\n")
####
####        if player2[SCORE]==3:
####            screen.fill(BLUE)
####            leadFile.write("Player 1:",str(player1[SCORE]),",","Player 2:",str(player2[SCORE])+"\n")
##
##        leadFile.close()
##        if key.get_pressed()[27]:
##            gameReset()
##            runnnig=False
##        display.flip()
##    return "menu"

def board():
    running=True
    leadFile=open("leaderboard.txt","r")
    leadlist=leadFile.read().split(",")
    
    while running:
        for evt in event.get():
            if evt.type==QUIT:
                running=False

        screen.blit(backg,(0,0))
        lead=familyFont.render("Player 1: "+leadlist[0],True,BLACK)
        #"player2:",leadlist[1]
        screen.blit(lead,(350,150))
        screen.blit(picon2,(250,125))

        lead=familyFont.render("Player 2: "+leadlist[1],True,BLACK)
        #"player2:",leadlist[1]
        screen.blit(lead,(350,250))
        screen.blit(picon1,(250,225))

        #print("player1:",leadlist[0],"\nplayer2:",leadlist[1])
        #turn into text onscreen
        
        leadFile.close()
        if key.get_pressed()[27]:
            #gameReset(player1,player2)
            return "menu"
            runnnig=False
        display.flip()
    return "menu"


def gameReset(player1,player2):
    player1[HP]=100
    player1[X]=50
    player1[Y]=320
    player1[SCORE]=0
    
    player2[X]=750
    player2[Y]=320
    player2[HP]=100
    player2[SCORE]=0
 

def check(player1,player2,plats): #check for collision
    global jump1,jump2
    
    for plat in plats: #individual platform
        #check if player1 is colliding
        if player1[X]+player1[W]>plat[X] and player1[X]<plat[X]+plat[W] and player1[Y]+player1[H]<=plat[Y] and player1[Y]+player1[H]+v[Y]>plat[Y]:
            v[BOT] = plat[Y] #set bottom to y
            player1[Y] = v[BOT] - player1[H] #reset to ground level
            v[Y] =0
            jump1=False
            #check if player2 is colliding
        if player2[X]+player2[W]>plat[X] and player2[X]<plat[X]+plat[W] and player2[Y]+player2[H]<=plat[Y] and player2[Y]+player2[H]+Ev[Y]>plat[Y]:
            Ev[BOT] = plat[Y]
            player2[Y] = Ev[BOT] - player2[H]
            Ev[Y] =0
            jump2=False
            
    player1[Y]+=v[Y]
    player2[Y]+=Ev[Y]
    
    if player1[Y]+player1[H]>=ground:
        v[2]=ground
        v[Y]=0
        player1[Y]=ground-player1[H]
        jump1=False

    if player2[Y]+player2[H]>=ground:
        Ev[2]=ground
        Ev[Y]=0
        player2[Y]=ground-player2[H]
        jump2=False





pics1=[]  #2d list (2 rows 8 columns) for player 1
pics1.append(addPics("char",1,8)) #idle row0
pics1.append(addPics("char",9,16)) #right row1
pics1.append(addPics("char",17,24)) #left row2
pics1.append(addPics("char",25,32)) #jump row3

pics2=[]  #2d list (2 rows 8 columns) for player 2
pics2.append(addPics("plar",1,8)) #idle row0
pics2.append(addPics("plar",9,16)) #right row1
pics2.append(addPics("plar",17,24)) #left row2
pics2.append(addPics("plar",25,32)) #jump row3



print(len(pics1[0]))


def level1():
    running=True
    myClock=time.Clock()
    while running:
        for evt in event.get():            
            if evt.type == QUIT:
                running=False

    
        drawScene(screen,player1,pics1,player2,pics2,bullets,Ebullets,bg1) #draw scene
        checkAttack(bullets,player1,Ebullets,player2) #check for attacking
        moveBullets(bullets,Ebullets) #move the bullets

        checkScore(player1,player2) #check the score
        check(player1,player2,plats1) #check the collisions
        movePlayer1(player1,playerSpeed,bullSpeed) #move player 1
        movePlayer2(player2,playerSpeed,bullSpeed) #move player 2

        
        display.flip()
        
        if key.get_pressed()[27]:
            running = False 
            gameReset(player1,player2)
        myClock.tick(60)    
    return "menu"

def level2():
    running=True
    myClock=time.Clock()
    while running:
        for evt in event.get():            
            if evt.type == QUIT:
                running=False

    
        drawScene(screen,player1,pics1,player2,pics2,bullets,Ebullets,bg2) #draw scene
        checkAttack(bullets,player1,Ebullets,player2) #check for attacking
        moveBullets(bullets,Ebullets) #move the bullets

        checkScore(player1,player2) #check the score
        check(player1,player2,plats2) #check the collisions
        movePlayer1(player1,playerSpeed,bullSpeed) #move player 1
        movePlayer2(player2,playerSpeed,bullSpeed) #move player 2
        
        display.flip()
        
        if key.get_pressed()[27]:
            running = False 
            gameReset(player1,player2)
        myClock.tick(60)    
    return "menu"





def playMap():
    #pick map
    running=True
    myClock=time.Clock()
    buttons=[Rect(200+x*225,150,150,150) for x in range(2)] #makes buttons

    gicon1=transform.scale(bg1,(150,150)) #map1
    gicon2=transform.scale(bg2,(150,150)) #map2
    gameIcons=[gicon1,gicon2] #list of maps
    
    while running:
        for evt in event.get():
            if evt.type==QUIT:
                running=False
                return "menu"
                

        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        screen.blit(backg,(0,0)) #background image

        for i in range(2): #add images of maps
            screen.blit(gameIcons[i],buttons[i])
            
            if mb[0]==1: #if left click
                if buttons[0].collidepoint(mx,my): #button 1
                    return "lvl1" #map 1
                if buttons[1].collidepoint(mx,my): #button 2
                    return "lvl2" #map 2

        if key.get_pressed()[27]: #if esc
            return "menu"         #go back to menu
            runnnig=False
            
        display.flip()
        myClock.tick(60)
    return "menu"


def inst(): #instructions
    running=True
    inst=image.load("images/howtoplay.png").convert() #how to play image
    screen.blit(inst,(0,0)) #add image
    while running:
        for evt in event.get():
            if evt.type==QUIT:
                running=False
        if key.get_pressed()[27]: #if esc
            return "menu"         #go back to menu
            runnnig=False
        display.flip()
    return "menu"

def menu():
    running=True
    myClock=time.Clock()
    buttons=[Rect(325,200+x*60,125,40) for x in range(4)] #makes buttons
    
    playB=image.load("images/button_p.png").convert()
    settingsB=image.load("images/button_s.png").convert()
    leaderB=image.load("images/button_l.png").convert()
    title=image.load("images/title.png").convert_alpha()

    
    bImg=[playB,settingsB,leaderB,playB]

    while running:
        for evt in event.get():
            if evt.type==QUIT:
                return "exit"
                
        screen.blit(backg,(0,0))
        screen.blit(title,(200,50))
        #draw.rect(screen,RED,(200,50,400,100))

        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        for i in range(3):
            screen.blit(bImg[i],buttons[i]) #draw buttons

            if mb[0]==1:
                if buttons[0].collidepoint(mx,my):
                    return "playMap"
                if buttons[1].collidepoint(mx,my):
                    return "inst"
                if buttons[2].collidepoint(mx,my):
                    return "board"
                           
        display.flip()
        myClock.tick(60)




running=True
page = "menu" #start game with menu

while page != "exit":
    if page == "menu":
        page = menu()
    if page == "inst":
        page = inst()
    if page == "board":
        page = board()

    if page == "playMap":
        page = playMap()
    if page == "lvl1":
        page = level1()
    if page == "lvl2":
        page = level2()
            
quit()
