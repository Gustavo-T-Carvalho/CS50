#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int getCharValue(char c);
int getStringScore(string s);

int main(void)
{
    string p1String = get_string("Player 1: \n");
    string p2String = get_string("Player 2: \n");

    int score1 = getStringScore(p1String);
    int score2 = getStringScore(p2String);

    if (score1 == score2)
    {
        printf("%s", "Tie!");
    }
    else if (score1 > score2)
    {
        printf("%s", "Player 1 wins");
    }
    else
    {
        printf("%s", "Player 2 wins!");
    }
}

int getStringScore(string s)
{
    int score = 0;
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        score += getCharValue(toupper(s[i]));
    }
    return score;
}

int getCharValue(char c)
{
    if (c < 'A' || c > 'Z')
    {
        return 0;
    }

    int i = c - 65;

    const int points[] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                          1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

    return points[i];
}
