#AUTHOR: KACPER PIKULSKI
#pikulak1@gmail.com
#facebook.com/2plus2to3
from funs import trim, load_players, load_villages, load_allies, load_top15_ally, load_top15_players, sort_allies, sort_players,generate_player,generate_top15_players,generate_top15_allies
from PIL import Image, ImageDraw,ImageFont, ImageFilter, ImageChops
#list of worlds...
worlds = ['101']
#fonts...
font_ally = ImageFont.truetype("arial.ttf",20)
font_pkt = ImageFont.truetype("arial.ttf",13)
#background...
im = Image.open("mapa_background.png")
#country...
nat = 'pl'
#families...
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
for world in worlds:
    try:
        families = families_all[world] # if any families...
    except KeyError:
        families = {} # if not then make empty list
    im_temp = Image.open("mapa_background.png")
    draw = ImageDraw.Draw(im_temp)
    pixels = im_temp.load()# making a pixel map
    players = load_players(world, nat) # loading players
    villages = load_villages(world, nat) # loading villages
    allies = load_allies(world, nat) # loading allies
    ally_15 = load_top15_ally(allies) # pull top15 allies
    ally_15 = sort_allies(ally_15) # sort top15 allies
    pixels = generate_top15_allies(villages, pixels, ally_15, families, players, allies, font_ally, font_pkt, draw) # generate map
    im_temp = trim(im_temp) # trim map
    im_temp.save('allies_'+world+'.png','PNG') # and save ;)