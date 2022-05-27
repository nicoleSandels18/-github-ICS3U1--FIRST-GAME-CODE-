mode = 1 

background
def setup():
    global background_pic, img, back
    size(800, 600)
    background_pic = loadImage("space.jpg")
    back = loadImage("back.jpg") 
    
def draw():
    
    global mode 
    
    if mode == 1: 
        #Initial Background 
        background(0) 
        image(background_pic, 0, 0) 
        fill(255) 
        textSize(70)
        text("Aesteroids", 220, 250)
        
        #Instructions Page 
        fill(255) 
        rect(100, 400, 590, 100) 
        fill(0)
        textSize(30) 
        fill(0)
        text("Instructions", 300, 455)
        
    if mode == 2:
        instructions_screen()
        
def instructions_screen():
    
    global back 
    
    background(168, 45, 51)
    image(back, 0, 0) 
    fill(255)
    textSize(30)
    text("Here are the game rules", 240, 100)
    textSize(15) 
    text("1. Move your player using WASD and the arrow keys", 220, 250)
    text("2. DO not hit any aesteroids. If you do game over!", 220, 290)
    text("3. Shoot down moving aesteroids by pressing SPACE.", 220, 330)
    text("4. Goodluck ;)", 220, 363 ) 
        
def mousePressed():
    global mode 
    
    if mode == 1:
        if 590 > mouseX > 100 and 500 > mouseY >400:
            mode = 2 
        

    
