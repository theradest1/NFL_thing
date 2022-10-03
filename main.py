import random
import itertools
from operator import itemgetter
import math
from fpdf import FPDF
import os

#set_points - weekly score for each team,
#weekly_winners - input week #

back = "ticket_back.png"
front = "ticket_front.png"

total_players = 4960
weeks = 18

jump = 496

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
allTeamStats = [["Arizona Cardinals", 12], ["Atlanta Falcons", 27], ["Baltimore Ravens", 37], ["Buffalo Bills", 19],
                ["Carolina Panthers", 22], ["Chicago Bears", 23], ["Cincinnati Bengals", 27], ["Cleveland Browns", 29],
                ["Dallas Cowboys", 23], ["Denver Broncos", 11], ["Detroit Lions", 24], ["Green Bay Packers", 14],
                ["Houston Texans", 20], ["Indianapolis Colts", 20], ["Jacksonville Jaguars", 38],
                ["Kansas City Chiefs", 17], ["Las Vegas Raiders", 22], ["Los Angeles Chargers", 10],
                ["Los Angeles Rams", 20], ["Miami Dolphins", 21], ["Minnesota Vikings", 28], ["New England Patriots", 26],
                ["New Orleans Saints", 14], ["New York Giants", 16], ["New York Jets", 12], ["Philadelphia Eagles", 24],
                ["Pittsburgh Steelers", 17], ["San Francisco 49ers", 10], ["Seattle Seahawks", 23],
                ["Tampa Bay Buccaneers", 12], ["Tennessee Titans", 24], ["Washington Football Team", 8]]

team_names = ['Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens', 'Buffalo Bills', 'Carolina Panthers',
              'Chicago Bears', 'Cincinnati Bengals', 'Cleveland Browns', 'Dallas Cowboys', 'Denver Broncos',
              'Detroit Lions', 'Green Bay Packers', 'Houston Texans', 'Indianapolis Colts', 'Jacksonville Jaguars',
              'Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers', 'Los Angeles Rams', 'Miami Dolphins',
              'Minnesota Vikings', 'New England Patriots', 'New Orleans Saints', 'New York Giants', 'New York Jets',
              'Philadelphia Eagles', 'Pittsburgh Steelers', 'San Francisco 49ers', 'Seattle Seahawks',
              'Tampa Bay Buccaneers', 'Tennessee Titans', 'Washington Football Team']

abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
       'W', 'Y', 'X', 'Z', 'a', 'b', 'c', 'd', 'e', 'f']

commands = ["set_points", "weekly_winners", "test_pdf", "create_tickets", "display_points", "random_points", "disp_week_step", "disp_player_step", "help"]

combinations = list(itertools.combinations(range(len(allTeamStats)), 3))  # generate the list of all combinations

comb_size = len(combinations)
player_step = int(comb_size / total_players)
week_step = int(comb_size / weeks)
print(week_step)


def weekly_winners():
    week = int(input("What week (1-18): ")) - 1
    player_scores = []
    player_ID = -1
    #print(week_step)
    #print(week)
    #print(week * week_step)
    for i in range(len(combinations)):  # combination in combinations:
        player_ID += 1
        total_score = 0
        for team in combinations[i]:
            total_score += allTeamStats[team][1]
        player_scores.append(round(total_score + player_ID / 10000 + .00001, 5))  # need to add .00001 to get rid of rounding and round() to get rid of floating points errors
    # print(player_scores)
    player_scores.sort(reverse=True)
    # print(player_scores)

    print("\nHighest scores:")
    for i in range(40):
        print(f"{i + 1}. Ticket No. {displayNumber(int(str(player_scores[i])[-5:-1]), week)}  Score: {int(player_scores[i])}, Teams: {combinations[int(str(player_scores[i])[-5:-1])]}")  # Actual No. {int(str(player_scores[i])[-5:-1])}
    print("\nLowest scores:")
    for i in range(len(player_scores) - 1, len(player_scores) - 41, -1):
        print(f"{total_players - i}. Ticket No. {displayNumber(int(str(player_scores[i])[-5:-1]), week)}, Score: {int(player_scores[i])}")
    #print(player_scores)

def create_tickets():
    loop = 0
    print("Setting up pdf...")
    pdf = FPDF("P", "in", (8.5, 2.75))
    pdf.set_auto_page_break(0)
    print("Done")
    print("Creating information page...")
    pdf.add_page()
    pdf.image(back, 0, 0, 8.5, 2.75, 'PNG')  # - how to add an image
    print("Done")
    print("Creating teams page...")
    for player_ID in range(total_players):
        base_ticket(pdf)
        text(pdf, "Ticket No. " + str(player_ID + 1) , .5, .1, 7, '', 'L') # + " Actual: " + str(actualTicketNumber(player_ID))
        text(pdf, "Ticket No. " + str(player_ID + 1), 2.5, .6, 7, '', 'L')
        print("ticket made, ticket ID:", player_ID + 1)
        for week in range(weeks):
            teams = []
            # print(player_ID * player_step + week * week_step)
            for team_ID in combinations[(actualTicketNumber(player_ID) * player_step + week * week_step)%(len(combinations) - 1)]:
                teams.append(''.join(abc[team_ID]))
            pdf.set_y(teams_starting_y + teams_y_spacing * int(week / 6))
            pdf.set_x(teams_starting_x + week * teams_x_spacing - teams_x_spacing * 6 * int(week / 6))
            pdf.set_font('Arial', 'B', teams_font_size)
            pdf.cell(0, 0, ''.join(teams), 0, 0, "L", False, "")
            pdf.set_y(teams_starting_y + teams_y_spacing * int(week / 6) - week_y)
            pdf.set_x(teams_starting_x + week * teams_x_spacing - teams_x_spacing * 6 * int(week / 6) - week_x)
            pdf.set_font('Arial', 'BU', weeks_font_size)
            pdf.cell(0, 0, "Week " + str(week + 1), 0, 0, "L", False, "")

            # print(teams, end = "")
        # print()
    print("Done")
    delete_past_pdf("tickets.pdf")
    name = input(
        "Enter the path and name you want it to have (example: C:\\\\Users\\\\18326\\\\Desktop\\\\tickets.pdf): ")
    print("Exporting...")
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


# end of commands -------------------
def actualTicketNumber(ID):
    return (ID * jump + int(ID * jump / len(combinations))) % len(combinations)

def displayNumber(ID, week = 0):
    return (int((ID + (ID%jump) * len(combinations))/jump) + 1 + week * 2209) % (len(combinations) - 1)

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