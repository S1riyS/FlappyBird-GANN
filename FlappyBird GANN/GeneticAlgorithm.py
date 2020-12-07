import numpy
import random


class GeneticAlgorithm:
    def __init__(
        self,
        bird_count: int,
        mutation_chance: int,
        cross_count: int,
        network,
        input_nodes=3,
        hidden_nodes=4,
        output_nodes=1,
    ):

        self.bird_count = bird_count
        self.mutation_chance = mutation_chance
        self.cross_count = cross_count
        self.network = network
        self.inodes = input_nodes
        self.hnodes = hidden_nodes
        self.onodes = output_nodes

    def cross(self, father, mother):
        father, mother = sorted((father, mother), key=lambda x: x[0], reverse=True)
        father_NN = self.network[father[1]]
        mother_NN = self.network[mother[1]]
        child = []

        father_wih = father_NN.wih.flatten()
        father_who = father_NN.who.flatten()

        mother_wih = mother_NN.wih.flatten()
        mother_who = mother_NN.who.flatten()

        father_fit, mother_fit = father[0], mother[0]
        domination_value = max(abs(father_fit // max(1, mother_fit)), 2)

        print(f'Father: fit - {father_fit}, index - {father[1] + 1}; Mother: fit - {mother_fit}, index - {mother[1] + 1}, Domination - {domination_value}')

        father = numpy.concatenate([father_wih, father_who])
        mother = numpy.concatenate([mother_wih, mother_who])

        for i in range(len(father)):
            if i % domination_value == 0:
                chromosome = mother[i]
            else:
                chromosome = father[i]

            # Мутация гена
            if random.uniform(1, 100) < self.mutation_chance:
                chromosome += random.uniform(-0.5, 0.5)
            child.append(chromosome)

        return (
            numpy.array(child[:self.inodes * self.hnodes]).reshape(
                (self.hnodes, self.inodes)
            ),
            numpy.array(child[self.inodes * self.hnodes:]).reshape(
                (self.onodes, self.hnodes)
            )
        )

    @staticmethod
    def save_weights(folder, wih, who):
        numpy.save(f"Birds/Bird{folder}/Input_hidden", wih)
        numpy.save(f"Birds/Bird{folder}/Hidden_out", who)

    def new_generation(self, results):
        children = []
        for index, bird in enumerate(results):
            self.save_weights(
                folder=index + 1,
                wih=self.network[bird[1]].wih,
                who=self.network[bird[1]].who,
            )
        best_birds = sorted(results, key=lambda x: x[0], reverse=True)[:self.bird_count // 2]
        # Скрещивание лучшей пары
        best_couple = self.cross(best_birds[-1], best_birds[-2])
        children.append(best_couple)
        # Случайные скрещивания
        for i in range(self.cross_count - 1):
            father = random.choice(best_birds)
            mother = random.choice(best_birds)
            while father[1] == mother[1]:
                father = random.choice(best_birds)
                mother = random.choice(best_birds)

            couple = self.cross(father, mother)
            children.append(couple)
        # Сохранение результатов скрещивания
        for index, bird in enumerate(children):
            input_hidden, hidden_output = bird
            self.save_weights(folder=index + 1, wih=input_hidden, who=hidden_output)
        # Выбор случайных птиц и сохранение их весов
        for index in range(self.cross_count + 1, self.bird_count):
            bird = random.choice(best_birds)
            current_network = self.network[bird[1]]
            input_hidden, hidden_output = current_network.wih, current_network.who
            self.save_weights(folder=index + 1, wih=input_hidden, who=hidden_output)
