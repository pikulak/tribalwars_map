#AUTHOR: KACPER PIKULSKI
#pikulak1@gmail.com
#facebook.com/2plus2to3
from PIL import Image, ImageDraw,ImageFont, ImageFilter, ImageChops
import urllib.parse, urllib.request
from random import randint
import os
#^ trim white spaces from image->https://stackoverflow.com/questions/1185524/how-to-trim-whitespace-including-tabs
def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,10)))
    #diff = ImageChops.difference(im, bg)
    #diff = ImageChops.add(diff, diff, 50.0, -1)
    #bbox = diff.getbbox()
    #if bbox:
        #return im.crop(bbox)
    im.crop((100,100,100,100))
 
    return im
#^ urldecode 
def decode(s):
    return urllib.parse.unquote_plus(s)
   
class Map:
    colors = {
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
    domains = {
    'pl':'.plemiona.pl',
    'en':'.tribalwars.net',
    'de':'.die-staemme.de',
    'ch':'.staemme.ch',
    'us':'.tribalwars.us'
    }
    families_all = {
        '97':
        {
            'HNŁ': ['HNŁ','-HNŁ-'],
            '~~F~~': ['~~F~~','~F~'],
            'MzM': ['MzM','MzM.']
        },
        '101':
        {
            '.1.'   : ['.1.','.2.'],
            'PIEKŁO': ['PIEKŁO', 'NIEBO'],
            'PHLL'  : ['PHLL','PHLL.'],
            'IC'    : ['IC','IC!','IC.'],
            'Areams': ['Areams', 'Ar3ams'],
            'LDT'   : ['LDT', 'LOT'],
            'OMERTA': ['OMERTA','Om3rta']
        }
    }
    f_ally = ImageFont.truetype("arial.ttf",20)
    f_pkt = ImageFont.truetype("arial.ttf",13)
    
    def __init__(self, world, nat):
        self.domain = 'https://'+nat+world+self.domains[nat]
        self.world = world
        self.nat = nat
        self.im = Image.open("mapa_background.png")
        self.draw = ImageDraw.Draw(self.im)
        self.pixels = self.im.load()
        self.players = []
        self.villages = []
        self.allies = {}
        self.top15_allies = []
        self.top10_players = []
        try:
            self.families = self.families_all[world]
        except KeyError:
            self.families = {}
    def __exit__(self, *err):
        self.close()
    def __enter__(self):
        return self
    def close(self):
        del self.players[:]
        del self.villages[:]
        del self.top15_allies[:]
        del self.top10_players[:]
    def save_map(self, name):
        try:
            self.im.save(os.getcwd()+'/'+self.nat+self.world+'/'+name+'.png','PNG') # and save ;)
        except FileNotFoundError:
            os.mkdir(os.getcwd()+'/'+self.nat+self.world+'/')
            self.im.save(os.getcwd()+'/'+self.nat+self.world+'/'+name+'.png','PNG') # and save ;)
        
    def renew_map(self):
        self.im = Image.open("mapa_background.png")
        self.draw = ImageDraw.Draw(self.im)
        self.pixels = self.im.load()
        
    # decode player name from urlencoded chars + new contener with player's informations    
    def load_players(self):
        players_dir, headers = urllib.request.urlretrieve(self.domain+"/map/player.txt")
        players_in = open(players_dir)
        for player in players_in:
            player = player.split(',')
            player[1] = decode(player[1])
            self.players.append(player)  
        players_in.close()
        
    #^ decode village name from urlencoded chars + new contener with village's informations   
    def load_villages(self):
        villages_dir, headers = urllib.request.urlretrieve(self.domain+"/map/village.txt")
        villages_in = open(villages_dir)
        for village in villages_in:
            village = village.split(',')
            village[1] = decode(village[1])
            if village[4]!='0':
                self.villages.append(village)
        villages_in.close()
        
    #^ decode ally name from urlencoded chars + new contener with ally's informations       
    def load_allies(self):
        allies_dir, headers = urllib.request.urlretrieve(self.domain+"/map/ally.txt")
        allies_in = open(allies_dir)
        for ally in allies_in:
            ally = ally.split(',')
            ally[1] = decode(ally[1])
            ally[2] = decode(ally[2])
            self.allies[ally[2]]=ally
        allies_in.close()
    
    def load_top15_allies(self):
        for ally in self.allies:
            if 1 <= int(self.allies[ally][7]) <=15: #allies[ally][7] = rank of ally
                self.top15_allies.append(self.allies[ally])
    
    def load_top10_players(self):
        for player in self.players:
            if 1 <=int(player[5]) <= 10: #_player[5] = rank of player
                self.top10_players.append(player)
    
    def sort_allies(self):
        self.top15_allies = sorted(self.top15_allies,key=lambda ally: int(ally[7]))
        
    def sort_players(self):
        self.top10_players = sorted(self.top10_players, key=lambda player: int(player[5]))
    
    def generate_player(self, player_id, R, G, B, size=1):
        for village in self.villages:
            if village[4] == player_id:
                x = int(village[2]) # convert from string
                y = int(village[3]) # convert from string
                #^1x1^
                self.pixels[x,y] = (R,G,B)
                if size == 2:
                #^2x2^
                    self.pixels[x+1,y] = (R,G,B)
                    self.pixels[x+1,y-1] = (R,G,B)
                    self.pixels[x,y-1] = (R,G,B)
                #^3x3^
                #self.pixels[x-1,y] = (R,G,B)
                #self.pixels[x-1,y-1] = (R,G,B)
                #self.pixels[x-1,y-2] = (R,G,B)
                #self.pixels[x,y-2] = (R,G,B)
                #self.pixels[x+1,y-2] = (R,G,B)
                
    def generate_top10_players(self):
        print("[+]Trwa generowanie top10_players...")
        for player in self.top10_players:
            print (player)
        i = 1;
        for player in self.top10_players:
            player_id = player[0]
            R = self.colors[i][0]
            G = self.colors[i][1]
            B = self.colors[i][2]
    
            self.generate_player(player_id, R, G, B,2)
            i += 1
    
    def generate_top15_allies(self):
        ally_text_y = 70 # top margin 
        i = 1 # id of color list
        for ally in self.top15_allies:
        
            if ally[0]=='0': # if ally has been processed then skip it
                continue
                
            R = self.colors[i][0]
            G = self.colors[i][1]
            B = self.colors[i][2]
            i += 1
            ally_id = ally[0]
            ally_name = ally[2]
            #ally_rank = int(ally[7])
            #ally_pkt = int(ally[6])
            
            try:
                # if any ally relation
                ally_family = self.families[ally_name]
                ally_ids=[]
                ally_pkt=0
                ally_text=""
                for ally in ally_family:
                    ally_text=ally_text+ally+"&" # generating an ally text like ally1&ally&
                    
                ally_text=ally_text[:-1] # cut last &
                for ally in ally_family:
                    ally_pkt += int(self.allies[ally][6]) # sum pkts
                    ally_ids.append(self.allies[ally][0]) # make a list with related ally's
               
                for ally in self.top15_allies: # zero the flag
                    if ally[0]!=0 and ally[2] in ally_family:
                        ally[0]='0'
                        
            except KeyError:
                ally_ids = ally_id
                ally_text = ally_name
            
            # put chars into map
            #self.draw.text((0,ally_text_y),str(ally_rank) + ". " + ally_text,(R,G,B),font=self.f_ally)    
            #self.draw.text((0,ally_text_y+30),str(ally_pkt)+"pkt.",(R,G,B),font=self.f_pkt)
            ally_text_y+=45 # transfer cursor into new line
            for player in self.players:
                if player[2]!='0' and player[2] in ally_ids: # if it's player(or flag wasn't set) and player belong to family
                    self.generate_player(player[0],R,G,B,2) # player[0] = player_id
                    player[2]='0' 
                    
    def make_maps(self):
        self.load_players()
        self.load_allies()
        self.load_villages()
        self.load_top15_allies()
        self.load_top10_players()
        self.sort_allies()
        self.sort_players()
        self.generate_top10_players()
        self.im = trim(self.im)
        self.save_map('players')
        self.renew_map()
        self.generate_top15_allies()
        self.im = trim(self.im)
        self.save_map('allies')
        


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        