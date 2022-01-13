import random
import itertools
from operator import itemgetter
import math
from fpdf import FPDF

square = "Square.png"

#SETUP -------------------------------------------------------------
#[[name, score], [name, score]]
allTeamStats = [["Arizona Cardinals", 0],["Atlanta Falcons", 0],["Baltimore Ravens", 0], ["Buffalo Bills", 0],["Carolina Panthers", 0],["Chicago Bears", 0],["Cincinnati Bengals", 0],["Cleveland Browns", 0],["Dallas Cowboys", 0],["Denver Broncos", 0],["Detroit Lions", 0],["Green Bay Packers", 0],["Houston Texans", 0],["Indianapolis Colts", 0],["Jacksonville Jaguars", 0],["Kansas City Chiefs", 0],["Las Vegas Raiders", 0],["Los Angeles Chargers", 0],["Los Angeles Rams", 0],["Miami Dolphins", 0],["Minnesota Vikings", 0],["New England Patriots", 0],["New Orleans Saints", 0],["New York Giants", 0],["New York Jets", 0],["Philadelphia Eagles", 0],["Pittsburgh Steelers", 0],["San Francisco 49ers", 0],["Seattle Seahawks", 0],["Tampa Bay Buccaneers", 0],["Tennessee Titans", 0],["Washington Football Team", 0]]

shortNames = ["ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN", "DET", " GB", "HOU", "IND", "JAX", " KC", "MIA", "MIN", " NE", " NO", "NYG", "NYJ", " LV", "PHI", "PIT", "LAC", " SF", "SEA", "LAR", " TB", "TEN", "WAS"] 

commands = ["lookup_player", "set_points", "weekly_winners", "test_pdf", "test_print", "print_tickets", "points", "set_random_points"]

combinations = list(itertools.combinations(range(len(allTeamStats)), 3)) #generate the list of all combinations

#commands not done
def weekly_winners():
  print()
def print_tickets():
  print()
def test_print():
  print()

def base_ticket(pdf):
  pdf.add_page()
  pdf.set_fill_color(255, 255, 255)
  pdf.rect(0, 0, 200, 1000, "FD")
  #pdf.image(square, 10, 10, 0, 0, 'PNG')# - how to add an image
  pdf.set_font('Arial', 'B', 13)
  pdf.cell(0, 20, "Total Prizes: $17,170 - $1,010 Given Each Week For 17 Weeks", 0, 2, "C", False, "")
  
  pdf.multi_cell(0, 4, "")

  pdf.set_font('Arial', 'B', 9)
  pdf.cell(0, 0, "Rules:", 0, 2, "l", False, "")
  #pdf.cell(w, h, txt, border, ln, align, fill = False, link = '') -- just a reference
  pdf.set_font('Arial', '', 7)
  pdf.multi_cell(0, 4, "\n1. This ticket is valid for the 17 \nweeks of the regular season.\n2. Each ticket has three teams/week and the\nscores added together determine the winners\n3. In case of ties, prizes are combined and\nsplit wetween the ties.\n4. No other ticket hs the same team combination\nfor each week as this ticket.\n5. Teams not playing on a given week will\nbe assigned the previous week's score.", 0, 'L', False)
  pdf.rect(5, 5, 200, 100, "D")
  pdf.output('tuto1.pdf', 'F')

#commands being worked on
def test_pdf():
  pdf = FPDF()
  for ii in range(245):
    for i in range(0, 20):
      base_ticket(pdf)
      print("ticket pdf made, ticket ID:", i + 1 + ii * 20 + 1, )
    print("ticket chunks:", ii + 1)
  print("Done")

#commands that are done
def lookup_player():
  player_ID = int(input("Player ID: "))
  player_step = 1 # change if less than 4.9k players       len(combinations) / int(input("players: "))
  week_step = int(len(combinations)/int(input("weeks: ")))
  for week in range(0, 17):
    print("Week", week)
    for team in combinations[player_ID*player_step + week * week_step]:
      print(team)
    print()
def set_random_points():
  for team in allTeamStats:
    team[1] = random.randrange(0, 100)
  print("done")
def set_scores():
  for team in allTeamStats:
    team[1] = int(input(team[0] + "'s Score: "))
def points():
  for team in allTeamStats:
    print(str("{}: {}").format(team[0], team[1]))

#end of commands -------------------

test_pdf()

inp = ""
while inp != "done":
  if len(inp.split()) > 0:
    cmd = inp.split()[0]
    if cmd in commands:
      eval(cmd)()
    elif cmd == "exit":
      exit()
    else:
      print(str("'{}' is not a command").format(cmd))
  inp = input(">>")

players = 0 #counts up (simulating another person getting a ticket)
step = 0 #is re-declared lower, its just here to remind me that it is here
weeks = 17 #the amount of weeks this goes on for (change to 17 when done with dev)
playerScores = [] # [[234, 26, 234, 567], [235, 235, 235]...]

for i in range(weeks):
  playerScores.append([]) #setting up the list (not sure how else to do this just let me know if there is a better way)

for teamInfo in allTeamStats:
  teamInfo[1] = random.randrange(1, 100) #setting scores for all the teams (will need to be not random later)

step = int(len(combinations)/weeks) #the amount of combinations skipped for every week (starts from the player's starting number) **this has to be less than combinations/weeks or the player could have multible of the same combinations (even though its basicly impossible)
estimated_players = int(input("Estimated amount of players:\n>> "))
player_step = int(len(combinations)/estimated_players) #same just a step for each player
#estimated_players = int(len(combinations)/player_step)
print("Do you want the estimated players to be adjusted to", int(len(combinations)/player_step), "to fit better")

if input("(y/n)") == "y":
  estimated_players = int(len(combinations)/player_step)
print(estimated_players)

#print(len(combinations), "/", 

#debug
print("Format: [Team_Name, Score] \n", allTeamStats)
print("\n" + str(len(combinations)), "combinations")#"\n", combinations) #display all combinations (a lot)
#print("# of players:", players) #not an exact amount so I removed it
print("Per week step amount:", step)
print("Per player step amount:", player_step, "\n")

def getScores():
  #player_step = int((len(combinations) - step)/(int(input("Estimated amount of players:\n>> ")) * 3))
  command = ""
  player_ID = 0
  while player_ID < estimated_players:#command != "done":
    #for player_ID in range(players):
    print("\nPlayer_ID:", player_ID) #debug
    for week_number in range(weeks): 
      score = 0 #reset the score every time it loops over another player
      combination_ID = player_step * player_ID + week_number * step #for every player adds a player_step, for every week it adds a step, making it so everyone has different combinations no matter what
      if combination_ID >= len(combinations):
        combination_ID -= len(combinations) #if the combination_ID will go over the length of the combination list, it loops back to the beginning
      for team_ID in combinations[combination_ID]:
        score += allTeamStats[team_ID][1] #combining all the scores of the teams for that week to compare with others
      playerScores[week_number].append(score + player_ID / 10000) #add the score and the player_ID to a list so we can sort it later to find the winners
      #print("Comb_ID: " + str(combination_ID) + ",", combinations[combination_ID],"=", score) #debug
      for team in combinations[combination_ID]:
        print(shortNames[team] + ", ", end = '')
      print("")
    #command = input(">> ")
    player_ID += 1
  return(playerScores)

def getWinners(): #***** does not do ties yet
  winners = [] #declare var
  for week in playerScores:
    week.sort(reverse = True) #sort the points in decending order
    #print(week) #debug
    winners.append(0) #a spacer so i can see the end of the week (and im too lazy to make a array of lists)
    for i in range(3):
      winners.append(week[i]) #adds the top 3 scores to a list (with 0s to seperate the weeks)
  return winners

playerScores = getScores()
winners = getWinners()
#print(playerScores) #debug
#print("\n", winners) #debug
week = 0
for player in winners:
  if player != 0:
    print(int(round(math.modf(player)[0] * 10000,0))) #display the winner's ID
  else:
    week += 1
    print("\nWeek", week, "winners:") #some ease of life stuffs

#print(playerScores) debug
    