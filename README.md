# Dijkstra-Shortest-Path-Demo
This project is a demonstration of finding the shortest path by Dijkstra algorithm.

The project is written in Python. I also use some other libraries, such as Tkinter for making the GUI, Matplotlib for visualizing.

About the functions, my project have 4 buttons. First two are Map1 and Map2. These clearly mean that I have created only 2 maps, and you can switch between them.
The third one is **Visualize**. This function will create every VALID line between two vertex. About the terminology, vertices are the "break points" between two perpendicular lines, and a line is VALID when it does not travel outside the map AT ANY TIME. <br>

The algorithms to check the VALIDITY are based on _RAY-CASTING_ algo. However, there are still edge cases that can only be solved with some tricky implementations (I'm not sure if I still remember it lol). <br>

The last function is Find which finds the shortest path between two points (user chooses them). 
More about [the Dijkstra algorithm](https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/) that I used to implement this function. I prefer this link since [Wikipedia's](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) is a bit lengthy.

Here's my demo: <br>
<a href="http://www.youtube.com/watch?feature=player_embedded&v=1y6D9M5s5Ww
" target="_blank"><img src="http://img.youtube.com/vi/1y6D9M5s5Ww/0.jpg" 
alt="dijkstra demo" width="240" height="180" border="10" /></a>


