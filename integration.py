import math

class Function():
    
    def __init__(self, func_information, borders):
        self.function = func_information["function"]
        self.points_continuity = func_information["special_points"]["continuity"]
        self.points_discontinuity = func_information["special_points"]["discontinuity"]
        self.description = func_information["description"]
        self.integration = None
        
        if(borders[0] > borders[1]):
            self.left_border = borders[1]
            self.right_border = borders[0]
            self.sign = -1
        else:
            self.left_border = borders[0]
            self.right_border = borders[1]
            self.sign = 1

    def comp_y(self, x):
        if self.points_continuity is not None:
            for point in self.points_continuity:
                if point[0] == x: return point[1]
        return self.function(x)

    def check_discontinuity(self):
        if self.points_discontinuity is not None:
            for point in self.points_discontinuity:
                assert (point < self.left_border or point > self.right_border), "Невозможно вычислить интеграл: в интервале содержится точка неустранимого разрыва {0}".format(point)

    def comp_accuracy(self, current_integration):
        if self.integration is None: return None
        return 1/3*abs(current_integration - self.integration)

    def __str__(self):
        return self.description


def comp_integration(function: Function, accuracy):
    function.check_discontinuity()
    n = 1
    while True:
        h = (function.right_border - function.left_border)/n
        riemann_sum = (function.comp_y(function.left_border) + function.comp_y(function.right_border))/2
        for i in range(1, n):
            riemann_sum +=function.comp_y(function.left_border + i*h)
        riemann_sum = function.sign*riemann_sum*h
        current_accuracy = function.comp_accuracy(riemann_sum)
        if current_accuracy is not None and current_accuracy < accuracy: return riemann_sum, n, current_accuracy
        function.integration = riemann_sum
        n*=2

f1 = {
    'description': 'x + 5',
    'special_points': {
        'continuity': None,
        'discontinuity': None
    },
    'function': lambda x : x + 5
}

f2 = {
    'description': '2*x^3 + 6 * x^2 - 5 * x + 12',
    'special_points': {
        'continuity': None,
        'discontinuity': None
    },
    'function': lambda x: 2*x**3 + 6*x**2 - 5*x + 12
}

f3 = {
    'description': '3/((x+2)*(x-5))',
    'special_points': {
        'continuity': None,
        'discontinuity': [-2.0, 5.0]
    },
    'function': lambda x: 3/(x+2)/(x-5)
}

f4 = {
    'description': '(x^3-x^2)/((x-1)*(x+10))',
    'special_points': {
        'continuity': [[1.0, 1.0/11.0]],
        'discontinuity': [-10.0]
    },
    'function': lambda x: (x**3-x**2)/(x-1)/(x+10)
}

f5 = {
    'description': 'sin(x)/x',
    'special_points': {
        'continuity': [[0.0, 1.0]],
        'discontinuity': None
    },
    'function': lambda x: math.sin(x)/x
}

def read_parametres():
    print("Введите номер функции, интеграл которой вы хотите вычислить")
    print("1. {0}\n2. {1}\n3. {2}\n4. {3}\n5. {4}".format(f1["description"], f2["description"], f3["description"], f4["description"], f5["description"]))
    while True:
        try:
            number = int(input().strip())
            assert number <= 5 and number >= 1, "Введите число от 1 до 5"
            break
        except ValueError:
            print("Неверный формат числа. Введите число от 1 до 5")
        except AssertionError as inst:
            print(inst.args[0])
    print("Введите пределы интгрирования через пробел")
    while True:
        try:
            borders = input().split(" ")
            assert len(borders) == 2
            borders[0] = float(borders[0])
            borders[1] = float(borders[1])
            break
        except Exception:
            print("Введите два числа - левую и правую границу интегрирования через пробел")
    print("Введите точность")
    while True:
        try:
            accuracy = abs(float(input().strip()))
            break
        except Exception:
            print("Неверный формат числа. Попробуйте ещё раз")

    if number == 1: f = f1
    if number == 2: f = f2
    if number == 3: f = f3
    if number == 4: f = f4
    if number == 5: f = f5
    try:
        integration, n, result_accuracy = comp_integration(Function(f, borders), accuracy)
        print("Функция:\n{0}\nПределы интегрирования:\n{1}\nВведенная точность\n{2}\nПолученное значение интеграла:\n{3}\nКоличество разбиений:\n{4}\nПолученная погрешность:\n{5}".format(f["description"], borders, accuracy, integration, n, result_accuracy))
    except AssertionError as inst:
        print(inst.args[0])