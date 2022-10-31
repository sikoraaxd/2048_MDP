import numpy as np


class Game2048:

    # Конструктор игры 2048
    #
    # Params:
    # rows: int - количество строк на игровом поле
    # cols: int - количество столбцов на игровом поле.
    # Необязательный параметр, если не задан, то
    # cols = rows
    def __init__(self, rows, cols=None):
        self.rows = rows
        self.max_tile_value = 2
        self.cols = rows if cols is None else cols
        self.game = []
        self.start_state = None
        self.game_over = False

    # Заполнение поля начальными данными
    #
    # Params:
    # startState: bool - если True, то заполняет игровое поле 
    # данными из состояния S0
    #
    # Returns -> void
    def __fill_tiles(self, start_state):
        list_state = None
        if start_state:
            list_state = [int(num) for num in str(self.start_state)]
        
        for i in range(self.rows):
            row = []
            for j in range(self.rows):
                if start_state:
                    row.append(0 if list_state[j+i*self.rows] == 9 else list_state[j+i*self.rows])
                else:
                    row.append(0)
            self.game.append(row)

    # Игровой ход влево
    #
    # Returns -> void
    def __switch_left(self):
        for i in range(self.rows):
            j = 0
            while j < self.cols:
                if j != 0:
                    if self.game[i][j] != 0 and self.game[i][j-1] == self.game[i][j]:
                        self.game[i][j-1] += self.game[i][j]
                        self.game[i][j] = 0
                        continue
                    if self.game[i][j] != 0 and self.game[i][j-1] == 0:
                        self.game[i][j-1] = self.game[i][j]
                        self.game[i][j] = 0
                        j -= 1
                        continue
                j += 1

    # Игровой ход вправо
    #
    # Returns -> void
    def __switch_right(self):
        for i in range(self.rows):
            j = self.cols - 1
            while j >= 0:
                if j != self.cols - 1:
                    if self.game[i][j] != 0 and self.game[i][j+1] == self.game[i][j]:
                        self.game[i][j+1] += self.game[i][j]
                        self.game[i][j] = 0
                        continue
                    if self.game[i][j] != 0 and self.game[i][j+1] == 0:
                        self.game[i][j+1] = self.game[i][j]
                        self.game[i][j] = 0
                        j += 1
                        continue
                j -= 1

    # Игровой ход вниз
    #
    # Returns -> void
    def __switch_down(self):
        for j in range(self.cols):
            i = self.rows - 1
            while i >= 0:
                if i != self.rows - 1:
                    if self.game[i][j] != 0 and self.game[i+1][j] == self.game[i][j]:
                        self.game[i+1][j] += self.game[i][j]
                        self.game[i][j] = 0
                        continue
                    if self.game[i][j] != 0 and self.game[i+1][j] == 0:
                        self.game[i+1][j] = self.game[i][j]
                        self.game[i][j] = 0
                        i += 1
                        continue
                i -= 1

    # Игровой ход вверх
    #
    # Returns -> void
    def __switch_up(self):
        for j in range(self.cols):
            i = 0
            while i < self.rows:
                if i != 0:
                    if self.game[i][j] != 0 and self.game[i-1][j] == self.game[i][j]:
                        self.game[i-1][j] += self.game[i][j]
                        self.game[i][j] = 0
                        continue
                    if self.game[i][j] != 0 and self.game[i-1][j] == 0:
                        self.game[i-1][j] = self.game[i][j]
                        self.game[i][j] = 0
                        i -= 1
                        continue
                i += 1

    # Добавление новой ячейки на игровое поле
    #
    # Returns -> void
    def __add_elem(self):
        row = np.random.randint(0, self.rows)
        col = np.random.randint(0, self.cols)

        while self.game[row][col] != 0:
            row = np.random.randint(0, self.rows)
            col = np.random.randint(0, self.cols)

        if np.random.rand() <= 0.1:
            self.game[row][col] = 4
        else:
            self.game[row][col] = 2

    # Проверка на наличие свободных ячеек на игровом поле
    #
    # Returns -> bool:
    # True - если есть свободные ячейки
    def __is_enaugh_place(self):
        for i in range(self.rows):
            if 0 in self.game[i]:
                return True
        return False

    # Проверка на окончание игры
    #
    # Returns -> bool:
    # True - если игра окончена
    def __is_game_over(self):
        if self.__is_enaugh_place():
            return False

        for i in range(self.rows-1):
            for j in range(self.cols):
                if self.game[i][j] == self.game[i+1][j]:
                    return False

        for i in range(self.rows):
            for j in range(self.cols-1):
                if self.game[i][j] == self.game[i][j+1]:
                    return False

        return True

    # Вычисление и возврат максимального значения
    # в ячейках на игровом поле
    #
    # Returns -> int:
    # Максимальное значение ячейки на игровом поле
    def __get_max_tile(self):
        return np.max([num for row in self.game for num in row])

    # Вычисление хеша игры
    #
    # Returns -> int:
    # Хеш игры - последовательность чисел в ячейках от левой верхней
    # до правой нижней. Если ячейка свободная, то записывается число 9.
    #
    # Example:
    # Игровое поле - [0, 0]
    #                [16,4]
    # Hash = 99164
    def __hash__(self) -> int:
        return int(''.join([str(x if x > 0 else 9) for row in self.game for x in row]))

    # Перевод игры в начальное состояние
    #
    # Params:
    # startState: bool - если True, то переводит игру
    # в состояние S0
    #
    # Returns -> void
    def init(self, start_state=False):
        self.game = []

        self.__fill_tiles(start_state)

        if not start_state:
            row = np.random.randint(0, self.rows)
            col = np.random.randint(0, self.cols)
            self.game[row][col] = 2
            self.start_state = self.get_state()
        
        self.max_tile_value = self.__get_max_tile()
        self.game_over = self.__is_game_over()

    # Получение состояния игры
    #
    # Returns -> int
    # Состояние игры, то есть её хеша
    def get_state(self):
        return hash(self)

    # Вычисление и возврат числового значения игры
    #
    # Returns -> int:
    # Числовое значение игры, равное сумме всех чисел в ячейках
    def get_value(self):
        return np.sum([num for row in self.game for num in row])

    # Получение количества свободных ячеек на игровом поле
    #
    # Returns -> int:
    # Количество свободных ячеек на игровом поле
    def get_free_tiles(self):
        return [x for row in self.game for x in row].count(0)

    # Совершение игрового действия
    #
    # Params:
    # action: int - игровое действие:  
    #   0 - Влево
    #   1 - Вверх
    #   2 - Вправо
    #   3 - Вниз
    #
    # Returns -> void
    def forward(self, action):
        if action == 0:
            self.__switch_left()
        elif action == 1:
            self.__switch_up()
        elif action == 2:
            self.__switch_right()
        else:
            self.__switch_down()

        self.max_tile_value = self.__get_max_tile()

        if self.__is_game_over():
            self.game_over = True

        if self.__is_enaugh_place():
            self.__add_elem()
            