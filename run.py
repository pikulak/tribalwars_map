from PIL import Image, ImageDraw,ImageFont, ImageFilter, ImageChops
import urllib.parse, urllib.request
from random import randint
im = Image.open("mapa_background.png")
draw = ImageDraw.Draw(im)
font_ally = ImageFont.truetype("arial.ttf",30)
font_pkt = ImageFont.truetype("arial.ttf",18)
pixels = im.load()
families = {
    'HNŁ': ['HNŁ','-HNŁ-'],
    '~~F~~': ['~~F~~','~F~'],
    'MzM': ['MzM','MzM.']
}
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
def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 50.0, -1)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
def decode(s):
    return urllib.parse.unquote_plus(s)
            
def load_players(world, nat):
    players_dir, headers = urllib.request.urlretrieve("https://"+nat+world+".plemiona."+nat+"/map/player.txt")
    players_in = open(players_dir)
    players = []
    for player in players_in:
        player = player.split(',')
        player[1] = decode(player[1])
        players.append(player)
    
    return players
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
        
def load_top15_ally(allies):
    ally_15=[]
    for ally in allies:
        if 1<=int(allies[ally][7])<=15:
            ally_15.append(allies[ally])
    
    return ally_15
       
def load_top15_players(players):
    player_15=[]
    for _player in players:
        if 1 <=int(_player[5]) <= 15:
            player_15.append(_player)
    return player_15
    
def sort_allies(ally_15):
    ally_15 = sorted(ally_15,key=lambda ally: int(ally[7]))
    return ally_15
    
def sort_players(player_15):
    player_15 = sorted(player_15,key=lambda player:int(player[5]))
    return player_15
    
def generate_player(villages, pixels, player_id,R,G,B):
    for _village in villages:
        if _village[4]==player_id:
            x = int(_village[2])
            y = int(_village[3])
            pixels[x,y] = (R,G,B)
            pixels[x+1,y] = (R,G,B)
            pixels[x+1,y-1] = (R,G,B)
            pixels[x,y-1] = (R,G,B)
            #pixels[x-1,y] = (R,G,B)
            #pixels[x-1,y-1] = (R,G,B)
            #pixels[x-1,y-2] = (R,G,B)
            #pixels[x,y-2] = (R,G,B)
            #pixels[x+1,y-2] = (R,G,B)
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
    ally_text_y=70
    i=1
    for ally in ally_15:
        if ally[0]=='0':
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
            ally_family = families[ally_name]
            ally_ids=[]
            ally_pkt=0
            ally_text=""
            for ally in ally_family:
                ally_text=ally_text+ally+"&"
            ally_text=ally_text[:-1]
            for ally in ally_family:
                ally_pkt += int(allies[ally][6])
                ally_ids.append(allies[ally][0])
            for item in ally_15:
                if item[0]!=0 and item[2] in ally_family:
                    item[0]='0'
        except KeyError:
            ally_ids = ally_id
            ally_text = ally_name
        draw.text((0,ally_text_y),str(ally_rank) + ". " + ally_text,(R,G,B),font=font_ally)    
        draw.text((0,ally_text_y+30),str(ally_pkt)+"pkt.",(R,G,B),font=font_pkt)
        for _player in players:
            if _player[2]!='0' and _player[2] in ally_ids:
                pixels = generate_player(villages, pixels, _player[0],R,G,B)
                _player[2]='0'
        ally_text_y+=45
    return pixels
                
#im = trim(im)
#im.save("mapka.png","PNG")