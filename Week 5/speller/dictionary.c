// Implements a dictionary's functionality

#include "dictionary.h"
#include <ctype.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

void unloadLinkedList(node *n);

// TODO: Choose number of buckets in hash table
const unsigned int N = 143093;

unsigned int words = 0;
// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);

    node *n = table[index];

    while (n != NULL)
    {
        if (strcasecmp(word, n->word) == 0)
        {
            return true;
        }
        else
        {
            n = n->next;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int sum = 0;
    int multiplier = 13;
    int module = 143093;
    int base = 13;
    for (int i = 0; word[i] != '\0'; i++)
    {

        sum = (sum * base + tolower(word[i])) % module;
    }
    return sum;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open file.\n");
        return false;
    }

    char word[LENGTH + 1];
    char c;
    int index = 0;

    while (fread(&c, sizeof(char), 1, file))
    {
        // Allow only alphabetical characters and apostrophes
        if (isalpha(c) || c == '\'')
        {
            // Append character to word
            word[index] = c;
            index++;
        }
        else if (c == '\n')
        {
            // Terminate current word
            word[index] = '\0';
            unsigned int hashResult = hash(word);
            node *n = malloc(sizeof(node));
            n->next = NULL;
            strcpy(n->word, word);
            if (table[hashResult] == NULL)
            {
                table[hashResult] = n;
            }
            else
            {
                node *currentPosition = table[hashResult];
                while (currentPosition->next != NULL)
                {
                    currentPosition = currentPosition->next;
                }
                currentPosition->next = n;
            }
            words++;
            index = 0;
        }
    }

    fclose(file);
    return true;
}

// Returns number of words = 0; in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        unloadLinkedList(table[i]);
    }
    return true;
}

void unloadLinkedList(node *n)
{
    if (n == NULL)
    {
        return;
    }
    unloadLinkedList(n->next);
    free(n);
}
