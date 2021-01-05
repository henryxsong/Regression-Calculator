# Created by Henry Song
# for CS492 Research project
#
# Professor: Dr. Zou

# Import Statements
import sys
import numpy as np
import matplotlib.pyplot as plt
# from covidtracking import CovidTracking


# Global Variables
global size
global m11, m12, m13, m14
global m21, m22, m23, m24
global m31, m32, m33, m34
global l0, l1, l2, l3
global a, b, c
global slope, y_intercept


# Calculates the values of an Logarithmic Regression Line equation
# @param x - list of integer values representing data on the x-axis
# @param y - list of integer values representing data on the y-axis
def find_log_regression(x, y):
    sum_of_y = find_sum(y)
    y_lnx = 0
    lnx = 0
    lnx_2 = 0

    for i in range(len(x)):
        y_lnx += y[i] * np.log(x[i])
        lnx += np.log(x[i])
        lnx_2 += (np.log(x[i]))**2
    
    global a, b
    b = ((size * y_lnx) - (sum_of_y * lnx))/((size * lnx_2) - (lnx**2))
    a = (sum_of_y - (b * lnx))/(size)


# Calculates the values of an Exponential Regression Line equation
# @param x - list of integer values representing data on the x-axis
# @param y - list of integer values representing data on the y-axis
def find_exponential_regression(x, y):
    linearalized = convert_exponential_to_linear(y)
    find_linear_regression(x, linearalized)

    global a, b, c, slope, y_intercept
    b = slope
    c = y_intercept
    a = np.exp(c)


# Calculates the values of a Quadratic Regression Line equation
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


# Calculates the values of a Linear Regression Line equation
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


# Calculates logarithmic prediction
# Y(x; a,b) = a + b*ln(x)
# @param _a - variable a of logarithmic equation
# @param _b - variable b of logarithmic equation
# @param i - x value
def log_function(_a, _b, i):
    return (_a + _b * np.log(i))


# Calculates exponential prediction
# Y(x; a,b) = a*e^(bx)
# @param _a - variable a of exponential equation
# @param _b - variable b of exponential equation
# @param i - x value
def exponential_function(_a, _b, i):
    return (_a * np.exp(_b * i))


# Calculates quadratic prediction
# y = ax^2 + bx + c
# @param _a - variable a of quadratic equation
# @param _b - variable b of quadratic equation
# @param _c - variable c of quadratic equation
# @param i - x value
def quadratic_function(_a, _b, _c, i):
    return (_a * pow(i, 2) + _b * i + _c)


# Calculates linear prediction
# y = mx + b
# @param m - slope of line
# @param b - y-intercept of line
# @param i - x value
def linear_function(_m, _b, _i):
    return (_m*_i+_b)


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
def find_x_data(s, add_on):
    array = []
    for i in range(s + add_on):
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


# Calculates regression line using respective algorithm
def find_regression_line(xData_in, yData_in, option):
    array = []
    if option == 1:
        for i in range(len(xData_in)):
            array.append(linear_function(slope, y_intercept, xData_in[i]))
    elif option == 2:
        for i in range(len(xData_in)):
            array.append(quadratic_function(a, b, c, xData_in[i]))
    elif option == 3:
        for i in range(len(xData_in)):
            array.append(exponential_function(a, b, xData_in[i]))
    elif option == 4:
        for i in range(len(xData_in)):
            array.append(log_function(a, b, xData_in[i]))
    return np.asarray(array)


# Uses MatPlotLib to visualize dataset
# @param xData_in - input data of x-values (utilizes numpy array data structure)
# @param yData_in - input data of y-values (utilizes numpy array data structure)
def plot_data(xData_in, xData_predictions, yData_in, yData_predictions, _title):
    plt.plot(xData_in, yData_in, 'bo')
    plt.plot(xData_in, yData_in, 'b-', label='Original')
    plt.plot(xData_predictions, yData_predictions, 'r--', label='Regression Line')
    plt.plot(xData_predictions, yData_predictions, 'ro')
    plt.title(_title)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()
    

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
        print(" ", n + size + 1, " : ", '%.4f' % linear_function(slope, y_intercept, n + size + 1))


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
        print(" ", n + size + 1, " : ", '%.4f' % quadratic_function(a, b, c, n + size + 1))


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
        print(" ", n + size + 1, " : ", '%.4f' % exponential_function(a, b, n + size + 1))


# Prints logarithmic-related data values, calculations, and predictions
def print_log():
    print()
    print("Logarithmic Formula:")
    print("Y(x; a,b) = a * b*ln(x), where:")
    print("a = ", '%.4f' % a)
    print("b = ", '%.4f' % b)
    print("Giving us: Y(x; a,b) = ", '%.4f' % a, " + ", '%.4f' % b,"* ln(x)")
    print()
    print("Future Predictions:")
    print("  x  |  y")
    for n in range(5):
        print(" ", n + size + 1, " : ", '%.4f' % log_function(a, b, n + size + 1))


if __name__ == '__main__':
    print("Linear, Quadratic, Exponential, & Logarithmic Regression Calculator [written in Python]")
    print("By Henry Song")
    print()

    print("Enter 1 to use hard-coded data for Guam's COVID cases from March-December")
    print("Enter 2 to use user-input data")
    # print("Enter 3 to CovidTracking.com API data")
    data_option = int(input("Select option: "))
    while data_option > 2 or data_option < 1: data_option = int(input("Please enter valid option: "))
    print()

    print("Enter 1 to calculate Linear Regression")
    print("Enter 2 to calculate Quadratic Regression")
    print("Enter 3 to calculate Exponential Regression")
    print("Enter 4 to calculate Logarithmic Regression")
    method_option = int(input("Select option: "))
    while method_option > 4 or method_option < 1: method_option = int(input("Please enter valid option: "))
    print()

    plot_title = ""

    if data_option == 1:
        if method_option == 1:
            print("Using Linear Regression on Guam's COVID cases from March-December:")
            plot_title = "Guam's COVID cases from March-December, linear regression"
        elif method_option == 2:
            print("Using Quadratic Regression on Guam's COVID cases from March-December:")
            plot_title = "Guam's COVID cases from March-December, quadratic regression"
        elif method_option == 3:
            print("Using Exponential Regression on Guam's COVID cases from March-December:")
            plot_title = "Guam's COVID cases from March-December, exponential regression"
        elif method_option == 4:
            print("Using Logarithmic Regression on Guam's COVID cases from March-December:")
            plot_title = "Guam's COVID cases from March-December, logarithmic regression"
    elif data_option == 2:
        if method_option == 1:
            print("Using Linear Regression on user-entered data:")
            plot_title = "User-Entered Data, linear regression"
        elif method_option == 2:
            print("Using Quadratic Regression on user-entered data:")
            plot_title = "User-Entered Data, quadratic regression"
        elif method_option == 3:
            print("Using Exponential Regression on user-entered data:")
            plot_title = "User-Entered Data, exponential regression"
        elif method_option == 4:
            print("Using Logarithmic Regression on user-entered data:")
            plot_title = "User-Entered Data, logarithmic regression"

    if data_option == 1:
        xData = np.asarray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        yData = np.asarray([71, 142, 167, 259, 354, 1442, 2550, 4763, 6902, 7317])
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
        elif method_option == 4:
            find_log_regression(xData, yData)
            print_log()
        
        xData_predictions = np.asarray(list(find_x_data(len(yData), 5)))
        yData_predictions = find_regression_line(xData_predictions, yData, method_option)

        plot_option = str(input("Plot data (y/n): "))
        while plot_option not in ("y", "n"): plot_option = input("Please enter valid option (y/n): ")
        if plot_option[0] == "y":
            plot_data(xData, xData_predictions, yData, yData_predictions, plot_title)
    elif data_option == 2:
        yData = np.asarray(list(read_data()))
        xData = np.asarray(list(find_x_data(len(yData), 0)))
        size = len(xData)
        print()
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
        elif method_option == 4:
            find_log_regression(xData, yData)
            print_log()

        xData_predictions = np.asarray(list(find_x_data(len(yData), 5)))
        yData_predictions = find_regression_line(xData_predictions, yData, method_option)

        plot_option = str(input("Plot data (y/n): "))
        while plot_option not in ("y", "n"): plot_option = input("Please enter valid option (y/n): ")
        if plot_option[0] == "y":
            plot_data(xData, xData_predictions, yData, yData_predictions, plot_title)