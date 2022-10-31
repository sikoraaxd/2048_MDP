import json
from time import sleep
import numpy as np
import sys
import config

class Player:
    def __init__(self):
        self.states = {}

    # Проверка состояния на посещённость
    #
    # Params:
    # state: int - состояние среды
    #
    # Returns -> bool:
    # True - если состояние уже было посещено
    def __is_visited_state(self, state):
        return state in self.states.keys()

    # Добавление состояния в список посещённых
    #
    # Params:
    # state: int - состояние среды
    #
    # Returns -> void
    def __add_new_state(self, state):
        self.states[state] = {
        'solved_V': False,
        'R': 0,
        'V': 0,       
        'actions': {
            0: {
                'Prs': []
            },
            1: {
                'Prs': []
            },
            2: {
                'Prs': []
            },
            3: {
                'Prs': []
            }
        }
    }

    # Выбор следующего действия в среде
    #
    # Returns -> int:
    # Следующее действие - целое число из диапазона [0, 3]
    def __next_action(self):
        return np.random.randint(0, 4)

    # Проверка, является ли состояние терминальным
    # Начисляет награду, если состояние победное
    #
    # Params:
    # environment - среда
    # state: int - состояние среды
    # needed: int - победное значение ячейки
    #
    # Returns -> bool:
    # True - если состояние терминальное
    def __check_terminate_state(self, environment, state, needed):
        is_terminate_state = False

        if environment.max_tile_value == needed:
            self.states[state]['R'] = config.WIN_REWARD
            is_terminate_state = True

        if environment.game_over:
            is_terminate_state = True

        return is_terminate_state

    # Вычисление вероятности перехода в текущее состояние
    #
    # Params:
    # environment - среда
    # value_plus: int - числовое значение среды после действия
    #
    # Returns -> float:
    # Вероятность перехода в текущее состояние
    def __get_state_pr(self, environment, value_plus):
        free_tiles = environment.getFreeTiles() + 1
        probabitily = 1/free_tiles

        if value_plus == 2:
            probabitily *= config.PROB_OF_2
        elif value_plus == 4:
            probabitily *= config.PROB_OF_4
        
        return probabitily

    # Фиксирование вероятности перехода из состояния state
    # в состояние next_state после совершения действия action
    #
    # Params:
    # state: int - состояние среды
    # action: int - действие
    # next_state: int - состояние среды после действия action
    # value_plus: int - числовое значение среды после действия
    # needed: int - победное значение ячейки
    # environment - среда
    #
    # Returns -> void
    def __add_state_action_pr(self, state, action, next_state, value_plus, environment):
        state_action_prs = self.states[state]['actions'][action]['Prs']
        state_pr = self.__get_state_pr(environment, value_plus)

        if [state_pr, next_state] not in state_action_prs:
                state_action_prs.append([state_pr, next_state])

    # Вывод прогресса изучения среды
    #
    # Params:
    # states_count: int - количество найденных состояний
    # bound_of_states: int - нужное количество состояний
    #
    # Returns -> void
    def __progress_bar(self, states_count, bound_of_states):
        persents = (states_count/bound_of_states) * 100
        persents = int(persents)
        if persents % 10 == 0:
            print("Прогресс: " + str(persents) + '%')

    # Изучение среды environment до момента, пока не будет
    # изучено bound_of_states состояний, а также начисление
    # награды за переход в состояние с максимальным значением
    # ячейки, равным needed.
    #
    # Params:
    # environment - среда
    # bound_of_states: int - нужное количество состояний
    # needed: int - победное значение ячейки
    #
    # Returns -> void
    def train(self, environment, bound_of_states, needed):
        states_count = len(self.states.keys())

        while states_count < bound_of_states:
            if states_count == 0:
                environment.init()
            else:
                environment.init(startState = True)
            
            while True:
                state = environment.get_state()
                value = environment.get_value()

                if not self.__is_visited_state(state):
                    self.__add_new_state(state)
                    states_count += 1
                    self.__progress_bar(states_count, bound_of_states)
                
                if self.__check_terminate_state(environment, state, needed):
                    break
                
                action = self.__next_action()
                environment.forward(action)
                next_state = environment.get_state()
                value_plus = environment.get_value() - value

                if next_state == state:
                    continue

                self.__add_state_action_pr(state,
                                        action, 
                                        next_state,
                                        value_plus,
                                        environment)

    # Рекурсивное вычисление ценности состояния
    #
    # Params:
    # state: int - состояние среды
    #
    # Returns -> float:
    # Ценность состояния state
    def __find_state_value(self, state):
        if self.states[state]['solved_V']:
            return self.states[state]['V']

        if self.states[state]['R'] == config.WIN_REWARD:
            self.states[state]['V'] = config.WIN_REWARD
            self.states[state]['solved_V'] = True
            return self.states[state]['V']
        else:
            sum = 0
            for action in range(4):
                prs = self.states[state]['actions'][action]['Prs']
                if prs:
                    for elem in prs:
                        pr = elem[0]
                        next_state = elem[1]
                        vs_plus = self.__find_state_value(next_state)
                        sum += pr * vs_plus
            self.states[state]['V'] = self.states[state]['R'] + config.Y*sum
            self.states[state]['solved_V'] = True
            return self.states[state]['V']

    # Создание стратегии
    #
    # Params:
    # environment - среда
    #
    # Returns -> void
    def create_policy(self, environment):
        self.__find_state_value(environment.start_state)

    # Получение ценности состояния
    #
    # Params:
    # state: int - состояние среды
    #
    # Returns -> float:
    # Ценность состояния
    def get_state_value(self, state):
        return self.states[state]['V']

    # Вычисление следующего действия из состояния state
    # согласно стратегии
    #
    # Params:
    # state: int - состояние среды
    #
    # Returns -> int:
    # Следующее действие 
    def forward(self, state):
        action_values = []

        for action in range(4):
            value = 0
            prs = self.states[state]['actions'][action]['Prs']
            for elem in prs:
                pr = elem[0]
                next_state = elem[1]
                vs_plus = self.states[next_state]['V']
                value += pr * vs_plus
            action_values.append(value)

        return np.argmax(action_values)

    # Сохранение стратегии игрока
    #
    # Params:
    # environment - среда
    #
    # Returns -> void
    def save(self, environment):
        filename = 'policy'
        filename += str(environment.rows) + 'x' + str(environment.rows)
        filename += 'st' + str(len(self.states.keys()))
        filename += 'm' + str(config.NEEDED)
        filename += '.json'

        with open(config.POLICIES_PATH + filename, 'w') as f:
            json.dump(self.states, f)
    
    # Загрузка стратегии игрока из файла filename
    #
    # Params:
    # filename: string - название файла со стратегией
    #
    # Returns -> void
    def load(self, filename):
        with open(config.POLICIES_PATH + filename, 'r') as f:
            self.states = json.load(self.states, f)