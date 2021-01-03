import cv2
import pandas as pd
import numpy

def sumar_regio(players, region, points, shooter):
    if points > 0:
        players.loc[players.PLAYER == shooter, region] += 1
    players.loc[players.PLAYER == shooter, region + '_A'] += 1

def order_name(row):
    if isinstance(row.PLAYER, str):
        p = row.PLAYER.split(', ')
        row.PLAYER = p[1] + ' ' + p[0]
        return row
    else:
        return row

#imatge amb les regions de tir
img = cv2.imread('../data/shot_chart/prova.png')
img_height, img_width, channels = img.shape

year = 18
shots = pd.read_csv('../Europe/Euroleague_Shots_20{}.csv'.format(year), sep = '|')
year += 1

dist_rim_side_line = 750
dist_rim_base_line = 157.5
dist_court_width = 1500
dist_court_height = 1400

offset_x = dist_rim_side_line * img_width/dist_court_width #distancia de la linia de banda a l'aro en pixels
offset_y = dist_rim_base_line * img_height/dist_court_height #distancia de l'aro a la linia de fons en pixels

players = shots[['PLAYER', 'TEAM']].drop_duplicates(subset = ['PLAYER']).sort_values(by='PLAYER')
games = shots[['PLAYER', 'Game']].groupby('PLAYER').Game.nunique()
zeros = numpy.zeros(len(players), dtype=int)
menys_u = numpy.ones(len(players), dtype=int)*(-1)
players = players.assign(Games = games.values ,Season = numpy.full(len(players), year, dtype=int), C3R = zeros, C3R_A = zeros, E3R = zeros, E3R_A = zeros, Ce3R = zeros, Ce3R_A = zeros, 
Ce3L = zeros, Ce3L_A = zeros, E3L = zeros, E3L_A = zeros, C3L = zeros, C3L_A = zeros, MBR = zeros, MBR_A = zeros, MER = zeros, MER_A = zeros, MEL = zeros, MEL_A = zeros, 
MBL = zeros, MBL_A = zeros, PR = zeros, PR_A = zeros, PC = zeros, PC_A = zeros, PL = zeros, PL_A = zeros)

shots = shots.loc[shots['ID_ACTION'] != 'FTM']

for index, shot in shots.iterrows():
    COORD_X = shot['COORD_X']
    COORD_Y = shot.loc['COORD_Y']

    """
    if "3" in shot['ID_ACTION']:
        color_point = (0,0,255) #red
    else:
        color_point = (255,0,0) #blue
    """
    
    #passem de cms a pixels
    PIXELS_X = COORD_X * img_width/dist_court_width
    PIXELS_Y = COORD_Y * img_height/dist_court_height

    value = img[img_height - round(PIXELS_Y + offset_y)-1][round(PIXELS_X + offset_x)-1]
    
    if (img_height - round(PIXELS_Y + offset_y)) < 0:
        region = 'OUT'
    elif value[0] == 15:
        region = 'PR'
    elif value[0] == 25:
        region = 'PC'
    elif value[0] == 35:
        region = 'PL'
    elif value[0] == 45:
        region = 'MBR'
    elif value[0] == 55:
        region = 'MBL'
    elif value[0] == 65:
        region = 'MER'
    elif value[0] == 75:
        region = 'MEL'
    elif value[0] == 85:
        region = 'C3R'
    elif value[0] == 95:
        region = 'C3L'
    elif value[0] == 105:
        region = 'E3R'
    elif value[0] == 115:
        region = 'E3L'
    elif value[0] == 125:
        region = 'Ce3R'
    elif value[0] == 135:
        region = 'Ce3L'
    else:
        region = 'OUT'
    
    """
    if color_point == (0,0,255) and '3' not in region and region != 'OUT':
        print("\nX: " + str(COORD_X))
        print("Y: " + str(COORD_Y))
        print("pixels X: " + str(round(PIXELS_X + offset_x)))
        print("pixels Y: " + str(img_height - round(PIXELS_Y + offset_y)))
        print(region)
        img = cv2.circle(img, (round(PIXELS_X + offset_x),img_height - round(PIXELS_Y + offset_y)), radius=0, color=color_point, thickness=2)

        cv2.imshow('image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        img = cv2.imread('../data/shot_chart/prova.png')

    """

    if region != 'OUT':
        sumar_regio(players, region, shot['POINTS'], shot['PLAYER'])

new_players = players.apply(order_name, axis='columns')
#new_players.to_csv('/Users/dmolins/Desktop/david/uni/TFG/data/shot_chart/Euroleague_shots{}.csv'.format(year), sep=';', index = False)