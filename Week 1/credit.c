#include <cs50.h>
#include <stdio.h>

string verifyCreditCard(long n);
int getDigits(long n);
bool luhnVerification(long creditCard);
int main(void)
{
    long creditCard;

    creditCard = get_long("Credit Card: ");
    printf("%s\n", verifyCreditCard(creditCard));
}

string verifyCreditCard(long n)
{
    int digits = getDigits(n);

    if (digits != 13 && digits != 15 && digits != 16)
    {
        return "INVALID";
    }

    if (!luhnVerification(n))
    {
        return "INVALID";
    }

    if (digits == 13)
    {
        if (n / 1000000000000 == 4)
        {
            return "VISA";
        }
    }

    if (digits == 15)
    {
        if (n / 10000000000000 == 37 || n / 10000000000000 == 34)
        {
            return "AMEX";
        }
    }

    if (digits == 16)
    {
        printf("entrou 16");
        if (n / 1000000000000000 == 4)
        {
            return "VISA";
        }

        if (n / 100000000000000 == 51 || n / 100000000000000 == 52 || n / 100000000000000 == 53 ||
            n / 100000000000000 == 54 || n / 100000000000000 == 55)
        {
            return "MASTERCARD";
        }
    }

    return "INVALID";
}

int getDigits(long n)
{
    int digits = 0;
    if (n == 0)
    {
        return 1;
    }

    while (n > 0)
    {
        n = n / 10;
        digits++;
    }
    return digits;
}

bool luhnVerification(long creditCard)
{
    int doubled = 0;
    int others = 0;
    long remainingDigits = creditCard;
    int digits = getDigits(creditCard);

    bool shouldDouble = false;

    for (int i = 0; i < digits; i++)
    {
        int lastDigit = remainingDigits % 10;
        remainingDigits = remainingDigits / 10;
        if (shouldDouble)
        {
            if (lastDigit * 2 >= 10)
            {
                doubled += (lastDigit * 2) % 10;
                doubled += (lastDigit * 2) / 10;
            }
            else
            {
                doubled += (lastDigit * 2);
            }
        }
        else
        {
            others += lastDigit;
        }
        shouldDouble = !shouldDouble;
    }
    printf("%d\n", doubled);
    printf("%d\n", others);
    int sum = doubled + others;

    if (sum % 10 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}
