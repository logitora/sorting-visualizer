import pygame
import random
import math
pygame.init()

# set up a class so that it can be imported to other files and easy callback
class drawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = BLACK
    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont("arial", 20)
    LARGE_FONT = pygame.font.SysFont("arial", 30)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        #sets up window in pygame
        self.window = pygame.display.set_mode((width, height))
        #caption for window
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)
    
    # dynamically changes the size of the bars depending on how many bars and the range of the values
    def set_list(self, lst):
        # store list internally
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        # calculate width of bars/blocks
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        # calculate height of bars/block. use math.floor to prevent stacking above the top pad
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        # start drawing blocks at x coord
        self.start_x = self.SIDE_PAD // 2

# drawing the screen by filling w bg color and then drawing the list
def draw(draw_info, sorting_algo_name, ascending):
    # fill w bg color
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # draws what the sorting algo selected is and if it is ascending or descending
    title = draw_info.LARGE_FONT.render(f"{sorting_algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))
    
    # draws the key controls on the screen
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D = Descending | 1 - 15fps | 2 - 30fps | 3 - 60fps | 4 - 120fps", 1, draw_info.WHITE)
    # draw the font in the middle of the screen
    # will draw the font box from top left down to bottom right. x coord will have to be (screen width)/2 - (size of controls text box)/2
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 40))

    # implement more sorting algos 
    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | Q - R-Quick Sort | M - Merge Sort", 1, draw_info.WHITE)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 70))

    draw_list(draw_info)
    pygame.display.update()

# draw the list
def draw_list(draw_info, color_positions={}, clear_bg=False):
    # need to consider the height of the element, x coord of it, and the colors of the bars
    lst = draw_info.lst

    # clears a portion of the screen below the static controls text.
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        # calc x and y coord for top left hand corner of bar. drawn down and to the right
        x = draw_info.start_x + i * draw_info.block_width
        # min is represented as height of 0 or 1. subtract min val from val to get the proportionality
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        # draw onto screen
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    
    if clear_bg:
        pygame.display.update()

# generate the starting list function
def generate_starting_list(n, min_val, max_val):
    lst = []
    
    for _ in range(n):
        val = random.randint(min_val, max_val) # inclusively!
        lst.append(val)

    return lst

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1 = lst[j]
            num2 = lst[j+1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                # generator. pauses execution half way but stores current state of function until the generator is called again. doing this will allow us to 
                # control the app while it is being sorted. Without it, we would have to sit and wait for the sorting to finish before being able to do anything
                yield True
    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i>0 and lst[i-1] > current and ascending
            descending_sort = i>0 and lst[i-1] < current and not ascending
            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i-1]
            i = i-1
            lst[i] = current
            draw_list(draw_info, {i-1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True
    return lst

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)):
        minimum = i
        for j in range(i+1, len(lst)):
            if (lst[minimum] > lst[j] and ascending) or (lst[minimum] < lst[j] and not ascending):
                minimum = j
            draw_list(draw_info, {minimum: draw_info.GREEN, j: draw_info.RED}, True)
            yield True            
        lst[i], lst[minimum] = lst[minimum], lst[i]
    return lst

def partition(lst, beg, end, pivot, draw_info, ascending):
    lst[end], lst[pivot] = lst[pivot], lst[end]
    new_piv = beg-1
    for i in range(beg, end):
        if (lst[i] < lst[end] and ascending) or (lst[i] > lst[end] and not ascending):
            new_piv += 1
            lst[new_piv], lst[i] = lst[i], lst[new_piv]
            draw_list(draw_info, {new_piv: draw_info.GREEN, i: draw_info.RED}, True)

    lst[new_piv+1], lst[end] = lst[end], lst[new_piv+1]
    return (new_piv+1)
def quick_sort(lst, beg, end, draw_info, ascending):
    if beg < end:
        pivot = random.randint(beg, end)
        lst[end], lst[pivot] = lst[pivot], lst[end]

        p = partition(lst, beg, end, pivot, draw_info, ascending)
        quick_sort(lst, beg, p-1, draw_info, ascending)
        quick_sort(lst, p+1, end, draw_info, ascending)
def qs_start(draw_info, ascending=True):
    lst = draw_info.lst
    quick_sort(lst, 0, len(lst)-1, draw_info, ascending)
    yield True
    return lst

def merge_sort(lst, draw_info, ascending):
    if len(lst) > 1:
        mid = len(lst) // 2
        left = lst[:mid]
        right = lst[mid:]

        merge_sort(left, draw_info, ascending)
        merge_sort(right, draw_info, ascending)
        i = j = k = 0

        while i < len(left) and j < len(right):
            if (left[i] <= right[j] and ascending) or (left[i] > right[j] and not ascending):
                lst[k] = left[i]
                i += 1
            else:
                lst[k] = right[j]
                j += 1
            draw_list(draw_info, {k: draw_info.GREEN, i: draw_info.RED, j: draw_info.RED}, True)
            yield True
            k += 1
        while i < len(left):
            lst[k] = left[i]
            i += 1
            k += 1
def ms_start(draw_info, ascending=True):
    lst = draw_info.lst
    merge_sort(lst, draw_info, ascending=True)

# render screen and interactable buttons and then start drawing the list
def main():
    run = True
    clock = pygame.time.Clock()

    n = 250
    min_val = 0
    max_val = 150

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = drawInformation(1200, 700, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "O(n^2) Bubble Sort"
    sorting_algorithm_generator = None
    fps = 60

    # while loop must run as long as the program is up. without this, the program would just prematurely end 
    while run:
        # 60fps -- loop can only run 60 times/sec
        clock.tick(fps)

        # if generator reaches the end, set sorting to false
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            # adding ability to actually quit the program
            if event.type == pygame.QUIT:
                run = False
            # event listener for "r" key to reset the list
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                # draw_info has the lst stored, so we have to pass in the new updated lst into it again
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                # takes generator object
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "O(n^2) Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "O(n^2) Bubble Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "O(n^2) Selection Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = qs_start
                sorting_algo_name = "O(nlogn) R-Quick Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = qs_start
                sorting_algo_name = "O(nlogn) Merge Sort"
            elif event.key == pygame.K_1 and not sorting:
                fps = 15
            elif event.key == pygame.K_2 and not sorting:
                fps = 30
            elif event.key == pygame.K_3 and not sorting:
                fps = 60
            elif event.key == pygame.K_4 and not sorting:
                fps = 120
                   
    pygame.quit()

if __name__ == "__main__":
    main()