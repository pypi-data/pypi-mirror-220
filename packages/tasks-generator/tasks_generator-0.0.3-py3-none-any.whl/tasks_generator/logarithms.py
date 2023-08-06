import random
import fractions
import math


# Задача № 10991
def random_logarithm():
    base_of_logarithm = random.randint(2, 15)
    answer_of_logarithm = random.randint(0, 4)
    degree_of_logarithm = base_of_logarithm**answer_of_logarithm
    answer = round(math.log(degree_of_logarithm, base_of_logarithm))
    task = f'Вычислите: \(log_'"{" + str(base_of_logarithm)+'}{'+str(degree_of_logarithm)+'}\)'
    return answer, task


# Task № 14615
def logarithm_multiplication():
    base_of_logarithm1 = random.randint(2, 10)
    answer_of_logarithm1 = random.randint(0, 4)
    degree_of_logarithm1 = base_of_logarithm1 ** answer_of_logarithm1
    m = random.randint(1, 3)
    k = random.randint(1, 3)
    base_of_logarithm2 = random.randint(2, 10)
    answer_of_logarithm2 = random.randint(0, 4)
    degree_of_logarithm2 = base_of_logarithm2 ** answer_of_logarithm2
    answer = round(k * math.log(degree_of_logarithm2, base_of_logarithm2) *(m * math.log(degree_of_logarithm1,
                                                                                   base_of_logarithm1)))
    if m >= 2 and k < 2:
        task = f'Вычислите:' f'(\(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '})' "*" f'({m}*(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})\)'
    elif m < 2 and k < 2:
        task = f'Вычислите:' f'(\(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '})' "*" f'(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})\)'
    elif m >= 2 and k >= 2:
        task = f'Вычислите:' f'(\({k}*(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '}))' "*" f'({m}*(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '}))\)'
    elif m < 2 and k >= 2:
        task = f'Вычислите:' f'(\({k}*(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '}))' "*" f'(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})\)'
    return answer, task


def logarithm_division():
        base_of_logarithm1 = random.randint(2, 10)
        answer_of_logarithm1 = random.randint(1, 4)
        degree_of_logarithm1 = base_of_logarithm1 ** answer_of_logarithm1
        m = random.randint(1, 3)
        k = random.randint(1, 3)
        base_of_logarithm2 = random.randint(2, 10)
        answer_of_logarithm2 = random.randint(1, 4)
        degree_of_logarithm2 = base_of_logarithm2 ** answer_of_logarithm2
        answer = format(k * math.log(degree_of_logarithm2, base_of_logarithm2) / (m * math.log(degree_of_logarithm1,
                                                                                        base_of_logarithm1)), '.4')
        if m >= 2 and k < 2:
            task = f'Вычислите:' f'(\(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
                   '})' "/" f'({m}*(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})\)'
        elif m < 2 and k < 2:
            task = f'Вычислите:' f'(\(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
                   '})' "/" f'(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})\)'
        elif m >= 2 and k >= 2:
            task = f'Вычислите:' f'(\({k}*(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
                   '}))' "/" f'({m}*(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '}))\)'
        elif m < 2 and k >= 2:
            task = f'Вычислите:' f'(\({k}*(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
                   '}))' "/" f'(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})\)'

        return answer, task


#Задача 14526
def random_logarithm_in_degree():
    base_of_logarithm = random.randint(2, 15)
    answer = random.randint(0, 4)
    degree_of_logarithm = base_of_logarithm**answer
    n = random.randint(1, 5)
    answer = round(n ** math.log(degree_of_logarithm, base_of_logarithm))
    if n < 2:
        task = f'Вычислите: \(log_'"{" + str(base_of_logarithm)+'}{'+str(degree_of_logarithm)+'}\)'
    else:
        task = f'Вычислите: \({n}^'"{"'log_'"{" + str(base_of_logarithm) + '}{' + str(degree_of_logarithm) + '}}\)'
    return answer, task


#Задачи 14526, 14567, 10991
def random_figure_in_logarithm_degree_multiplication():
    base_of_logarithm = random.randint(2, 6)
    answer = random.randint(0, 4)
    degree_of_logarithm = base_of_logarithm ** answer
    n = random.randint(1, 3)
    m = random.randint(1, 3)
    answer = round(n ** (m * math.log(degree_of_logarithm, base_of_logarithm)))
    if n < 2 and m < 2:
        task = f'Вычислите: \(log_'"{" + str(base_of_logarithm) + '}{' + str(degree_of_logarithm) + '}\)'
    elif n >= 2 and m >= 2:
        task = f'Вычислите:' f'\({n}^'"{"f'{m}*log_'"{" + str(base_of_logarithm) + '}{' \
               + str(degree_of_logarithm) + '}}\)'
    elif n < 2 and m >= 2:
        task = f'Вычислите:' f'\({n}^'"{"f'{m}*log_'"{" + str(base_of_logarithm) + '}{' \
               + str(degree_of_logarithm) + '}}\)'
    elif n >= 2 and m < 2:
        task = f'Вычислите:' f'\({n}^'"{"f'log_'"{" + str(base_of_logarithm) + '}{' \
               + str(degree_of_logarithm) + '}}\)'
    return answer, task


# Задание № 14591
def random_figure_in_logarithm_degree_addition():
    base_of_logarithm = random.randint(2, 6)
    answer_of_logarithm = random.randint(0, 4)
    degree_of_logarithm = base_of_logarithm ** answer_of_logarithm
    n = random.randint(1, 3)
    m = random.randint(0, 3)
    answer_of_logarithm = round(n ** (m + math.log(degree_of_logarithm, base_of_logarithm)))
    if n < 2 and m < 2:
        task = f'Вычислите: \(log_'"{" + str(base_of_logarithm) + '}{' + str(degree_of_logarithm) + '}\)'
    elif n >= 2 and m >= 2:
        task = f'Вычислите:' f'\({n}^'"{("f'{m}+log_'"{" + str(base_of_logarithm) + '}{' \
               + str(degree_of_logarithm) + '})}\)'
    elif n < 2 and m >= 2:
        task = f'Вычислите:' f'\({n}^'"{("f'{m}+log_'"{" + str(base_of_logarithm) + '}{' \
               + str(degree_of_logarithm) + '})}\)'
    elif n >= 2 and m < 2:
        task = f'Вычислите:' f'\({n}^'"{("f'log_'"{" + str(base_of_logarithm) + '}{' \
               + str(degree_of_logarithm) + '})}\)'
    return answer_of_logarithm, task


# Задание № 14592
def random_logarithm_in_degree_subtraction():
    base_of_logarithm = random.randint(2, 6)
    answer_of_logarithm = random.randint(0, 4)
    degree_of_logarithm = base_of_logarithm ** answer_of_logarithm
    n = random.randint(1, 3)
    m = random.randint(1, 3)
    answer_of_logarithm = format(n ** (m - math.log(degree_of_logarithm, base_of_logarithm)), '.4')
    if n < 2 and m < 2:
        task = f'Вычислите: \(log_'"{" + str(base_of_logarithm) + '}{' + str(degree_of_logarithm) + '}\)'
    elif n >= 2 and m >= 2:
        task = f'Вычислите:' f'\({n}^'"{("f'{m}-log_'"{" + str(base_of_logarithm) + '}{' \
               + str(degree_of_logarithm) + '})}\)'
    elif n < 2 and m >= 2:
        task = f'Вычислите:' f'\({n}^'"{("f'{m}-log_'"{" + str(base_of_logarithm) + '}{' \
               + str(degree_of_logarithm) + '})}\)'
    elif n >= 2 and m < 2:
        task = f'Вычислите:' f'\({n}^'"{("f'log_'"{" + str(base_of_logarithm) + '}{' \
               + str(degree_of_logarithm) + '})}\)'
    return answer_of_logarithm, task


#Задача № 12242
def random_logarithm_with_fractions():
    list = [2, 3, 4, 8, 9, 16, 27, 81]
    even_or_odd = random.choice(list)
    if even_or_odd % 2 == 0:
        fraction = fractions.Fraction(1, even_or_odd)
        answer = round(math.log(fraction, 2))
        task = f'Вычислите: \(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(2) + '}\)'
    else:
        fraction = fractions.Fraction(1, even_or_odd)
        answer = round(math.log(fraction, 3))
        task = f'Вычислите: \(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(3) + '}\)'
    return answer, task


def random_logarithm_with_fractions_in_degree():
    list = [2, 3, 4, 8, 9, 16, 27, 81]
    even_or_odd = random.choice(list)
    n = random.randint(1, 3)
    if even_or_odd % 2 == 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 2))
        if b < 0:
            x = b*(-1)
            answer = format(pow(n, 1 / x), '.4')
        task = f'Вычислите: \({n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(2) + '})}\)'
    else:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 3))
        if b < 0:
            x = b*(-1)
            answer = format(pow(n, 1 / x), '.4')
        task = f'Вычислите: \({n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(3) + '})}\)'
    return answer, task


def random_logarithm_with_fractions_in_degree_subtraction():
    list = [2, 3, 4, 8, 9, 16, 27, 81]
    even_or_odd = random.choice(list)
    n = random.randint(1, 3)
    p = random.randint(0, 4)
    if even_or_odd % 2 == 0 and p > 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 2))
        if b < 0:
            x = b * (-1)
            answer = format((pow(n, 1 / x) - p), '.4')
        task = f'Вычислите: \(({n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(2) +"})}{-" f"{p}"'})\)'
    elif even_or_odd % 2 != 0 and p > 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 3))
        if b < 0:
            x = b*(-1)
            answer = format((pow(n, 1 / x) - p), '.4')
        task = f'Вычислите: \(({n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(3) + "})}{-" f"{p}"'})\)'
    elif even_or_odd % 2 == 0 and p == 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 2))
        if b < 0:
            x = b * (-1)
            answer = format((pow(n, 1 / x) - p), '.4')
        task = f'Вычислите: \(({n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(
            2) + '})}\)'
    elif even_or_odd % 2 != 0 and p == 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 3))
        if b < 0:
            x = b * (-1)
            answer = format((pow(n, 1 / x) - p), '.4')
        task = f'Вычислите: \(({n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(
            3) + '})}\)'
    return answer, task


def random_logarithm_with_fractions_in_degree_addition():
    list = [2, 3, 4, 8, 9, 16, 27, 81]
    even_or_odd = random.choice(list)
    n = random.randint(1, 3)
    p = random.randint(0, 4)
    if even_or_odd % 2 == 0 and p > 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 2))
        if b < 0:
            x = b * (-1)
            answer = format((pow(n, 1 / x) + p), '.4')
        task = f'Вычислите: \({n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(2) +"})}{+" f"{p}"'}\)'
    elif even_or_odd % 2 != 0 and p > 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 3))
        if b < 0:
            x = b * (-1)
            answer = format((pow(n, 1 / x) + p), '.4')
        task = f'Вычислите: \({n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(3) + "})}{+" f"{p}"'}\)'
    elif even_or_odd % 2 == 0 and p == 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 2))
        if b < 0:
            x = b * (-1)
            answer = format((pow(n, 1 / x) + p), '.4')
        task = f'Вычислите: \({n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(
            2) + '})}\)'
    elif even_or_odd % 2 != 0 and p == 0:
        fraction = fractions.Fraction(1, even_or_odd)
        b = (math.log(fraction, 3))
        if b < 0:
            x = b * (-1)
            answer = format((pow(n, 1 / x) + p), '.4')
        task = f'Вычислите: \({n}^'r'{(log_' r"{\frac" + '{' + str(1) + '}' + '{' + str(even_or_odd) + '}}{' + str(
            3) + '})}\)'
    return answer, task


# № Задача 14069
def logarithms_addition():
    base_of_logarithm1 = random.randint(2, 10)
    answer_of_logarthm1 = random.randint(0, 4)
    degree_of_logarithm1 = base_of_logarithm1**answer_of_logarthm1
    m = random.randint(1, 3)
    k = random.randint(1, 3)
    base_of_loogarithm2 = random.randint(2, 10)
    answer_of_loogarithm2 = random.randint(0, 4)
    degree_of_logarithm2 = base_of_loogarithm2**answer_of_loogarithm2
    answer = round(k*math.log(degree_of_logarithm2, base_of_loogarithm2) + m*math.log(degree_of_logarithm1, base_of_logarithm1))
    if m >= 2 and k < 2:
        task = f'Вычислите:' f'\(log_'"{" + str(base_of_loogarithm2) + '}{' + str(degree_of_logarithm2) + \
               '}' "+" f'{m}*log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '}\)'
    elif m < 2 and k < 2:
        task = f'Вычислите:' f'\(log_'"{" + str(base_of_loogarithm2) + '}{' + str(degree_of_logarithm2) + \
               '}' "+" f'log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '}\)'
    elif m >= 2 and k >= 2:
        task = f'Вычислите:' f'\({k}*log_'"{" + str(base_of_loogarithm2) + '}{' + str(degree_of_logarithm2) + \
               '}' "+" f'{m}*log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '}\)'
    elif m < 2 and k >= 2:
        task = f'Вычислите:' f'\({k}*log_'"{" + str(base_of_loogarithm2) + '}{' + str(degree_of_logarithm2) + \
               '}' "+" f'log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '}\)'
    return answer, task


def figure_in_logaritms_degree_addition():
    base_of_logarithm1 = random.randint(2, 10)
    answer_of_logarithm1 = random.randint(0, 4)
    degree_of_logarithm1 = base_of_logarithm1**answer_of_logarithm1
    n = random.randint(1, 3)
    m = random.randint(1, 3)
    k = random.randint(1, 3)
    base_of_loogarythm2 = random.randint(2, 10)
    answer_of_loogarythm2 = random.randint(0, 4)
    degree_of_logarythm2 = base_of_loogarythm2**answer_of_loogarythm2
    answer = round(n**(k*math.log(degree_of_logarythm2, base_of_loogarythm2) + m*math.log(degree_of_logarithm1, base_of_logarithm1)))
    if m >= 2 and k < 2:
        task = f'Вычислите:' f'\({n}^'"{"f'(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) +\
           '}' "+" f'{m}*log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'
    elif m < 2 and k < 2:
        task = f'Вычислите:' f'\({n}^'"{"f'(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}' "+" f'log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'
    elif m >= 2 and k >= 2:
        task = f'Вычислите:' f'\({n}^'"{"f'{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}' "+" f'{m}*log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'
    elif m < 2 and k >= 2:
        task = f'Вычислите:' f'\({n}^'"{"f'{k}*(log_'"{" + str(base_of_loogarythm2) + '}{' + str(degree_of_logarythm2) + \
               '}' "+" f'log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'
    return answer, task


# 14540, 14599
def figures_in_logaritms_degree_addition():
    base_of_loogarithm1 = random.randint(2, 10)
    answer_of_loogarithm1 = random.randint(0, 4)
    degree_of_logarithm1 = base_of_loogarithm1**answer_of_loogarithm1
    n = random.randint(1, 3)
    m = random.randint(1, 3)
    k = random.randint(1, 3)
    l = random.randint(1, 3)
    base_of_logarithm2 = random.randint(2, 10)
    answer_of_logarithm2 = random.randint(0, 4)
    degree_of_logarithm2 = base_of_logarithm2**answer_of_logarithm2
    answer = round(n**(k*math.log(degree_of_logarithm2, base_of_logarithm2)) + l**((m*math.log(degree_of_logarithm1, base_of_loogarithm1))))
    if m >= 2 and k < 2:
        task = f'Вычислите:' f'\({n}^'"{"f'(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) +\
           '})}' "+" f'{l}^'"{"f'{m}*(log_'"{" + str(base_of_loogarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'
    elif m < 2 and k < 2:
        task = f'Вычислите:' f'\({n}^'"{"f'(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '})}' "+" f'{l}^'"{"f'(log_'"{" + str(base_of_loogarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'
    elif m >= 2 and k >= 2:
        task = f'Вычислите:' f'\({n}^'"{"f'{k}*(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '})}' "+" f'{l}^'"{"f'{m}*(log_'"{" + str(base_of_loogarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'
    elif m < 2 and k >= 2:
        task = f'Вычислите:' f'\({n}^'"{"f'{k}*(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '})}' "+" f'{l}^'"{"f'(log_'"{" + str(base_of_loogarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'
    return answer, task


# Задачи 14510, 14515
def logarithms_subtraction():
    base_of_logarithm1 = random.randint(2, 10)
    answer_of_logarithm1 = random.randint(0, 4)
    degree_of_logarithm1 = base_of_logarithm1**answer_of_logarithm1
    n = random.randint(1, 3)
    base_of_logarithm2 = random.randint(2, 10)
    answer_of_logarithm2 = random.randint(0, 4)
    degree_of_logarithm2 = base_of_logarithm2**answer_of_logarithm2
    answer = round(math.log(degree_of_logarithm2, base_of_logarithm2) - n*math.log(degree_of_logarithm1, base_of_logarithm1))
    if n > 1:
        task = f'Вычислите разницу логарифмов:\(log_'"{" + str(base_of_logarithm2) +\
                         '}{' + str(degree_of_logarithm2) + '}\)' "-" f'{n}*\(log_'"{" + str(base_of_logarithm1) + \
                         '}{' + str(degree_of_logarithm1) + '}\)'
    else:
        task = f'Вычислите разницу логарифмов:\(log_'"{" + str(base_of_logarithm2) + '}{' + str(
            degree_of_logarithm2) + '}\)' "-" f'\(log_'"{" + str(base_of_logarithm1) + '}{' + str(
            degree_of_logarithm1) + '}\)'
    return answer, task


# Задача 14510
def logarithms_subtraction_new():
    base_of_logarithm1 = random.randint(2, 10)
    answer_of_logarithm1 = random.randint(0, 4)
    degree_of_logarithm1 = base_of_logarithm1**answer_of_logarithm1
    m = random.randint(1, 3)
    k = random.randint(1, 3)
    base_of_logarithm2 = random.randint(2, 10)
    answer_of_logarithm2 = random.randint(0, 4)
    degree_of_logarithm2 = base_of_logarithm2**answer_of_logarithm2
    answer = round(k*math.log(degree_of_logarithm2, base_of_logarithm2) - m*math.log(degree_of_logarithm1, base_of_logarithm1))
    if m >= 2 and k < 2:
        task = f'Вычислите:' f'\((log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '})' "-" f'{m}*(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})\)'
    elif m < 2 and k < 2:
        task = f'Вычислите:' f'\((log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '})' "-" f'(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})\)'
    elif m >= 2 and k >= 2:
        task = f'Вычислите:' f'\({k}*(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '})' "-" f'{m}*(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})\)'
    elif m < 2 and k >= 2:
        task = f'Вычислите:' f'\({k}*(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '})' "-" f'(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})\)'
    return answer, task


# 14601, № 14604
def figure_in_logaritms_degree_subtarction():
    base_of_logarithm1 = random.randint(2, 10)
    answer_of_logarithm1 = random.randint(0, 4)
    degree_of_logarithm1 = base_of_logarithm1**answer_of_logarithm1
    n = random.randint(1, 4)
    m = random.randint(1, 4)
    k = random.randint(1, 4)
    base_of_logarithm2 = random.randint(2, 10)
    answer_of_logarithm2 = random.randint(0, 4)
    degree_of_logarithm2 = base_of_logarithm2**answer_of_logarithm2
    answer = format(n**(k*math.log(degree_of_logarithm2, base_of_logarithm2) - m*math.log(degree_of_logarithm1, base_of_logarithm1)), '.8')
    if m >= 2 and k < 2:
        task = f'Вычислите:' f'\({n}^'"{"f'(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) +\
           '})' "-" f'{m}*(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'
    elif m < 2 and k < 2:
        task = f'Вычислите:' f'\({n}^'"{"f'(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '})' "-" f'(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'
    elif m >= 2 and k >= 2:
        task = f'Вычислите:' f'\({n}^'"{"f'{k}*(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '})' "-" f'{m}*(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'
    elif m < 2 and k >= 2:
        task = f'Вычислите:' f'\({n}^'"{"f'{k}*(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '})' "-" f'(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'
    return answer, task


# Задача № 14537
def figures_in_logaritms_degree_subtarction():
    base_of_logarithm1 = random.randint(2, 10)
    answer_of_logarithm1 = random.randint(0, 4)
    degree_of_logarithm1 = base_of_logarithm1**answer_of_logarithm1
    n = random.randint(1, 3)
    m = random.randint(1, 3)
    k = random.randint(1, 3)
    o = random.randint(1, 3)
    base_of_logarithm2 = random.randint(2, 10)
    answer_of_logarithm2 = random.randint(0, 4)
    degree_of_logarithm2 = base_of_logarithm2**answer_of_logarithm2
    answer = round(n**(k*math.log(degree_of_logarithm2, base_of_logarithm2)) - o**(m*math.log(degree_of_logarithm1, base_of_logarithm1)))
    if m >= 2 and k < 2:
        task = f'Вычислите:' f'\({n}^'"{"f'(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) +\
           '})}' "-" f'{o}^'"{"f'{m}*(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'

    elif m < 2 and k < 2:
        task = f'Вычислите:' f'\({n}^'"{"f'(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '})}' "-" f'{o}^'"{"f'(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'

    elif m >= 2 and k >= 2:
        task = f'Вычислите:' f'\({n}^'"{"f'{k}*(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '})}' "-" f'{o}^'"{"f'{m}*(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'
    elif m < 2 and k >= 2:
        task = f'Вычислите:' f'\({n}^'"{"f'{k}*(log_'"{" + str(base_of_logarithm2) + '}{' + str(degree_of_logarithm2) + \
               '})}' "-" f'{o}^'"{"f'(log_'"{" + str(base_of_logarithm1) + '}{' + str(degree_of_logarithm1) + '})}\)'
    return answer, task


task_1 = random_logarithm()
task_2 = logarithm_multiplication()
task_3 = logarithm_division()
task_4 = random_logarithm_in_degree()
task_5 = random_figure_in_logarithm_degree_multiplication()
task_6 = random_figure_in_logarithm_degree_addition()
task_7 = random_logarithm_in_degree_subtraction()
task_8 = random_logarithm_with_fractions()
task_9 = random_logarithm_with_fractions_in_degree()
task_10 = random_logarithm_with_fractions_in_degree_subtraction()
task_11 = random_logarithm_with_fractions_in_degree_addition()
task_12 = logarithms_addition()
task_13 = figure_in_logaritms_degree_addition()
task_14 = figures_in_logaritms_degree_addition()
task_15 = logarithms_subtraction()
task_16 = logarithms_subtraction_new()
task_17 = figure_in_logaritms_degree_subtarction()
task_18 = figures_in_logaritms_degree_subtarction()


stack_of_functions = [task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8, task_9, task_10, task_11,
                      task_12, task_13, task_14, task_15, task_16, task_17, task_18]



def logarithm_generator():
    answer = random.choice(stack_of_functions)
    return answer


if __name__ == "__main__":
    ...





