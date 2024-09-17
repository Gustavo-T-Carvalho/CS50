#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int countLetters(string text);
int countWords(string text);
int countSentences(string text);
int calculateIndex(int letters, int words, int sentences);

bool isLetter(char c);
int main(void)
{
    string text = get_string("Text: \n");

    int letters = countLetters(text);
    int words = countWords(text);
    int sentences = countSentences(text);

    int index = calculateIndex(letters, words, sentences);

    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int countLetters(string text)
{
    int letters = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isLetter(text[i]))
        {
            letters++;
        }
    }

    return letters;
}

int countWords(string text)
{
    int words = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == ' ')
        {
            words++;
        }
    }

    return words + 1;
}

int countSentences(string text)
{
    int sentences = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }

    return sentences;
}

bool isLetter(char c)
{
    return ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z'));
}

int calculateIndex(int letters, int words, int sentences)
{
    // average number of letters per 100 words
    float l = 100.0 * letters / words;
    // average number of sentences per 100 words
    float s = 100.0 * sentences / words;

    float result = 0.0588 * l - 0.296 * s - 15.8;
    int roundedResult = round(result);
    return roundedResult;
}
