import numpy as np
import matplotlib.pyplot as plt

SORTEDCHARS = """ `.-_',~:*;!"^/\+><r=?()|7LxtcYivTljsz[]1Jnufy{}oI#FC4VX2ehk3aZw5ASbdpqUP6%9G8mKO&0EDHg$MWRNQB@"""

class Dist:
    def __init__(self, chars, unique=True, order=False) -> None:
        if unique:
            self.chars = []
            for char in chars:
                if char not in self.chars:
                    self.chars.append(char)
        else:
            self.chars = list(chars)
        if order:
            chars = []
            for char in SORTEDCHARS:
                while char in self.chars:
                    chars.append(char)
                    self.chars.remove(char)
            self.chars = chars
        self.cmap = plt.get_cmap("tab20")
        self.y = lambda x: x
        self.char_dict = {}

    def check_ele(self, list):
        if len(list) != 1 + len(self.chars):
            raise ValueError(f"{1 + len(self.chars)} number of elements expected in the list.")

    def normal_to_hex(self):
        self.check_ele(self.list)
        self.list[0], self.list[-1] = 0, 1
        self.list = 255*self.list
        self.list = self.list.astype(int)

    def hex_to_normal(self):
        self.check_ele(self.list)
        self.list = self.list/255
        self.list[0], self.list[-1] = 0, 1

    def generate_char_dict(self):
        self.check_ele(self.list)
        j = 1
        for i in range(256):
            self.char_dict[i] = self.chars[j-1]
            if not i<self.list[j]:
                j += 1
    def show(self):
        self.hex_to_normal()
        x = np.arange(0, 1.001, 0.001)
        y = self.y(x)
        plt.plot(x,y)
        # plt.fill_between(x, y, np.max(y), facecolor='red', alpha=0.5)
        colors = [self.cmap(i) for i in range(len(self.chars))] 
        for i in range(len(self.list)-1):
            a = int(self.list[i]/0.001)
            b = int(self.list[i+1]/0.001)
            np.array([y[a]])
            np.array([y[b]])
            np.array([0])
            X = np.concatenate((np.array([0]), x[a:b], np.array([0]), np.array([0])))
            Y = np.concatenate((np.array([y[a]]), y[a:b], np.array([y[b]]), np.array([y[50]])))
            plt.fill_between(X, Y, facecolor=colors[i], alpha=0.3)
            plt.fill_between(x[a:b], y[a:b], facecolor=colors[i], alpha=0.3)
        for i, color in enumerate(colors[::-1]):
            plt.plot([2], [0], marker='o', markersize=10, color=color, alpha=0.3, label=self.chars[-(i+1)]+f": {self.list[-(i+2)]:.2f}-{self.list[-(i+1)]:.2f}")
        plt.legend(fontsize=8)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.show()
        self.normal_to_hex()


class Linear(Dist):
    def __init__(self, chars, unique=True, order=False) -> None:
        super().__init__(chars, unique, order)
        num = 255/len(self.chars)
        self.list = [0]
        for i in range(len(self.chars)):
            j = int(num * (i + 1))
            self.list.append(j)
        self.list[-1] = 255
        self.list = np.array(self.list)
        self.generate_char_dict()

class Exponential(Linear):
    def __init__(self, chars, power, unique=True, order=False) -> None:
        super().__init__(chars, unique, order)
        self.hex_to_normal()
        self.list = self.list**power
        self.normal_to_hex()
        self.y = lambda x: x**power
        self.generate_char_dict()  
        
class Normal(Linear):
    def __init__(self, chars, mean, var, unique=True, order=False) -> None:
        super().__init__(chars, unique, order)
        self.mean = mean
        self.var = var
        self.hex_to_normal()
        self.list[0], self.list[-1] = 0.0001, 0.9999
        self.list = self.normalizer(self.list)
        self.normal_to_hex()
        self.y = self.normalizer
        self.generate_char_dict()
    
    def normalizer(self, x):
        inv = (x*(1-self.mean))/(self.mean*(1-x))
        inv **= -self.var
        inv += 1
        return inv**(-1)
    
    def show(self):
        self.hex_to_normal()
        x = np.arange(0.001, 0.999, 0.001)
        y = self.y(x)
        plt.plot(x,y)
        # plt.fill_between(x, y, np.max(y), facecolor='red', alpha=0.5)
        colors = [self.cmap(i) for i in range(len(self.chars))]
        for i in range(len(self.list)-1):
            a = int(self.list[i]/0.001)
            b = int(self.list[i+1]/0.001) - 3 # Index error
            np.array([y[a]])
            np.array([y[b]])
            np.array([0])
            X = np.concatenate((np.array([0]), x[a:b], np.array([0]), np.array([0])))
            Y = np.concatenate((np.array([y[a]]), y[a:b], np.array([y[b]]), np.array([y[50]])))
            plt.title("Normal")
            plt.fill_between(X, Y, facecolor=colors[i], alpha=0.3)
            plt.fill_between(x[a:b], y[a:b], facecolor=colors[i], alpha=0.3)
        for i, color in enumerate(colors[::-1]):
            plt.plot([2], [0], marker='o', markersize=10, color=color, alpha=0.3, label=self.chars[-(i+1)]+f": {self.list[-(i+2)]:.2f}-{self.list[-(i+1)]:.2f}")
        plt.legend(fontsize=8)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.show()
        self.normal_to_hex()