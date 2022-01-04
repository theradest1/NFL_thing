import random
import itertools
from operator import itemgetter
import math

#SETUP -------------------------------------------------------------
#[[name, score], [name, score]]
allTeamStats = [["Arizona Cardinals", 0],["Atlanta Falcons", 0],["Baltimore Ravens", 0], ["Buffalo Bills", 0],["Carolina Panthers", 0],["Chicago Bears", 0],["Cincinnati Bengals", 0],["Cleveland Browns", 0],["Dallas Cowboys", 0],["Denver Broncos", 0],["Detroit Lions", 0],["Green Bay Packers", 0],["Houston Texans", 0],["Indianapolis Colts", 0],["Jacksonville Jaguars", 0],["Kansas City Chiefs", 0],["Las Vegas Raiders", 0],["Los Angeles Chargers", 0],["Los Angeles Rams", 0],["Miami Dolphins", 0],["Minnesota Vikings", 0],["New England Patriots", 0],["New Orleans Saints", 0],["New York Giants", 0],["New York Jets", 0],["Philadelphia Eagles", 0],["Pittsburgh Steelers", 0],["San Francisco 49ers", 0],["Seattle Seahawks", 0],["Tampa Bay Buccaneers", 0],["Tennessee Titans", 0],["Washington Football Team", 0]]

players = 100 #the amount of players
step = 0 #is re-declared lower, is just here to remind me that it is here
weeks = 3 #the amount of weeks this goes on for (change to 18 when done with dev)
playerScores = [] # [[234, 26, 234, 567], [235, 235, 235]...]
for i in range(weeks):
  playerScores.append([])
  #setting scores for all the teams (will need to be not random later)
for teamInfo in allTeamStats:
  teamInfo[1] = random.randrange(1, 100)

#generate the list of all combinations
combinations = list(itertools.combinations(range(len(allTeamStats)), 3))

step = int(len(combinations)/weeks)#the amount of combinations skipped for every week (starts from the player's starting number) **this has to be less than combinations/weeks or the player could have multible of the same combinations (even though its basicly impossible)
player_step = int((len(combinations) - weeks)/players)

#debug
print("Format: [Team_Name, Score] \n", allTeamStats)
print("\n", len(combinations), "combinations")#"\n", combinations) -- display all combinations (a lot)
print("\n# of players:", players)
print("Per week step amount:", step)
print("Per player step amount:", player_step, "\n")

def getScores():
  for player_ID in range(players):
    print("\nPlayer_ID:", player_ID) #debug
    for week_number in range(weeks): 
      score = 0 #reset the score every time it loops over another player
      combination_ID = player_step * player_ID + week_number * step #for every player adds a player_step, for every week it adds a step, making it so everyone has different combinations no matter what
      if combination_ID >= len(combinations):
        combination_ID -= len(combinations) #if the combination_ID will go over the length of the combination list, it loops back to the beginning
      for team_ID in combinations[combination_ID]:
        score += allTeamStats[team_ID][1] #combining all the scores of the teams in the combination
      playerScores[week_number].append(score + player_ID / 10000) #add the score and the player_ID to a list so we can sort it later to find the winners
      print("Comb_ID: " + str(combination_ID) + ",", combinations[combination_ID],"=", score) #debug
  return(playerScores)

def getWinners(): #***** does not do ties yet
  winners = []
  for week in playerScores:
    week.sort(reverse = True)
    print(week) #debug
    for i in range(3):
      winners.append(week[i])
    winners.append(0)
  return winners

playerScores = getScores()
winners = getWinners()
#print(playerScores) #debug
print("\n", winners, "\n\n\n")
for player in winners:
  if player != 0:
    print(int(round(math.modf(player)[0] * 10000,0)))
  else:
    print("")



