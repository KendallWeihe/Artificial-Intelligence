Author: Kendall Weihe
Assignment: CS463G Fall 2016 Bayes Net programming assignment
Date: November 18th 2016
Purpose: To teach students about Bayes Nets and a basic MCMC algorithm

The CPT's of A,D,E and F conditioned on their Markov blankets are stored in the following files.
In order to understand each table, please refer to this key that shows what each column represents.
I have also included pictures of the hand written tables -- tables1.jpeg tables2.jpeg

  cp_mb_A.csv: (1 = True || 0 = False)
    C | D | a | ~a

  cp_mb_D.csv:
    A | E | F | d | ~d

  cp_mb_E.csv:
    B | D | F | e | ~e

  cp_mb_F.csv:
    D | E | f | ~f

Calculating the condition probability given the Markov blanket for each node was challenging, but once I understood
  certain identities I was able to figure it out. Also, Adam Whidden provided some help on the discussion
  board. I verified some of my table values with several people on the discussion board: Olivia Houghton and Kristina Shaffer.

  Basic identities:
    P(AB) = P(A|B)*P(B) = P(B|A)*P(A)
    P(A) = P(A|B)*P(B) + P(A|~B)P(~B)
      --> given that A depends on B
    P(A|B) = P(B|A)*P(A) / P(B)
    P(A|B) = P(AB) / P(B)

To run the program:
  - navigate to this directory in the terminal
  - `python main.py`

Program notes:
  This is a rather naive implementation. This algorithm could be written in fewer lines of code.
  The reason why I went with a naive solution was so that I could allow the user to
  change the values of the probability tables stored in CSV files.

  The MCMC algorithm is run 5 different times, with 10,000 iterations for each run.

  The program saves the ratio values for each of the 5 runs to CSV files.
  Check the file graph.xls for graphs of the runs.

  General pseudocode is:
    iterate over number of runs
      initialize random starting states -- fix evidence nodes (C and B)
      iterate 10,000 times
        for each node:
          find current row in CPT conditioned given the Markov blanket
          flip a biased coin
          if the flip > current node value then flip the state of the node
        if a == true then increment count
        if iteration % 40 == 0 then append count / iteration_number to ratio array
      save ratio list to CSV file

A pattern I noticed:
  I noticed a recurring pattern in the formulas to compute the CPT conditioned on each nodes Markov blanket.
  When I saw that pattern show up again, I was confident that I was on the right track.
  The pattern looked similar to this:

            P(A|B)*P(C|D)
      -----------------------------
      P(A|B)*P(C|D) + P(A|~B)P(C|~D)


What I learned:
  - I learned the basic MCMC algorithm
  - I learned how to solve for CPT conditioned on a Markov blanket by using probability identities
    - I was rusty on my probability skills, but after this project I feel a little bit better 
