
def recurssive_factor(count, containerSize):
    if (count==1):
        return 1
    return (1.0 - ( (count-1)/float(containerSize) )) * recurssive_factor(count-1, containerSize)


class Cont:
    def __init__(self, size):
        self.size = size
        
    def coincide(self, number):
        return recurssive_factor(number, self.size)


if __name__=="__main__":
    sample_space = Cont(365)
    print(sample_space.coincide(23))
