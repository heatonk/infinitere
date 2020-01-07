import random
import numpy
import csv
from datetime import datetime
import matplotlib.pyplot as plt


maxBalls = 5
maxCycles = 5
numMatches = 1000000
numAlliances = numMatches * 2
numTeams = numAlliances * 3


class Robot:
    def __init__(self):
        self.score = 0
        self.autoCells = random.randint(0, 5)
        self.autoMove = random.randint(0, 1)
        self.teleCycles = random.randint(0, maxCycles)
        self.storage = random.randint(0, maxBalls)
        # self.cellsScored = self.autoCells + self.teleCycles*self.storage
        self.goal = random.randint(1, 3)
        self.hang = random.randint(0, 1)
        self.rotate = random.randint(0, 1)
        self.auto = 0
        self.tele = 0
        self.end = 0
        self.auto = self.autoMove * 5 + self.goal * 2 * self.autoCells
        self.tele = self.goal * self.teleCycles * self.storage
        if self.goal == 3:
            self.tele += (self.goal - 1) * self.teleCycles * (maxBalls - self.storage)
        self.end = self.hang * 25 + (1 - self.hang) * 5
        self.score = self.auto + self.tele + self.end

    def calculate(self):
        self.auto = self.autoMove * 5 + self.goal * 2 * self.autoCells
        self.tele = self.goal * self.teleCycles * self.storage
        self.end = self.hang * 25 + (1 - self.hang) * 5
        self.score = self.auto + self.tele + self.end


class Alliance:
    def __init__(self, num):
        self.number = num
        self.team = []
        self.score = 0
        self.sumBalls = 0
        self.done = True
        self.endGame = 0
        self.level = random.randint(0, 1) * 15
        self.levelDone = True
        self.auto = 0
        self.tele = 0
        self.end = 0
        self.goal = 0.0
        self.control = 0

    def add(self, robot):
        self.endGame += robot.end
        self.team.append(robot)
        self.sumBalls += robot.teleCycles * robot.storage + robot.autoCells
        self.score += robot.score
        if len(self.team) == 3:
            if self.sumBalls >= 20:
                self.score += 10
                self.control = 1
            if self.sumBalls >= 40:
                self.score += 20
                self.control = 2
        self.auto += robot.auto
        self.tele += robot.tele
        self.end += robot.end
        self.goal += robot.goal
        if robot.end >= 25 and self.levelDone:
            self.end += self.level
            self.levelDone = False


if __name__ == '__main__':
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    teams = []
    for i in range(numTeams):
        teams.append(Robot())

    alliances = []
    for i in range(numAlliances):
        a = Alliance(i + 1)
        a.add(teams.pop())
        a.add(teams.pop())
        a.add(teams.pop())
        alliances.append(a)

    autoMax = 0
    teleMax = 0
    endMax = 0
    totalWin = 0
    wins = []
    maxs = 0
    mins = 999
    data = []
    winData = []
    winLevel = 0.0
    panel = [0, 0, 0]
    for i in range(numMatches):
        red = alliances.pop()
        blue = alliances.pop()
        data.append([red.number, red.auto, red.tele, red.end, red.score, blue.number, blue.auto, blue.tele, blue.end,
                     blue.score])

        if red.score > blue.score:
            totalWin += red.score
            wins.append(red.score)
            winLevel += red.level
            winData.append([red.number, red.auto, red.tele, red.end, red.score, (red.goal/3), red.sumBalls])
            panel[red.control] += 1
        else:
            totalWin += blue.score
            wins.append(blue.score)
            winLevel += blue.level
            winData.append([blue.number, blue.auto, blue.tele, blue.end, blue.score, (blue.goal/3), blue.sumBalls])
            panel[blue.control] += 1

        if red.score >= maxs:
            maxs = red.score
        if red.score <= mins:
            mins = red.score
        if blue.score >= maxs:
            maxs = blue.score
        if blue.score <= mins:
            mins = blue.score

        autoMax = max(autoMax, max(red.auto, blue.auto))
        teleMax = max(teleMax, max(red.tele, blue.tele))
        endMax = max(endMax, max(red.end, blue.end))

    print("Average Winning Score: ", float(totalWin) / numMatches)
    print("Winning Score Stdev: ", numpy.std(wins))
    print("Max Auto Score: ", autoMax)
    print("Max TeleOp Score: ", teleMax)
    print("Max Endgame Score: ", endMax)
    print("Max Component Score: ", autoMax + teleMax + endMax)

    print("Average Winning Level: ", winLevel/numMatches)

    plt.hist([row[6] for row in winData])
    # plt.hist(panel)
    print(panel)
    plt.show()

    with open('output.csv', 'w', newline='') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        wr.writerows(data)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
