#include <stdlib.h>
#include <stdio.h>
/* 
# ==============================================================================
#
# randySolution.c
#
# This program brute-forces the "random" seeds used in the randy (100)
# challenge to recover the flag
#
# Authors: Ryan Grandgenett and James Nesta
# For:     Boston Key Party (Team NULLify)
# Date:    June 8, 2013
#
# ==============================================================================
*/

int main() 
{
	unsigned char i;
	unsigned char j;
	unsigned char k;
	unsigned char l;
	unsigned int m;
	unsigned int seed;
	unsigned int result;
	unsigned int solution[] = {0x7358837a, 0x34d8c3b5, 0x1f49456c, 0x1fea6614 , 0x4e81abc7, 0x683d3f5d, 0x28c9a8fe};

	/* Generate all printable 4 character ascii values */
	for (i = 0x20; i < 0x7F; i++) 
	{
		for (j = 0x20; j < 0x7F; j++) 
		{
			for (k = 0x20; k < 0x7F; k++) 
			{
				for (l = 0x20; l < 0x7F; l++) 
				{
					/* Set the seed */
					seed = (l << 24) | (k << 16 ) | (j << 8) | (i);
					srand(seed);
					/* Call the newly seeded random function */
					result = rand();
					/* Check if the output from the random function is in the solution array
                       if so print the results*/
					for (m = 0; m < 8; m++) 
					{
						if (result == solution[m]) 
						{
							printf("solution[%d] = %c %c %c %c\n", m, i, j, k, l);
						}
					}
				}
			}
		}
	}
        
    return (0);
}
