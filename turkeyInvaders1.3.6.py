# g4
# Turkey Invaders

import turtle
import math
import random
#For sounds
import winsound
import pygame
# Biraz fazla cpu kullanıyor, gpu kullanırsa çok az güç tüketecek yüksek ihtimal
# To Lower cpu usage, couldn't do it tho :/
import time
# To run it on other computers
import os, sys

# Set up the SCREEN

sc = turtle.Screen()
sc.title("Turkey Invaders by g4")
sc.bgcolor("#000")
sc.bgpic(os.path.dirname(sys.argv[0])+"/turkey_invaders_background.gif")
sc.tracer(0)

# Background Music

winsound.PlaySound(os.path.dirname(sys.argv[0])+"/onuncuYilMars.wv", winsound.SND_ASYNC|winsound.SND_NOSTOP|winsound.SND_LOOP)

# Register the shapes

turtle.register_shape(os.path.dirname(sys.argv[0])+"/ataturk.gif")
turtle.register_shape(os.path.dirname(sys.argv[0])+"/bullet.gif")
turtle.register_shape(os.path.dirname(sys.argv[0])+"/ampul2.gif")

# Draw BORDERS

border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("#fff")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4): #4 4 kenar için
    border_pen.fd(600) # forward
    border_pen.lt(90) # left
border_pen.hideturtle()

# Set the score to 0
score = 0
high_score = 0

# Draw both score and high score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.shape("square")
score_pen.color("white")
score_pen.penup()
score_pen.goto(-290,270)
score_pen.write("Score: {}    High Score: {}".format(score,high_score), False, align="left", font=("Arial",14,"normal"))
score_pen.hideturtle()

# Create the PLAYER turtle

player = turtle.Turtle()
player.color("blue")
player.shape(os.path.dirname(sys.argv[0])+"/ataturk.gif")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90) # üçgeni 90* çevirir
playerspeed = 25

# Choose a number of enemies 
number_of_enemies = 7
# Create an empty list of enemies
enemies = []
# Add enemies to the list
for i in range(number_of_enemies):
    #Create the enemy
    enemies.append(turtle.Turtle())
for enemy in enemies:
    enemy.color("red")
    enemy.shape(os.path.dirname(sys.argv[0])+"/ampul2.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200,200)
    y = random.randint(100,250)
    enemy.setposition(x,y)
enemyspeed = 0.2

# Create the player's bullet

bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape(os.path.dirname(sys.argv[0])+"/bullet.gif")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()

bulletspeed = 2

# Define bullet state
# ready- ready to fire
# fire - bullet is firing
bulletstate = "ready"

# Move the player left and right

def move_left():
    player.speed = -15
    x = player.xcor() # x koordinatı
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)

def move_right():
    player.speed = 15
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    # Declare bulletstate as a global if it needs changed
    global bulletstate
    if bulletstate == "ready":
        bulletstate = "fire"
        # Move the bullet to the just above the player
        x = player.xcor()
        y = player.ycor() +10
        bullet.setposition(x,y)
        bullet.showturtle()
        # Play sound
        pygame.mixer.init()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.dirname(sys.argv[0])+"/gunshot.wav"))
    
def isCollision(t1,t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 20:
        return True
    else:
        return False

# Create keybord bindings

turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_left, "a")
turtle.onkey(move_left, "A")
turtle.onkey(move_right, "Right")
turtle.onkey(move_right, "d")
turtle.onkey(move_right, "D")
turtle.onkey(fire_bullet, "space")


# Main Game Loop
while True:
    sc.update()

    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)
        
        # Move the enemy back and down
        if enemy.xcor() > 280:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemyspeed *= - 1

        if enemy.xcor() < -280:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemyspeed *= - 1
        
        # Check for a collision between the bullet and the enemy
        if isCollision(bullet,enemy):
            # Play sound
            pygame.mixer.init()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.dirname(sys.argv[0])+"/bulb_breaking.wav"))
            # Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0,-400)
            # Reset the enemy
            x = random.randint(-200,200)
            y = random.randint(100,250)
            enemy.setposition(x,y)
            # Update Score
            score += 10
            if score > high_score:
                high_score = score
                score_pen.clear()
                score_pen.write("Score: {}  High Score: {}".format(score, high_score),False, align="left", font=("Arial",14,"normal"))
            
        if enemy.ycor() <= -220 :
            player.hideturtle()
            for enemy in enemies:
                enemy.hideturtle()
            bullet.hideturtle() 
            # GAME OVER
            game_over = turtle.Turtle()
            game_over.speed(0)
            game_over.color("white")
            game_over.penup()
            game_over.setposition(0,0)
            game_over.write("GAME OVER", False, align="center", font=("Arial",30,"normal"))
            game_over.hideturtle()
            # Write total score
            total_score = turtle.Turtle()
            total_score.speed(0)
            total_score.color("white")
            total_score.penup()
            total_score.setposition(0,-40)
            total_score.write("Score: {}  High Score: {}".format(score, high_score), False, align="center", font=("Arial",25,"normal"))
            total_score.hideturtle()
            break    

        if isCollision(player,enemy):
            player.hideturtle()
            for enemy in enemies:
                enemy.hideturtle()
            bullet.hideturtle() 
            # GAME OVER
            game_over = turtle.Turtle()
            game_over.speed(0)
            game_over.color("white")
            game_over.penup()
            game_over.setposition(0,0)
            game_over.write("GAME OVER", False, align="center", font=("Arial",30,"normal"))
            game_over.hideturtle()
            # Write total score
            total_score = turtle.Turtle()
            total_score.speed(0)
            total_score.color("white")
            total_score.penup()
            total_score.setposition(0,-40)
            total_score.write("Score: {}  High Score: {}".format(score, high_score), False, align="center", font=("Arial",25,"normal"))
            total_score.hideturtle()
            break

        

    
    # Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)
    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"


time.sleep(1000) # to lower cpu usage, not very effective tho :D
