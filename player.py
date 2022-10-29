import json
from time import sleep
import numpy as np
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
    def __isVisitedState(self, state):
        return state in self.states.keys()

    # Добавление состояния в список посещённых
    #
    # Params:
    # state: int - состояние среды
    #
    # Returns -> void
    def __addNewState(self, state):
        self.states[state] = {
        'SolvedV': False,
        'R': 0,
        'V': 0,       
        'Actions': {
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
    def __nextAction(self):
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
    def __checkTerminateState(self, environment, state, needed):
        isTerminateState = False

        if environment.maxTileValue == needed:
            self.states[state]['R'] = config.WIN_REWARD
            isTerminateState = True

        if environment.game_over:
            isTerminateState = True

        return isTerminateState

    # Вычисление вероятности перехода в текущее состояние
    #
    # Params:
    # environment - среда
    # valuePlus: int - числовое значение среды после действия
    #
    # Returns -> float:
    # Вероятность перехода в текущее состояние
    def __getStatePr(self, environment, valuePlus):
        freeTiles = environment.getFreeTiles() + 1
        probabitily = 1/(freeTiles)

        if valuePlus == 2:
            probabitily *= config.PROB_OF_2
        elif valuePlus == 4:
            probabitily *= config.PROB_OF_4
        
        return probabitily

    # Фиксирование вероятности перехода из состояния state
    # в состояние nextState после совершения действия action
    #
    # Params:
    # state: int - состояние среды
    # action: int - действие
    # nextState: int - состояние среды после действия action
    # valuePlus: int - числовое значение среды после действия
    # needed: int - победное значение ячейки
    # environment - среда
    #
    # Returns -> void
    def __addStateActionPr(self, state, action, nextState, valuePlus, environment):
        stateActionPrs = self.states[state]['Actions'][action]['Prs']
        statePr = self.__getStatePr(environment, valuePlus)

        if [statePr, nextState] not in stateActionPrs:
                stateActionPrs.append([statePr, nextState])

    # Вывод прогресса изучения среды
    #
    # Params:
    # statesCount: int - количество найденных состояний
    # boundOfStates: int - нужное количество состояний
    #
    # Returns -> void
    def __progressBar(self, statesCount, boundOfStates):
        persents = (statesCount/boundOfStates) * 100
        persents = int(persents)
        if persents % 10 == 0:
            print("Прогресс: " + str(persents) + '%')

    # Изучение среды environment до момента, пока не будет
    # изучено boundOfStates состояний, а также начисление
    # награды за переход в состояние с максимальным значением
    # ячейки, равным needed.
    #
    # Params:
    # environment - среда
    # boundOfStates: int - нужное количество состояний
    # needed: int - победное значение ячейки
    #
    # Returns -> void
    def train(self, environment, boundOfStates, needed):
        statesCount = len(self.states.keys())

        while statesCount < boundOfStates:
            if statesCount == 0:
                environment.init()
            else:
                environment.init(startState = True)
            
            while True:
                state = environment.getState()
                value = environment.getValue()

                if not self.__isVisitedState(state):
                    self.__addNewState(state)
                    statesCount += 1
                    self.__progressBar(statesCount, boundOfStates)
                
                if self.__checkTerminateState(environment, state, needed) == True:
                    break
                
                action = self.__nextAction()
                environment.forward(action)
                nextState = environment.getState()
                valuePlus = environment.getValue() - value

                if nextState == state:
                    continue

                self.__addStateActionPr(state, 
                                        action, 
                                        nextState, 
                                        valuePlus, 
                                        environment)

    # Рекурсивное вычисление ценности состояния
    #
    # Params:
    # state: int - состояние среды
    #
    # Returns -> float:
    # Ценность состояния state
    def __findStateValue(self, state):
        if self.states[state]['SolvedV']:
            return self.states[state]['V']

        if self.states[state]['R'] == config.WIN_REWARD:
            self.states[state]['V'] = config.WIN_REWARD
            self.states[state]['SolvedV'] = True
            return self.states[state]['V']
        else:
            sum = 0
            for action in range(4):
                prs = self.states[state]['Actions'][action]['Prs']
                if prs != []:
                    for elem in prs:
                        pr = elem[0]
                        nextState = elem[1]
                        Vsplus = self.__findStateValue(nextState)
                        sum += pr * Vsplus
            self.states[state]['V'] = self.states[state]['R'] + config.Y*sum
            self.states[state]['SolvedV'] = True
            return self.states[state]['V']

    # Создание стратегии
    #
    # Params:
    # environment - среда
    #
    # Returns -> void
    def createPolicy(self, environment):
        self.__findStateValue(environment.startState)

    # Получение ценности состояния
    #
    # Params:
    # state: int - состояние среды
    #
    # Returns -> float:
    # Ценность состояния
    def getStateValue(self, state):
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
        actionValues = []

        for action in range(4):
            value = 0
            prs = self.states[state]['Actions'][action]['Prs']
            for elem in prs:
                pr = elem[0]
                nextState = elem[1]
                Vsplus = self.states[nextState]['V']
                value += pr * Vsplus
            actionValues.append(value)

        return np.argmax(actionValues)

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