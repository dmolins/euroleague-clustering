import csv
import numpy as np
import pandas as pd
import itertools
from collections import Counter
from itertools import chain

#strCompetitions = ['Euroleague','Eurocup']
strCompetitions = ['Euroleague']

def readPlayByPlay(folder,yearBeg,yearFin):
    lYear = []
    lTeam = [] #0
    lTime = [] #3
    lMinute = [] #4
    lNumberOfPlay = [] #5
    lPlayer = [] #6
    lPlay = [] #8
    lPointsA = [] #10
    lPointsB = [] #12
    locTeam = [] # 14
    visTeam = [] # 15
    idGame = [] # 16
    lastPtsA = 0
    lastPtsB = 0

    for iYear in range(yearBeg, yearFin):
        print(str(iYear))
        if iYear == 2017:
            a = 1
        for iCompetition in range(0,len(strCompetitions)):
            print(strCompetitions[iCompetition])
            fileShots = folder + strCompetitions[iCompetition] + '_' + str(iYear) + '.csv'
            bFirst = True
            with open(fileShots, 'rt', encoding='utf-8') as csvfile:
                spamreader = csv.reader(csvfile, delimiter='|')
                for row in spamreader:
                    if bFirst:
                        bFirst = False
                    else:
                        lYear.append(iYear)
                        lTeam.append(row[0].replace(' ','')) # 0
                        lTime.append(row[3])  # 3
                        lMinute.append(int(row[4]))  # 4
                        lNumberOfPlay.append(int(row[5])) # 5
                        lPlayer.append(row[6])  # 6
                        lPlay.append(row[9].replace(' ',''))  # 8
                        try:
                            lPointsA.append(int(float(row[11])))  # 10
                            lastPtsA = int(float(row[11]))
                        except:
                            if int(float(row[17])) == idGame[-1]:
                                lPointsA.append(lastPtsA)
                            else:
                                lPointsA.append(0)
                                lastPtsA = 0
                        try:
                            lPointsB.append(int(float(row[13])))  # 12
                            lastPtsB = int(float(row[13]))
                        except:
                            if int(float(row[17])) == idGame[-1]:
                                lPointsB.append(lastPtsB)
                            else:
                                lPointsB.append(0)
                                lastPtsB = 0
                        locTeam.append(row[15])  # 14
                        visTeam.append(row[16]) # 15
                        idGame.append(int(float(row[17])))  # 16

    # intialise data of lists.
    data = {'Year': lYear, 'Team': lTeam, 'Clock': lTime, 'Minute': lMinute, 'nPlay': lNumberOfPlay, 'Player':lPlayer, 'Action':lPlay, 'PointsA':lPointsA, 'PointsB':lPointsA, 'locTeam':locTeam, 'visTeam':visTeam, 'Game': idGame}
    df = pd.DataFrame(data)
    df.to_pickle(folder + "PBP" + str(yearBeg) + "-" +  str(yearFin-1) + "EL.pkl")

def find5Court(team, playerN, action, game, locTeam, visTeam, indGames, year):
    player = np.copy(playerN)
    teamA = []
    teamB = []
    iPlayer = 0
    nGames = 0

    while iPlayer < len(player):
        if game[iPlayer-1] != game[iPlayer]:
            if nGames > 0:
                #print('Game: ' + str(nGames))
                teamA = fillIncomplete(teamA, indGames[nGames])
                teamB = fillIncomplete(teamB, indGames[nGames])
            if year[iPlayer-1] != year[iPlayer]:
                print(year[iPlayer])
            nGames += 1
            sLocT = locTeam[iPlayer]
            sVisT = visTeam[iPlayer]
            indLoc = iPlayer
            indVis = iPlayer
            bNewLoc = True
            iTimesLoc = 0
            bNewVis = True
            iTimesVis = 0
            inPlLoc = 'A'
            outPlLoc = 'B'
            inPlVis = 'C'
            outPlVis = 'D'
            lineupLoc = []
            lineupVis = []

        if action[iPlayer] == 'IN' or action[iPlayer] == 'OUT':
            if team[iPlayer] == sLocT:
                inPlLoc, outPlLoc, indLoc, lineupLoc, iPlayer, teamA, inPlLoc, outPlLoc, bNewLoc = buildLineup(iPlayer, bNewLoc, action, player, team, sLocT, indLoc, inPlLoc, outPlLoc, lineupLoc, teamA, iTimesLoc)
                iTimesLoc += 1
            else:
                inPlVis, outPlVis, indVis, lineupVis, iPlayer, teamB, inPlVis, outPlVis, bNewVis = buildLineup(iPlayer, bNewVis, action, player, team, sVisT, indVis, inPlVis, outPlVis, lineupVis, teamB, iTimesVis)
                iTimesVis += 1
        iPlayer += 1

    teamA = fillIncomplete(teamA, len(team))
    teamB = fillIncomplete(teamB, len(team))
    np.save('/Users/arbues/Documents/DataBasketball/Europe/PlayByPlay/Locals.npy',teamA)
    np.save('/Users/arbues/Documents/DataBasketball/Europe/PlayByPlay/Visitants.npy',teamB)

def permutePlayers(allLineups, allTeams, sFolder, nPlayers):
    positionN = range(0, 5)
    sortedPlayers = list(itertools.combinations(positionN, nPlayers))
    lPerm = []
    lTeamsPerm = []
    for iLineup in range(0, len(allLineups)):
        for iPerm in range(0, len(sortedPlayers)):
            permutInd = []
            for iLen in range(0, nPlayers):
                permutInd.append(allLineups[iLineup][sortedPlayers[iPerm][iLen]])
            lPerm.append(permutInd)
            lTeamsPerm.append(allTeams[iLineup])

    uniquePerm = [list(x) for x in set(tuple(x) for x in lPerm)]
    uniqueTeam = []
    print(str(len(uniquePerm)))
    for iPerm in range(0, len(uniquePerm)):
        uniqueTeam.append(lTeamsPerm[lPerm.index(uniquePerm[iPerm])])
    np.save(sFolder + "PermPlayers" + str(nPlayers) + ".npy", uniquePerm)
    np.save(sFolder + "PermTeams" + str(nPlayers) + ".npy", uniqueTeam)

def findUniques(locLineup, team):
    uniqueLineupsLocNoise, indPos = np.unique(locLineup, return_index=True)
    uniqueLineupsLoc = []
    uniqueLineupsPos = []
    teamVec = []
    for iLin in range(0, len(uniqueLineupsLocNoise)):
        if 'UNKNOWN' not in uniqueLineupsLocNoise[iLin] and (len(uniqueLineupsLocNoise[iLin]) == 5 or (len(uniqueLineupsLocNoise[iLin]) == 6 and  uniqueLineupsLocNoise[iLin][0] == '')):
            if uniqueLineupsLocNoise[iLin][0] == '':
                uniqueLineupsLoc.append(list(uniqueLineupsLocNoise[iLin][1:]))
                #uniqueLineupsLocNoise[iLin] = uniqueLineupsLocNoise[iLin][1:]
            else:
                uniqueLineupsLoc.append(list(uniqueLineupsLocNoise[iLin]))
            uniqueLineupsPos.append(indPos[iLin])
            teamVec.append(team[indPos[iLin]+1])
    return uniqueLineupsLoc,teamVec


def readPIPM(folder, yearBeg, yearFin, league):
    lPlayer = []
    lMinutes = []
    lOPIPM = []
    lDPIPM = []
    lPIPM = []
    lWa = []
    lYear = []
    file = folder + league + '.csv'
    bFirst = True

    with open(file, 'rt', encoding='utf-8') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    if bFirst:
                        bFirst = False
                    else:
                        if int(row[6]) >= yearBeg and int(row[6]) < yearFin:
                            if row[0] == 'Ante Tomic' and int(row[6]) == 2020:
                                a = 1
                            lPlayer.append(row[0])
                            lMinutes.append(float(row[1].replace(',','')))
                            lOPIPM.append(float(row[2].replace('p','')))
                            lDPIPM.append(float(row[3].replace('p','')))
                            lPIPM.append(float(row[4].replace('p','')))
                            lWa.append(float(row[5]))
                            lYear.append(int(row[6]))

    return lPlayer, lMinutes, lOPIPM, lDPIPM, lPIPM, lWa, lYear

def readDunks(folder,yearBeg,yearFin):
    lYear = []
    lDunks = []
    lAssisted = []
    lPlayer = []

    for iYear in range(yearBeg, yearFin):
        print(str(iYear))
        for iCompetition in range(0,len(strCompetitions)):
            print(strCompetitions[iCompetition])
            fileShots = folder + strCompetitions[iCompetition] + '_' + str(iYear) + '.csv'
            bFirst = True
            bDunk = False
            posPrev = 0
            with open(fileShots, 'rt', encoding='utf-8') as csvfile:
                spamreader = csv.reader(csvfile, delimiter='|')
                for row in spamreader:
                    if bFirst:
                        bFirst = False
                    else:
                        if bDunk:
                            if row[9].replace(' ', '') == 'AS':
                                lAssisted[posPrev] = lAssisted[posPrev]+1
                            bDunk = False
                        else:
                            if row[9].replace(' ','') == 'DUNK':
                                bDunk = True
                                if row[6] not in lPlayer:
                                    lPlayer.append(row[6])
                                    lDunks.append(1)
                                    lAssisted.append(0)
                                    posPrev = len(lPlayer)-1
                                else:
                                    posPrev = lPlayer.index((row[6]))
                                    lDunks[posPrev] = lDunks[posPrev]+1

    np.save(folder + 'dunks.npy', lDunks)
    np.save(folder + 'dunksAs.npy', lAssisted)
    np.save(folder + 'dunkPlay.npy', lPlayer)
    return lDunks, lAssisted, lPlayer

def getGamesDunkers(folder,yearBeg,yearFin):
    lPlayers = list(np.load(folder + 'dunkPlay.npy'))
    lGames = np.zeros(len(lPlayers))
    lLastGame = np.zeros(len(lPlayers))
    for iYear in range(yearBeg, yearFin):
        print(str(iYear))
        for iCompetition in range(0,len(strCompetitions)):
            print(strCompetitions[iCompetition])
            fileShots = folder + strCompetitions[iCompetition] + '_' + str(iYear) + '.csv'
            bFirst = True
            bDunk = False
            posPrev = 0
            with open(fileShots, 'rt', encoding='utf-8') as csvfile:
                spamreader = csv.reader(csvfile, delimiter='|')
                for row in spamreader:
                    if bFirst:
                        bFirst = False
                    else:
                        if row[6] in lPlayers:
                            posPl = lPlayers.index(row[6])
                            if lLastGame[posPl] != int(float(row[17])):
                                lGames[posPl] = lGames[posPl]+1
                                lLastGame[posPl] = int(float(row[17]))
    np.save(folder + 'dunksGames.npy', lGames)
    return lGames

def readRebPer(folder,yearBeg,yearFin):
    lYear = []
    ofRebs2 = []
    defRebs2 = []
    ofRebs3 = []
    defRebs3 = []
    #lMiss2 = ['2FGA', '2FGAB', 'LAYUPATT']
    lMiss2 = ['2FGA', '2FGAB']
    lMiss3 = ['3FGA', '3FGAB']

    for iYear in range(yearBeg, yearFin):
        iDefRebs2 = 0
        iOfRebs2 = 0
        iDefRebs3 = 0
        iOfRebs3 = 0
        print(str(iYear))
        if iYear == 2017:
            a = 1
        for iCompetition in range(0,len(strCompetitions)):
            print(strCompetitions[iCompetition])
            fileShots = folder + strCompetitions[iCompetition] + '_' + str(iYear) + '.csv'
            bFirst = True
            bMissed2 = False
            bMissed3 = False
            with open(fileShots, 'rt', encoding='utf-8') as csvfile:
                spamreader = csv.reader(csvfile, delimiter='|')
                for row in spamreader:
                    if bFirst:
                        bFirst = False
                    else:
                        if bMissed2:
                            if row[9].replace(' ','') == 'O':
                                iOfRebs2 += 1
                            elif row[9].replace(' ','') == 'D':
                                iDefRebs2 += 1
                            bMissed2 = False
                        elif bMissed3:
                            if row[9].replace(' ','') == 'O':
                                iOfRebs3 += 1
                            elif row[9].replace(' ','') == 'D':
                                iDefRebs3 += 1
                            bMissed3 = False
                        else:
                            if row[9].replace(' ','') in lMiss2:
                                bMissed2 = True
                            elif row[9].replace(' ','') in lMiss3:
                                bMissed3 = True
            ofRebs2.append(iOfRebs2)
            ofRebs3.append(iOfRebs3)
            defRebs2.append(iDefRebs2)
            defRebs3.append(iDefRebs3)
    np.save(folder + 'ofRebs2.npy', ofRebs2)
    np.save(folder + 'ofRebs3.npy', ofRebs3)
    np.save(folder + 'defRebs2.npy', defRebs2)
    np.save(folder + 'defRebs3.npy', defRebs3)
    return ofRebs2, ofRebs3, defRebs2, defRebs3

def buildLineup(iPlayer, bNew, action, player, team, sTagT, ind, inPl, outPl, lineup, teamV, iTimes):
    nChanges = 0
    bAhead = True

    for iAux in range(0, 20):
        if (action[iPlayer + iAux] == 'IN' or action[iPlayer + iAux] == 'OUT') and team[iPlayer + iAux] == sTagT:
            nChanges += 1
        else:
            break

    iOffset = 0

    if np.mod(nChanges,2) == 1 and nChanges != 1:
        for iAux in range(nChanges+1, 20):
            if (action[iPlayer + iAux] == 'IN' or action[iPlayer + iAux] == 'OUT') and team[iPlayer + iAux] == sTagT:
                nChanges += 1
                iOffset = 1
            else:
                break
    elif nChanges == 1:
        if action[iPlayer] == 'IN':
            for iAux in range(nChanges+1, 20):
                if (action[iPlayer + iAux] == 'OUT' and team[iPlayer + iAux] == sTagT):
                    nChanges += 1
                    iOffset += 1
                    break
                elif action[iPlayer + iAux] == 'IN':
                    bAhead = False
                    break
                else:
                    iOffset += 1

    nChanges = nChanges / 2

    if iOffset == 18:
        bAhead = False
        inPl = []
        outPl = []

    if bAhead:
        try:
            if bNew == False:
                teamV = appendPlayers(iPlayer, ind, inPl, outPl, lineup, teamV)
            else:
                appendPlayersFirst(player, team, ind, sTagT, iPlayer, teamV)
                bNew = False
            bEmergency = False
        except:
            if bNew == False:
                appendEmergency(iPlayer, ind, inPl, outPl, lineup, teamV)
                bEmergency = True
            pass

        if nChanges == 1:
            iAdd = 1
            inPl, outPl = findMultPlayerInOut(team, action, player, sTagT, iPlayer, inPl, outPl, nChanges, iOffset)
        else:
            iAdd = int(nChanges * 2)-1
            inPl, outPl = findMultPlayerInOut(team, action, player, sTagT, iPlayer, inPl, outPl, nChanges, iOffset)

        if ind != iPlayer:
            if bEmergency:
                if len(teamV[-1]) > 5:
                    lineup = quitSusp(teamV[-1],ind,player,iPlayer)
            else:
                lineup = quitSpace(teamV[-1])
        else:
            lineup = []
            for iUnk in range(0,5):
                lineup.append('UNKNOWN')

        if len(inPl) > 1 and len(outPl) == 1:
            inPl = quitIn(inPl,ind,player,iPlayer)

        ind = iPlayer
        iPlayer = iPlayer + iAdd + iOffset

    return inPl, outPl, ind, lineup, iPlayer, teamV, inPl, outPl, bNew

def quitSpace(lineup):
    lineupR = []
    for iPlaux in range(0, len(lineup)):
        if lineup[iPlaux] != '':
            lineupR.append(lineup[iPlaux])
    return lineupR

def quitSusp(lineup,ind,player,iPlayer):
    pastPlayers = player[ind:iPlayer]
    lineupR = []
    for iPlaux in range(0,len(lineup)):
        if lineup[iPlaux] in pastPlayers:
            lineupR.append(lineup[iPlaux])
    if len(lineupR) == 5:
        return lineupR
    else:
        return lineup

def quitIn(inPl,ind,player,iPlayer):
    pastPlayers = player[ind:iPlayer]
    inPlR = []
    for iPlaux in range(0,len(inPl)):
        if inPl[iPlaux] not in pastPlayers:
            inPlR.append(inPl[iPlaux])
    if len(inPlR) == 1:
        return inPlR
    else:
        futPlayers = player[iPlayer:iPlayer+50]
        inPlR = []
        for iPlaux in range(0, len(inPl)):
            if inPl[iPlaux] in futPlayers:
                inPlR.append(inPl[iPlaux])
        if len(inPlR) == 1:
            return inPlR
        else:
            return inPl[0]


def fillIncomplete(teamV, indGamesVal):
    if len(teamV) < indGamesVal:
        iMiss = indGamesVal - len(teamV)
        lineupAux = teamV[-1]
        for iComp in range(0, iMiss):
            teamV.append(lineupAux)
    return teamV

def appendEmergency(iPlayer, indGame, inPlayer, outPlayer, lineup, teamV):
    lineupAux = list(np.copy(lineup))
    for iPlAux in range(0, min(len(inPlayer),len(outPlayer))):
        if outPlayer[iPlAux] not in lineupAux:
            lineupAux.append(inPlayer[iPlAux])
        else:
            lineupAux[lineupAux.index(outPlayer[iPlAux])] = inPlayer[iPlAux]

    for iTimes in range(0, (iPlayer - indGame)):
        teamV.append(lineupAux)
    return teamV

def appendPlayers(iPlayer, indGame, inPlayer, outPlayer, lineup, teamV):
    lineupAux = list(np.copy(lineup))
    if len(inPlayer) == 1:
        try:
            lineupAux[lineup.index(outPlayer[0])] = inPlayer[0]
        except:
            try:
                lineupAux[lineup.index('UNKNOWN')] = inPlayer[0]
            except:
                lineupAux[lineup.index('')] = inPlayer[0]
    else:
        for iPlAux in range(0, len(inPlayer)):
            try:
                lineupAux[lineup.index(outPlayer[iPlAux])] = inPlayer[iPlAux]
            except:
                try:
                    lineupAux[lineup.index('UNKNOWN')] = inPlayer[iPlAux]
                except:
                    lineupAux[lineup.index('')] = inPlayer[iPlAux]

    lineupAux = list(np.sort(lineupAux))
    for iTimes in range(0, (iPlayer - indGame)):
        teamV.append(lineupAux)
    return teamV

def findPlayerInOut(team,action,player,ind,iPlayer,inPlayer,outPlayer):
    bFound = False
    prevIn = inPlayer
    prevOut = outPlayer
    indAux = iPlayer
    while bFound == False:
        if action[indAux] == 'IN' and team[indAux] == ind and player[indAux] != 'o':
            inPlayer = player[indAux]
            #player[indAux] = 'o'
        elif action[indAux] == 'OUT' and team[indAux] == ind and player[indAux] != 'o':
            outPlayer = player[indAux]
            #player[indAux] = 'o'

        if prevIn != inPlayer and prevOut != outPlayer:
            bFound = True
        else:
            indAux += 1
    return inPlayer, outPlayer

def findMultPlayerInOut(team,action,player,ind,iPlayer,inPlayer,outPlayer,nChanges, offset):
    inPlayer = []
    inPlayerB = []
    outPlayer = []
    outPlayerB = []
    for indAux in range(iPlayer, int(iPlayer + nChanges*2 + offset)):
        if action[indAux] == 'IN' and team[indAux] == ind and player[indAux] != 'o':
            inPlayer.append(player[indAux])
            #player[indAux] = 'o'
        elif action[indAux] == 'OUT' and team[indAux] == ind and player[indAux] != 'o':
            outPlayer.append(player[indAux])
            #player[indAux] = 'o'
    if len(set(inPlayer) & set(outPlayer)) > 0:
        quitNames = set(inPlayer) & set(outPlayer)
        for iPaux in range(0, len(inPlayer)):
            if inPlayer[iPaux] not in quitNames:
                inPlayerB.append(inPlayer[iPaux])
        for iPaux in range(0, len(outPlayer)):
            if outPlayer[iPaux] not in quitNames:
                outPlayerB.append(outPlayer[iPaux])
    else:
        inPlayerB = inPlayer
        outPlayerB = outPlayer

    return inPlayerB, outPlayerB


def appendPlayersFirst(player, team, indGame, iTag, iPlayer, teamV):
    allPl = player[indGame:iPlayer-1]
    allTeam = team[indGame:iPlayer-1]
    posTeam = allTeam == iTag
    playersUnique = list(np.sort(np.unique(allPl[posTeam])))
    if len(playersUnique) < 5:
        for iUnk in range(0,5-len(playersUnique)):
            playersUnique.append('UNKNOWN')
    if len(playersUnique) == 5 and '' in playersUnique:
        playersUnique[playersUnique.index('')] = 'UNKNOWN'
        playersUnique = list(np.sort(playersUnique))

    for iTimes in range(0, iPlayer - indGame):
        teamV.append(playersUnique)

def readShotchartsInd(folder,yearBeg,yearFin):
    lYear = []
    lAction = []
    lConsole = []
    lCoordX = []
    lCoordY = []
    lIdAction = []
    lIdPlayer = []
    lNum = []
    lPlayer = []
    lTeam = []
    lGame = []

    iInPlayer = 0

    for iYear in range(yearBeg, yearFin):
        print(str(iYear))
        for iCompetition in range(0,len(strCompetitions)):
            print(strCompetitions[iCompetition])
            fileShots = folder + strCompetitions[iCompetition] + '_Shots_' + str(iYear) + '.csv'
            bFirst = True
            with open(fileShots, 'rt', encoding='utf-8') as csvfile:
                spamreader = csv.reader(csvfile, delimiter='|')
                for row in spamreader:
                    if bFirst:
                        bFirst = False
                    else:
                        if row[9] in lPlayer:
                            posPlayer = lPlayer.index(row[9])
                            lYear[posPlayer].append(iYear)
                            #lAction[posPlayer].append(row[0])
                            #lConsole[posPlayer].append(row[1])
                            lCoordX[posPlayer].append(float(row[2]))
                            lCoordY[posPlayer].append(float(row[3]))
                            lIdAction[posPlayer].append(row[5].replace(' ',''))
                            #lIdPlayer[posPlayer].append(row[6].replace(' ',''))
                            #lNum[posPlayer].append(int(row[8]))
                            lTeam[posPlayer].append(row[15].replace(' ',''))
                            lGame[posPlayer].append(row[18])
                        else:
                            lYear.append([])
                            lYear[iInPlayer].append(iYear)
                            lPlayer.append(row[9])
                            #lAction.append([])
                            #lAction[iInPlayer].append(row[0])
                            #lConsole.append([])
                            #lConsole[iInPlayer].append(row[1])
                            lCoordX.append([])
                            lCoordX[iInPlayer].append(float(row[2]))
                            lCoordY.append([])
                            lCoordY[iInPlayer].append(float(row[3]))
                            lIdAction.append([])
                            lIdAction[iInPlayer].append(row[5].replace(' ',''))
                            lIdPlayer.append([])
                            #lIdPlayer[iInPlayer].append(row[6].replace(' ',''))
                            #lNum.append([])
                            #lNum[iInPlayer].append(int(row[8]))
                            lTeam.append([])
                            lTeam[iInPlayer].append(row[15].replace(' ',''))
                            lGame.append([])
                            lGame[iInPlayer].append(row[18])
                            iInPlayer += 1

    lGameCop = np.copy(lGame)
    realGames = np.zeros((1,len(lGameCop)))

    for iPlayer in range(0, len(lPlayer)):
        totGames = 0
        for iGame in range(1, len(lGameCop[iPlayer])):
            if lGameCop[iPlayer][iGame] != lGameCop[iPlayer][iGame-1]:
                totGames += 1
        realGames[0,iPlayer] = totGames

    # for iPlayer in range(0, len(lGameCop)):
    #     lGameCop[iPlayer] = len(np.unique(lGameCop[iPlayer]))

    data = {'Year': lYear, 'CoordX': lCoordX, 'CoordY':lCoordY, 'IDAction':lIdAction, 'Player': lPlayer, 'Games':realGames[0], 'Team':lTeam, 'NGames':lGame}
    df = pd.DataFrame(data)
    df.to_pickle(folder + "IndShots" + str(yearBeg) + "-" + str(yearFin - 1) + "EL.pkl")
    return lPlayer, lCoordX, lCoordY, lIdAction, lGame

def readShotcharts(folder,yearBeg,yearFin):
    lYear = []
    lAction = []
    lConsole = []
    lCoordX = []
    lCoordY = []
    lFastbreak = []
    lIdAction = []
    lIdPlayer = []
    lMinute = []
    lNum = []
    lPlayer = []
    lPoints = []
    lPointsA = []
    lPointsB = []
    lPointsTur = []
    l2nChance = []
    lTeam = []
    lGame = []
    lSuccess = []

    for iYear in range(yearBeg, yearFin):
        print(str(iYear))
        for iCompetition in range(0,len(strCompetitions)):
            print(strCompetitions[iCompetition])
            fileShots = folder + strCompetitions[iCompetition] + '_Shots_' + str(iYear) + '.csv'
            bFirst = True
            with open(fileShots, 'rt', encoding='utf-8') as csvfile:
                spamreader = csv.reader(csvfile, delimiter='|')
                for row in spamreader:
                    if bFirst:
                        bFirst = False
                    else:
                        lYear.append(iYear)
                        lAction.append(row[0])
                        if row[0][:6] == 'MISSED':
                            lSuccess.append(False)
                        else:
                            lSuccess.append(True)
                        lConsole.append(row[1])
                        lCoordX.append(float(row[2]))
                        lCoordY.append(float(row[3]))
                        try:
                            lFastbreak.append(bool(row[4]))
                        except:
                            lFastbreak.append(False)
                        lIdAction.append(row[5].replace(' ',''))
                        lIdPlayer.append(row[6].replace(' ',''))
                        lMinute.append(int(row[7]))
                        lNum.append(int(row[8]))
                        lPlayer.append(row[9])
                        lPoints.append(int(row[10]))
                        lPointsA.append(int(row[11]))
                        lPointsB.append(int(row[12]))
                        try:
                            lPointsTur.append(int(row[13]))
                        except:
                            lPointsTur.append(0)
                        try:
                            l2nChance.append(int(row[14]))
                        except:
                            l2nChance.append(0)
                        lTeam.append(row[15].replace(' ',''))
                        lGame.append(row[18])
    # intialise data of lists.
    data = {'Year': lYear, 'Action': lAction, 'Success': lSuccess, 'Clock': lConsole, 'CoordX': lCoordX, 'CoordY':lCoordY, 'Fastbreak':lFastbreak, 'IDAction':lIdAction, 'Team':lTeam, 'IDPlayer':lIdPlayer, 'Player': lPlayer, 'Points':lPoints, 'Minute':lMinute, 'Number':lNum, 'Game':lGame, 'PointsA': lPointsA, 'PointsB':lPointsB, 'PointsTur':lPointsTur, 'Points2ndCh':l2nChance }
    df = pd.DataFrame(data)
    df.to_pickle(folder + "Shotcharts" + str(yearBeg) + "-" +  str(yearFin-1) + "EL.pkl")

