import sys # not needed with argparse?
import random
import argparse
import math


DIRECTIONS = ["n", "e", "s", "w"]




    #       Turn this into a class, at least the parts that make sense
    #       that will solve the recalling of the generate xy function,
    #       can store that as a class/instance variable
    #
    #       TODO:
    #           make class
    #           error checking/handling
    #           each data layer stored separately
    #           all stored in json


    #   TODO:
    #       if distance is specified, it cannot be more than
    #       width - 1 + height - 1
    #       specify within distance or must be
    #       outside distance?
    #       Make a function to take all the arrays and make a NEW array
    #       superimpose the arrays to make a new array with all the
    #       values applied and return that
    #       try to remove the string keys values from the xy dict
    #       and make them ints instead and clean up the code
    #       everywhere they are referenced as strings? DONE?

    #   TODO:
    #       Make sure to make a copy of the maze and then apply the other data to it
    #       according to the arguments:
    #       manhattan numbers, entrance/exit etc

    #    TODO:
    #        Refactor
    #        Make everything that uses horrible array maths use
    #        enumerate and slices?
    #        Save maze to text file! (see above: json!)
    #


    #   TODO:
    #       Function that returns a character from whichever character set has been specified by the user using command line flag for the wall pieces
    #       Default pieces are the current ones
    #       Those characters can be stored in a dict, and returned depending on which charset is specified with a command line flag
    #       a command line flag for specifying a single char to replace ALL wall pieces, i.e. "@" makes a maze with @ for walls
    #       build_blank_maze function and clean_maze function would need to be modified at least?
    #       need a new function to return the correct wall piece
    #       this function is called from the previous 2 maze functions instead of hard coded wall piece?

def main():
    parser = argparse.ArgumentParser(description="Generate a maze in the terminal with a variety of options, minimum size 3 x 3", formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=True)

    parser.add_argument("width", help="the width of the maze you wish to generate", type=int)

    parser.add_argument("height", help="the height of the maze you wish to generate", type=int)

    parser.add_argument("-a", "--algorithm", type=str, choices=["rnd", "bt", "sw", "rw", "rb"], default="recursive_backtrack", help="specify maze generating algorithm (random, binary tree, sidewinder, random walk, recursive backtrack)")

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-n", "--numbers", default=False, help="numbers the cells of the maze", action="store_true")

    group.add_argument("-m", "--manhattan_distance", default=False, help="numbers the cells of the maze with manhattan distance numbering", action="store_true")

    parser.add_argument("-p", "--portals", default=True, help="show entry and exit points in the maze", action="store_false")

    parser.add_argument("-e", "--edge", default=False, help="align portals to the outside edge of the maze",  action="store_true")

    parser.add_argument("-d", "--distance", type=int, default=0, help="the minimum distance the entry and exit can be apart")

    # flags: distance between portals, portals on/off, manhattan numbers on/off, numbers on/off, portals on the edge on/off, minimum size for maze: 3
    args = parser.parse_args()

    width = args.width
    height = args.height

    if (args.algorithm == "random" or args.algorithm == "rnd"):
        algorithm = "random"
    elif (args.algorithm == "binarytree" or args.algorithm == "bt"):
        algorithm = "binarytree"
    elif (args.algorithm == "sidewinder" or args.algorithm == "sw"):
        algorithm = "sidewinder"
    elif (args.algorithm == "randomwalk" or args.algorithm == "rw"):
        algorithm = "randomwalk"
    elif (args.algorithm == "recursive_backtrack" or args.algorithm == "rb"):
        algorithm = "recursive_backtrack"

    numbers = args.numbers
    manhattan_distance = args.manhattan_distance
    portals = args.portals
    edge = args.edge
    distance = args.distance


    maze = build_blank_maze(width, height)
    # print(output_maze(maze, width, height))
    viable_pos = get_viable_pos(width, height)
    xy = generate_xy(width, viable_pos)
    # distance needs command line arg? maybe others too?
    portal_in, portal_out = get_portals(width, height, viable_pos, xy, distance, edge)

    maze = construct_maze(maze, portal_in, portal_out, width,
                        viable_pos, xy, num_maze=numbers, portals=portals, mn_num=manhattan_distance, algorithm=algorithm)

    print(args)
    print(width, height, algorithm, numbers, manhattan_distance, portals, edge, distance)
    print(type(width), type(height), type(algorithm), type(numbers), type(manhattan_distance), type(portals), type(edge), type(distance))

    print(output_maze(maze, width, height))


def build_blank_maze(width: int, height: int) -> []:
    maze_w, maze_h = width * 4 + 1, height * 2 + 1
    maze = []
    for y in range(maze_h):
        for x in range(maze_w):
            # top left (┏━)
            if x == 0 and y == 0:
                maze.append("\u250f")
            # top right (━┓)
            elif x == width * 4 and y == 0:
                maze.append("\u2513")
            # bottom left (┗━)
            elif x == 0 and y == height * 2:
                maze.append("\u2517")
            # bottom right (━┛)
            elif x == width * 4 and y == height * 2:
                maze.append("\u251b")
            # down t piece (┳)
            elif x % 4 == 0 and y == 0:
                maze.append("\u2533")
            # up t piece (┻)
            elif x % 4 == 0 and y == height * 2:
                maze.append("\u253b")
            # vertical line (┃)
            elif x % 4 == 0 and y % 2 == 1:
                maze.append("\u2503")
            # left side t piece (┣)
            elif x == 0 and y % 2 == 0:
                maze.append("\u2523")
            # right side t piece (┫)
            elif x == width * 4 and y % 2 == 0:
                maze.append("\u252b")
            # cross piece (╋)
            elif x % 4 == 0 and y % 2 == 0:
                maze.append("\u254b")
            # horizontal line (━)
            elif y % 2 == 0:
                maze.append("\u2501")
            else:
                maze.append(" ")

    return maze


def output_maze(maze: [], width: int, height: int) -> str:
    maze_w, maze_h = width * 4 + 1, height * 2 + 1
    combined = ""
    for i in range(maze_h):
        combined += "".join(maze[i * maze_w: (i + 1) * maze_w]) + "\n"

    return combined


# need to rethink arguments
# process them and add them to some list? or use argv? well
# have to do that regardless
def construct_maze(
        maze: [],
        portal_in: int,
        portal_out: int,
        width: int,
        viable_pos: [],
        xy: {},
        num_maze: bool = None,
        portals: bool = None,
        mn_num: bool = None,
        algorithm: str = None,
) -> []:
    if algorithm == "random":
        algo_random(maze, width, viable_pos)

    if algorithm == "binarytree":
        algo_binarytree(maze, width, viable_pos)

    if algorithm == "sidewinder":
        algo_sidewinder(maze, width, viable_pos)

    if algorithm == "randomwalk":
        algo_randomwalk(maze, width, viable_pos)

    if algorithm == "recursive_backtrack":
        algo_recursive_backtracking(maze, width, viable_pos, portal_in, portal_out)

    cleaned_maze = clean_maze(maze, width, viable_pos)
    for _ in cleaned_maze:
        maze[_] = cleaned_maze[_]

    cleaned_walls = clean_walls(maze, width, viable_pos)
    for _ in cleaned_walls:
        maze[_] = cleaned_walls[_]

    if num_maze and not mn_num:
        num = number_maze(viable_pos)
        for _ in num:
            maze[_] = num[_]
    if portals:
        ports = set_portals(portal_in, portal_out)
        for _ in ports:
            maze[_] = ports[_]
    if mn_num:
        manhattan = manhattan_numbers(xy, portal_in, portal_out)
        for _ in manhattan:
            maze[_] = manhattan[_]

    return maze


def algo_random(maze, width, viable_pos):
    for pos in viable_pos:
        direction = random_direction()[0]
        remove_wall(maze, width, viable_pos, pos, direction)


def random_direction():
    direction = random.choice(DIRECTIONS)
    opposite_direction = DIRECTIONS[(DIRECTIONS.index(direction) + 2) % 4]
    return direction, opposite_direction


# North/West version of binary tree maze algorithm
def algo_binarytree(maze, width, viable_pos):
    for pos in viable_pos:
        if viable_pos.index(pos) < width:
            direction = "w"
        elif viable_pos.index(pos) % width == 0:
            direction = "n"
        else:
            direction = random.choice(["n", "w"])
        remove_wall(maze, width, viable_pos, pos, direction)


def algo_sidewinder(maze, width, viable_pos):
    current_position = 0
    length_of_maze = len(viable_pos)
    cells = []
    while current_position < length_of_maze:
        pos = viable_pos[current_position]
        if current_position < width:
            remove_wall(maze, width, viable_pos, pos, "e")
        if current_position >= width:
            cells.append(pos)
        if current_position >= width and ((current_position + 1) % width) == 0:
            cell_up = random.choice(cells)
            remove_wall(maze, width, viable_pos, cell_up, "n")
            cells.clear()
        elif current_position >= width and ((current_position + 1) % width) > 0:
            carve = random.choice([True, False])
            if carve:
                remove_wall(maze, width, viable_pos, pos, "e")
            else:
                cell_up = random.choice(cells)
                remove_wall(maze, width, viable_pos, cell_up, "n")
                cells.clear()
        current_position += 1


def algo_randomwalk(maze, width, viable_pos):
    current_position = random.choice(viable_pos)
    pos = viable_pos[current_position]
    visited_cells = []
    while pos not in visited_cells:
        next_direction = random.choice(DIRECTIONS)
        old_pos, pos, old_direction = remove_wall(maze, width, viable_pos, pos, next_direction)
        visited_cells.append(old_pos)


def algo_recursive_backtracking(maze, width, viable_pos, portal_in, portal_out):
    start_position = get_random_pos(viable_pos, portal_in, portal_out)
    visited_cells = [start_position]


    def visit_pos(position: int):
        while True:
            unvisited_cells = []
            position_index = viable_pos.index(position)

            if check_direction(width, viable_pos, position, "n")[1] and viable_pos[position_index - width] not in visited_cells:
                unvisited_cells.append("n")

            if check_direction(width, viable_pos, position, "s")[1] and viable_pos[position_index + width] not in visited_cells:
                unvisited_cells.append("s")

            if check_direction(width, viable_pos, position, "w")[1] and viable_pos[position_index - 1] not in visited_cells:
                unvisited_cells.append("w")

            if check_direction(width, viable_pos, position, "e")[1] and viable_pos[position_index + 1] not in visited_cells:
                unvisited_cells.append("e")

            if len(unvisited_cells) == 0:
                return
            else:
                next_direction = random.choice(unvisited_cells)
                if next_direction == "n":
                    position = remove_wall(maze, width, viable_pos, position, "n")[1]
                elif next_direction == "s":
                    position = remove_wall(maze, width, viable_pos, position, "s")[1]
                elif next_direction == "w":
                    position = remove_wall(maze, width, viable_pos, position, "w")[1]
                elif next_direction == "e":
                    position = remove_wall(maze, width, viable_pos, position, "e")[1]

                visited_cells.append(position)
                visit_pos(position)

    visit_pos(start_position)


def manhattan_numbers(xy: {}, portal_in: int, portal_out: int) -> {}:
    out_xy = get_xy(portal_out, xy)
    mn_dict = {}
    for k, v in enumerate(xy):
        if v not in [portal_in, portal_out]:
            mn = get_mn(get_xy(v, xy), out_xy)
            if mn > 99:
                mn_dict[v - 1] = f"{str(mn)[:1]}"
                mn_dict[v] = f"{str(mn)[1:2]}"
                mn_dict[v + 1] = f"{str(mn)[2:]}"
            elif mn > 9:
                mn_dict[v] = f"{str(mn)[:1]}"
                mn_dict[v + 1] = f"{str(mn)[1:]}"
            else:
                mn_dict[v] = f"{mn}"

    return mn_dict


def get_mn(start_pos: tuple, end_pos: tuple) -> int:
    return abs(end_pos[0] - start_pos[0]) + abs(end_pos[1] - start_pos[1])


def get_portals(
        width: int,
        height: int,
        viable_pos: [],
        xy: {},
        distance: int = None,
        edge: bool = None,
) -> tuple:
    if (distance > math.floor(math.sqrt(pow(width, 2) + pow(height, 2)))):
        distance = math.floor(math.sqrt(pow(width, 2) + pow(height, 2)))
    if edge:
        edges = get_edge_pos(width, height, viable_pos)

        while True:
            portal_in = random.choice(edges)
            portal_out = random.choice(edges)
            if (
                    get_mn(get_xy(portal_in, xy), get_xy(portal_out, xy))
                    < distance
            ):
                continue
            if portal_in != portal_out:
                break

        return portal_in, portal_out

    else:
        while True:
            portal_in = random.choice(viable_pos)
            portal_out = random.choice(viable_pos)
            if (
                    get_mn(get_xy(portal_in, xy), get_xy(portal_out, xy))
                    < distance
            ):
                continue
            if portal_in != portal_out:
                break

        return portal_in, portal_out


def set_portals(portal_in: int, portal_out: int) -> {}:
    return {
        portal_in - 1: " ",
        portal_in: "\033[1;38;5;40mI\033[00m",
        portal_in + 1: "\033[1;38;5;40mN\033[00m",
        portal_out - 1: "\033[1;38;5;214mO\033[00m",
        portal_out: "\033[1;38;5;214mU\033[00m",
        portal_out + 1: "\033[1;38;5;214mT\033[00m"
    }


def get_random_pos(viable_pos: [], portal_in: int, portal_out: int) -> int:
    random_pos = random.choice(viable_pos)
    while random_pos in (portal_in, portal_out):
        random_pos = random.choice(viable_pos)
    return random_pos


def get_viable_pos(width: int, height: int) -> []:
    maze_w, maze_h = width * 4 + 1, height * 2 + 1
    viable_pos = []
    for y in range(0, maze_h):
        for x in range(0, maze_w):
            if y * maze_w % 2 == 1:
                if x > 0 and (x % 4) + 1 == 3:
                    viable_pos.append(x + y * maze_w)

    return viable_pos


def get_edge_pos(width: int, height: int, viable_pos: []) -> []:
    edge_pos = []
    for _ in viable_pos[:width]:
        edge_pos.append(_)
    for _ in range(height):
        edge_pos.append(viable_pos[width * _])
        edge_pos.append(viable_pos[width * _ - 1])
    for _ in viable_pos[-width:]:
        edge_pos.append(_)

    edges_set = set()
    edges_set.update(edge_pos)
    edge_pos = sorted(list(edges_set))

    return edge_pos


def number_maze(viable_pos: []) -> {}:
    number_dict = {}
    for i, _ in enumerate(viable_pos):
        if i > 99:
            number_dict[_ - 1] = f"{str(i)[:1]}"
            number_dict[_] = f"{str(i)[1:2]}"
            number_dict[_ + 1] = f"{str(i)[2:]}"
        elif i > 9:
            number_dict[_] = f"{str(i)[:1]}"
            number_dict[_ + 1] = f"{str(i)[1:]}"
        else:
            number_dict[_] = f"{i}"

    return number_dict


def remove_wall(maze: [], width: int, viable_pos: [], cell: int, direction: str) -> tuple:
    cell1, cell2, direction = check_direction(width, viable_pos, cell, direction)

    if (cell2 == None):
        return cell1, cell2, direction

    if direction in ["e", "w"]:
        maze[int((cell1 + cell2) / 2)] = " "
    elif direction in ["n", "s"]:
        maze[int((cell1 + cell2) / 2)] = " "
        maze[int((cell1 + cell2) / 2) - 1] = " "
        maze[int((cell1 + cell2) / 2) + 1] = " "

    return cell1, cell2, direction


def check_direction(width: int, viable_pos: [], cell: int, direction: str) -> tuple:
    cell1 = cell
    if direction == "n":
        if viable_pos.index(cell1) < width:
            return cell1, None, direction
        cell2 = viable_pos[viable_pos.index(cell1) - width]
    elif direction == "s":
        if viable_pos.index(cell1) >= (len(viable_pos) - width):
            return cell1, None, direction
        cell2 = viable_pos[viable_pos.index(cell1) + width]
    elif direction == "e":
        if (viable_pos.index(cell1) + 1) % width == 0:
            return cell1, None, direction
        cell2 = viable_pos[viable_pos.index(cell1) + 1]
    elif direction == "w":
        if (viable_pos.index(cell1) + 1) % width == 1:
            return cell1, None, direction
        cell2 = viable_pos[viable_pos.index(cell1) - 1]

    return cell1, cell2, direction



def clean_maze(maze: [], width: int, viable_pos: []) -> {}:
    cleaned_maze_dict = {}
    for pos in viable_pos:
        if not viable_pos.index(pos) < width + 1 and not (viable_pos.index(pos) + 1) % width == 1:
            gaps = []

            tl = viable_pos[viable_pos.index(pos) - width - 1]
            tr = viable_pos[viable_pos.index(pos) - width]
            bl = viable_pos[viable_pos.index(pos) - 1]
            br = viable_pos[viable_pos.index(pos)]

            gaps.append(1 if maze[int((tl + tr) / 2)] == " " else 0)
            gaps.append(1 if maze[int((tr + br) / 2)] == " " else 0)
            gaps.append(1 if maze[int((bl + br) / 2)] == " " else 0)
            gaps.append(1 if maze[int((bl + tl) / 2)] == " " else 0)

            centre = int((tl + tr + bl + br) / 4)
            if gaps == [1, 1, 1, 0]:
                cleaned_maze_dict[centre] = "\u2578"
            elif gaps == [1, 1, 0, 1]:
                cleaned_maze_dict[centre] = "\u257B"
            elif gaps == [1, 0, 1, 1]:
                cleaned_maze_dict[centre] = "\u257A"
            elif gaps == [0, 1, 1, 1]:
                cleaned_maze_dict[centre] = "\u2579"
            elif gaps == [1, 1, 0, 0]:
                cleaned_maze_dict[centre] = "\u2513"
            elif gaps == [0, 1, 1, 0]:
                cleaned_maze_dict[centre] = "\u251B"
            elif gaps == [0, 0, 1, 1]:
                cleaned_maze_dict[centre] = "\u2517"
            elif gaps == [1, 0, 0, 1]:
                cleaned_maze_dict[centre] = "\u250F"
            elif gaps == [1, 0, 1, 0]:
                cleaned_maze_dict[centre] = "\u2501"
            elif gaps == [0, 1, 0, 1]:
                cleaned_maze_dict[centre] = "\u2503"
            elif gaps == [0, 1, 0, 0]:
                cleaned_maze_dict[centre] = "\u252B"
            elif gaps == [0, 0, 1, 0]:
                cleaned_maze_dict[centre] = "\u253B"
            elif gaps == [0, 0, 0, 1]:
                cleaned_maze_dict[centre] = "\u2523"
            elif gaps == [1, 0, 0, 0]:
                cleaned_maze_dict[centre] = "\u2533"
            elif gaps == [1, 1, 1, 1]:
                cleaned_maze_dict[centre] = " "

    return cleaned_maze_dict


def clean_walls(maze: [], width: int, viable_pos: []) -> {}:
    maze_w = width * 4 + 1
    top = viable_pos[:width]
    bottom = viable_pos[-width:]
    left = viable_pos[:-1:width]
    right = viable_pos[width - 1::width]
    cleaned_walls_dict = {}

    for k, v in enumerate(top[:-1]):
        wall = int((v + top[k + 1]) / 2) - maze_w
        if maze[wall] == "\u2533" and (maze[wall + maze_w]) == " ":
            cleaned_walls_dict[wall] = "\u2501"

    for k, v in enumerate(bottom[:-1]):
        wall = int((v + bottom[k + 1]) / 2) + maze_w
        if maze[wall] == "\u253B" and (maze[wall - maze_w]) == " ":
            cleaned_walls_dict[wall] = "\u2501"

    for k, v in enumerate(left[:-1]):
        wall = int((v + left[k + 1]) / 2) - 2
        if maze[wall] == "\u2523" and (maze[wall + 2]) == " ":
            cleaned_walls_dict[wall] = "\u2503"

    for k, v in enumerate(right[:-1]):
        wall = int((v + right[k + 1]) / 2) + 2
        if maze[wall] == "\u252B" and (maze[wall - 2]) == " ":
            cleaned_walls_dict[wall] = "\u2503"

    return cleaned_walls_dict


def generate_xy(width: int, viable_pos: []) -> {}:
    return {v: (k % width, int(k / width)) for k, v in enumerate(viable_pos)}


def get_xy(pos: int, xy: {}) -> tuple:
    return xy[pos]


def get_pos(xy: {}, cell: tuple) -> int:
    for k, v in xy.items():
        if v == cell:
            return k


if __name__ == "__main__":
    main()
