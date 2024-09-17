#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE pixel = image[i][j];
            int sum = pixel.rgbtBlue + pixel.rgbtGreen + pixel.rgbtRed;
            int average = round(sum / 3.0);

            pixel.rgbtBlue = average;
            pixel.rgbtGreen = average;
            pixel.rgbtRed = average;

            image[i][j] = pixel;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            RGBTRIPLE aux = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = aux;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Allocate memory for copy image
    RGBTRIPLE(*copyImage)[width] = calloc(height, width * sizeof(RGBTRIPLE));
    if (copyImage == NULL)
    {
        printf("Not enough memory to store image.\n");
        return;
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int quantityOfPixels = 0;
            int sumGreen = 0;
            int sumRed = 0;
            int sumBlue = 0;

            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    if ((ni > -1 && ni < height) && (nj > -1 && nj < width))
                    {
                        quantityOfPixels++;
                        sumBlue += image[ni][nj].rgbtBlue;
                        sumGreen += image[ni][nj].rgbtGreen;
                        sumRed += image[ni][nj].rgbtRed;
                    }
                }
            }
            RGBTRIPLE editedPixel = image[i][j];

            editedPixel.rgbtBlue = round((double) sumBlue / quantityOfPixels);
            editedPixel.rgbtGreen = round((double) sumGreen / quantityOfPixels);
            editedPixel.rgbtRed = round((double) sumRed / quantityOfPixels);

            copyImage[i][j] = editedPixel;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copyImage[i][j];
        }
    }
    free(copyImage);
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Allocate memory for copy image
    RGBTRIPLE(*copyImage)[width] = calloc(height, width * sizeof(RGBTRIPLE));
    if (copyImage == NULL)
    {
        printf("Not enough memory to store image.\n");
        return;
    }

    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumXGreen = 0;
            int sumXRed = 0;
            int sumXBlue = 0;
            int sumYGreen = 0;
            int sumYRed = 0;
            int sumYBlue = 0;

            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {

                    int ni = i + di;
                    int nj = j + dj;

                    if ((ni > -1 && ni < height) && (nj > -1 && nj < width))
                    {
                        sumXBlue += image[ni][nj].rgbtBlue * Gx[di + 1][dj + 1];
                        sumXGreen += image[ni][nj].rgbtGreen * Gx[di + 1][dj + 1];
                        sumXRed += image[ni][nj].rgbtRed * Gx[di + 1][dj + 1];

                        sumYBlue += image[ni][nj].rgbtBlue * Gy[di + 1][dj + 1];
                        sumYGreen += image[ni][nj].rgbtGreen * Gy[di + 1][dj + 1];
                        sumYRed += image[ni][nj].rgbtRed * Gy[di + 1][dj + 1];
                    }
                }
            }

            RGBTRIPLE editedPixel = image[i][j];
            int rgbtBlue = round(pow((double) (sumXBlue * sumXBlue + sumYBlue * sumYBlue), 0.5));
            if (rgbtBlue > 255)
            {
                rgbtBlue = 255;
            }
            int rgbtGreen =
                round(pow((double) (sumXGreen * sumXGreen + sumYGreen * sumYGreen), 0.5));
            if (rgbtGreen > 255)
            {
                rgbtGreen = 255;
            }
            int rgbtRed = round(pow((double) (sumXRed * sumXRed + sumYRed * sumYRed), 0.5));
            if (rgbtRed > 255)
            {
                rgbtRed = 255;
            }

            editedPixel.rgbtBlue = rgbtBlue;
            editedPixel.rgbtGreen = rgbtGreen;
            editedPixel.rgbtRed = rgbtRed;

            copyImage[i][j] = editedPixel;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copyImage[i][j];
        }
    }
    free(copyImage);
    return;
}
