Christian Dunne
cdunne7
traceTM_cdunne7

The code simulates a NTM by taking a .csv NTM file and test input strings and creating a tree of all possible configurations, meaning all paths of execution, to determine whether each input string is accepted or rejected.
It measures and models nondeterminism by keeping count of how many "branches" it discovers and taking an average once the tree is complete, finding the mean number of configurations at each level.
I used various NTMs as test cases, showing a range of nondeterminism, from low (e.g. bstar.csv) to high (e.g. hind.csv)
As the code traces the given NTM, it creates a tree which is shown at the end of each trace to further illuminate the process.

Overall, the code does a good job of measuring nondeterminism, and shows the varying levels that come with more advanced NTMs or more complicated inputs.