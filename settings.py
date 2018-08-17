# World Size
FIELD_SIZE_X = 32
FIELD_SIZE_Y = 32

GAME_SPEED = 6.0

# Number Of Color Type 
COLOR_LEVEL = 4

# Value Of Attack Once 
OCCUPY_VALUE = 5

MAX_OCCUPY = OCCUPY_VALUE * COLOR_LEVEL
LEVEL = [5,10,15,20]
# Define Color
kind_of_color = ["red", "blue", "green", "yellow", "orange"]
colorlist = {"blue":"#7BBFEA", "green":"#A3CF62", "yellow":"#FFE600", "red":"#F58F90", "orange":"#FAA755"}
basecolor = "#F8F8FF"

#left up right down
Direction = [[-1,0], [0,-1], [1,0], [0,1]]
# Direction = [[1,0], [-1,0], [0,1], [0,-1], [1,1], [-1,1], [1,-1], [-1,-1]]

def GetColor(color, value):
    level = 0
    for i in range(COLOR_LEVEL):
        level = i
        if value < LEVEL[i]:
            break
    return colorlist[color][level]


def ColorChange(value):
    return int((value+1)/OCCUPY_VALUE) != int(value/OCCUPY_VALUE)

def InitColorList():
    global colorlist
    list = {}
    for color in kind_of_color:
        colortype = []
        for i in range(1,COLOR_LEVEL+1):
            colortype.append(MixColor(colorlist[color],basecolor,i/COLOR_LEVEL))
        print(colortype)
        list[color] = colortype 
    colorlist = list
    
def MixColor(color1, color2, ratio):   
    mixcolor = "#"
    for i in range(3):
        c1 = "0x" + color1[i*2+1:i*2+3]
        c2 = "0x" + color2[i*2+1:i*2+3]
        # print(str(int(c1,16))+" "+str(int(c2,16)))
        result = int(int(c1,16)*ratio + int(c2,16)*(1-ratio))
        # print(c1+" + "+c2+ " = "+str(result))
        mixcolor += hex(result)[2:4]
        if result == 0:
            mixcolor += '0'
        # print(mixcolor)
    # print(color1+" + "+color2+" = "+mixcolor + " ratio = "+str(ratio))
    return mixcolor