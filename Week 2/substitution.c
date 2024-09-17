#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

bool isLetter(char c);
bool hasInvalidCharacter(string s);
void cipher(string key, string text);
string convertKeyToUpperCase(string key);
char getCharInKey(string key, char c);
bool hasEveryLetterOnce(string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Function expects one argument\n");
        return 1;
    }

    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }

    if (hasInvalidCharacter(argv[1]))
    {
        printf("Key must contain only letters\n");
        return 1;
    }

    if (!hasEveryLetterOnce(argv[1]))
    {
        printf("Every letter must be in the key exactly once\n");
        return 1;
    }

    string key = convertKeyToUpperCase(argv[1]);

    string text = get_string("plaintext: ");
    cipher(key, text);
}

bool isLetter(char c)
{
    return ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z'));
}

bool hasInvalidCharacter(string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (!isLetter(s[i]))
        {
            return true;
        }
    }
    return false;
}

void cipher(string key, string text)
{
    int length = strlen(text);
    char cipher[length + 1];
    for (int i = 0; i < length; i++)
    {
        if (isLetter(text[i]))
        {
            cipher[i] = getCharInKey(key, text[i]);
        }
        else
        {
            cipher[i] = text[i];
        }
    }
    cipher[length] = '\0';
    printf("ciphertext: %s\n", cipher);
}

char getCharInKey(string key, char c)
{
    if (c >= 'a' && c <= 'z')
    {
        return (key[c - 97] + 32);
    }

    if (c >= 'A' && c <= 'Z')
    {
        return (key[c - 65]);
    }
    return c;
}

string convertKeyToUpperCase(string key)
{
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        key[i] = toupper(key[i]);
    }
    return key;
}

bool hasEveryLetterOnce(string key)
{
    int letters[26] = {0};

    for (int i = 0, n = strlen(key); i < n; i++)
    {
        char c = key[i];
        int position;

        if (c >= 'a' && c <= 'z')
        {
            position = c - 97;
        }
        else
        {
            position = c - 65;
        }

        if(letters[position] == 0){
            letters[position]++;
        } else {
            return false;
        }
    }
    return true;
}
