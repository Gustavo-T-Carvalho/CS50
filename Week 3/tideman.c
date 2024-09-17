#include <cs50.h>
#include <stdio.h>
#include <string.h>
// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
void swap(int i, int j);
bool willCreateCycle(int i, int j);
bool hasCycles();
bool isCyclicDFS(int i, bool visited[], bool stack[]);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{

    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            for (int j = 0; j < rank; j++)
            {
                if (i == ranks[j])
                {
                    return false;
                }
            }

            ranks[rank] = i;
            return true;
        }
    }

    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        int preferred = ranks[i];
        for (int j = i + 1; j < candidate_count; j++)
        {
            int unfavored = ranks[j];
            preferences[preferred][unfavored]++;
        }
    }
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            pair p;
            if (preferences[i][j] != preferences[j][i])
            {

                if (preferences[i][j] > preferences[j][i])
                {
                    p.winner = i;
                    p.loser = j;
                }
                else
                {
                    p.winner = j;
                    p.loser = i;
                }
                pairs[pair_count] = p;
                pair_count++;
            }
        }
    }
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    bool noSwaps;
    for (int j = pair_count; j > 0; j--)
    {
        noSwaps = true;
        for (int i = 0; i < j - 1; i++)
        {
            pair p1 = pairs[i];
            pair p2 = pairs[i + 1];

            if (preferences[p1.winner][p1.loser] < preferences[p2.winner][p2.loser])
            {
                noSwaps = false;
                swap(i, i + 1);
            }
        }
    }
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        pair p = pairs[i];
        int winner = p.winner;
        int loser = p.loser;

        if (!willCreateCycle(winner, loser))
        {
            locked[winner][loser] = true;
        }
    }
}

// Print the winner of the election
void print_winner(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        bool isSource = true;
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i])
            {
                isSource = false;
            }
        }
        if (isSource)
        {
            printf("%s\n", candidates[i]);
        }
    }
}

void swap(int i, int j)
{
    pair aux = pairs[i];
    pairs[i] = pairs[j];
    pairs[j] = aux;
}

bool willCreateCycle(int i, int j)
{
    locked[i][j] = true;
    bool result = hasCycles();
    locked[i][j] = false;
    return result;
}

bool hasCycles()
{
    bool visited[MAX] = {false};
    bool stack[MAX] = {false};

    for (int i = 0; i < candidate_count; i++)
    {
        if (!visited[i])
        {
            if (isCyclicDFS(i, visited, stack))
            {
                return true;
            }
        }
    }

    return false;
}

bool isCyclicDFS(int i, bool visited[], bool stack[])
{
    if (stack[i])
    {
        return true;
    }
    if (visited[i])
    {
        return false;
    }
    visited[i] = true;
    stack[i] = true;

    for (int j = 0; j < candidate_count; j++)
    {
        if (locked[i][j])
        {
            if (isCyclicDFS(j, visited, stack))
            {
                return true;
            }
        }
    }

    stack[i] = false;
    return false;
}
