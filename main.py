import random
import itertools
from operator import itemgetter
import math
from fpdf import FPDF
import os

square = "Square.png"
football = "Football.png"

total_players = 4960
weeks = 17

teams_x_spacing = 12
teams_y_spacing = 12
teams_starting_y = 120
teams_starting_x = 10
teams_font_size = 7
week_y = 3
week_x = 3

names_x_spacing = 40
names_y_spacing = 3
names_starting_y = 30
names_starting_x = 10
names_font_size = 5
name_ID_length = 4

#SETUP -------------------------------------------------------------
#[[name, score], [name, score]]
allTeamStats = [["Arizona Cardinals", 0],["Atlanta Falcons", 0],["Baltimore Ravens", 0], ["Buffalo Bills", 0],["Carolina Panthers", 0],["Chicago Bears", 0],["Cincinnati Bengals", 0],["Cleveland Browns", 0],["Dallas Cowboys", 0],["Denver Broncos", 0],["Detroit Lions", 0],["Green Bay Packers", 0],["Houston Texans", 0],["Indianapolis Colts", 0],["Jacksonville Jaguars", 0],["Kansas City Chiefs", 0],["Las Vegas Raiders", 0],["Los Angeles Chargers", 0],["Los Angeles Rams", 0],["Miami Dolphins", 0],["Minnesota Vikings", 0],["New England Patriots", 0],["New Orleans Saints", 0],["New York Giants", 0],["New York Jets", 0],["Philadelphia Eagles", 0],["Pittsburgh Steelers", 0],["San Francisco 49ers", 0],["Seattle Seahawks", 0],["Tampa Bay Buccaneers", 0],["Tennessee Titans", 0],["Washington Football Team", 0]]

team_names = ['Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens', 'Buffalo Bills', 'Carolina Panthers', 'Chicago Bears', 'Cincinnati Bengals', 'Cleveland Browns', 'Dallas Cowboys', 'Denver Broncos', 'Detroit Lions', 'Green Bay Packers', 'Houston Texans', 'Indianapolis Colts', 'Jacksonville Jaguars', 'Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers', 'Los Angeles Rams', 'Miami Dolphins', 'Minnesota Vikings', 'New England Patriots', 'New Orleans Saints', 'New York Giants', 'New York Jets', 'Philadelphia Eagles', 'Pittsburgh Steelers', 'San Francisco 49ers', 'Seattle Seahawks', 'Tampa Bay Buccaneers', 'Tennessee Titans', 'Washington Football Team']

abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'X', 'Z', 'a', 'b', 'c', 'd', 'e', 'f']

commands = ["lookup_player", "set_points", "weekly_winners", "test_pdf", "create_tickets", "display_points", "set_random_points", "disp_week_step", "disp_player_step" , "help"]

combinations = list(itertools.combinations(range(len(allTeamStats)), 3)) #generate the list of all combinations

comb_size = len(combinations)
player_step = int(comb_size / total_players)
week_step = int(comb_size / weeks)

#commands not done
def weekly_winners():
  print()

#commands being worked on
def create_tickets():
  loop = 0
  pre_pdf()
  pdf = FPDF()
  pdf.set_auto_page_break(0)
  for player_ID in range(100): #total_players):
    base_ticket(pdf, player_ID)
    print("ticket made, ticket ID:", player_ID)
    if player_ID * player_step + weeks * week_step >= comb_size:
        loop = comb_size
    text(pdf, "Your Teams Are:", 19, 110, 15, 'B', 'L')
    pdf.set_font('Arial', '', teams_font_size)
    for week in range(weeks):
      teams = []
      #print(player_ID * player_step + week * week_step)
      for team_ID in combinations[player_ID * player_step + week * week_step - loop]:
        teams.append(''.join(abc[team_ID]))
      pdf.set_y(teams_starting_y + teams_y_spacing * int(week/6))
      pdf.set_x(teams_starting_x + week * teams_x_spacing - teams_x_spacing * 6 * int(week/6))
      pdf.cell(0, 0, ''.join(teams), 0, 0, "L", False, "")
      pdf.set_y(teams_starting_y + teams_y_spacing * int(week/6) - week_y)
      pdf.set_x(teams_starting_x + week * teams_x_spacing - teams_x_spacing * 6 * int(week/6) - week_x)
      pdf.cell(0, 0, "Week: " + str(week), 0, 0, "L", False, "")

      #print(teams, end = "")
    print()
  print("Exporting...")
  pdf.output('tickets.pdf', 'F')
  print("Done")

  
#commands that are done
def disp_player_step():
  print(player_step)
def disp_week_step():
  print(week_step)
def help():
  print("Commands: ", end = "")
  for command in commands:
    print(command, end = "")
    if command != commands[-1]:
      print(", ", end = "")
  print()
def lookup_player():
  player_ID = int(input("Player ID: "))
  print()
  for week in range(0, weeks):
    print("Week", week)
    for team in combinations[player_ID*player_step + week * week_step]:
      print(*allTeamStats[team])
    print()
def test_pdf():
  pre_pdf()
  pdfs = int(input("How many (all in one pdf): "))
  pdf = FPDF()
  pdf.set_auto_page_break(0)
  for i in range(0, pdfs):
    base_ticket(pdf, i)
    print("ticket pdf made, ticket ID:", i)
  print("Exporting...")
  pdf.output('tickets.pdf', 'F')
  print("Done")
def set_random_points():
  for team in allTeamStats:
    team[1] = random.randrange(0, 100)
  print("done")
  display_points()
def set_scores():
  for team in allTeamStats:
    team[1] = int(input(team[0] + "'s Score: "))
    display_points()
def display_points():
  for team in allTeamStats:
    print(str("{}: {}").format(team[0], team[1]))

#end of commands -------------------

def base_ticket(pdf, ID):
  pdf.add_page()
  pdf.set_fill_color(255, 255, 255)
  pdf.rect(5, 5, 200, 100, "D")
  #pdf.image(football, 50, 30, 0, 0, 'PNG') # - how to add an image

  text(pdf, "Total Prizes: $17,170 - $1,010 Given Each Week For 17 Weeks", 20, 10, 13, 'b', 'L')

  text(pdf, 'Rules:', 10, 60, 9, '', 'L')

  multi_text(pdf, ["1. This ticket is valid for the 17 weeks of the regular season.", "2. Each ticket has three teams/week and the scores added together determine the winners", "3. In case of ties, prizes are combined and split wetween the ties.", "4. No other ticket hs the same team combination for each week as this ticket.", "5. Teams not playing on a given week will be assigned the previous week's score."], 10, 60, 4, 7, '', "L")

  #pdf.set_font('Arial', '', names_font_size)
  for i in range(8):
    for j in range(4):
      pdf.set_y(i * names_y_spacing + names_starting_y)
      pdf.set_x(j * names_x_spacing + names_starting_x)
      pdf.cell(0, 0, abc[i*4 + j] + ": " + team_names[i*4 + j], 0, 0, "L", False, "")
  
    
  text(pdf, "Your Teams Are:", 306, 110, 13, "B", "C")
  text(pdf, "Player ID: " + str(ID), 10, 10, 7, '', 'L')

def text(pdf, text, x, y, size, style, position):
  pdf.set_y(y)
  pdf.set_x(x)
  pdf.set_font('Arial', style, size)
  pdf.cell(0, 0, text, 0, 2, position, False, "")

def multi_text(pdf, texts, x, y, y_step, size, style, position):
  i = 0
  pdf.set_font('Arial', style, size)
  for text in texts:
    i += y_step
    pdf.set_x(x)
    pdf.set_y(i + y)
    pdf.cell(0, 0, text, 0, 0, position, False, "")

def pre_pdf():
  if os.path.isfile("tickets.pdf"):
    print("Deleting past pdf...")
    os.remove("tickets.pdf")
    print("Done")

create_tickets()
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



#Things that are not in the program but are going to be put in soon

players = 0 #counts up (simulating another person getting a ticket)
step = 0 #is re-declared lower, its just here to remind me that it is here
weeks = 17 #the amount of weeks this goes on for (change to 17 when done with dev)
playerScores = [] # [[234, 26, 234, 567], [235, 235, 235]...]

for i in range(weeks):
  playerScores.append([]) #setting up the list (not sure how else to do this just let me know if there is a better way)

for teamInfo in allTeamStats:
  teamInfo[1] = random.randrange(1, 100) #setting scores for all the teams (will need to be not random later)

week_step = int(len(combinations)/17)

#debug
print("Format: [Team_Name, Score] \n", allTeamStats)
print("\n" + str(len(combinations)), "combinations")#"\n", combinations) #display all combinations (a lot)
#print("# of players:", players) #not an exact amount so I removed it
print("Per week step amount:", step)
print("Per player step amount:", 1, "\n")

def getScores():
  estimated_players = len(combinations)
  player_step = 1
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