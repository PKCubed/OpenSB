import socket
import threading
import time

import os
import sys

HOST=""
PORT=60140

# Import and initialize the pygame library
import pygame
pygame.init()

timer_value = 61 # Seconds
counting = False # Whether or not the timer should be counting
direction = True # True = up, false = down
local_time = True

buzz = 0
buzzer = False

score_a = 0
score_b = 0
scores = True

period = 0

bonus = 0

# Set up the drawing window
screen = pygame.display.set_mode([500, 500], pygame.RESIZABLE)
WIDTH = screen.get_width()
HEIGHT = screen.get_height()
EM = ((WIDTH+HEIGHT)/2)/32

def sbtext(surface, xpos, ypos, string, size):
    font = pygame.font.Font(os.path.join(sys.path[0], 'font_txt.ttf'), int(size))
    text = font.render(string, True, (255,255,255), (0,0,0))
    textRect = text.get_rect()
    textRect.center = (xpos, ypos)
    surface.blit(text, (textRect.x, textRect.y))

def sbnum(surface, xpos, ypos, string, size):
    font = pygame.font.Font(os.path.join(sys.path[0], 'font_num.ttf'), int(size))
    text = font.render(string, True, (255,255,255), (0,0,0))
    textRect = text.get_rect()
    textRect.center = (xpos, ypos)
    surface.blit(text, (textRect.x, textRect.y))

cnt_start_val = 0
cnt_start_time = 0

def socket_thread():
    global timer_value
    global counting
    global direction

    global local_time

    global score_a
    global score_b
    global scores

    global period
    global bonus

    global cnt_start_val
    global cnt_start_time

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT)) # Bind to port
        s.listen() # Start listening
        while True:
            conn, addr = s.accept() # Accept connection
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                print(f"Data received: {data}")
                if data.decode("utf-8")[:4] == "tme:": # Set timer
                    timer_value = int(data.decode("utf-8")[4:])
                    if counting:
                        cnt_start_val = timer_value
                        cnt_start_time = time.time()
                    local_time = False
                    print(f"timer_value={timer_value}")
                if data.decode("utf-8")[:4] == "dir:": # Direction of Counting (Bool)
                    direction = bool(int(data.decode("utf-8")[4:]))
                    print(f"direction={direction}")
                    if counting:
                        cnt_start_val = timer_value
                        cnt_start_time = time.time()
                if data.decode("utf-8")[:4] == "cnt:": # Counting T/F
                    counting = bool(int(data.decode("utf-8")[4:]))
                    if counting:
                        cnt_start_val = timer_value
                        cnt_start_time = time.time()
                        local_time = False
                    print(f"counting={counting}")
                if data.decode("utf-8")[:4] == "lcl:": # Display Local Time
                    counting = False
                    local_time = True
                    print(f"local_time={local_time}")
                if data.decode("utf-8")[:4] == "sca:": # Set Score A
                    score_a = int(data.decode("utf-8")[4:])
                    print(f"score_a={score_a}")
                if data.decode("utf-8")[:4] == "scb:": # Set Score B
                    score_b = int(data.decode("utf-8")[4:])
                    print(f"score_b={score_b}")
                if data.decode("utf-8")[:4] == "spd:": # Set Period
                    period = int(data.decode("utf-8")[4:])
                    print(f"period={period}")
                if data.decode("utf-8")[:4] == "sbs:": # Set Bonus
                    bonus = str(data.decode("utf-8")[4:])
                    print(f"bonus={bonus}")
                if data.decode("utf-8")[:4] == "scr:": # Set Scores Enable
                    scores = bool(int(data.decode("utf-8")[4:]))
                    print(f"scores={scores}")

x = threading.Thread(target=socket_thread)
x.start()

# Run until the user asks to quit
running = True
while running:

    if buzz >= time.time():
        buzzer = True
    else: 
        buzzer = False

    if buzzer:
        print("BUZZ")

    if counting:
        if direction:
            timer_value = cnt_start_val + (time.time() - cnt_start_time)
        else:
            timer_value = cnt_start_val - (time.time() - cnt_start_time)
        if timer_value <= 0:
            timer_value = 0
            counting = 0
            buzz = time.time() + 1

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            surface = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
            WIDTH = screen.get_width()
            HEIGHT = screen.get_height()
            EM = ((WIDTH+HEIGHT)/2)/32

    # Fill the background with black
    screen.fill((0, 0, 0))

    if local_time:
        timer = f"{time.strftime('%H')}:{time.strftime('%M')}"
    else:
        if timer_value >= 10:
            timer = str(int(timer_value/60))+":"+str(int(timer_value)-int(timer_value/60)*60).zfill(2)
        else:
            timer = str(int(timer_value))+":"+str(int(timer_value*100)-int(timer_value)*100).zfill(2)

    #Timer
    sbnum(screen, int(WIDTH*4/8), int(HEIGHT*3/12), str(timer), 10*EM)

    #Scores
    if scores:
        #Score A
        sbtext(screen, int(WIDTH*2/12), int(HEIGHT*8/12), "GUEST", 2*EM)
        sbnum(screen, int(WIDTH*2/12), int(HEIGHT*10/12), str(score_a), 8*EM)

        #Score B
        sbtext(screen, int(WIDTH*10/12), int(HEIGHT*8/12), "HOME", 2*EM)
        sbnum(screen, int(WIDTH*10/12), int(HEIGHT*10/12), str(score_a), 8*EM)

        #Period
        sbtext(screen, int(WIDTH*4/8), int(HEIGHT*12/16), "PERIOD", 2*EM)
        sbnum(screen, int(WIDTH*4/8), int(HEIGHT*14/16), str(period), 6*EM)

        #Bonus
        if bonus == "A":
            #Bonus A
            sbtext(screen, int(WIDTH*5/16), int(HEIGHT*10/12), "< B", 2*EM)
        elif bonus == "B":
            #Bonus B
            sbtext(screen, int(WIDTH*11/16), int(HEIGHT*10/12), "B >", 2*EM)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()