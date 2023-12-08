# Terminal Maze Generator

#### Video Demo: <URL HERE>

## Description: A Terminal Maze Generator

A Terminal Maze Generator that allows you to maze a maze of dynamic size, from 3 x 3 cells in size minimum, to 45 x 45 cells in size maximum, using a variety of algorithms to form the maze, and some options to change the display of the finished maze.

### Usage:

#### Help:

Entering `python project.py -h` will give you the help:

```
usage: project.py [-h] [-a {rnd,bt,sw,rb}] [-n | -m] [-p] [-e] [-b] [-d DISTANCE] width height

Generate a maze in the terminal with a variety of options, minimum size 3 x 3

positional arguments:
  width                 the width of the maze you wish to generate, range(3 to 45)
  height                the height of the maze you wish to generate, range(3 to 45)

options:
  -h, --help            show this help message and exit
  -a {rnd,bt,sw,rb}, --algorithm {rnd,bt,sw,rb}
                        specify maze generating algorithm (random, binary tree, sidewinder,
                        random walk, recursive backtrack) (default: recursive_backtrack)
  -n, --numbers         numbers the cells of the maze, limited to mazes less than 1000 cells in
                        size (default: False)
  -m, --manhattan_distance
                        numbers the cells of the maze with manhattan distance numbering (default:
                        False)
  -p, --portals         show entry and exit points in the maze (default: True)
  -e, --edge            align portals to the outside edge of the maze (default: False)
  -b, --blank           print a blank maze (default: False)
  -d DISTANCE, --distance DISTANCE
                        the minimum distance the entry and exit can be apart (default: 0)

terminal maze generator v1.0
```

#### Standard Use:

Entering `python project.py width height` will produce a maze of the specified width and height, e.g:

`width` and `height` are restricted to between 3 and 45 units inclusively each.

`python project.py 10 10` will produce: ![standard 10 x 10 maze](/images/1010.png)

#### Flags:

`-h` : Show help\
`-a` : Specifies algorithm used to generate maze, options are:

- `rnd` : Random, not a true maze
- `bt` : Binary Tree, a maze with distinct open paths on two sides
- `sw` : Sidewinder, a maze with a distinct open path along the top edge
- `rb` : Recursive Backtrack, a true maze (default algorithm)

`-n` : Show numbered cells in the maze (mutually exclusive with manhattan distance)\
`-m` : Show manhattan distance in the maze (mutually exclusive with numbered cells)

`-p` : Show portals in the maze (IN/OUT markers)\
`-e` : Force portals to appear in the outermost cells of the maze

`-b` : Draw a blank unmodified maze

`-d DISTANCE`: Forces the portals to be `DISTANCE` units apart up to the limits of the maze boundarys

#### Examples:

`python project.py 10 10 -p`:\ 
![no portals 10 x 10 maze](/images/1010noportal.png)

`python project.py 10 10 -n`:\ 
![numbered 10 x 10 maze](/images/1010numbered.png)

`python project.py 10 10 -m`:\ 
![manhattan distance 10 x 10 maze](/images/1010manhattan.png)

`python project.py 10 10 -p -m`:\ 
![no portals manhattan distance 10 x 10 maze](/images/1010noportalmanhattan.png)

`python project.py 10 10 -d 20`:\ 
![standard 10 x 10 maze maximum distance](/images/1010distancemax.png)

`python project.py 10 10 -b`:\ 
![blank 10 x 10 maze](/images/1010blank.png)
