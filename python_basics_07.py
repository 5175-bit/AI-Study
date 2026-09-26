# %% 1
def say_hello():
    print("Hello Python")
say_hello()
# %% 2
def greet(name):
    print(f'你好, {name}')
greet("Bob")
# %% 3
def add(a, b):
    return(a + b)
x = add(2,5)
print(x)
# %% 4
def rectangle_area(length, width):
    return(length * width)
x = rectangle_area(3, 5)
print(x)
# %% 5
def is_even(n):
    if n % 2 == 0:
        return True
    else:
        return False
is_even(13)
# %% 6
def calculate_average(scores):
    return(sum(scores)/len(scores))
calculate_average([80, 90, 100])
# %%
