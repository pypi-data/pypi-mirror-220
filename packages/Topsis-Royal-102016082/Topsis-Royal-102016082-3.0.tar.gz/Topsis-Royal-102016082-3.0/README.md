## About TOPSIS

The Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS) is a multi-criteria decision analysis method. TOPSIS is based on the concept that the chosen alternative should have the shortest geometric distance from the positive ideal solution (PIS) and the longest geometric distance from the negative ideal solution

## The Method
- Step 1 
Calculating Normalized Matrix and weighted Normalize matrix. We normalize each value by making it: where m is the number of rows in the dataset and n is the number of columns. I vary along rows and j varies along the column.

- Step 2
Calculating Ideal Best and Ideal worst and Euclidean distance for each row from ideal worst and ideal best value. First, we will find out the ideal best and ideal worst value: Now here we need to see the impact, i.e. is it ‘+’ or ‘-‘ impact. If ‘+’ impact Ideal best for a column is the maximum value in that column and the ideal worst is the minimum value in that column, and vice versa for the ‘-‘ impact.

- Step 3
    Calculating Topsis Score and Ranking. Now we have Distance positive and distance negative with us, let’s calculate the Topsis score for each row on basis of them.
    TOPSIS Score = diw / (dib + diw)  for each row
    Now rank according to the TOPSIS score, i.e. higher the score, better the rank

## Installation

On the Python console, run 'pip install Topsis-Royal-102016082'

## License

MIT

**Free Software, Hell Yeah!**
