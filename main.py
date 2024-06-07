import collections
import pygame
import pygame_gui
import sys


solution_path = []


def get_neighbouring_states(x):
    # x is a string of length 9
    # returns a list of strings of length 9
    # each string is a neighbouring state of x
    # a neighbouring state is a state that can be reached by moving the empty tile left, right, up, or down
    # if the empty tile is at a corner, it can only be moved in two directions
    # if the empty tile is at an edge, it can only be moved in three directions
    # if the empty tile is in the middle, it can be moved in all four directions
    empty_tile_pos = x.index("x")
    neighbour_states = []
    if empty_tile_pos % 3 != 0:
        left_state = x[:empty_tile_pos-1] + "x" + x[empty_tile_pos-1] + x[empty_tile_pos+1:]
        neighbour_states.append(left_state)
    if empty_tile_pos % 3 != 2:
        right_state = x[:empty_tile_pos] + x[empty_tile_pos+1] + "x" + x[empty_tile_pos+2:]
        neighbour_states.append(right_state)
    if empty_tile_pos // 3 != 0:
        up_state = x[:empty_tile_pos-3] + "x" + x[empty_tile_pos-2:empty_tile_pos] + x[empty_tile_pos-3] + x[empty_tile_pos+1:]
        neighbour_states.append(up_state)
    if empty_tile_pos // 3 != 2:
        down_state = x[:empty_tile_pos] + x[empty_tile_pos+3] + x[empty_tile_pos+1:empty_tile_pos+3] + "x" + x[empty_tile_pos+4:]
        neighbour_states.append(down_state)

    return neighbour_states

def pretty_print(x, y=None):
    if y is None:
        for i in range(3):
            print(x[i*3:i*3+3])
        print()
    else:
        for i in range(3):
            print(x[i*3:i*3+3], end="   ")
            print(y[i*3:i*3+3])
        print()


#if __name__ == "__main__":
#    curr_state = input()
#    #for i in get_neighbouring_states(curr_state):
#    #    pretty_print(curr_state, i)
#    desired_state = "12345678x"
#
#    # BFS
#    queue = collections.deque([curr_state])
#    visited = set()
#    parent = {}
#    while queue:
#        state = queue.popleft()
#        if state == desired_state:
#            break
#        for neighbour in get_neighbouring_states(state):
#            if neighbour not in visited:
#                visited.add(neighbour)
#                queue.append(neighbour)
#                parent[neighbour] = state
#
#    path = []
#    while state != curr_state:
#        path.append(state)
#        state = parent[state]
#    path.append(curr_state)
#    path.reverse()
#    for i in path:
#        pretty_print(i)
#
#    print("Number of steps:", len(path)-1)
# Define some constants
TILE_SIZE = 100
GRID_SIZE = 3
WINDOW_SIZE = TILE_SIZE * GRID_SIZE
WINDOW_HEIGHT = WINDOW_SIZE + 50
# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
# Create the window
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_HEIGHT))
manager = pygame_gui.UIManager((WINDOW_SIZE, WINDOW_HEIGHT))

# Create the Enter State button
enter_state_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, WINDOW_SIZE), (100, 50)), text='Enter State', manager=manager)
solve_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, WINDOW_SIZE), (100, 50)), text='Solve', manager=manager)
# Create a panel and a text entry box for the dialog
dialog_panel = pygame_gui.elements.UIPanel(pygame.Rect((100, 100), (200, 200)), manager=manager)
text_entry = pygame_gui.elements.UITextEntryLine(pygame.Rect((0, 0), (200, 50)), manager=manager, container=dialog_panel)
dialog_panel.hide()

grid = "12345678x"

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            tile = grid[GRID_SIZE*y + x]
            if tile != "x":
                pygame.draw.rect(window, (255, 255, 255), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                font = pygame.font.Font(None, 36)
                text = font.render(str(tile), 1, (10, 10, 10))
                window.blit(text, (x * TILE_SIZE + TILE_SIZE / 2 - text.get_width() / 2, y * TILE_SIZE + TILE_SIZE / 2 - text.get_height() / 2))

def swap_empty_tile(x, y):
    global grid
    empty_y, empty_x = divmod(grid.index("x"), GRID_SIZE)
    # Check if the clicked tile is next to the empty tile
    if (abs(empty_x - x) == 1 and empty_y == y) or (abs(empty_y - y) == 1 and empty_x == x):
        # Swap the empty tile with the clicked tile
        grid = list(grid)
        grid[GRID_SIZE*empty_y + empty_x], grid[GRID_SIZE*y + x] = grid[GRID_SIZE*y + x], grid[GRID_SIZE*empty_y + empty_x]
        grid = "".join(grid)

# Game loop
while True:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == enter_state_button:
                    # Show the dialog panel
                    dialog_panel.show()
                elif event.ui_element == solve_button:
                    # Run the BFS algorithm
                    curr_state = grid
                    desired_state = "12345678x"
                    queue = collections.deque([curr_state])
                    visited = set()
                    parent = {}
                    while queue:
                        state = queue.popleft()
                        if state == desired_state:
                            break
                        for neighbour in get_neighbouring_states(state):
                            if neighbour not in visited:
                                visited.add(neighbour)
                                queue.append(neighbour)
                                parent[neighbour] = state
                                
                    path = []
                    while state != curr_state:
                        path.append(state)
                        state = parent[state]
                    path.append(curr_state)
                    path.reverse()
                    if desired_state in path:
                        solution_path = path
                    else:
                        # Create a font object
                        font = pygame.font.Font(None, 36)

                        # Create a Surface with the error message
                        text_surface = font.render("Error: Unsolvable!", True, (255, 0, 0))

                        # Blit the Surface onto the screen at the position (10, 10)
                        window.blit(text_surface, (10, 10))

                        # Update the display
                        pygame.display.flip()

                        # Wait for two seconds
                        pygame.time.wait(2000)
            elif event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == text_entry:
                    # Set the state to the entered string
                    grid = event.text
                    # Convert the string to a 2D array and update the grid
                    # Hide the dialog panel
                    dialog_panel.hide()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Adjust the mouse click coordinates
            tile_x, tile_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
            if 0 <= tile_x < GRID_SIZE and 0 <= tile_y < GRID_SIZE:
                swap_empty_tile(tile_x, tile_y)

        manager.process_events(event)

    if solution_path:
        grid = solution_path.pop(0)

    window.fill((0, 0, 0))
    draw_grid()
    manager.update(time_delta)
    manager.draw_ui(window)
    pygame.display.flip()

    if solution_path:
        pygame.time.wait(300)  # Wait for 500 milliseconds