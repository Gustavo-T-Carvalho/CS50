from cs50 import get_int

while (True):
    n = get_int("Height: ")
    if (n > 0 and n < 9):
        break


for i in range(n):
    quantity = i + 1
    print(" " * (n - quantity), end="")
    print("#" * quantity, end="")
    print(" " * 2, end="")
    print("#" * quantity)
