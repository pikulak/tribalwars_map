#AUTHOR: KACPER PIKULSKI
#pikulak1@gmail.com
#facebook.com/2plus2to3
from PIL import Image, ImageDraw,ImageFont, ImageFilter, ImageChops
import urllib.parse, urllib.request
from random import randint

im = Image.open("mapa_background.png")
draw = ImageDraw.Draw(im)
font_ally = ImageFont.truetype("arial.ttf",30)
font_pkt = ImageFont.truetype("arial.ttf",18)
pixels = im.load()
list_of_colors = {
    1:[255,255,255],
    2:[191,96,0],
    3:[64,255,0],
    4:[255,0,0],
    5:[0,0,255],
    6:[255,255,0],
    7:[255,0,255],
    8:[0,255,255],
    9:[61,41,0],
    10:[235,150,235],
    11:[150,250,0],
    12:[50,100,0],
    13:[28,150,134],
    14:[161,107,0],
    15:[0,51,0]    
}
#^ colors like id: R, G, B^

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 50.0, -1)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
#^ trim white spaces from image->https://stackoverflow.com/questions/1185524/how-to-trim-whitespace-including-tabs

def decode(s):
    return urllib.parse.unquote_plus(s)
#^ urldecode            

def load_players(world, nat):
    players_dir, headers = urllib.request.urlretrieve("https://"+nat+world+".plemiona."+nat+"/map/player.txt")
    players_in = open(players_dir)
    players = []
    for player in players_in:
        player = player.split(',')
        player[1] = decode(player[1])
        players.append(player)
    
    return players
#^ decode player name from urlencoded chars + new contener with player's informations   
    
def load_villages(world, nat):
    villages_dir, headers = urllib.request.urlretrieve("https://"+nat+world+".plemiona."+nat+"/map/village.txt")
    villages_in = open(villages_dir)
    villages = []
    for village in villages_in:
        village = village.split(',')
        village[1] = decode(village[1])
        if village[4]!='0':
            villages.append(village)
    
    return villages
#^ decode village name from urlencoded chars + new contener with village's informations   

def load_allies(world, nat):
    allies_dir, headers = urllib.request.urlretrieve("https://"+nat+world+".plemiona."+nat+"/map/ally.txt")
    allies_in = open(allies_dir)
    allies = {}
    for ally in allies_in:
        ally = ally.split(',')
        ally[1] = decode(ally[1])
        ally[2] = decode(ally[2])
        allies[ally[2]]=ally
    allies_in.close()
    
    return allies     
#^ decode ally name from urlencoded chars + new contener with ally's informations   
        
def load_top15_ally(allies):
    ally_15=[]
    for ally in allies:
        if 1<=int(allies[ally][7])<=15: #allies[ally][7] = rank of ally
            ally_15.append(allies[ally])
    
    return ally_15
       
def load_top15_players(players):
    player_15=[]
    for _player in players:
        if 1 <=int(_player[5]) <= 15: #_player[5] = rank of player
            player_15.append(_player)
    return player_15
    
def sort_allies(ally_15):
    ally_15 = sorted(ally_15,key=lambda ally: int(ally[7]))
    return ally_15
#^sorting...
    
def sort_players(player_15):
    player_15 = sorted(player_15,key=lambda player:int(player[5]))
    return player_15
#^sorting... 
    
def generate_player(villages, pixels, player_id,R,G,B):
    for _village in villages:
        if _village[4]==player_id:
            x = int(_village[2]) # convert from string
            y = int(_village[3]) # convert from string
            pixels[x,y] = (R,G,B)
            #^1x1^
            pixels[x+1,y] = (R,G,B)
            pixels[x+1,y-1] = (R,G,B)
            pixels[x,y-1] = (R,G,B)
            #^2x2^
            #pixels[x-1,y] = (R,G,B)
            #pixels[x-1,y-1] = (R,G,B)
            #pixels[x-1,y-2] = (R,G,B)
            #pixels[x,y-2] = (R,G,B)
            #pixels[x+1,y-2] = (R,G,B)
            #^3x3^ 
    return pixels
            
def generate_top15_players(villages, pixels, player_15):
    for player in player_15:
        player_id = player[0]
        R = randint(0,255)
        G = randint(0,255)
        B = randint(0,255)
        pixels = generate_player(villages,pixels, player_id,R,G,B)
    return pixels
        
def generate_top15_allies(villages, pixels, ally_15, families, players, allies, font_ally, font_pkt, draw):
    ally_text_y=70 # top margin 
    i=1 # id of color list
    for ally in ally_15:
        if ally[0]=='0': # if ally has been processed then skip it
            continue
        R = list_of_colors[i][0]
        G = list_of_colors[i][1]
        B = list_of_colors[i][2]
        i+=1
        ally_id = ally[0]
        ally_name = ally[2]
        ally_rank = int(ally[7])
        ally_pkt = int(ally[6])
        try:
            # if any ally relation
            ally_family = families[ally_name]
            ally_ids=[]
            ally_pkt=0
            ally_text=""
            for ally in ally_family:
                ally_text=ally_text+ally+"&" # generating an ally text like ally1&ally&
            ally_text=ally_text[:-1] # cut last &
            for ally in ally_family:
                ally_pkt += int(allies[ally][6]) # sum pkts
                ally_ids.append(allies[ally][0]) # make a list with related ally's
            for ally in ally_15: # zero the flag
                if ally[0]!=0 and ally[2] in ally_family:
                    ally[0]='0'
        except KeyError:
            ally_ids = ally_id
            ally_text = ally_name
            
        # put chars into map
        draw.text((0,ally_text_y),str(ally_rank) + ". " + ally_text,(R,G,B),font=font_ally)    
        draw.text((0,ally_text_y+30),str(ally_pkt)+"pkt.",(R,G,B),font=font_pkt)
        
        for _player in players:
            if _player[2]!='0' and _player[2] in ally_ids: # if it's player(or flag wasn't set) and player belong to family
                pixels = generate_player(villages, pixels, _player[0],R,G,B)
                _player[2]='0' 
        ally_text_y+=45 # transfer cursor into new line
    return pixels
                