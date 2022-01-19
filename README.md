# WordleSolver

This [Wordle](https://www.powerlanguage.co.uk/wordle/) solver depends on the output from my [WordleDictionaryCreator](https://github.com/jmonty42/WordleDictionaryCreator) repo. See that repo for a detailed description of the dictionary object used in this solver.

The basic approach to solve the daily puzzle here is:

For each word guess:
1. Record which letters are green, yellow, and gray.
2. Filter the words in the dictionary based on the constraints implied by the colored letters.
3. Suggest the most common remaining words in the dictionary for the next guess.

## Input

This Python script runs in the terminal and uses stdin and stdout for i/o. It is pretty brittle and ugly as far as getting input is concerned as I was more focussed on the algorithm for solving the puzzle. It'll probably break if you put in too many constraints or conflicting constraints.