import random
import itertools
from operator import itemgetter
import math
from fpdf import FPDF
import os

#display_points - weekly score for each team,
#weekly_winners - input week #

back = "ticket_back.png"
front = "ticket_front.png"

def mixList(listToBeMixed):
    for i in range(len(listToBeMixed)):
        newIndex = random.randint(0, len(listToBeMixed) - 1)
        temp = listToBeMixed[i]
        listToBeMixed[i] = listToBeMixed[newIndex]
        listToBeMixed[newIndex] = temp
    return listToBeMixed

total_players = 4960
weeks = 18
playersToShow = 20
ticketRandomSeed = 1
random.seed(1)
ticketsInfo = [[]]
for i in range(total_players - 1): #-2 because it already has a list element in it
    ticketsInfo.append([])
for week in range(weeks):
    weekIDs = list(range(total_players))
    weekIDs = mixList(weekIDs)
    for playerID in range(total_players):
        randID = random.randint(0, len(weekIDs) - 1)
        ticketsInfo[playerID].append(weekIDs.pop(randID))

teams_x_spacing = .6
teams_y_spacing = .6
teams_starting_y = 1.2
teams_starting_x = 2.5
teams_font_size = 9
weeks_font_size = 7

week_y = .2
week_x = 0

# SETUP -------------------------------------------------------------
# [[name, score], [name, score]]
allTeamStats = [["Arizona Cardinals", 0], ["Atlanta Falcons", 0], ["Baltimore Ravens", 0], ["Buffalo Bills", 1],
                ["Carolina Panthers", 1], ["Chicago Bears", 1], ["Cincinnati Bengals", 1], ["Cleveland Browns", 1],
                ["Dallas Cowboys", 1], ["Denver Broncos", 1], ["Detroit Lions", 1], ["Green Bay Packers", 1],
                ["Houston Texans", 1], ["Indianapolis Colts", 1], ["Jacksonville Jaguars", 1],
                ["Kansas City Chiefs", 1], ["Las Vegas Raiders", 1], ["Los Angeles Chargers", 1],
                ["Los Angeles Rams", 1], ["Miami Dolphins", 1], ["Minnesota Vikings", 1], ["New England Patriots", 1],
                ["New Orleans Saints", 1], ["New York Giants", 1], ["New York Jets", 1], ["Philadelphia Eagles", 1],
                ["Pittsburgh Steelers", 1], ["San Francisco 49ers", 1], ["Seattle Seahawks", 1],
                ["Tampa Bay Buccaneers", 1], ["Tennessee Titans", 1], ["Washington Football Team", 1]]

team_names = ['Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens', 'Buffalo Bills', 'Carolina Panthers',
                'Chicago Bears', 'Cincinnati Bengals', 'Cleveland Browns', 'Dallas Cowboys', 'Denver Broncos',
                'Detroit Lions', 'Green Bay Packers', 'Houston Texans', 'Indianapolis Colts', 'Jacksonville Jaguars',
                'Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers', 'Los Angeles Rams', 'Miami Dolphins',
                'Minnesota Vikings', 'New England Patriots', 'New Orleans Saints', 'New York Giants', 'New York Jets',
                'Philadelphia Eagles', 'Pittsburgh Steelers', 'San Francisco 49ers', 'Seattle Seahawks',
                'Tampa Bay Buccaneers', 'Tennessee Titans', 'Washington Football Team']

abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f']

commands = ["set_points", "weekly_winners", "test_pdf", "create_tickets", "display_points", "random_points", "disp_week_step", "disp_player_step", "help"]

combinations = list(itertools.combinations(range(len(allTeamStats)), 3))  # generate the list of all combinations


def topIndexes(bigList, amount):
    topIndexeList = []
    #setup list
    for i in range(amount):
        topIndexeList.append(i)
    #find top
    for i in range(len(bigList) - 1):
        for j in range(len(topIndexeList)):
            if bigList[i] > bigList[topIndexeList[j]] and not i in topIndexeList:
                topIndexeList[j] = i
            
    #adding score duplicates
    for i in range(len(bigList) - 1):
        for j in range(len(topIndexeList)):
            if bigList[i] == bigList[topIndexeList[j]] and not i in topIndexeList:
                topIndexeList.insert(j, i)
    return topIndexeList

def bottomIndexes(bigList, amount):
    bottomIndexeList = []
    #setup list
    for i in range(amount):
        bottomIndexeList.append(i)
    #find top
    for i in range(len(bigList) - 1):
        for j in range(len(bottomIndexeList)):
            if bigList[i] < bigList[bottomIndexeList[j]] and not i in bottomIndexeList:
                bottomIndexeList[j] = i
            
    #adding score duplicates
    for i in range(len(bigList) - 1):
        for j in range(len(bottomIndexeList)):
            if bigList[i] == bigList[bottomIndexeList[j]] and not i in bottomIndexeList:
                bottomIndexeList.insert(j, i)
    return bottomIndexeList

def getTicketInfo(ticketID, player_scores, week):
    #getting teams
    teams = ""
    for teamID in combinations[ticketsInfo[ticketID][week]]:
        teams += abc[teamID] + ", "
    teams = teams[:-2]
    #+1 is because ticketID starts from 0 and the printed tickets start from 1
    return "ticket " + str(ticketID + 1) + " has the score " + str(player_scores[ticketID]) + " with the teams " + teams

def weekly_winners():
    week = int(input("What week (1-18): ")) - 1
    player_scores = []
    #print(week_step)
    #print(week)
    #print(week * week_step)
    for playerID in range(total_players):
        score = 0
        for team in combinations[ticketsInfo[playerID][week]]:
            score += allTeamStats[team][1] #1 because that is the index of the score of that team
        player_scores.append(score)
        
    winners = topIndexes(player_scores, playersToShow)
    losers = bottomIndexes(player_scores, playersToShow)
    print("\nHighest scores:")
    for winner in winners:
        print(getTicketInfo(winner, player_scores, week))
        
    print("\nLowest scores:")
    for loser in losers:
        print(getTicketInfo(loser, player_scores, week))

def create_tickets():
    print(ticketsInfo)
    loop = 0
    print("Setting up pdf...")
    pdf = FPDF("P", "in", (8.5, 2.75))
    pdf.set_auto_page_break(0)
    print("Creating information page...")
    pdf.add_page()
    pdf.image(back, 0, 0, 8.5, 2.75, 'PNG')  # - how to add an image
    print("Creating teams page...")
    for player_ID in range(total_players):
        base_ticket(pdf)
        text(pdf, "Ticket No. " + str(player_ID + 1) , .5, .1, 7, '', 'L') # + " Actual: " + str(actualTicketNumber(player_ID))
        text(pdf, "Ticket No. " + str(player_ID + 1), 2.5, .6, 7, '', 'L')
        weeklyCombinations = ticketsInfo[player_ID]
        for week in range(weeks):
            teams = []
            # print(player_ID * player_step + week * week_step)
            for team_ID in combinations[weeklyCombinations[week]]:
                teams.append(''.join(abc[team_ID]))
            pdf.set_y(teams_starting_y + teams_y_spacing * int(week / 6))
            pdf.set_x(teams_starting_x + week * teams_x_spacing - teams_x_spacing * 6 * int(week / 6))
            pdf.set_font('Arial', 'B', teams_font_size)
            pdf.cell(0, 0, ''.join(teams), 0, 0, "L", False, "")
            pdf.set_y(teams_starting_y + teams_y_spacing * int(week / 6) - week_y)
            pdf.set_x(teams_starting_x + week * teams_x_spacing - teams_x_spacing * 6 * int(week / 6) - week_x)
            pdf.set_font('Arial', 'BU', weeks_font_size)
            pdf.cell(0, 0, "Week " + str(week + 1), 0, 0, "L", False, "")

        print("ticket with ID of ", player_ID + 1, " made")
            # print(teams, end = "")
        # print()
    print("Done")
    delete_past_pdf("tickets.pdf")
    name = input(
        "Enter the path and name you want it to have (example: C:\\\\Users\\\\lando\\\\OneDrive\\\\Documents\\\\GitRepos\\\\NFL_thing\\\\final_tickets.pdf): ")
    print("Exporting... (this takes a while)")
    pdf.output(name, 'F')
    print("Done")


def disp_player_step():
    print(player_step)


def disp_week_step():
    print(week_step)


def help():
    print("Commands: ", end="")
    for command in commands:
        print(command, end="")
        if command != commands[-1]:
            print(", ", end="")
    print()


def lookup_player():
    player_ID = int(input("Ticket No. "))
    print()
    for week in range(0, weeks):
        print("Week", week)
        for team in combinations[player_ID * player_step + week * week_step]:
            print(*allTeamStats[team])
        print()


def test_pdf():
    pdfs = int(input("How many (all in one pdf): "))
    pdf = FPDF()
    pdf.set_auto_page_break(0)
    for i in range(0, pdfs):
        base_ticket(pdf, i)
        print("ticket pdf made, ticket ID:", i)
    delete_past_pdf("tickets.pdf")
    print("Exporting...")
    pdf.output('C:\\Users\\18326\PycharmProjects\\first\\tickets.pdf', 'F')
    print("Done")


def random_points():
    for team in allTeamStats:
        team[1] = random.randrange(0, 100)
    print("done")
    display_points()


def set_points():
    for team in allTeamStats:
        team[1] = int(input(team[0] + "'s Score: "))
    display_points()


def display_points():
    for team in allTeamStats:
        print(str("{}: {}").format(team[0], team[1]))

def base_ticket(pdf):
    pdf.add_page()
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(0, 0, 1000, 1000, "FD")
    pdf.rect(5, 5, 200, 100, "D")
    pdf.image(front, 0, 0, 8.5, 2.75, 'PNG')  # - how to add an image


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


def delete_past_pdf(pdf):
    if os.path.isfile(pdf):
        print("Deleting past pdf...")
        os.remove(pdf)
        print("Done")


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