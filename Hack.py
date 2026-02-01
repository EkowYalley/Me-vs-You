import turtle as t
import random
import time

# Game variables
delay = 0.1  # delay - renamed from 'd' to avoid conflicts
seg1 = []  # snake1 body segments (white snake)
seg2 = []  # snake2 body segments (green snake)

# Scores
score1 = 0  # Player 1 (white snake) score
score2 = 0  # Player 2 (green snake) score

sc = t.Screen()
sc.title("Me vs You")
sc.bgcolor("purple")
sc.setup(width=600, height=600)
sc.tracer(0)

# Scoreboard
score_display = t.Turtle()
score_display.speed(0)
score_display.shape("square")
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write("Player 1: 0  |  Player 2: 0", align="center", font=("Arial", 18, "bold"))

# First snake (white) - controlled by arrow keys
h1 = t.Turtle()
h1.shape("square")
h1.color("white")
h1.penup()
h1.goto(-100, 0)
h1.direction = "Stop"

# Second snake (green) - controlled by WASD
h2 = t.Turtle()
h2.shape("square")
h2.color("green")
h2.penup()
h2.goto(100, 0)
h2.direction = "Stop"

# Food
food = t.Turtle()  # Renamed from 'f' to avoid confusion
food.speed(0)
food.shape("square")
food.color("red")
food.penup()
food.goto(0, 100)

# Direction functions for snake 1 (arrow keys)
def up():
    if h1.direction != "down":
        h1.direction = "up"

def down():
    if h1.direction != "up":
        h1.direction = "down"

def left():
    if h1.direction != "right":
        h1.direction = "left"

def right():
    if h1.direction != "left":
        h1.direction = "right"

# Direction functions for snake 2 (WASD keys)
def w():
    if h2.direction != "down":
        h2.direction = "up"

def s():
    if h2.direction != "up":
        h2.direction = "down"

def a():
    if h2.direction != "right":
        h2.direction = "left"

def d():
    if h2.direction != "left":
        h2.direction = "right"

# Movement functions
def move_snake(snake_head):
    if snake_head.direction == "up":
        snake_head.sety(snake_head.ycor() + 20)
    if snake_head.direction == "down":
        snake_head.sety(snake_head.ycor() - 20)
    if snake_head.direction == "left":
        snake_head.setx(snake_head.xcor() - 20)
    if snake_head.direction == "right":
        snake_head.setx(snake_head.xcor() + 20)

def update_scoreboard():
    score_display.clear()
    score_display.write(f"Player 1: {score1}  |  Player 2: {score2}", align="center", font=("Arial", 18, "bold"))

def reset_snake(snake, segments, start_x, start_y, is_snake1=True):
    """Reset a snake to its starting position and clear its segments"""
    snake.goto(start_x, start_y)
    snake.direction = "Stop"
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    update_scoreboard()

# Key bindings
sc.listen()
sc.onkeypress(up, "Up")
sc.onkeypress(down, "Down")
sc.onkeypress(left, "Left")
sc.onkeypress(right, "Right")

sc.onkeypress(w, "w")
sc.onkeypress(s, "s")
sc.onkeypress(a, "a")
sc.onkeypress(d, "d")

# Main Gameplay
while True:
    sc.update()
    
    # Boundary check for snake 1
    if h1.xcor() > 290 or h1.xcor() < -290 or h1.ycor() > 290 or h1.ycor() < -290:
        time.sleep(1)
        reset_snake(h1, seg1, -100, 0, True)
        food.goto(random.randint(-270, 270), random.randint(-270, 270))
    
    # Boundary check for snake 2
    if h2.xcor() > 290 or h2.xcor() < -290 or h2.ycor() > 290 or h2.ycor() < -290:
        time.sleep(1)
        reset_snake(h2, seg2, 100, 0, False)
        food.goto(random.randint(-270, 270), random.randint(-270, 270))
    
    # Food collision for snake 1
    if h1.distance(food) < 20:
        food.goto(random.randint(-270, 270), random.randint(-270, 270))
        
        # Adding segment to snake 1
        n_seg = t.Turtle()
        n_seg.speed(0)
        n_seg.shape("square")
        n_seg.color("orange")
        n_seg.penup()
        seg1.append(n_seg)
        delay = max(0.01, delay - 0.001)  # Prevent delay from going too low
        
        # Increase score for player 1
        score1 += 1
        update_scoreboard()
    
    # Food collision for snake 2
    if h2.distance(food) < 20:
        food.goto(random.randint(-270, 270), random.randint(-270, 270))
        
        # Adding segment to snake 2
        n_seg = t.Turtle()
        n_seg.speed(0)
        n_seg.shape("square")
        n_seg.color("yellow")
        n_seg.penup()
        seg2.append(n_seg)
        delay = max(0.01, delay - 0.001)  # Prevent delay from going too low
        
        # Increase score for player 2
        score2 += 1
        update_scoreboard()
    
    # Move segments for snake 1
    for i in range(len(seg1)-1, 0, -1):
        x, y = seg1[i-1].xcor(), seg1[i-1].ycor()
        seg1[i].goto(x, y)
    
    if len(seg1) > 0:
        x, y = h1.xcor(), h1.ycor()
        seg1[0].goto(x, y)
    
    # Move segments for snake 2
    for i in range(len(seg2)-1, 0, -1):
        x, y = seg2[i-1].xcor(), seg2[i-1].ycor()
        seg2[i].goto(x, y)
    
    if len(seg2) > 0:
        x, y = h2.xcor(), h2.ycor()
        seg2[0].goto(x, y)
    
    # Move heads
    move_snake(h1)
    move_snake(h2)

    # Checking for self-collision for snake 1
    for segment in seg1:
        if segment.distance(h1) < 20:
            time.sleep(1)
            reset_snake(h1, seg1, -100, 0, True)
            food.goto(random.randint(-270, 270), random.randint(-270, 270))
    
    # Checking for self-collision for snake 2
    for segment in seg2:
        if segment.distance(h2) < 20:
            time.sleep(1)
            reset_snake(h2, seg2, 100, 0, False)
            food.goto(random.randint(-270, 270), random.randint(-270, 270))
    
    # Check for head-to-head collision (mutual loss)
    if h1.distance(h2) < 20:
        time.sleep(1)
        reset_snake(h1, seg1, -100, 0, True)
        reset_snake(h2, seg2, 100, 0, False)
        food.goto(random.randint(-270, 270), random.randint(-270, 270))
    
    # Check if snake 1 hits snake 2's body
    for segment in seg2:
        if h1.distance(segment) < 20:
            time.sleep(1)
            reset_snake(h1, seg1, -100, 0, True)
            food.goto(random.randint(-270, 270), random.randint(-270, 270))
    
    # Check if snake 2 hits snake 1's body
    for segment in seg1:
        if h2.distance(segment) < 20:
            time.sleep(1)
            reset_snake(h2, seg2, 100, 0, False)
            food.goto(random.randint(-270, 270), random.randint(-270, 270))
    
    time.sleep(delay)  # Fixed: using 'delay' instead of 'd'