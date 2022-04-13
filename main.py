import random
import itertools
from operator import itemgetter
import math
from fpdf import FPDF
import os
import tkinter as tk

# window = tk.Tk()
# greeting = tk.Label(text="Hello, Tkinter")
# greeting.pack()


square = "Square.png"
football = "Football.png"
back = "C:\\Users\\18326\PycharmProjects\\first\\ticket_back.png"
front = "C:\\Users\\18326\PycharmProjects\\first\\ticket_front.png"

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
allTeamStats = [["Arizona Cardinals", 10], ["Atlanta Falcons", 5], ["Baltimore Ravens", 2], ["Buffalo Bills", 0],
                ["Carolina Panthers", 0], ["Chicago Bears", 0], ["Cincinnati Bengals", 0], ["Cleveland Browns", 0],
                ["Dallas Cowboys", 0], ["Denver Broncos", 0], ["Detroit Lions", 0], ["Green Bay Packers", 0],
                ["Houston Texans", 0], ["Indianapolis Colts", 0], ["Jacksonville Jaguars", 0],
                ["Kansas City Chiefs", 0], ["Las Vegas Raiders", 0], ["Los Angeles Chargers", 0],
                ["Los Angeles Rams", 0], ["Miami Dolphins", 0], ["Minnesota Vikings", 0], ["New England Patriots", 0],
                ["New Orleans Saints", 0], ["New York Giants", 0], ["New York Jets", 0], ["Philadelphia Eagles", 0],
                ["Pittsburgh Steelers", 0], ["San Francisco 49ers", 0], ["Seattle Seahawks", 0],
                ["Tampa Bay Buccaneers", 0], ["Tennessee Titans", 0], ["Washington Football Team", 0]]

team_names = ['Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens', 'Buffalo Bills', 'Carolina Panthers',
              'Chicago Bears', 'Cincinnati Bengals', 'Cleveland Browns', 'Dallas Cowboys', 'Denver Broncos',
              'Detroit Lions', 'Green Bay Packers', 'Houston Texans', 'Indianapolis Colts', 'Jacksonville Jaguars',
              'Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers', 'Los Angeles Rams', 'Miami Dolphins',
              'Minnesota Vikings', 'New England Patriots', 'New Orleans Saints', 'New York Giants', 'New York Jets',
              'Philadelphia Eagles', 'Pittsburgh Steelers', 'San Francisco 49ers', 'Seattle Seahawks',
              'Tampa Bay Buccaneers', 'Tennessee Titans', 'Washington Football Team']

abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
       'W', 'Y', 'X', 'Z', 'a', 'b', 'c', 'd', 'e', 'f']

commands = ["lookup_player", "set_points", "weekly_winners", "test_pdf", "create_tickets", "display_points",
            "random_points", "disp_week_step", "disp_player_step", "help"]

prizes = [500, 250, 100, 75, 50, 25, 10]

combinations = list(itertools.combinations(range(len(allTeamStats)), 3))  # generate the list of all combinations

comb_size = len(combinations)
player_step = int(comb_size / total_players)
week_step = int(comb_size / weeks)
print(week_step)


# commands not done


# commands being worked on


def weekly_winners():
    week = int(input("What week: "))
    player_scores = []
    player_ID = -1

    for i in range(len(combinations)):  # combination in combinations:
        player_ID += 1
        total_score = 0
        if (i + week * week_step >= len(combinations)):
            combination = combinations[i + week * week_step - len(combinations)]
            print(i + week * week_step - len(combinations))
        else:
            combination = combinations[i + week * week_step]
            print(i + week * week_step)

        print(combination)
        for team in combination:
            total_score += allTeamStats[team][1]
        player_scores.append(round(total_score + player_ID / 10000 + .00001,5))  # need to add .00001 to get rid of rounding and round() to get rid of floating points errors
    # print(player_scores)
    player_scores.sort(reverse=True)
    # print(player_scores)
    i = -1
    j = -1
    winners = []

    print("\nHighest scores:")
    for i in range(50):
        print(f"Ticket No. {displayNumber(int(str(player_scores[i])[-5:-1]))}, Score: {int(player_scores[i])}")

    print("\nLowest scores:")
    for i in range(len(player_scores) - 1, len(player_scores) - 20, -1):
        print(f"Ticket No. {displayNumber(int(str(player_scores[i])[-5:-1]))}, Score: {int(player_scores[i])}")


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
        text(pdf, "Ticket No. " + str(player_ID + 1) + " Actual: " + str(actualTicketNumber(player_ID)), .5, .1, 7, '', 'L')
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
            pdf.set_font('Arial', 'B', weeks_font_size)
            pdf.cell(0, 0, "Week " + str(week), 0, 0, "L", False, "")

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

def displayNumber(ID):
    return (ID - 1 * jump) % (len(combinations) - 1)


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