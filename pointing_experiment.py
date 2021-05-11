import sys
import json
import math
import random
from PyQt5 import QtGui, QtWidgets, QtCore
import csv

"""
setup file should look like this:
{"USER_ID": 1,
 "REPETITIONS": 5,
  "COLORS": [[200,0,0],[0,200,0],[0,0,200]],
  "TARGETS": (4,4),
  "NOVEL_TECHNIQUE": False}
"""


class PointingModel(object):

    def __init__(self, user_id, colors, targets, novel_technique, repetitions):
        self.timer = QtCore.QTime()
        self.user_id = user_id
        self.latin_square = self.balanced_latin_squares(len(colors), user_id)
        self.colors = colors
        self.current_color = [0, 0, 0]
        self.targets = targets
        self.elapsed_repetitions = 0
        self.mouse_moving = False
        self.elapsed_conditions = 0
        self.errors = 0
        self.novel_technique = novel_technique
        self.repetitions = repetitions
        self.log_writer = csv.writer(sys.stdout)
        #sys.stdout.write("user_id, elapsed_conditions, elapsed_repetitions,"
                                  "target, click_offset, distance, time, errors, timestamp \n")

    # creates latin squares for counter balancing and selects square baed on user id
    # code for creating squares taken from https://medium.com/@graycoding/balanced-latin-squares-in-python-2c3aa6ec95b9
    def balanced_latin_squares(self,n, id):
        l = [[((j // 2 + 1 if j % 2 else n - j // 2) + i) % n + 1 for j in range(n)] for i in range(n)]
        if n % 2:  # Repeat reversed for odd n
            l += [seq[::-1] for seq in l]
        square = l[(id % len(l))]
        return square

    '''def start_measurement(self):
        if not self.mouse_moving:
            self.timer.start()
            self.mouse_moving = True

    def stop_measurement(self):
        if self.mouse_moving:
            elapsed = self.timer.elapsed()
            self.mouse_moving = False
            return elapsed
        else:
            self.debug("not running")
            return -1
    '''
    # sets highlight color depending on the current condition
    def setColor(self):
        self.color = self.colors[self.latin_square[self.elapsed_conditions]-1]

    # checks if click was on the current target
    def clickOnTarget (self, click_pos, target):
        distance = math.sqrt(((click_pos[0] - target[0]) ** 2) + ((click_pos[1] - target[1]) ** 2))
        if distance < target[2]:
            click_offset = (target[0] - click_pos[0], target[1] - click_pos[1])
            self.elapsed_repetitions += 1
            self.logging(click_offset, distance, target, self.timer.restart())
            self.errors = 0
            return True
        else:
            self.errors += 1
            return False

    # logs test results to tdout in csv format
    def logging(self, click_offset, distance, target, time):
        self.log_writer.writerow([self.user_id, self.elapsed_conditions, self.elapsed_repetitions,
                                  target, click_offset, distance, time, self.errors, self.timestamp()])

    # returns timestamp of current time
    def timestamp(self):
        return QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)

class PointingTest(QtWidgets.QWidget):

    def __init__(self, model):
        super(PointingTest, self).__init__()
        self.model = model
        if self.model.targets[0] > self.model.targets[1]:
            self.screen_x_size = int(800 * self.model.targets[1]/self.model.targets[0])
            self.screen_y_size = int(800)
        else:
            self.screen_x_size = int(800)
            self.screen_y_size = int(800 * self.model.targets[0] / self.model.targets[1])
        self.start_pos = (self.screen_x_size/2, self.screen_y_size/2)
        self.target_circle = 0
        self.circles = []

        self.setFixedSize(self.screen_x_size, self.screen_y_size)
        self.show_explanation = True
        self.initUi()

    def initUi(self):
        self.setGeometry(0, 0, self.screen_x_size, self.screen_y_size)
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawBackground(event, qp)
        if self.show_explanation:
            self.drawExplanation(event, qp)
        else:
            self.circles = self.drawCircles(qp)
        qp.end()

    def drawBackground(self, event, qp):
        qp.setBrush(QtGui.QColor(200, 200, 200))
        qp.drawRect(event.rect())

    # writes test explanation on screen
    def drawExplanation(self, event, qp):
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 11))
        if self.model.elapsed_conditions >= len(self.model.colors):
            self.text = "The test is done, good job!. \n " \
                        "Press any key to exit"
        else:
            self.text = "In this test a bunch of circles will be shown on the screen. \n "\
                        "One of the circles will be highlighted by a color. \n"\
                        "Click on the highlighted circle as fast as you can, this will be repeated several times. \n"\
                        "As soon as you are ready start the test by pressing any key on your keyboard"
            self.model.setColor()
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    # is called when key is pressed an starts a test with the current condition. Quits app if all conditions were tested
    def keyPressEvent(self, event):
        if self.show_explanation:
            if self.model.elapsed_conditions >= len(self.model.colors):
                sys.exit()
            else:
                self.show_explanation = False
                self.model.timer.start()
                self.update()

    # is called when mouse button is clicked and then calls the clickOnTarget function of the model
    def mousePressEvent(self, event):
        if not self.show_explanation:
            click_pos = [event.x(), event.y()]
            if self.model.clickOnTarget(click_pos, self.target_circle):
                if self.model.elapsed_repetitions >= self.model.repetitions:
                    self.show_explanation = True
                    self.model.elapsed_repetitions = 0
                    self.model.elapsed_conditions += 1
                self.update()

    '''def mouseMoveEvent(self, ev):
        self.model.start_measurement()
        '''
    # draws circles on window
    def drawCircles(self, qp):
        x_circles = self.model.targets[0]
        y_circles = self.model.targets[1]
        circle_value = max(x_circles, y_circles)
        screen_value = max(self.screen_x_size, self. screen_y_size)
        distance = self.screen_x_size/(circle_value*4)
        diameter = screen_value/circle_value - distance
        radius = diameter/2
        pos_y = int(distance/2)
        pos_x = int(distance/2)
        target_num = random.randint(0, (x_circles*y_circles)-1)
        checkTarget = 0
        for i in range(x_circles):
            for k in range(y_circles):
                if checkTarget == target_num:
                    qp.setBrush(QtGui.QColor(self.model.color[0], self.model.color[1], self.model.color[2]))
                    qp.setPen(QtGui.QColor(self.model.color[0], self.model.color[1], self.model.color[2]))
                    self.target_circle = (pos_x+radius, pos_y+radius, radius)
                else:
                    qp.setBrush(QtGui.QColor(0, 0, 0))
                    qp.setPen(QtGui.QColor(0, 0, 0))
                qp.drawEllipse(pos_x, pos_y, diameter, diameter)
                self.circles.append((pos_x+radius, pos_y+radius, radius))
                pos_x += diameter + distance
                checkTarget += 1
            pos_x = distance/2
            pos_y += diameter + distance
        self.setMousePosition(self.start_pos)
        return self.circles

    # sets mouse position to desired coordinates
    def setMousePosition(self,coordinates):
        QtGui.QCursor.setPos(self.mapToGlobal(QtCore.QPoint(coordinates[0], coordinates[1])))

def main():
    app = QtWidgets.QApplication(sys.argv)
    if len(sys.argv) < 2:
        sys.stderr.write("you need to pass a setup json file")
        sys.exit(1)
    model = PointingModel(*parsedata(sys.argv[1]))
    pointing_test = PointingTest(model)
    sys.exit(app.exec_())

# reads setup information from json file
def parsedata(file):
    with open(str(file)) as f:
        setup_dict = json.load(f)
    user_id = setup_dict["USER_ID"]
    colors = setup_dict["COLORS"]
    targets = setup_dict["TARGETS"]
    if setup_dict["USE_NOVEL_TECHNIQUE"] == "yes":
        novel_technique = True
    else:
        novel_technique = False
    repetitions = setup_dict["REPETITIONS"]
    return user_id, colors, targets, novel_technique, repetitions

if __name__ == '__main__':
    main()