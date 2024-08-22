import random
import itertools
from fpdf import FPDF
import os

#display_points - weekly score for each team,
#weekly_winners - input week #

back = "ticket_back_4-19-24.png"
front = "ticket_front_5-6-24.png"
randomInfoFile = "random_info.txt"


def mixList(listToBeMixed):
    for i in range(len(listToBeMixed)):
        newIndex = random.randint(0, len(listToBeMixed) - 1)
        temp = listToBeMixed[i]
        listToBeMixed[i] = listToBeMixed[newIndex]
        listToBeMixed[newIndex] = temp
    return listToBeMixed


def generateRandomTicketInfo(seed):
    random.seed(seed)
    ticketsInfo = [[]]
    for i in range(total_players -
                   1):  #-1 because it already has a list element in it
        ticketsInfo.append([])
    for week in range(weeks):
        weekIDs = list(range(total_players))
        weekIDs = mixList(weekIDs)
        for playerID in range(total_players):
            randID = random.randint(0, len(weekIDs) - 1)
            ticketsInfo[playerID].append(weekIDs.pop(randID))
    return ticketsInfo


total_players = 4960
weeks = 18
playersToShow = 10
ticketsInfoLoaded = False

#pdf settings
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
allTeamStats = [["Arizona Cardinals", 13], ["Atlanta Falcons", 12],
                ["Baltimore Ravens", 13], ["Buffalo Bills", 9],
                ["Carolina Panthers", 12], ["Chicago Bears", 27],
                ["Cincinnati Bengals", 3], ["Cleveland Browns", 12],
                ["Dallas Cowboys", 27], ["Denver Broncos", 27],
                ["Detroit Lions", 24], ["Green Bay Packers", 2],
                ["Houston Texans", 28], ["Indianapolis Colts", 21],
                ["Jacksonville Jaguars", 20], ["Kansas City Chiefs", 23],
                ["Las Vegas Raiders", 12], ["Los Angeles Chargers", 9],
                ["Los Angeles Rams", 13], ["Miami Dolphins", 13],
                ["Minnesota Vikings", 27], ["New England Patriots", 13],
                ["New Orleans Saints", 10], ["New York Giants", 10],
                ["New York Jets", 15], ["Philadelphia Eagles", 14],
                ["Pittsburgh Steelers", 3], ["San Francisco 49ers", 16],
                ["Seattle Seahawks", 15], ["Tampa Bay Buccaneers", 7],
                ["Tennessee Titans", 16], ["Washington Football Team", 6]]

team_names = [
    'Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens',
    'Buffalo Bills', 'Carolina Panthers', 'Chicago Bears',
    'Cincinnati Bengals', 'Cleveland Browns', 'Dallas Cowboys',
    'Denver Broncos', 'Detroit Lions', 'Green Bay Packers', 'Houston Texans',
    'Indianapolis Colts', 'Jacksonville Jaguars', 'Kansas City Chiefs',
    'Las Vegas Raiders', 'Los Angeles Chargers', 'Los Angeles Rams',
    'Miami Dolphins', 'Minnesota Vikings', 'New England Patriots',
    'New Orleans Saints', 'New York Giants', 'New York Jets',
    'Philadelphia Eagles', 'Pittsburgh Steelers', 'San Francisco 49ers',
    'Seattle Seahawks', 'Tampa Bay Buccaneers', 'Tennessee Titans',
    'Washington Football Team'
]

abc = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
    'e', 'f'
]

commands = [
    "set_points", "weekly_winners", "test_pdf", "create_tickets",
    "display_points", "random_points", "help", "test_rotated_text",
    "load_randoms", "set_seed", "player_info", "team_comb_lookup"
]

combinations = list(itertools.combinations(range(
    len(allTeamStats)), 3))  # generate the list of all combinations


def topIndexes(bigList, amount):
    topIndexeList = []
    #setup list
    for i in range(amount):
        topIndexeList.append(i)
    #find top
    for i in range(len(bigList) - 1):
        for j in range(len(topIndexeList)):
            if bigList[i] > bigList[
                    topIndexeList[j]] and not i in topIndexeList:
                topIndexeList[j] = i

    #adding score duplicates
    for i in range(len(bigList) - 1):
        for j in range(len(topIndexeList)):
            if bigList[i] == bigList[
                    topIndexeList[j]] and not i in topIndexeList:
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
            if bigList[i] < bigList[
                    bottomIndexeList[j]] and not i in bottomIndexeList:
                bottomIndexeList[j] = i

    #adding score duplicates
    for i in range(len(bigList) - 1):
        for j in range(len(bottomIndexeList)):
            if bigList[i] == bigList[
                    bottomIndexeList[j]] and not i in bottomIndexeList:
                bottomIndexeList.insert(j, i)
    return bottomIndexeList


def getAstheticNumbers(num, digits):
    numInString = str(num)
    while len(numInString) < digits:
        numInString = "0" + numInString
    return numInString


def getTicketInfo(ticketID, player_scores, week):
    #getting teams
    teams = ""
    for teamID in combinations[ticketsInfo[ticketID][week]]:
        teams += abc[teamID] + ", "
    teams = teams[:-2]
    #+1 is because ticketID starts from 0 and the printed tickets start from 1
    return f"#{ticketID + 1}, Score: {player_scores[ticketID]}, Teams: {teams}"


def weekly_winners():
    week = int(input("What week (1-18): ")) - 1
    player_scores = []
    for playerID in range(total_players):
        score = 0
        for team in combinations[ticketsInfo[playerID][week]]:
            score += allTeamStats[team][1]  #1 because that is the index of the score of that team
        player_scores.append(score)

    winners = topIndexes(player_scores, playersToShow)
    losers = bottomIndexes(player_scores, playersToShow)
    
    print("\nHighest scores:")
    i = 1
    for winner in winners:
        print(f"{i}. " + getTicketInfo(winner, player_scores, week))
        i += 1

    print("\nLowest scores:")
    i = 1
    for loser in losers:
        print(f"{i}. " + getTicketInfo(loser, player_scores, week))
        i += 1
        
def player_info():
    ticketID = int(input("\nTicket ID: ")) - 1
    print("")
    
    for week in range(18):
        #getting score
        score = 0
        for team in combinations[ticketsInfo[ticketID][week]]:
            score += allTeamStats[team][1]  #1 because that is the index of the score of that team
        
        #getting teams
        teams = ""
        for teamID in combinations[ticketsInfo[ticketID][week]]:
            teams += abc[teamID] + ", "
        teams = teams[:-2]
        
        print(f"Week: {week + 1}, Score: {score}, Teams: {teams}")


def team_comb_lookup():
    print("Not done yet")
    return
    team1 = input("\nTeam 1: ")
    team2 = input("Team 2: ")
    team3 = input("Team 3: ")
    print("")
    
    print(combinations[0])
    #for week in range(18):
        
        
        #print(f"Week: {week + 1}, Ticket ID: {ticketID}, Score: {teams}")


def create_tickets():
    if ticketsInfoLoaded == False:
        print("Ticket info hasn't been loaded")
        return
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
        ticketIDWithZeros = getAstheticNumbers(player_ID + 1, 4)
        text(pdf, "No.", .5, .15, 7, '', 'L')
        text(pdf, "No.", 2.5, .6, 7, '', 'L')
        text(pdf, ticketIDWithZeros, .67, .15, 12, '', 'L')
        text(pdf, ticketIDWithZeros, 2.67, .6, 12, '', 'L')

        weeklyCombinations = ticketsInfo[player_ID]
        for week in range(weeks):
            teams = []
            for team_ID in combinations[weeklyCombinations[week]]:
                teams.append(''.join(abc[team_ID]))
            pdf.set_y(teams_starting_y + teams_y_spacing * int(week / 6))
            pdf.set_x(teams_starting_x + week * teams_x_spacing -
                      teams_x_spacing * 6 * int(week / 6))
            pdf.set_font('Arial', 'B', teams_font_size)
            pdf.cell(0, 0, ''.join(teams), 0, 0, "L", False, "")
            pdf.set_y(teams_starting_y + teams_y_spacing * int(week / 6) -
                      week_y)
            pdf.set_x(teams_starting_x + week * teams_x_spacing -
                      teams_x_spacing * 6 * int(week / 6) - week_x)
            pdf.set_font('Arial', 'BU', weeks_font_size)
            pdf.cell(0, 0, "Week " + str(week + 1), 0, 0, "L", False, "")

        print("ticket with ID of ", player_ID + 1, " made")
        # print(teams, end = "")
        # print()
    print("Done")
    delete_past_pdf("tickets.pdf")
    name = input(
        "Enter the path and name you want it to have (example: C:\\\\Users\\\\lando\\\\OneDrive\\\\Documents\\\\GitRepos\\\\NFL_thing\\\\final_tickets.pdf): "
    )
    print("Exporting... (this takes a while)")
    pdf.output(name, 'F')
    print("Done")


def help():
    print("Commands: ", end="")
    for command in commands:
        print(command, end="")
        if command != commands[-1]:
            print(", ", end="")
    print()


def save_randoms(ticketsInfo):
    with open(randomInfoFile, 'w') as file:
        for ticket in ticketsInfo:
            for number in ticket:
                file.write(str(number) + ' ')
            file.write('\n')


def load_randoms():
    global ticketsInfo, ticketsInfoLoaded
    ticketsInfo = []
    try:
        with open(randomInfoFile, 'r') as file:
            for line in file:
                ticket = [int(item) for item in line.strip().split()]
                ticketsInfo.append(ticket)
    except FileNotFoundError:
        print(
            "Random info has not been generated yet, use set_seed to generate it"
        )

    ticketsInfoLoaded = True


def set_seed():
    seed = int(input("Seed: "))
    print("Generating random info...")
    ticketsInfo = generateRandomTicketInfo(seed)
    print("Saving random info to file...")
    save_randoms(ticketsInfo)
    print("Loading random info...")
    load_randoms()


def test_pdf():
    pdfs = int(input("How many (all in one pdf): "))
    pdf = FPDF()
    pdf.set_auto_page_break(0)
    for i in range(0, pdfs):
        base_ticket(pdf, i)
        print("ticket pdf made, ticket ID:", i)
    delete_past_pdf("tickets.pdf")
    print("Exporting...")
    pdf.output('C:\\Users\\18326\\PycharmProjects\\first\\tickets.pdf', 'F')
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
        print(f"({abc[allTeamStats.index(team)]}) {team[0]}: {team[1]}")


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


load_randoms()
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
