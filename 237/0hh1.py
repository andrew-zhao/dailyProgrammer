import sys
import time
import win32gui
import win32api
import win32con
from PIL import ImageGrab

"""
Reads an image and extracts the puzzle.
Converts puzzle to an internal representation (2D Array).
Returns converted puzzle where x is row # and y is column #.
"""
def read_puzzle(im, dim):
	def get_rgb(x, y, width, pixels):
		return pixels[x + y * width]

	h1 = {
		(34, 34, 34): -1,
		(42, 42, 42): -1,
		(213, 83, 54): 0,
		(48, 167, 194): 1,
	}

	n0 = {
		(255, 255, 255): -1,
		(238, 238, 238): -1,
		(255, 56, 75): 0,
		(28, 192, 224): 1
	}

	contranoid = {
		(15, 15, 15): -1,
		(79, 79, 79): -1,
		(125, 125, 125): 0,
		(201, 201, 201): 1
	}

	width, height = im.size
	tile_dim = width / dim
	offset = tile_dim / 2

	pixels = list(im.getdata())

	if pixels[0] in contranoid:
		theme = contranoid
	elif pixels[0] in n0:
		theme = n0
	else:
		theme = h1

	puzzle = []

	for x in range(dim):
		row = []
		for y in range(dim):
			rgb = get_rgb(offset + x * tile_dim, offset + y * tile_dim, width, pixels)
			if rgb in theme.keys():
				row.append(theme[rgb])
			else:
				min_key = (0, 0, 0)
				min_value = 255 * 3
				for key in theme.keys():
					val = sum(map(lambda x, y: abs(x - y), key, rgb))
					if val < min_value:
						min_value = val
						min_key = key
				row.append(theme[min_key])
		puzzle.append(row)

	return puzzle

"""
Outputs the puzzle solution by clicking on each tile to solve.
Input original puzzle, puzzle solution, image width, screen offset, time between clicks
"""
def output_puzzle(original, solution, width, screen_offset, speed):
	def click(x,y):
	    win32api.SetCursorPos((x, y))
	    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x, y, 0, 0)
	    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

	dim = len(original)
	tile_dim = width / dim
	offset = tile_dim / 2
	x_off, y_off = map(lambda x: x + offset, screen_offset)
	for x in range(dim):
		for y in range(dim):
			if original[x][y] == -1:
				click(x_off + x * tile_dim, y_off + y * tile_dim)
				time.sleep(speed)
				if solution[x][y] == 1:
					click(x_off + x * tile_dim, y_off + y * tile_dim)
					time.sleep(speed)

"""
Solve the given Takuzu puzzle.
Takuzu puzzle is represented as a 2D array.

Checks if a empty spot is has two opposite neighbors that have the same value.
If so, sets the spot to the opposite of that value.
Checks if a non-empty spot has a neighbor with the same value.
If so, sets the ends of the 'run' to the opposite value.
If a row or column has half of one number, fills the empty spots with the opposite.

If no simple logical moves can be made, take a guess and try again.
Uses backtracking with pruning to continue guessing until solved.
"""
def solve_puzzle(puzzle):
	dimension = len(puzzle)

	old_puzzle = map(list, puzzle)
	changed = True
	guess_stack = []
	to_guess = []
	num_guess = -1
	first_guess = False

	while True:
		if changed == False:
			if is_solved_puzzle(puzzle):
				return puzzle

			if first_guess == False:
				for x in range(dimension):
					for y in range(dimension):
						if puzzle[x][y] == -1:
							puzzle_copy = map(list,puzzle)
							puzzle_copy[x][y] = 0
							if is_valid_puzzle(puzzle_copy):
								to_guess.append((x, y, 0))
							puzzle_copy = map(list,puzzle)
							puzzle_copy[x][y] = 1
							if is_valid_puzzle(puzzle_copy):
								to_guess.append((x, y, 1))
				num_guess = int(len(to_guess))
				first_guess = True
			if len(guess_stack) == 0:
				if len(to_guess) < num_guess - 1:
					return -1
				else:
					if len(to_guess) == 0:
						return -1
					guess = to_guess.pop()
					guess_stack.append((map(list, puzzle), list(to_guess), len(to_guess)))
					puzzle[guess[0]][guess[1]] = guess[2]
			else:
				if len(guess_stack[-1][1]) < guess_stack[-1][2] - 2:
					stack_elem = guess_stack.pop()
					puzzle = map(list, stack_elem[0])
				else:
					x, y, guess = guess_stack[-1][1].pop()
					puzzle_copy = map(list,puzzle)
					puzzle_copy[x][y] = guess
					if is_valid_puzzle(puzzle_copy):
						guess_stack.append((map(list, puzzle), list(guess_stack[-1][1]), len(guess_stack[-1][1])))
						puzzle[x][y] = guess

		for x in range(dimension):
			for y in range(dimension):
				if puzzle[x][y] == -1:
					puzzle = empty_adjacent_check(x, y, puzzle)
				else:
					duo_check(x, y, puzzle)

		row_check(puzzle)
		column_check(puzzle)

		if puzzle == old_puzzle:
			changed = False
		else:
			old_puzzle = map(list, puzzle)
			changed = True

	return -1

"""
Checks if the input puzzle is solved.
Returns True is solved, False otherwise.
"""
def is_solved_puzzle(puzzle):
	if is_valid_puzzle(puzzle):
		filled = 0
		for row in puzzle:
			for cell in row:
				if cell > -1:
					filled += 1
		if filled == len(puzzle)**2:
			return True
	return False


"""
Checks if the input puzzle is valid.
If unsolved, returns False.
Otherwise returns True.
"""
def is_valid_puzzle(puzzle):
	dimension = len(puzzle)
	
	# Returns True if neighbors match original
	def check_neighbors(x, y, xd, yd, puzzle):
		if is_valid_coord(x + xd, y + yd, puzzle) and is_valid_coord(x - xd, y - yd, puzzle):
			if puzzle[x][y] == puzzle[x + xd][y + yd] and puzzle[x][y] == puzzle[x - xd][y - yd]:
				return True

	one_column_count = [0 for _ in range(dimension)]
	zero_column_count = [0 for _ in range(dimension)]

	rows = []
	cols = []

	# Check for max runs of 2 and row/col counts
	for x in range(dimension):
		one_count = 0
		zero_count = 0
		for y in range(dimension):
			if puzzle[x][y] != -1:
				if check_neighbors(x, y, -1, 0, puzzle) or check_neighbors(x, y, 0, -1, puzzle):
					return False

			if puzzle[x][y] == 1:
				one_count += 1
				one_column_count[y] += 1
			elif puzzle[x][y] == 0:
				zero_count += 1
				zero_column_count[y] += 1

		if (((one_count + zero_count == dimension) and (one_count != zero_count)) or
					one_count > dimension/2 or zero_count > dimension/2):
			return False

		if one_count + zero_count == dimension:
			rows.append("".join(map(str, puzzle[x])))

	for index in range(dimension):
		one_count = one_column_count[index]
		zero_count = zero_column_count[index]
		if (((one_count + zero_count == dimension) and (one_count != zero_count)) or
					one_count > dimension/2 or zero_count > dimension/2):
			return False
		if one_count + zero_count == dimension:
			cols.append("".join(map(str, [r[index] for r in puzzle])))

	if unique(rows) and unique(cols):
		return True
	else:
		return False

"""
Check if all elements of a set are unique.

Two line version from: http://stackoverflow.com/a/5281641
"""
def unique(elements):
	seen = set()
	return not any(i in seen or seen.add(i) for i in elements)

"""
Checks empty space in puzzle, to see if it is surrounded by the same number.
e.g. "0 _ 0" must be filled by a 1, and "1 _ 1" must be filled by a 0.
Returns the modified puzzle
"""
def empty_adjacent_check(x, y, puzzle):
	edge = len(puzzle) - 1

	# If position not empty or is a corner
	if puzzle[x][y] != -1 or ((x == 0 or x == edge) and (y == 0 or y == edge)):
		return puzzle
	else:
		# If position on horizontal edge
		if x == 0 or x == edge:
			if puzzle[x][y - 1] == puzzle[x][y + 1] and puzzle[x][y - 1] != -1:
				puzzle[x][y] = (puzzle[x][y - 1] + 1) % 2
		# If position on the vertical edge
		elif y == 0 or y == edge:
			if puzzle[x - 1][y] == puzzle[x + 1][y] and puzzle[x - 1][y] != -1:
				puzzle[x][y] = (puzzle[x - 1][y] + 1) % 2
		else:
			if puzzle[x][y - 1] == puzzle[x][y + 1] and puzzle[x][y - 1] != -1:
				puzzle[x][y] = (puzzle[x][y - 1] + 1) % 2
			elif puzzle[x - 1][y] == puzzle[x + 1][y] and puzzle[x - 1][y] != -1:
				puzzle[x][y] = (puzzle[x - 1][y] + 1) % 2
		
		return puzzle

"""
Takes in a non-empty coordinate.
Checks neighbors for a matching value, if found, marks both ends as the opposite.
Returns the modified table.
"""
def duo_check(x, y, puzzle):
	def check_helper(x, y, puzzle, xd, yd):
		value = puzzle[x][y]
		opposite = (value + 1) % 2
		if is_valid_coord(x + xd, y + yd, puzzle) and puzzle[x + xd][y + yd] == value:
			if is_valid_coord(x + (2 * xd), y + (2 * yd), puzzle) and puzzle[x + (2 * xd)][y + (2 * yd)] == -1:
				puzzle[x + (2 * xd)][y + (2 * yd)] = opposite
			if is_valid_coord(x - xd, y - yd, puzzle) and puzzle[x - xd][y - yd] == -1:
				puzzle[x - xd][y - yd] = opposite
		return puzzle

	if puzzle[x][y] != -1:
		puzzle = check_helper(x, y, puzzle, -1, 0)
		puzzle = check_helper(x, y, puzzle, 0, -1)
		puzzle = check_helper(x, y, puzzle, 0, 1)
		puzzle = check_helper(x, y, puzzle, 1, 0)
	return puzzle

"""
Checks if coordinate is in the puzzle.
"""
def is_valid_coord(x, y, puzzle):
	dimension = len(puzzle)
	if x < 0 or x >= dimension or y < 0 or y >= dimension:
		return False
	else:
		return True

"""
Checks if any row is half filled with one number.
If true, modifies those rows.
Returns puzzle.
"""
def row_check(puzzle):
	dimension = len(puzzle)
	for row_index in range(dimension):
		one_count = 0
		zero_count = 0
		for cell in puzzle[row_index]:
			if cell == 1:
				one_count += 1
			elif cell == 0:
				zero_count += 1

		if one_count == dimension/2:
			for column_index in range(dimension):
				if puzzle[row_index][column_index] == -1:
					puzzle[row_index][column_index] = 0
		elif zero_count == dimension/2:
			for column_index in range(dimension):
				if puzzle[row_index][column_index] == -1:
					puzzle[row_index][column_index] = 1
	return puzzle

"""
Checks if any column is half filled with one number.
If true, modifies those columns.
Returns puzzle.
"""

def column_check(puzzle):
	dimension = len(puzzle)
	for column_index in range(dimension):
		one_count = 0
		zero_count = 0
		for row in puzzle:
			cell = row[column_index]
			if cell == 1:
				one_count += 1
			elif cell == 0:
				zero_count += 1

		if one_count == dimension/2:
			for row in puzzle:
				if row[column_index] == -1:
					row[column_index] = 0
		elif zero_count == dimension/2:
			for row in puzzle:
				if row[column_index] == -1:
					row[column_index] = 1
	return puzzle

"""
Prints a puzzle.
"""
def print_puzzle(puzzle):
	try:
		dimension = len(puzzle)
		for x in range(dimension):
				for y in range(dimension):
					if puzzle[x][y] == -1:
						print ".",
					else:
						print puzzle[x][y],
				print ""
		print ""
	except:
		print "Not valid puzzle."

"""
Takuzu Solver.

Reads the board at http://0hh1.com/ with user input, and solves it.

https://www.reddit.com/r/dailyprogrammer/comments/3pwf17/20151023_challenge_237_hard_takuzu_solver/
"""
def main():
	# Get box positions
	raw_input("Position your cursor at the top-left corner of the board and press enter.")
	x1, y1 = win32gui.GetCursorPos()
	raw_input("Position your cursor at the bottom-right corner of the board and press enter.")
	x2, y2 = win32gui.GetCursorPos()
	dim = int(raw_input("Board dimension: "))

	board_im = ImageGrab.grab((x1, y1, x2, y2))

	# Solve the puzzle

	puzzle = read_puzzle(board_im, dim)
	original_puzzle = map(list, puzzle)
	print "Puzzle read."

	t = time.time()
	result = solve_puzzle(puzzle)

	print_puzzle(result)

	print "Time taken:", time.time() - t, "seconds"

	if result == -1:
		print "No solution found."
	else:
		print "Solution found."
		output_puzzle(original_puzzle, result, board_im.size[0], (x1, y1), 0.03)

if __name__ == "__main__":
	main()