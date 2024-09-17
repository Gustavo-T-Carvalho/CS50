#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

bool hasAJpegStart(uint8_t bytes[]);
char *getFileName(int count);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 2)
    {
        printf("Usage: ./recover file\n");
        return 1;
    }

    // Open input file
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    uint8_t bytes[512];
    bool isOpen = false;
    int count = 0;
    FILE *output;
    char *fileName;

    while (fread(&bytes, 512, 1, input) != 0)
    {
        if (hasAJpegStart(bytes))
        {
            if (isOpen)
            {
                fclose(output);
                count++;
            }

            fileName = getFileName(count);
            if (fileName == NULL)
            {
                fclose(input);
                printf("Not enough memory");
                return 2;
            }

            output = fopen(fileName, "a");
            free(fileName);
            if (output == NULL)
            {
                printf("Could not open %s.\n", fileName);
                return 1;
            }
            isOpen = true;
        }

        if (isOpen)
        {
            fwrite(&bytes, sizeof(bytes), 1, output);
        }
    }

    if (isOpen)
    {
        fclose(output);
    }
    fclose(input);
}

bool hasAJpegStart(uint8_t bytes[])
{
    bool threeFirstPositionsMatches = bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff;
    if (!threeFirstPositionsMatches)
    {
        return false;
    }

    bool fourthPositionMatches = (bytes[3] >= 0xe0 && bytes[3] <= 0xef);
    if (!fourthPositionMatches)
    {
        return false;
    }
    return true;
}

char *getFileName(int count)
{
    char *fileName = malloc(9 * sizeof(char));
    if (fileName == NULL)
    {
        return NULL;
    }
    if (count < 10)
    {
        sprintf(fileName, "00%d.jpg", count);
    }
    else if (count < 100)
    {
        sprintf(fileName, "0%d.jpg", count);
    }
    else if (count < 1000)
    {
        sprintf(fileName, "%d.jpg", count);
    }
    else
    {
        free(fileName);
        return NULL;
    }

    return fileName;
}
