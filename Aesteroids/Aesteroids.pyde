import random 
pos = PVector(50, 50)
vel = PVector(0, 0)
is_accel = False
dead = False
ship_size = 10


dir = 0
rotation = 0
max_speed = 4

def setup():
    global screenHeight, screenWidth, bulletDimensions, bulletDirection, whichKey, objX, objY
    global start_screen_image, help_screen_image, blow_up, bulletList, game_start, mode, asciiList, controlKeys
    global top_bound, left_bound, right_bound, bottom_bound, asteroid1, asteroids_list, num_asteroids, asteroids_sizes, asteroids_vel
    
    size(800, 800)
    screenHeight = 799
    screenWidth = 799
    
    # variables
    bulletDimensions = 8 
    bulletDirection = 0
    bulletList = []
    num_asteroids = 5
    
    # asteroids variables
    # list of x,y coordinates (PVectors)
    asteroids_list = []
    # list of corresponding sizes (int)
    asteroids_sizes = []
    # list of corresponding velocities (PVectors)
    asteroids_vel = []
    
    game_start = False
    mode = ""
    objX = 0
    objY = 1
    
    # boundaries 
    top_bound = 0
    left_bound = 0
    right_bound = screenWidth - bulletDimensions
    bottom_bound = screenHeight
    
    
    # load images
    start_screen_image = loadImage("startScreen.png")
    help_screen_image = loadImage("helpScreen.png")
    blow_up = loadImage("blowup.png")
    asteroid1 = loadImage("asteroid.png")
    
    # keys
    asciiList = "abcdefghijklmnopqrstuvwxyz"
    controlKeys = [ CONTROL ]
    whichKey = ""
    
    # asteroids coordinates
    for i in range(num_asteroids):
        asteroid_pos = PVector(random.randint(0+100, width-100), random.randint(0+100, height-100))
        # 0 < direction < 2*PI
        random_dir = random.uniform(0, 2*PI)
        asteroids_vel.append(PVector.fromAngle(random_dir))
        asteroids_list.append(asteroid_pos)
        asteroid_size = random.randint(20, 100)
        asteroids_sizes.append(asteroid_size)
    
    
def draw(): 
    global pos, vel, xspeed, yspeed, dir, rotation, is_accel, asteroid1
    global screenHeight, screenWidth, bulletDimensions, bulletDirection
    global start_screen_image, help_screen_image, blow_up, bulletList, game_start, mode, asciiList, controlKeys
    global dead
    
    if whichKey == "P" or whichKey == "p": # p key
        mode = "game screen"
        game_start = True
    elif whichKey == "H" or whichKey == "h": # h key
        mode = "help screen"
    elif whichKey == "b" or whichKey == "B": # b key
        mode = "back clicked"
    elif whichKey == "r" or whichKey == "R":
        print("r is pressed")
        reset()
    
    # different modes
    if game_start == False:
        image(start_screen_image, 0, 0, 800, 800)
        mode == "start screen"
    if mode == "start screen":
        image(start_screen_image, 0, 0, 800, 800)
        if mode == "back clicked" and game_start == False:
            image(start_screen_image, 0, 0, 800, 800)
    elif mode == "back clicked" and game_start == True:
        draw_game()
    if mode == "game screen" and game_start == True and dead == False:
        if (len(asteroids_list) > 0):
            draw_game()
        elif (len(asteroids_list) <= 0):
            draw_victory()
    if mode == "game screen" and dead == True:
        draw_game_over()    
    if mode == "help screen":
        image(help_screen_image, 0, 0, 800, 800)

def draw_game():
    global pos, vel, xspeed, yspeed, dir, rotation, is_accel, whichKey, asteroid1
    global screenHeight, screenWidth, bulletDimensions, bulletDirection, objX, objY
    global start_screen_image, help_screen_image, blow_up, bulletList, game_start, mode, asciiList, controlKeys
    global top_bound, left_bound, right_bound, bottom_bound, asteroids_list, num_asteroids, asteroids_list, asteroids_vel
    global dead

    background(0)
    fill(255)
    
    # ship functions
    keep_ship_onscreen()
    draw_ship()
    update_ship()
    turn_ship()
    if (ship_collision()):
        dead = True
    
    # asteroid functions
    draw_asteroids()
    update_asteroids()
    keep_asteroids_onscreen()
    
    # bullet functions
    create_bullet()
    draw_bullet()
    update_bullet()
    bullet_collision()
    
        

def draw_game_over():
    background(0)
    textSize(32)
    fill(255, 0, 0)
    text("Game Over", (height/2)-100, width/2)
    text("Press r to play again", (height/2)-100, width/2 + 100)
    
def draw_victory():
    background(0)
    textSize(32)
    fill(0, 255, 0)
    text("You win", (height/2)-100, width/2)
    
# ------------------------ ship related functions -------------------------
def accelerate():
    global vel
    force = PVector.fromAngle(dir-PI/2)
    vel.add(force)

def keep_ship_onscreen():
    global pos
    
    # brings the space craft back on the screen
    if (pos.x > width):
        pos.x = 0
    if (pos.x < 0):
        pos.x = width
    if (pos.y > height):
        pos.y = 0
    if (pos.y < 0):
        pos.y = height
        
def draw_ship():
    global pos, dir, ship_size
    
    pushMatrix()
    translate(pos.x, pos.y)
    rotate(dir)
    triangle(-ship_size, ship_size, ship_size, ship_size, 0, -ship_size)         
    popMatrix()
    #pos.add(vel)
    #dir += rotation
    
    #print("this is dir or direction??", dir)

# this should handle updating the position based on velocity of the ship, handling acceleration, etc
def update_ship():
    global pos, vel, is_accel
    pos.add(vel)
    
    if (is_accel):
        accelerate()
    
    # simulates air resistance
    vel.mult(0.85)

def turn_ship():
    global dir, rotation
    dir += rotation

def ship_collision():
    global asteroids_list, pos, asteroids_sizes, ship_size
    for i in range(len(asteroids_list)):
        
        dist_check = dist(pos.x, pos.y, asteroids_list[i].x, asteroids_list[i].y) < (ship_size/2) + (asteroids_sizes[i]/2)
        
        if (dist_check):
            return True
    return False

# ------------------------ asteroid related functions -------------------------
def draw_asteroids():
    global asteroids_list, asteroids_sizes, num_asteroids, asteroid1
    
    # draw asteroids of random size
    for i in range(num_asteroids):
        image(asteroid1, asteroids_list[i].x, asteroids_list[i].y, asteroids_sizes[i], asteroids_sizes[i])
    

# handles updating the position of the asteroids
def update_asteroids():
    global asteroids_list, asteroids_vel, num_asteroids
    for i in range(num_asteroids):
        # for the ith asteroid, add the ith velocity PVector to its position PVector
        asteroids_list[i].add(asteroids_vel[i])

    
def keep_asteroids_onscreen():
    global asteroids_list, asteroids_vel, num_asteroids
    for i in range(num_asteroids):
        if (asteroids_list[i].x > width):
            asteroids_list[i].x = 0
        if (asteroids_list[i].x < 0):
            asteroids_list[i].x = width
        if (asteroids_list[i].y > height):
            asteroids_list[i].y = 0
        if (asteroids_list[i].y < 0):
            asteroids_list[i].y = height
            

# ------------------------ bullet related functions -------------------------
# checks if any bullets are overlapping any asteroids
# if thats the case, then both the bullet and asteroid are destroyed
def bullet_collision():
    global bulletList, asteroids_list, objX, objY
    global asteroids_vel, asteroids_sizes, num_asteroids
    # for each bullet, check every asteroid and see if it collides with any
    
    hit_found = False
    found_i = -1
    found_j = -1
    
    for i in range(len(bulletList)):
        for j in range(len(asteroids_list)):
            
            x_hit_check = bulletList[i][objX] >= asteroids_list[j].x-asteroids_sizes[j] and bulletList[i][objX] <= asteroids_list[j].x+asteroids_sizes[j]
            y_hit_check = bulletList[i][objY] >= asteroids_list[j].y-asteroids_sizes[j] and bulletList[i][objY] <= asteroids_list[j].y+asteroids_sizes[j]
            
            if (x_hit_check and y_hit_check):
                # if we made it here, there's a collision with this bullet and this asteroid
                # delete the bullet from bulletList and delete the asteroid and its corresponding values from the appropriate asteroidlists
                #bulletList.remove(i)
                #asteroids_list.remove(j)
                #asteroids_vel.remove(j)
                #asteroids_sizes.remove(j)
                #num_asteroids -= 1
                hit_found = True
                found_i = i
                found_j = j
                break
        if (hit_found):
            break
    
    if (hit_found and found_i is not -1 and found_j is not -1):
        bulletList.pop(found_i)
        asteroids_list.pop(found_j)
        asteroids_vel.pop(found_j)
        asteroids_sizes.pop(found_j)
        num_asteroids -= 1
    

# deals with adding a bullet to bulletList
def create_bullet():
    global whichKey, bulletList, pos
    if whichKey == CONTROL:
        #print("control key presssed")
        # allSoundInfo[0][shotSound].trigger()
        #print("this is bullet list before append when control key is pressed", bulletList)
        bulletList.append( [ pos.x, pos.y ])
        #print("this is bullet list when the control key is pressed", bulletList)
        whichKey = ""

# draws all bullets in bulletList
def draw_bullet():
    global bulletList, bulletDimensions
    
    for bullet in bulletList:
        rect( bullet[objX], bullet[objY], bulletDimensions, bulletDimensions )


# controls movement of bullets
def update_bullet():
    global bulletList, dir, objX, objY
    for bullet in bulletList:
        #print("this is bullet in bulletlist", bullet)
        bullet[objX] += 5
        if dir == 0:
            bullet[objY] += 5 #* 1 # negative 1 for bullet to go other way
        elif dir <= 0:
            bullet[objY] += -5 
        else:
            bullet[objX] += 5

def reset():
    global bulletList, game_start, whichKey, asteroids_list, asteroids_sizes, asteroids_vel, mode
    global screenHeight, screenWidth, bulletDimensions, bulletDirection, whichKey, objX, objY
    global start_screen_image, help_screen_image, blow_up, bulletList, game_start, mode, asciiList, controlKeys
    global top_bound, left_bound, right_bound, bottom_bound, asteroid1, asteroids_list, num_asteroids, asteroids_sizes, asteroids_vel
    global dead, ship_size, is_accel, pos, vel, doir, rotation, max_speed
    
    
    pos = PVector(50, 50)
    vel = PVector(0, 0)
    is_accel = False
    dead = False
    ship_size = 10
    
    
    dir = 0
    rotation = 0
    max_speed = 4
    bulletList = []
    game_start = False
    whichKey = ""
    
    size(800, 800)
    screenHeight = 799
    screenWidth = 799
    
    # variables
    bulletDimensions = 8 
    bulletDirection = 0
    bulletList = []
    num_asteroids = 5
    
    # asteroids variables
    # list of x,y coordinates (PVectors)
    asteroids_list = []
    # list of corresponding sizes (int)
    asteroids_sizes = []
    # list of corresponding velocities (PVectors)
    asteroids_vel = []
    
    game_start = False
    mode = ""
    objX = 0
    objY = 1
    
    # boundaries 
    top_bound = 0
    left_bound = 0
    right_bound = screenWidth - bulletDimensions
    bottom_bound = screenHeight
    
    
    # keys
    asciiList = "abcdefghijklmnopqrstuvwxyz"
    controlKeys = [ CONTROL ]
    whichKey = ""
    
    # asteroids coordinates
    for i in range(num_asteroids):
        asteroid_pos = PVector(random.randint(0+100, width-100), random.randint(0+100, height-100))
        # 0 < direction < 2*PI
        random_dir = random.uniform(0, 2*PI)
        asteroids_vel.append(PVector.fromAngle(random_dir))
        asteroids_list.append(asteroid_pos)
        asteroid_size = random.randint(20, 100)
        asteroids_sizes.append(asteroid_size)
    
    
    
    

def keyPressed():
    global mode, whichKey, asciiList, controlKeys, game_start, rotation, is_accel, restart
    
    if (keyCode == LEFT):
        rotation = -0.1
    elif (keyCode == RIGHT):
        rotation = 0.1
    elif (keyCode == UP):
        is_accel = True
    
    if key == CODED:
       if keyCode in controlKeys:
        whichKey = keyCode
    elif key in asciiList:
        whichKey = key
    else:
        whichKey = ""
        
                        
def keyReleased():
    global rotation, vel, is_accel
    if key == CODED:
        if (keyCode == LEFT or keyCode == RIGHT):
            rotation = 0
        if (keyCode == UP):
            is_accel = False
        
