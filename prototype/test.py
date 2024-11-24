class test:
    def __init__(self, test_value="test"):
        self.test = test_value

    def __str__(self):
        return self.test

    def __eq__(self, other):
        if isinstance(other, test):
            return self.test == other.test
        return False

    @staticmethod
    def is_type_in_list(lst):
        return any(isinstance(item, test) for item in lst)

l = [test(1), test(2), test(3)]

print(test.is_type_in_list(l))  # This will now print True