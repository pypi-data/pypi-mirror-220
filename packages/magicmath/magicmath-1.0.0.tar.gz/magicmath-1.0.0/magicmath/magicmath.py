
class Magicmath:
    """This class will do the basic math operations
    You will need to pass a list of numbers
    You can also pass the invert=True argument to the class
    to reverse the list
    You can also call the methods add(), sub(), mul(), div()
    and getgreater()
    The methods will return the result
    You can also call the numberlist attribute to see the numbers
    in the list
    You can also call the invert attribute to see if the numbers
    are reversed or not
    Example:
        listA = [21, 22, 23, 24, 25, 26, 27, 28, 29]
        mynewnumber = Magicmath(listA, invert=True)
        print(mynewnumber.add())
        print(mynewnumber.sub())
        print(mynewnumber.mul())
        print(mynewnumber.div(showerror=True))
        print(mynewnumber.getgreater())
        print(mynewnumber.numberlist)
        print(mynewnumber.invert)
        print(mynewnumber.div(showerror=True))
        print(mynewnumber.getgreater())
    """
    def __init__(self, numberlist:list, invert:bool=False):
        self.numberlist = numberlist
        self.invert = invert
        if invert == True:
            self.numberlist.reverse()

    def add(self):
        return sum(self.numberlist)

    def sub(self):
        for n in self.numberlist:
            if n == self.numberlist[0]:
                result = n
            else:
                result -= n
        return result

    def mul(self):
        result = 1
        for n in self.numberlist:
            result *= n
        return result

    def div(self, showerror=False):
        for n in self.numberlist:
                if n != 0:
                    if n == self.numberlist[0]:
                        result = n
                    else:
                        result /= n
                else:
                    if showerror:
                        raise TypeError("Your list contains 0 and cannot be divided")
                    else:
                        result = 0
        return result

    def getgreater(self):
        return max(self.numberlist)

    def getminor(self):
        return min(self.numberlist)

