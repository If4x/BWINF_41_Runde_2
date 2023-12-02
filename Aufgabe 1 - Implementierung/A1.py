
# Program by Imanuel Fehse

# 41. Bundeswettbewerb Informatik
# Round 2
# Exercise 1: Weniger krumme Touren

# -*- coding: utf-8 -*-


"""
------------------------------
IMPORTS
------------------------------
"""


import os
from datetime import datetime
from matplotlib import pyplot as plt
import math


"""
------------------------------
GENERAL FUNCTIONS
------------------------------
"""


# read file and return data as list split by line and removed empty lines
def read_file(filename):
    f = open(filename, "r")
    raw_data = f.read().split("\n")
    # remove empty lines
    raw_data.remove("")

    # convert data to usable format
    data = []
    for coordinate in raw_data:
        xy = coordinate.split(" ")
        x = xy[0]
        y = xy[1]
        data.append([float(x), float(y)])
    return data


# get and return current date and time
def get_time():
    return datetime.now().strftime("%d_%B_time_%H_%M_%S")


# get and return path of this file (python file that's executed)
def get_path():
    return os.path.dirname(os.path.abspath(__file__))


# calculate and return vector from point1 to point2
def get_vector(point1, point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    x = x2 - x1
    y = y2 - y1
    return [x, y]


# return distance between two points
def get_distance(point1, point2):
    return math.dist(point1, point2)


# return length of vector
def get_vector_length(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)


# get and return dot product of two vectors
def get_dot_product(vector_a, vector_b):
    return vector_a[0] * vector_b[0] + vector_a[1] * vector_b[1]


# return cutting angle of two vectors
def get_cutting_angle(vector_a, vector_b):
    # check if vectors are equal; if they are, the cutting angle is 0°
    if vector_a != vector_b:
        # get dot product
        dot_product = get_dot_product(vector_a, vector_b)
        # get length of vectors
        length_a = get_vector_length(vector_a)
        length_b = get_vector_length(vector_b)

        # calculate cutting angle
        cutting_angle = math.acos(dot_product / (length_a * length_b))
        return math.degrees(cutting_angle)

    # if vectors are equal, return 0°
    else:
        # print("vector_a == vector_b --> cutting angle is 0°")
        return 0


# create and save plot with results
def create_plot(done, not_done, path, time):
    # define path which plot will be saved to
    folder = path + "/renders/results_" + time
    # create plot
    plt.grid()
    plt.title(file + " " + time)

    # convert done points to usable format (line) plot can use
    done_converted = []
    for point in done:
        done_converted.append(point[0])

    # convert done points to format (line) plot can use
    x_done = []
    y_done = []
    for point in done_converted:
        x_done.append(point[0])
        y_done.append(point[1])
    # add to plot
    plt.plot(x_done, y_done, marker="o", markersize=3,
             markeredgecolor="black", markerfacecolor="green")

    # add not done points to plot
    for point in not_done:
        plt.plot(point[0], point[1], marker="o", markersize=5,
                 markeredgecolor="black", markerfacecolor="red")

    # create folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    # save plot and show it
    plt.savefig(folder + "/plot_" + time + ".png", dpi=600)
    plt.savefig(folder + "/plot_" + time + ".svg")
    plt.show()


# calculate length of route
def get_length_route(route):
    length = 0
    for i in range(len(route) - 1):
        length += get_distance(route[i], route[i + 1])
    return length


"""
------------------------------
CLASSES
------------------------------
"""


class Coordinates:
    # initialize class
    def __init__(self, filename):
        # general
        self.path = get_path()  # path of executed file
        self.time = get_time()  # current time

        # coordinates
        self.all_points = []    # all coordinates
        self.done = []          # coordinates that are already done
        self.not_done = []      # coordinates that are not done yet
        self.stp = []           # start point
        self.lp = []            # last point
        self.cp = []            # current point
        self.cor_path = []      # base path; source to search for other paths
        self.cur_path = []      # path to store current path (used to find other paths)
        self.cur_path1 = []     # path to store current path (used to find other paths) points added

        # set to values
        self.all_points = read_file(filename)   # read coordinates from file and save them to all_points
        self.not_done = self.all_points.copy()  # copy all_points to not_done

    def next_point(self):
        cp = self.cp.copy()
        lp = self.lp.copy()

        # calculate distances to all not done points
        distances = []
        for point in self.not_done.copy():
            distances.append([point, get_distance(cp, point)])
        # order from small distance to high distance
        distances.sort(key=lambda x: x[1])

        # check which points are valid
        valid_points = []
        for point in distances:
            # get vectors
            # if lp == [] --> first point is being checked (no lp available)
            if lp:
                vector_lp_cp = get_vector(lp, cp)
                vector_cp_point = get_vector(cp, point[0])
            else:
                vector_lp_cp = get_vector(cp, point[0])
                vector_cp_point = get_vector(cp, point[0])

            # get cutting angle
            cutting_angle = get_cutting_angle(vector_lp_cp, vector_cp_point)

            # check if cutting angle is smaller than or 90°
            if cutting_angle <= 90:
                valid_points.append(point)
            else:
                pass

        # check if there are valid points
        if not valid_points:
            return False

        else:
            # save current point and every possible point to done
            # add every valid point besides the first one to other_points
            other_points = []
            for point in valid_points[1:]:
                other_points.append(point[0])
            self.done.append([valid_points[0][0], other_points])
            self.not_done.remove(valid_points[0][0])

            # move cp to lp and nearest possible point to cp
            self.lp = cp.copy()
            self.cp = valid_points[0][0].copy()

            return True

    def find_solution(self):
        # search for next point till no valid point is found
        while self.next_point():
            pass

        # check if all points are done (solution was found)
        if self.check_results():
            self.save_results()
        else:
            """
            loop backwards through calculated path and search for other solutions by using other points (saved in
            self.done). For every of this actions calculate next points to search for an other path. Repeat this 
            process for this path and all following.
            """
            self.cor_path = self.done.copy() # save path to find other paths
            # reset values
            self.done = []
            self.not_done = self.all_points.copy()

            # loop backwards through calculated path
            for point in reversed(self.cor_path):
                # get index of point in self.cor_path
                index = self.cor_path.index(point)
                # copy cor_path to cur_path and remove all points after current point
                self.cur_path = self.cor_path.copy()[:index]

                # loop through all other points
                for other_point in point[1]:
                    leftover = point[1].copy()
                    leftover.remove(other_point)
                    self.cur_path1 = self.cur_path.copy()
                    self.cur_path1.append([other_point, [leftover]])
                    self.cp = self.cur_path1[-1][0].copy()
                    self.lp = self.cur_path1[-2][0].copy()

                    # add every point included in cur_path to done
                    # reset values
                    self.done = []
                    self.not_done = self.all_points.copy()
                    for p_in_cur_path in self.cur_path1.copy():
                        self.done.append(p_in_cur_path)
                        self.not_done.remove(p_in_cur_path[0])

                    # search for next point till no valid point is found
                    while self.next_point():
                        pass
                    # check if all points are done (solution was found)
                    if self.check_results():
                        self.save_results()
                        exit()
                    else:
                        pass

    def check_results(self):
        # check if all point are done
        if not self.not_done:
            print("\n\nALL POINTS ARE DONE\n")
            print("Saving results...")
            return True
        else:
            return False

    # save results
    def save_results(self):
        create_plot(self.done.copy(), self.not_done.copy(), self.path, self.time)

        # save done to file
        location = self.path + "/renders/results_" + self.time + "/results_" + self.time + ".txt"
        f = open(location, "a")
        data = []
        for point in self.done.copy():
            data.append(point[0])

        length_route = get_length_route(data)
        f.write(str(data) + "\nLength of route: " + str(length_route) + "km")
        print("Results saved to", location)


"""
------------------------------
Program
------------------------------
"""

# get file
while True:
    file = input("Enter file name: ")
    try:
        open(file, "r")
        break
    except FileNotFoundError:
        print("File not found")

Cor = Coordinates(file)

Cor.cp = Cor.not_done[0]
Cor.not_done.remove(Cor.cp.copy())
Cor.done.append([Cor.cp.copy(), Cor.not_done.copy()])
print("searching for solution...")
Cor.find_solution()
