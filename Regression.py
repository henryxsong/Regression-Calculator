# Created by Henry Song
# for CS492 Research project
#
# Professor: Dr. Zou

import sys
import numpy as np
# from covidtracking import CovidTracking

global size
global m11, m12, m13, m14
global m21, m22, m23, m24
global m31, m32, m33, m34
global l0, l1, l2, l3
global a, b, c
global slope, y_intercept


# Calculates the Exponential Regression Line
# @param x - list of integer values representing data on the x-axis
# @param y - list of integer values representing data on the y-axis
def find_exponential_regression(x, y):
    linearalized = convert_exponential_to_linear(y)
    find_linear_regression(x, linearalized)

    global a, b, c, slope, y_intercept
    b = slope
    c = y_intercept
    a = np.exp(c)


# Calculates the Quadratic Regression Line
# @param x - list of integer values representing data on the x-axis
# @param y - list of integer values representing data on the y-axis
def find_quadratic_regression(x, y):
    global m11
    m11 = find_sum(power_vector(x, 4))
    global m12
    m12 = find_sum(power_vector(x, 3))
    global m13
    m13 = find_sum(power_vector(x, 2))
    global m14
    m14 = find_sum(find_xy(power_vector(x, 2), yData))

    global m21
    m21 = m12
    global m22
    m22 = m13
    global m23
    m23 = find_sum(x)
    global m24
    m24 = find_sum(find_xy(x, y))

    global m31
    m31 = m13
    global m32
    m32 = m23
    global m33
    m33 = size
    global m34
    m34 = find_sum(y)

    global l0
    l0 = (m11 * m22 * m33) - (m11 * m23 * m32) - (m12 * m21 * m33) + (m12 * m23 * m31) + \
         (m13 * m21 * m32) - (m13 * m22 * m31)
    global l1
    l1 = (m14 * m22 * m33) - (m14 * m23 * m32) - (m12 * m24 * m33) + (m12 * m23 * m34) + \
         (m32 * m24 * m13) - (m34 * m13 * m22)
    global l2
    l2 = (m11 * m24 * m33) - (m11 * m23 * m34) - (m14 * m33 * m21) + (m14 * m23 * m31) + \
         (m13 * m21 * m34) - (m13 * m24 * m31)
    global l3
    l3 = (m11 * m22 * m34) - (m11 * m24 * m32) - (m12 * m34 * m21) + (m12 * m24 * m31) + \
         (m14 * m21 * m32) - (m14 * m22 * m31)

    global a
    a = l1 / l0
    global b
    b = l2 / l0
    global c
    c = l3 / l0


# Calculates the Linear Regression Line
# @param x - list of integer values representing data on the x-axis
# @param y - list of integer values representing data on the y-axis
def find_linear_regression(x, y):
    global m11
    m11 = find_sum(power_vector(x, 2))
    global m12
    m12 = find_sum(x)
    global m13
    m13 = find_sum(find_xy(x, y))
    global m21
    m21 = m12
    global m22
    m22 = len(x)
    global m23
    m23 = find_sum(y)

    global l0
    l0 = (m11*m22) - (m12*m21)
    global l1
    l1 = (m13*m22) - (m12*m23)
    global l2
    l2 = (m11*m23) - (m21*m13)

    global slope
    slope = l1/float(l0)
    global y_intercept
    y_intercept = l2/float(l0)


# Calculates Future Predictions Exponential Regression Line
# Y(x; a,b) = a*e^(bx)
# @param _a - variable a of exponential equation
# @param _b - variable b of exponential equation
# @param i - x value
def find_future_exponential_prediction(_a, _b, i):
    print(" ", i, " : ", '%.4f' % (_a * np.exp(_b * i)))


# Calculates Future Predictions Quadratic Regression Line
# y = ax^2 + bx + c
# @param _a - variable a of quadratic equation
# @param _b - variable b of quadratic equation
# @param _c - variable c of quadratic equation
# @param i - x value
def find_future_quad_prediction(_a, _b, _c, i):
    print(" ", i, " : ", '%.4f' % (_a * pow(i, 2) + _b * i + _c))


# Calculates Future Predictions Linear Regression Line
# y = mx + b
# @param m - slope of line
# @param b - y-intercept of line
# @param i - x value
def find_future_linear_prediction(_m, _b, _i):
    print(" ", _i, " : ", '%.4f' % (_m*_i+_b))


# Reads data from the user. The user can enter data without declaring the number of data entries.
# @return list of all data entered by the user
def read_data():
    print("Enter yearly data: ")
    print("Press 'q' to quit")

    year = 1
    user_in = []

    while True:
        user_in.append(input("Year " + str(year) + " : "))
        year = year + 1

        if user_in[-1] == 'q':
            user_in.remove('q')
            break

    # Converts string list to float list
    temp = []
    for i in user_in:
        temp.append(float(i))

    return temp


# Finds corresponding x-axis values
# @param s - Size of list
# @return list of x-axis values
def find_x_data(s):
    array = []
    for i in range(s):
        array.append(i+1)
    return array


# Calculates (x*y) of a list
# @param x values
# @param y values
# @return (x*y) values
def find_xy(x, y):
    out = []
    if len(x) == len(y):
        for i in range(len(x)):
            out.append(float(x[i]) * float(y[i]))
    return out


# Finds the sum of a group of numbers
# @param data_in - list array of integers
# @return Sum of all values in the list
def find_sum(data_in):
    return sum(data_in)


# Calculates the squared of a list
# For example: (x)^2
# @param data_in - list of base values
# @param exp - exponent
# @return list of squared values
def power_vector(data_in, exp):
    out = []
    for i in data_in:
        out.append(pow(i, exp))
    return out


# Converts exponential values into linear values (utilizing natural log)
# @param array - array of values to be converted
# @return list of converted values
def convert_exponential_to_linear(array):
    converted_output = []
    for x in array:
        converted_output.append(np.log(x))
    return converted_output


# Print data values of a vector
# @param data - vector of y-axis values
def print_data(data):
    print("Given Data: ")
    print("  x  |  y")
    i = 1
    for x in data:
        print(" ", i, " : ", x)
        i = i + 1


# Prints linear-related data values, calculations, and predictions
def print_linear():
    print()
    print("M11 = ", m11, "\t\tM21 = ", m21)
    print("M12 = ", m12, "\t\tM22 = ", m22)
    print("M13 = ", m13, "\t\tM23 = ", m23)
    print("L = ", '%.4f' % l0, "\t\tL1 = ", '%.4f' % l1, "\t\tL2 = ", '%.4f' % l2)
    print("a = L1/L = ", '%.4f' % slope, "\t\tb = L2/L = ", '%.4f' % y_intercept)

    print()
    print("f(x) = ", '%.4f' % slope, "x + ", '%.4f' % y_intercept)
    print("Slope(m) = ", '%.4f' % slope)
    print("Y-Intercept(b) = ", '%.4f' % y_intercept)

    print()
    print("Future Predictions:")
    print("  x  |  y")
    for n in range(5):
        find_future_linear_prediction(slope, y_intercept, n + size + 1)


# Prints quadratic-related data values, calculations, and predictions
def print_quadratic():
    print()
    print("| M11 = ", '%.4f' % m11, "\t\tM12 = ", '%.4f' % m12, "\t\tM13 = ", '%.4f' % m13,
          "\t|\tM14 = ", '%.4f' % m14, "\t|")
    print("| M21 = ", '%.4f' % m21, "\t\tM22 = ", '%.4f' % m22, "\t\tM23 = ", '%.4f' % m23,
          "\t|\tM24 = ", '%.4f' % m24, "\t\t|")
    print("| M31 = ", '%.4f' % m31, "\t\tM32 = ", '%.4f' % m32, "\t\tM33 = ", '%.4f' % m33,
          "\t|\tM34 = ", '%.4f' % m34, "\t\t|")
    print()
    print("L = ", '%.4f' % l0, "\t\tL1 = ", '%.4f' % l1, "\t\tL2 = ", '%.4f' % l2, "\t\tL3 = ", '%.4f' % l3)
    print("a = L1/L = ", '%.4f' % a, "\t\tb = L2/L = ", '%.4f' % b, "\t\tc = L3/L = ", '%.4f' % c)

    print()
    print("Quadratic Formula:")
    print("f(x) = ", '%.4f' % a, "*x^2 + ", '%.4f' % b, "*x + ", '%.4f' % c)
    print()

    print("Future Predictions:")
    print("  x  |  y")
    for n in range(5):
        find_future_quad_prediction(a, b, c, n + size + 1)


# Prints exponential-related data values, calculations, and predictions
def print_exponential():
    print()
    print("Exponential Formula:")
    print("Y(x; a,b) = a * e^(bx), where:")
    print("a = ", '%.4f' % a)
    print("b = ", '%.4f' % b)
    print("Giving us: Y(x; a,b) = ", '%.4f' % a, " * e^(", '%.4f' % b, "* x)")
    print()
    print("Future Predictions:")
    print("  x  |  y")
    for n in range(5):
        find_future_exponential_prediction(a, b, n + size + 1)


if __name__ == '__main__':
    print("Linear, Quadratic, & Exponential Regression Algorithms [written in Python]")
    print("By Henry Song")
    print()

    print("Enter 1 to use hard-coded data for Guam's COVID cases from March-December")
    print("Enter 2 to use user-input data")
    # print("Enter 3 to CovidTracking.com API data")
    data_option = int(input("Select option: "))
    print()

    print("Enter 1 to calculate Linear Regression")
    print("Enter 2 to calculate Quadratic Regression")
    print("Enter 3 to calculate Exponential Regression")
    method_option = int(input("Select option: "))
    print()

    if data_option == 1:
        if method_option == 1:
            print("Using Linear Regression on Guam's COVID cases from March-December:")
        elif method_option == 2:
            print("Using Quadratic Regression on Guam's COVID cases from March-December:")
        elif method_option == 3:
            print("Using Exponential Regression on Guam's COVID cases from March-December:")
    elif data_option == 2:
        if method_option == 1:
            print("Using Linear Regression on user-entered data:")
        elif method_option == 2:
            print("Using Quadratic Regression on user-entered data:")
        elif method_option == 3:
            print("Using Exponential Regression on user-entered data:")

    if data_option == 1:
        xData = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        yData = [71, 142, 167, 259, 354, 1442, 2550, 4761, 6889]
        size = len(xData)
        print_data(yData)
        if method_option == 1:
            find_linear_regression(xData, yData)
            print_linear()
        elif method_option == 2:
            find_quadratic_regression(xData, yData)
            print_quadratic()
        elif method_option == 3:
            find_exponential_regression(xData, yData)
            print_exponential()
    elif data_option == 2:
        yData = list(read_data())
        xData = list(find_x_data(len(yData)))
        size = len(xData)
        print_data(yData)
        if method_option == 1:
            find_linear_regression(xData, yData)
            print_linear()
        elif method_option == 2:
            find_quadratic_regression(xData, yData)
            print_quadratic()
        elif method_option == 3:
            find_exponential_regression(xData, yData)
            print_exponential()