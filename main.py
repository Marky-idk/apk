import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, NumericProperty
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.popup import Popup 

kivy.require('2.2.1') 

# --- PUZZLE DATA ---
TUTORIAL_PUZZLE = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

EASY_PUZZLE = [ 
    [5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

MEDIUM_PUZZLE = [ 
    [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 8, 5], [0, 0, 1, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 5, 0, 7, 0, 0, 0], [0, 0, 4, 0, 0, 0, 1, 0, 0], [0, 9, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 4, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

HARD_PUZZLE = [ 
    [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

PUZZLE_MAP = {
    'Tutorial': TUTORIAL_PUZZLE, 'Easy': EASY_PUZZLE, 'Medium': MEDIUM_PUZZLE, 'Hard': HARD_PUZZLE 
}

# -------------------------------------------------------------
# 🚨 KV_CODE - Kivy Design Language String (Single-line color expression for robustness)
# -------------------------------------------------------------
KV_CODE = r"""
# Define global constants for the cozy/modern theme
#:set PRIMARY_COLOR (0.2, 0.7, 0.8, 1)   
#:set BACKGROUND_COLOR (0.15, 0.15, 0.15, 1) 
#:set LIGHT_TEXT_COLOR (0.8, 0.8, 0.8, 1) 
#:set ACCENT_COLOR (0.8, 0.3, 0.3, 1) 
#:set SELECTION_COLOR (0.1, 0.4, 0.5, 1) 
#:set HINT_COLOR (0.9, 0.7, 0.3, 1) 
#:set HILIGHT_COLOR (0.1, 0.3, 0.15, 1) 

<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 20

        canvas.before:
            Color:
                rgba: BACKGROUND_COLOR
            Rectangle:
                pos: self.pos
                size: self.size

        # Title
        Label:
            text: 'SUDOKU:\nMODERN INTERFACE'
            font_size: '40sp'
            color: PRIMARY_COLOR
            size_hint_y: 0.2
            halign: 'center'

        # Rules/Instruction Panel
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.35
            padding: 10
            spacing: 5
            
            canvas.before:
                Color:
                    rgba: (0.2, 0.2, 0.2, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size
            
            Label:
                text: 'WELCOME!'
                color: PRIMARY_COLOR
                font_size: '22sp'
                size_hint_y: None
                height: self.texture_size[1]
                
            Label:
                text: '[b]Rules:[/b] Fill the 9x9 grid so that every row, column, and 3x3 block contains the digits 1-9 exactly once. [color=ff5555]Invalid numbers will be highlighted in red.[/color]'
                color: LIGHT_TEXT_COLOR
                font_size: '14sp'
                size_hint_y: 1
                halign: 'left'
                valign: 'top'
                markup: True
                text_size: self.width, None

        # Difficulty Buttons Layout
        GridLayout:
            cols: 1
            spacing: 10
            size_hint_y: 0.45

            Label:
                text: 'SELECT DIFFICULTY'
                color: LIGHT_TEXT_COLOR
                font_size: '20sp'
                size_hint_y: None
                height: self.texture_size[1]

            Button:
                text: 'TUTORIAL (Easy Focus)' 
                on_release: root.start_game('Tutorial')
                background_color: HINT_COLOR 
                color: BACKGROUND_COLOR
                size_hint_y: None
                height: dp(45)

            Button:
                text: 'EASY (Solvable)'
                on_release: root.start_game('Easy')
                background_color: PRIMARY_COLOR
                color: BACKGROUND_COLOR
                size_hint_y: None
                height: dp(45)

            Button:
                text: 'MEDIUM'
                on_release: root.start_game('Medium')
                background_color: PRIMARY_COLOR
                color: BACKGROUND_COLOR
                size_hint_y: None
                height: dp(45)

            Button:
                text: 'HARD'
                on_release: root.start_game('Hard')
                background_color: PRIMARY_COLOR
                color: BACKGROUND_COLOR
                size_hint_y: None
                height: dp(45)

<GameScreen>:
    name: 'game'
    tutorial_hint: '' 
    
    BoxLayout:
        orientation: 'vertical'

        canvas.before:
            Color:
                rgba: BACKGROUND_COLOR
            Rectangle:
                pos: self.pos
                size: self.size

        # 1. Top Bar/Title & Hint
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.13
            
            Label:
                text: "MODERN SUDOKU"
                size_hint_y: 0.5
                color: LIGHT_TEXT_COLOR
                text_size: self.size
                valign: 'middle'
                halign: 'center'
            
            # Tutorial Hint Label
            Label:
                text: root.tutorial_hint
                size_hint_y: 0.5
                color: HINT_COLOR
                text_size: self.size
                valign: 'top'
                halign: 'center'
                font_size: '14sp'

        # 2. Sudoku Board 
        SudokuBoard:
            id: sudoku_board
            size_hint: 0.9, 0.72 
            pos_hint: {'center_x': 0.5}

        # 3. Input Pad and Controls
        BoxLayout:
            size_hint_y: 0.15
            padding: dp(10)
            spacing: dp(10)

            # Number Pad (1-9)
            GridLayout:
                cols: 5
                rows: 2
                spacing: dp(5)
                size_hint_x: 0.8

                Button:
                    text: '1'
                    on_release: sudoku_board.set_value_of_selected_cell(self.text)
                    background_color: PRIMARY_COLOR
                    color: BACKGROUND_COLOR
                Button:
                    text: '2'
                    on_release: sudoku_board.set_value_of_selected_cell(self.text)
                    background_color: PRIMARY_COLOR
                    color: BACKGROUND_COLOR
                Button:
                    text: '3'
                    on_release: sudoku_board.set_value_of_selected_cell(self.text)
                    background_color: PRIMARY_COLOR
                    color: BACKGROUND_COLOR
                Button:
                    text: '4'
                    on_release: sudoku_board.set_value_of_selected_cell(self.text)
                    background_color: PRIMARY_COLOR
                    color: BACKGROUND_COLOR
                Button:
                    text: '5'
                    on_release: sudoku_board.set_value_of_selected_cell(self.text)
                    background_color: PRIMARY_COLOR
                    color: BACKGROUND_COLOR
                Button:
                    text: '6'
                    on_release: sudoku_board.set_value_of_selected_cell(self.text)
                    background_color: PRIMARY_COLOR
                    color: BACKGROUND_COLOR
                Button:
                    text: '7'
                    on_release: sudoku_board.set_value_of_selected_cell(self.text)
                    background_color: PRIMARY_COLOR
                    color: BACKGROUND_COLOR
                Button:
                    text: '8'
                    on_release: sudoku_board.set_value_of_selected_cell(self.text)
                    background_color: PRIMARY_COLOR
                    color: BACKGROUND_COLOR
                Button:
                    text: '9'
                    on_release: sudoku_board.set_value_of_selected_cell(self.text)
                    background_color: PRIMARY_COLOR
                    color: BACKGROUND_COLOR
                Button:
                    text: 'CLR' 
                    on_release: sudoku_board.set_value_of_selected_cell('')
                    background_color: (0.5, 0.5, 0.5, 1) 
                    color: BACKGROUND_COLOR
            
            # Menu Button & Status
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.2
                spacing: 5
                
                Button:
                    text: '<< MENU'
                    on_release: root.go_to_menu()
                    background_color: (0.3, 0.3, 0.3, 1) 
                    size_hint_y: 0.5

                Label:
                    text: 'Diff: ' + root.difficulty_level
                    color: LIGHT_TEXT_COLOR
                    size_hint_y: 0.5
                    text_size: self.size
                    valign: 'middle'
                    halign: 'center'
                    
<SudokuCell>:
    multiline: False
    input_filter: 'int'
    halign: 'center'
    valign: 'middle'
    write_tab: False
    
    font_size: '24sp'
    background_normal: ''
    
    color: LIGHT_TEXT_COLOR if root.is_fixed else ACCENT_COLOR if root.is_error else PRIMARY_COLOR

    canvas.before:
        Color:
            # THIS LINE HAS BEEN MODIFIED TO BE A SINGLE LINE FOR MAXIMUM PARSING SAFETY.
            rgba: ACCENT_COLOR if root.is_error else SELECTION_COLOR if root.is_selected else HILIGHT_COLOR if root.is_highlighted else (0.3, 0.3, 0.3, 1) if root.is_fixed else BACKGROUND_COLOR
        Rectangle:
            pos: self.pos
            size: self.size

        Color:
            rgba: (0.2, 0.2, 0.2, 1) # Subtle border color
        Line:
            width: 1 
            rectangle: self.x, self.y, self.width, self.height

<SudokuBigBox>:
    cols: 3
    rows: 3
    padding: 1
    canvas.before:
        Color:
            rgba: LIGHT_TEXT_COLOR 
        Line:
            width: 2 
            rectangle: self.x, self.y, self.width, self.height

<SudokuBoard>: 
    cols: 3
    rows: 3
    spacing: 5
    padding: 10
"""

# --- PYTHON LOGIC (Widget and App Classes) ---

class SudokuCell(TextInput):
    """Represents an individual 1x1 cell."""
    is_fixed = BooleanProperty(False)
    is_selected = BooleanProperty(False)
    is_error = BooleanProperty(False)
    is_highlighted = BooleanProperty(False) 
    row = NumericProperty(-1)
    col = NumericProperty(-1)

    def insert_text(self, substring, from_undo=False):
        """Filters input and triggers validation."""
        if self.is_fixed: return 
        if not substring:
            self.text = ''
            self.parent.parent.check_validation()
            return
        if substring.isdigit() and len(substring) == 1 and '1' <= substring <= '9':
            self.text = '' 
            super().insert_text(substring, from_undo=from_undo)
            self.parent.parent.check_validation()
        return

    def on_touch_down(self, touch):
        """Custom handler for selecting a cell."""
        if self.collide_point(*touch.pos):
            self.parent.parent.select_cell(self)
        return super().on_touch_down(touch)


class SudokuBigBox(GridLayout):
    """Holds a single 3x3 block of cells."""
    pass


class SudokuBoard(GridLayout):
    """Holds the 3x3 layout of the Big Boxes (9x9 total grid)."""
    selected_cell = ObjectProperty(None, allownone=True) 
    cells_by_pos = {} 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_board()

    def build_board(self):
        """Constructs the 9x9 grid, assigning explicit coordinates to each cell."""
        self.clear_widgets()
        self.cells_by_pos = {}
        
        for r_big in range(3):
            for c_big in range(3):
                big_box = SudokuBigBox()
                
                for r_small in range(3):
                    for c_small in range(3):
                        
                        r = r_big * 3 + r_small 
                        c = c_big * 3 + c_small 
                        
                        cell = SudokuCell(row=r, col=c) 
                        big_box.add_widget(cell)
                        self.cells_by_pos[(r, c)] = cell 
                        
                self.add_widget(big_box)

    def get_grid_values(self):
        """Retrieves the current state of the board as a 9x9 list of integers using the fixed lookup."""
        grid = [[0] * 9 for _ in range(9)]
        
        for r in range(9):
            for c in range(9):
                cell = self.cells_by_pos[(r, c)]
                grid[r][c] = int(cell.text) if cell.text.isdigit() else 0
        return grid

    def check_validation(self):
        """Main validation function: Checks every cell for conflicts."""
        grid = self.get_grid_values()
        has_empty_cells = False
        has_errors = False
        
        for r in range(9):
            for c in range(9):
                cell = self.cells_by_pos[(r, c)]
                value = grid[r][c]
                
                if value == 0:
                    cell.is_error = False
                    has_empty_cells = True
                    continue
                
                grid[r][c] = 0 
                is_invalid = self.check_conflict(grid, r, c, value)
                grid[r][c] = value
                
                cell.is_error = is_invalid
                if is_invalid:
                    has_errors = True
        
        if not has_empty_cells and not has_errors:
            self.parent.show_win_popup()

        return not has_errors 

    def check_conflict(self, grid, r, c, num):
        """Checks if placing 'num' conflicts with any EXISTING number in the grid."""
        # 1. Check Row and Column
        for i in range(9):
            if grid[r][i] == num or grid[i][c] == num:
                return True
        # 2. Check 3x3 Box
        start_row, start_col = r - r % 3, c - c % 3
        for i in range(3):
            for j in range(3):
                if grid[start_row + i][start_col + j] == num:
                    return True
        return False
    
    def clear_highlights(self):
        """Clears the highlight property from all cells."""
        for cell in self.cells_by_pos.values():
            cell.is_highlighted = False

    def select_cell(self, cell_instance):
        """Manages selection and applies green highlighting to the row/column/box."""
        if self.selected_cell:
            self.selected_cell.is_selected = False
            self.selected_cell.focus = False
        self.clear_highlights()
        
        self.selected_cell = cell_instance
        self.selected_cell.is_selected = True
        self.selected_cell.focus = True
        
        r = cell_instance.row
        c = cell_instance.col
        
        for i in range(9):
            self.cells_by_pos[(r, i)].is_highlighted = True
            self.cells_by_pos[(i, c)].is_highlighted = True
            
        start_row, start_col = r - r % 3, c - c % 3
        for i in range(3):
            for j in range(3):
                box_r = start_row + i
                box_c = start_col + j
                
                cell_to_highlight = self.cells_by_pos[(box_r, box_c)]
                if cell_to_highlight is not cell_instance:
                    cell_to_highlight.is_highlighted = True
        
        Window.release_all_keyboards()

    def set_value_of_selected_cell(self, value):
        """Called by the number pad buttons."""
        if self.selected_cell and not self.selected_cell.is_fixed:
            self.selected_cell.text = value
            self.check_validation() 
            
            if self.selected_cell:
                 self.selected_cell.is_selected = False
                 self.selected_cell = None


class MenuScreen(Screen):
    """The initial screen for selecting difficulty."""
    def start_game(self, difficulty):
        game_screen = self.manager.get_screen('game')
        game_screen.load_new_game(difficulty)
        self.manager.current = 'game'


class GameScreen(Screen):
    """The main screen where the Sudoku board is played."""
    difficulty_level = StringProperty('Easy')
    tutorial_hint = StringProperty('') 

    def load_new_game(self, difficulty):
        self.difficulty_level = difficulty
        
        board = self.ids.sudoku_board
        puzzle_data = PUZZLE_MAP.get(difficulty, EASY_PUZZLE)

        for r in range(9):
            for c in range(9):
                cell = board.cells_by_pos[(r, c)]
                value = puzzle_data[r][c]
                
                cell.text = str(value) if value != 0 else ''
                cell.is_fixed = (value != 0)
                cell.is_error = False 
                cell.is_highlighted = False
                cell.is_selected = False
        
        if difficulty == 'Tutorial':
            self.tutorial_hint = "HINT: Find the only empty cell and remember: each row must have 1-9 once. What is missing? (Answer: 9)"
        else:
            self.tutorial_hint = ""

        board.check_validation()

    def go_to_menu(self):
        self.manager.current = 'menu'
        
    def show_win_popup(self):
        """Creates and displays a 'You Win!' popup."""
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text='🎉 PUZZLE SOLVED! 🎉', font_size='30sp', color=(0.2, 0.7, 0.8, 1)))
        
        close_button = Button(text='Back to Menu', size_hint_y=None, height=dp(45), background_color=(0.2, 0.7, 0.8, 1), color=(0.15, 0.15, 0.15, 1))
        box.add_widget(close_button)
        
        popup = Popup(title='Congratulations!', content=box, size_hint=(0.7, 0.4), auto_dismiss=False)
        close_button.bind(on_release=lambda x: [popup.dismiss(), self.go_to_menu()])
        
        popup.open()


class SudokuApp(App):
    def build(self):
        Window.size = (dp(400), dp(650)) 
        
        # Load the KV string.
        Builder.load_string(KV_CODE)
        
        self.title = 'Modern Sudoku'
        
        sm = ScreenManager()
        sm.add_widget(MenuScreen())
        sm.add_widget(GameScreen())
        return sm

if __name__ == '__main__':
    SudokuApp().run()