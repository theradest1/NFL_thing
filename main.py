import random
import itertools
from operator import itemgetter
import math

#hey (;

def setPoints():
  for teamStats in allTeamStats:
    teamStats[1] = random.randrange(50) #input(teamStats[0]+ "'s points: ")

def topCombinations():
  combinationPoints = []
  topPlayers = []
  ii = 0
  for combination in usedCombinations:
    i = 0
    for j in range(3):
      i += allTeamStats[combination[j]][1]
    combinationPoints.append(i + ii/10000)
    ii += 1
  combinationPoints.sort(reverse = True)
  i = 0
  j = 0
  #print(combinationPoints)
  while j <= 2:
    topPlayers.append(combinationPoints[i])
    if int(combinationPoints[i]) == int(combinationPoints[i + 1]):
      print(int(combinationPoints[i]))
      j -= 1
    i += 1
    j += 1
  return topPlayers, combinationPoints

def displayTop():
    print("")
    print("")
    #print("player ID, Points, (team1: points, team2: points, team3: points)")
    team1points = team2points = team3points = 5
    team1 = team2 = team3 = "example team"
    i = 0
    print(usedCombinations)
    for player in topPlayers:
        ID = int(math.modf(player)[0] * 10000)
        team1points = allTeamStats[usedCombinations[ID][0]][1]
        team1 = allTeamStats[usedCombinations[ID][0]][0]
        team2points = allTeamStats[usedCombinations[ID][1]][1]
        team2 = allTeamStats[usedCombinations[ID][1]][0]
        team3points = allTeamStats[usedCombinations[ID][2]][1]
        team3 = allTeamStats[usedCombinations[ID][2]][0]
        print("")
        print("Player ID: " + str(ID) + ", Points: " + str(int(player)) + "   teams: " + team1 + ": " + str(team1points) + ", " + team2 + ": " + str(team2points) + ", " + team3 + ": " + str(team3points))
        i += 1
  

#[[name, score], [name, score]]
allTeamStats = [["Arizona Cardinals", 0],["Atlanta Falcons", 0],["Baltimore Ravens", 0],["Buffalo Bills", 0],["Carolina Panthers", 0],["Chicago Bears", 0],["Cincinnati Bengals", 0],["Cleveland Browns", 0],["Dallas Cowboys", 0],["Denver Broncos", 0],["Detroit Lions", 0],["Green Bay Packers", 0],["Houston Texans", 0],["Indianapolis Colts", 0],["Jacksonville Jaguars", 0],["Kansas City Chiefs", 0],["Las Vegas Raiders", 0],["Los Angeles Chargers", 0],["Los Angeles Rams", 0],["Miami Dolphins", 0],["Minnesota Vikings", 0],["New England Patriots", 0],["New Orleans Saints", 0],["New York Giants", 0],["New York Jets", 0],["Philadelphia Eagles", 0],["Pittsburgh Steelers", 0],["San Francisco 49ers", 0],["Seattle Seahawks", 0],["Tampa Bay Buccaneers", 0],["Tennessee Titans", 0],["Washington Football Team", 0]]

teamNames = []
teams = []
i = 0
for teamStats in allTeamStats:
  teamNames.append(teamStats[0])
  teams.append(i)
  i += 1

combinations = list(itertools.combinations(teams, 3))
usedCombinations = combinations

setPoints()
print(allTeamStats)

topPlayers, combinationPoints = topCombinations()
print(topPlayers)
displayTop()