# YOUR PROJECT TITLE

#### Video Demo: <URL HERE>

## Description: A Terminal Maze Generator

### Usage:

#### Help:

Entering `python project.py -h` will give you the help:

```usage: project.py [-h] [-a {rnd,bt,sw,rb}] [-n | -m] [-p] [-e] [-b] [-d DISTANCE] width height

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

`python project.py 10 10` will produce: ![standard 10 x 10 maze](/images/standard1010.png)

#### Flags:

`-h`: shows help
`-a`: specifies algorithm used to generate maze, options are:

- `rnd` : Random, not a true maze
- `bt` : Binary Tree, a maze with distinct open paths on two sides
- `sw` : Sidewinder, a maze with a distinct open path along the top edge
- `rb` : Recursive Backtrack, a true maze (default algorithm)
