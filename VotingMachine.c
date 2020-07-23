#include <cs50.h>
#include <stdio.h>
#include <string.h>


#define MAX 9

typedef struct 
{
    string name;
    int votes;
}
candidate;

candidate candidates[MAX];

candidates.name[0] = "Emma";
candidates.votes[0] = 0;
candidates.name[1] = "David";
candidates.votes[1] = 0;
candidates.name[2] = "Alice";
candidates.votes[2] = 0;


void vote(string NAME);
void print_winner();



int main(void)
{   

    int candidate_count = get_int("Number of Voters: ");
    
    for (int i=0; i < candidate_count; i++)
    {
        string candidate_name = get_string("Enter Candidate Name: ");
        vote(candidate_name);
    }

    print_winner();


}


void vote(string NAME)
{
    int len = sizeof(candidates)/sizeof(candidates[0]);

    for (int i=0; i < len; i++)
    {
        if (strcmp(candidates[i].name, NAME) == 0)
        {
            candidates[i].votes += 1;
        }
        else
        {
            printf("Invalid Vote\n");
			return 1
        }
    }
}


void print_winner()
{
    int high_num = 0;

    int len = sizeof(candidates)/sizeof(candidates[0]);
    for (int i=0; i < len; i++)
    {
        if (candidates[i].votes > high_num)
        {
            high_num = candidates[i].votes;
        }

    }

    for (int i=0; i<len; i++)
    {
        if (candidates[i].votes == high_num)
        {
            printf("Candidate %s had the highest votes\n",candidates[i].name);
        }
    }
    
    
}
