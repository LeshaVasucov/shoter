#Створи власний Шутер!
from random import randint
import pygame
import datetime
from threading import Thread
import json
from PyQt5.QtWidgets import QWidget , QApplication  , QHBoxLayout , QListWidget , QTextEdit , QLabel
app = QApplication([])
window1 = QWidget()
window1.resize(600,600)
line1 = QHBoxLayout()
text = QTextEdit()
window1.setLayout(line1)
score_list = QListWidget()
with open("scores.json", "r") as file:
    scores = json.load(file , )
    print(scores)

    for score in scores :
        date = scores[score]
        score = "Score : " + score + "  Date : "
        tag = f"{score   + date} "
        score_list.addItem(tag)
    s = list(scores.keys())
    s.sort(reverse=True)
    s = s[0]
    print(s)
label = QLabel(f"the best score : {s}  Date : {scores[s]} ")
line1.addWidget(score_list)
line1.addStretch()
line1.addWidget(label)
pygame.init()
win_wigth = 600
win_height = 900
missed_num = 0
max_score = 0
while True :
    try :
        with open("record.txt ", "r"  ) as file :
            try:
                record = file.read()
                max_score = int(record)
                break
            except :
                print('Щось нет так!')
    
    except FileNotFoundError:
        with open("record.txt ", "x") as file :
            file.close()

class GameObject(pygame.sprite.Sprite):
    def __init__(self , x ,y ,w ,h, image , speed ) :
        super().__init__()
        self.rect = pygame.Rect(x,y,w,h)
        image = pygame.transform.scale(image ,(w,h))
        self.image = image
        self.speed = speed
    def update(self):
        window.blit(self.image, (self.rect.x  ,self.rect.y ))
enemies_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
bullet_pict = pygame.image.load("bullet.png")
class Bullet(GameObject):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image, speed)
        bullets_group.add(self)
    def update(self):
        self.rect.y -= self.speed
hart_pict = pygame.image.load("hp.png")
class Player(GameObject):
    def __init__(self, x, y, w, h, image , speed , hp = 3):
        super().__init__(x, y, w, h, image , speed)
        self.hp = hp
        harts = []
        x= 350
        for i in range(self.hp) :
            heart = GameObject(x,0,50,50,hart_pict , 0)
            harts.append(heart)
            x += 50
        self.harts = harts
    def start (self):
        self.rect.y = randint(50,100)
        self.rect.x = randint(50,600)
    def move(self,K_left,K_right):
        k = pygame.key.get_pressed()
        if k[K_left]:
            if self.rect.x > 0 :
                self.rect.x -= self.speed
            
        if k[K_right]:
            if self.rect.x < 840 :
                self.rect.x += self.speed       
player_pict = pygame.image.load("rocket.png")
but_pict = pygame.image.load("but_pict.png")
player = Player(390,500,60,80,player_pict , 4)
class Enemy(GameObject) :
    def __init__(self, x, y, w, h, image, speed ):
        super().__init__(x, y, w, h, image, speed)
        self.x_speed = randint(-6,6)
        self.x_wait = randint(120,130)
        enemies_group.add(self)
    def update (self):
        self.rect.y += self.speed
        self.rect.x += self.x_speed
        if self.x_wait <= 0 or self.rect.x >= 845 or self.rect.x <= 0:
            self.x_wait = 130
            self.x_speed *= -1
        else :
            self.x_wait -= 1
        if self.rect.y > player.rect.y :
            global missed_num 
            missed_num += 1
            enemies_group.remove(self)

window = pygame.display.set_mode((win_height , win_wigth))
pygame.display.set_caption("shoter")
back = pygame.image.load("galaxy.jpg")
back = pygame.transform.scale(back , (900,600))
fire = pygame.mixer.Sound("fire.ogg")
fon = pygame.image.load("fon1.png")
fon1 =  pygame.transform.scale(fon , (900 ,600))
fire.set_volume(0.1)
pygame.mixer_music.load("space.ogg")
pygame.mixer_music.play()
pygame.mixer_music.set_volume(0.1)
enemy_pict = pygame.image.load("ufo.png")

FPS = 40
clock = pygame.time.Clock()
game = True

finish = False
enemy_wait = randint(1,20)

enemy = Enemy(randint(50,600),randint(50,100),70,45,enemy_pict, 1)
enemy = Enemy(randint(50,600),randint(50,100),70,45,enemy_pict, 1)
font = pygame.font.SysFont("Arial",75)
font1 = pygame.font.SysFont("Arial",20)
enemies_count = 0 
start = True
win = False
min_speed = 1
max_speed = 3
min_wait = 50
max_wait = 200
change = 5
#BUTTON 
click_y = 0
click_x = 0
but = GameObject(200,400,500,150,but_pict , 0)
hp_spis = 2 
class Thread2(Thread):
    def run(self):
        app.exec_()
class Thread1(Thread):
    while game :
        if start :
            question1 = font.render('Press "Enter" to play',True,(0,0,0))
            window.blit(fon1 , (0,0))
            window.blit(question1 , (200,100))
          #  score3 = font.render(f"Your best score{max_score}!",True , (0,0,0))
            but.update()
          #  window.blit(score3, (200,400))
        if start and click_x >= but.rect.x and click_x <= but.rect.x + but.rect.w and click_y >= but.rect.y and click_y <= but.rect.y + but.rect.h :
            with open("scores.json", "r") as file:
                scores = json.load(file , )
                print(scores)
                score_list.clear()
                for score in scores :
                    date = scores[score]
                    score = "Score : " + score + "  Date : "
                    tag = f"{score   + date} "
                    score_list.addItem(tag)
                s = list(scores.keys())
                s.sort(reverse=True)
                s = s[0]
                print(s)
            window1.show()
        # window1.show()
            click_x = 0 
            click_y = 0
        if not finish and start == False:
            window.blit(back , (0,0))
            score = font1.render(f"missed{missed_num}",True , (255,255,255))
            score2 = font1.render(f"enemies{enemies_count}",True , (255,255,255))
            for heart in player.harts :
                heart.update()
            window.blit(score , (0 , 0 ))
            window.blit(score2 , (800,0))
            if enemy_wait == 0 :
                enemy = Enemy(randint(50,600),randint(50,100),70,45,enemy_pict, randint(min_speed,max_speed))
                enemy_wait = randint(min_wait,max_wait)
            else:

                enemy_wait -=1
            if enemies_count >= change :
                min_speed += 2 
                max_speed += 2
                if min_wait > 35 :
                    min_wait -= 15
                if max_wait > 55 :
                    max_wait -= 10
                change += 5
            bullets_group.update()
            bullets_group.draw(window)
            enemies_group.update()
            enemies_group.draw(window)
            if pygame.sprite.groupcollide(enemies_group,bullets_group , True , True) :
                enemies_count += 1
            if pygame.sprite.spritecollide(player , enemies_group , True):
                player.hp -= 1
                player.harts.pop(hp_spis)
                hp_spis -= 1
                print(player.hp)
            if player.hp <= 0  or missed_num >= 3:
                finish = True
                b = datetime.datetime.now()
                date = b.strftime("%y-%m-%d %H:%M:%S")
                with open ("scores.json " , "r" , encoding="utf-8") as file :
                    score_file = json.load(file)
                    #score_file = dict()
                    score_file[enemies_count] = date 
                    print(score_file)
                with open ("scores.json " , "w" , encoding="utf-8") as file :
                    json.dump(score_file , file)
                print(max_score)
                




            player.move(pygame.K_a , pygame.K_d)
            player.update()
            if enemies_count >= 25:
                finish = True
                win = True
        if finish and win == False :
            player.rect.x = 350
            player.rect.y = 500
            game_over = font.render("GAME_OVER",True,(0,0,0))
            window.fill((255,0,0))
            window.blit(game_over,(200,300))
            question = font.render('Press "R" to countinie',True,(0,0,0))
            window.blit(question,(120,450))
        if finish and win :
            player.rect.x = 350
            player.rect.y = 500
            game_over = font.render("YOU WIN",True,(0,0,0))
            window.fill((0,255,0))
            window.blit(game_over,(200,300))
            question = font.render('Press "R" to countinie',True,(0,0,0))
            window.blit(question,(120,450))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_x ,click_y = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and finish : 
                player.hp = 3
                enemies_group.empty()
                missed_num = 0
                enemies_count = 0
                finish = False
                win = False
                hp_spis = 2
                x = 350
                for i in range(player.hp) :
                    heart = GameObject(x,0,50,50,hart_pict , 0)
                    player.harts.append(heart)
                    x += 50
                print(finish)
                print(win)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE  :
                bullet = Bullet(player.rect.x + (player.rect.width / 2), player.rect.y , 10,10,bullet_pict,5)
                fire.play()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and start:
                    start = False
                    print(start)

        pygame.display.update()
        clock.tick(FPS)
if not game :
    t1 = Thread1()
    t1.start()
    t2 = Thread2()
    t2.start() 
