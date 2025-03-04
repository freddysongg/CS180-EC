def simple_function(x):
    if x > 0:
        return x + 1
    else:
        return x - 1

def recursive_function(n):
    if n <= 1:
        return 1
    return n * recursive_function(n - 1)

def loop_function(n):
    result = 0
    for i in range(n):
        result += i
    return result

def infinite_loop(n):
    while True:
        n += 1

def complex_branches(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    elif x < 10:
        return 1
    else:
        return 2 