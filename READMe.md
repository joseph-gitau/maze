**Maze Search**

Tasks: 
Part 1: Basic pathfinding
To begin with, you will consider the problem of finding a path through a maze from a given start state to a given goal state. This scenario is illustrated in the figure above, where the start position is indicated by the "Pacman" icon and the goal state is a dot. The maze layout will be given to you in a simple text format, where '%' stands for walls, 'P' for the starting position, and '.' for the goal (see sample maze file). For this part of the assignment, all step costs are equal to one.
Select ONE from the following search algorithm Task choice 1 and the A* search algorithm in Task choice 2 for solving different mazes:
Task choice 1:
•	Depth-first search;
•	Breadth-first search;
Task choice 2: 
•	A* search.
For A* search, use the Manhattan distance from the current position to the goal as the heuristic function.
Run each of the above algorithms on the small maze, medium maze, big maze, and the open maze. For each problem instance and each search algorithm, report the following:
a.	The solution (Graphic Visualization) and its path cost;
b.	Number of nodes expanded;
c.	Maximum tree depth searched;
d.	Maximum size of the fringe.
You can display the solution by putting a '.' in every maze square visited on the path (example solution to the big maze).
Part 2: Search with multiple goals
Now we consider a harder problem of finding the shortest path through a maze while hitting multiple goals (that is, you want to make the Pacman, initially at P, eat all the dots). trickySearch.lay is a sample problem instance. Once again, in this part, we assume unit step costs.
Revise your code from Part 1 to deal with this scenario. This will require changing the goal test (have you eaten all the dots?) and the state representation (besides your current position in the maze, is there anything else you need to know?).
Run the two search algorithms from Part 1 on the tiny search, small search, and tricky search. For each search method and problem instance, report the solution cost and number of nodes expanded.
It may come as a surprise to discover that uninformed searches can be very inefficient even when dealing with small problems. As such, it is recommended to set a reasonable upper limit on the number of nodes to be expanded, and to terminate the search without a solution if this limit is surpassed. To improve the chances of finding a solution in a timely manner, it is crucial to develop a strong heuristic. It is advisable to dedicate some time to thinking about this. When writing the report, it is important to discuss the chosen heuristic and provide an explanation for why it is admissible. It is also acceptable to propose multiple heuristics and present the results for each of them. The goal should be to develop a heuristic that is even more effective than the others.
Tips
•	Make sure you get all the bookkeeping right. This includes handling of repeated states (in particular, what happens when you find a better path to a state already on the fringe) and saving the optimal solution path.
•	Pay attention to tiebreaking. If you have multiple nodes on the fringe with the same minimum value of the evaluation function, the speed of your search and the quality of the solution may depend on which one you select for expansion.
•	You will be graded on the correctness of your solution, not on the efficiency and elegance of your data structures. For example, I don't mind whether your priority queue or repeated state detection uses brute-force search, as long as you end up expanding (roughly) the correct number of nodes and find the optimal solution. So, feel free to use "dumb" data structures as long as it makes your life easier and still enables you to complete the assignment in a reasonable amount of time.
•	Make your report easy to understand and interesting to read. Feel free to note any interesting observations you made or insights you gained while doing the assignment. The goal of the assignments is to get you to explore and to learn, and I would like to see what you learned reflected in your report. 
•	I reserve the right to give bonus points for any advanced methods or especially challenging solutions that you implement. For this assignment, I may give you bonus points if you decide to do a nicer graphical visualization of the mazes and the found solutions. (bonus is 5 ~ 10 points)

