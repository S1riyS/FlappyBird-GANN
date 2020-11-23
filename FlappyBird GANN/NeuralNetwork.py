import numpy
import scipy.special
import random


class NeuralNetwork:
    # Инициализируем нейросеть
    def __init__(
        self,
        input_nodes: int,
        hidden_nodes: int,
        output_nodes: int,
        directory: int,
        is_random_generated: bool,
    ):
        # Устанавливаем количествой нейронов на всех слоях
        self.inodes = input_nodes
        self.hnodes = hidden_nodes
        self.onodes = output_nodes
        self.directory = directory
        self.is_random_generated = is_random_generated

        if self.is_random_generated:
            self.wih = numpy.random.normal(
                0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes)
            )
            self.who = numpy.random.normal(
                0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes)
            )
            numpy.save(f"Birds/Bird{self.directory}/Hidden_out", self.who)
            numpy.save(f"Birds/Bird{self.directory}/Input_hidden", self.wih)
        else:
            self.who = numpy.load(f"Birds/Bird{self.directory}/Hidden_out.npy")
            self.wih = numpy.load(f"Birds/Bird{self.directory}/Input_hidden.npy")

        # Функция активации
        self.activation_function = lambda x: scipy.special.expit(x)

    # Запрос к нейросети
    def query(self, inputs_list):
        # Конвертация входного массива в 2d массив
        inputs = numpy.array(inputs_list, ndmin=2).T
        # Рассчет значений, которые будут переданы в скрытый слой
        hidden_inputs = numpy.dot(self.wih, inputs)
        # Рассчет значений, которые получатся на выходе из скрытого слоя
        hidden_outputs = self.activation_function(hidden_inputs)
        # Рассчет значений, которые будут переданы в выходной слой
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # рассчет выходных значений
        final_outputs = self.activation_function(final_inputs)
        return final_outputs
