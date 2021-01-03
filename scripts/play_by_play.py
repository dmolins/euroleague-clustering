import pandas as pd
import numpy

year = 18
season = pd.read_csv("/Users/dmolins/Desktop/david/uni/TFG/Europe/Euroleague_20{}.csv".format(year), sep = '|')
year = year + 1

def search_starters(player_team_inout):
    player_team_inout = player_team_inout.drop_duplicates(subset=['PLAYER']) #remove duplicates
    pOn_court = (player_team_inout[player_team_inout.PLAYTYPE=='OUT'])[['PLAYER', 'CODETEAM']]
    return pOn_court

def sums_shots_n_TO(all_players, row, pOn_court):
    if row.PLAYTYPE == '2FGA' or row.PLAYTYPE == '2FGM':
        pTYPE = 'T2A'
    elif row.PLAYTYPE == '3FGA' or row.PLAYTYPE == '3FGM':
        pTYPE = 'T3A'
    elif row.PLAYTYPE == 'FTA' or row.PLAYTYPE == 'FTM':
        pTYPE = 'TLA'
    elif row.PLAYTYPE == 'TO':
        pTYPE = 'TO'
        
    all_players.loc[all_players['PLAYER'] == row.PLAYER, '{}_j'.format(pTYPE)] = all_players.loc[all_players['PLAYER'] == row.PLAYER, '{}_j'.format(pTYPE)] + 1
    #sums also to each player team stat
    for index2, row2 in pOn_court.iterrows():
        if row.CODETEAM == row2.CODETEAM:
            all_players.loc[all_players['PLAYER'] == row2.PLAYER, '{}_e'.format(pTYPE)] = all_players.loc[all_players['PLAYER'] == row2.PLAYER, '{}_e'.format(pTYPE)] + 1
    return all_players

def order_name(row):
    if isinstance(row.PLAYER, str):
        p = row.PLAYER.split(', ')
        row.PLAYER = p[1] + ' ' + p[0]
        return row
    else:
        return row

#creates dataframe with the info for all the players
all_players = season[['PLAYER', 'CODETEAM']].drop_duplicates(subset = ['PLAYER'])
                #subdataframe                                                   #deletes first row (NaN)

zeros = numpy.zeros(len(all_players), dtype=int)
all_players = all_players.assign(Season = numpy.full(len(all_players), year, dtype=int), T2A_j = zeros, T2A_e = zeros,
                                 T3A_j = zeros, T3A_e = zeros, TLA_j = zeros, TLA_e = zeros, DREB_j = zeros, 
                                 DREB_t = zeros, OREB_j = zeros, OREB_t = zeros, TO_j = zeros, TO_e = zeros)
#j=jugador, e=equipo, t=total

#iterates over all the games of the season
for num_game in range(max(season.Game)+1): #DESCOMENTAR LUEGO

    game = season.loc[season.Game == num_game] #QUITAR LUEGO

    df = game[['PLAYER', 'CODETEAM', 'PLAYTYPE']]
    player_team_inout = df[(df.PLAYTYPE == 'IN') | (df.PLAYTYPE == 'OUT')]

    pOn_court = search_starters(player_team_inout) 

    for index, row in game.iterrows():
        if row.PLAYTYPE in ('2FGA', '2FGM', '3FGA', '3FGM', 'FTA', 'FTM', 'TO'):
            all_players = sums_shots_n_TO(all_players, row, pOn_court)

        elif row.PLAYTYPE == 'D':
            all_players.loc[all_players['PLAYER'] == row.PLAYER, 'DREB_j'] = all_players.loc[all_players['PLAYER'] == row.PLAYER, 'DREB_j'] + 1
            #sums also to each player team stat
            for index2, row2 in pOn_court.iterrows():
                if row.CODETEAM == row2.CODETEAM:
                    all_players.loc[all_players['PLAYER'] == row2.PLAYER, 'DREB_t'] = all_players.loc[all_players['PLAYER'] == row2.PLAYER, 'DREB_t'] + 1
                else:
                    all_players.loc[all_players['PLAYER'] == row2.PLAYER, 'OREB_t'] = all_players.loc[all_players['PLAYER'] == row2.PLAYER, 'OREB_t'] + 1

        elif row.PLAYTYPE == 'O':
            all_players.loc[all_players['PLAYER'] == row.PLAYER, 'OREB_j'] = all_players.loc[all_players['PLAYER'] == row.PLAYER, 'OREB_j'] + 1
            #sums also to each player team stat
            for index2, row2 in pOn_court.iterrows():
                if row.CODETEAM == row2.CODETEAM:
                    all_players.loc[all_players['PLAYER'] == row2.PLAYER, 'OREB_t'] = all_players.loc[all_players['PLAYER'] == row2.PLAYER, 'OREB_t'] + 1
                else:
                    all_players.loc[all_players['PLAYER'] == row2.PLAYER, 'DREB_t'] = all_players.loc[all_players['PLAYER'] == row2.PLAYER, 'DREB_t'] + 1

        elif row.PLAYTYPE == 'OUT':
            # Get name of indexe for the player who gets off the court
            indexNames = pOn_court[ pOn_court['PLAYER'] == row.PLAYER ].index
            # Delete these row indexes from dataFrame
            pOn_court.drop(indexNames , inplace=True)

        elif row.PLAYTYPE == 'IN':
            new_row = {'PLAYER': row.PLAYER, 'CODETEAM': row.CODETEAM}
            #append row to the dataframe
            pOn_court = pOn_court.append(new_row, ignore_index=True)
            
all_players_mod = all_players.apply(order_name, axis='columns')
all_players_mod.to_csv('/Users/dmolins/Desktop/david/uni/TFG/data/pbp-stats/Euroleague_pbp_{}.csv'.format(year), sep=';', index = False)