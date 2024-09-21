from cs50 import get_int
import math


def main():
    creditCard = str(get_int("Credit card: "))
    print(verifyCreditCard(creditCard))


def verifyCreditCard(creditCard):
    digits = getDigits(creditCard)
    hasWrongSize = digits != 13 and digits != 15 and digits != 16

    if hasWrongSize or not luhnVerification(creditCard):
        return "INVALID"

    if digits == 13 and creditCard[0] == '4':
        return "VISA"

    if digits == 15 and creditCard[0] == '3' and (creditCard[1] == '7' or creditCard[1] == '4'):
        return "AMEX"

    if digits == 16:
        if creditCard[0] == '4':
            return "VISA"

        if creditCard[0] == '5' and (int(creditCard[1]) in range(1, 6)):
            return "MASTERCARD"

    return "INVALID"


def getDigits(creditCard):
    return len(creditCard)


def luhnVerification(creditCard):
    doubled = 0
    others = 0
    remainingDigits = creditCard

    shouldDouble = False
    for digit in creditCard:
        lastDigit = int(remainingDigits[-1])
        remainingDigits = remainingDigits[:-1]
        if shouldDouble:
            if lastDigit * 2 >= 10:
                doubled += (lastDigit * 2) % 10
                doubled += math.floor((lastDigit * 2) / 10)
            else:
                doubled += lastDigit * 2
        else:
            others += lastDigit
        shouldDouble = not shouldDouble
    sum = doubled + others
    return True if sum % 10 == 0 else False


main()
