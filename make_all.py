from run import trim, load_players, load_villages, load_allies, load_top15_ally, load_top15_players, sort_allies, sort_players,generate_player,generate_top15_players,generate_top15_allies
from PIL import Image, ImageDraw,ImageFont, ImageFilter, ImageChops
worlds = ['101']
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
nat = 'pl'
im = Image.open("mapa_background.png")
font_ally = ImageFont.truetype("arial.ttf",20)
font_pkt = ImageFont.truetype("arial.ttf",13)
for world in worlds:
    try:
        families = families_all[world]
    except KeyError:
        families = {}
    im_temp = Image.open("mapa_background.png")
    draw = ImageDraw.Draw(im_temp)
    pixels = im_temp.load()
    players = load_players(world, nat)
    villages = load_villages(world, nat)
    allies = load_allies(world, nat)
    ally_15 = load_top15_ally(allies)
    ally_15 = sort_allies(ally_15)
    pixels = generate_top15_allies(villages, pixels, ally_15, families, players, allies, font_ally, font_pkt, draw)
    im_temp = trim(im_temp)
    im_temp.save('allies_'+world+'.png','PNG')