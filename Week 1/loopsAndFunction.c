#include <cs50.h>
#include <stdio.h>

void iterate(int n);

int main(void)
{
    iterate(3);

    // int i = 0;
    // while(i < 3){
    //     iterate();
    //     i++;
    // }

    // for(int j = 0; j < 3; j++){
    //     iterate();
    // }
}

void iterate(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("iterating\n");
    }
}
