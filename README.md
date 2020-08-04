### CS 456 - Assignment 3

An assignment to implement Intra-AS Routing Prototol.

#### Instructions

##### Setup Instructions

1. run `pip3 install networkx`. `networkx` is a graphing library which helps us
  use Dijkstra's algorithms modularly while avoiding bloating the codebase.
  More information can be found at [NetworkX Doc](https://networkx.github.io/)

##### Running the Program

1. To run the program, make sure you have *Python3* installed.
2. Ensure `grading_topo.json` is in the current directory.
3. In a new tab, run `python3 nfe.py 127.0.0.1 9000 grading_topo.json`. This
  will start the Network Forwarding Emulator.
4. Now, Repeat these steps 7 times, and replace [router-id] with the IDs 1, 2,
  3, 4, 5, 6 and 7.
  a) open a new tab
  b) run `python3 virtualrouter.py 127.0.0.1 9000 [router-id]`
