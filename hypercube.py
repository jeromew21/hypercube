def flip(bit):
    return 1 if bit == 0 else 0

class Hypercube:
    def __init__(self, n):
        self.nodes = []
        self._hash = {}
        if n == 1:
            self.nodes = [Node([0], self), Node([1], self)]
        else:
            cube1 = Hypercube(n - 1)
            cube2 = Hypercube(n - 1)
            cube1.pad_all(0)
            cube2.pad_all(1)
            self.nodes = cube1.nodes + cube2.nodes
        for node in self.nodes:
            node.hypercube = self
            self._hash[node.string_rep] = node
    
    def get_node_by_hash(self, h):
        if h not in self._hash:
            print(f"Invalid hash '{h}'")
            raise Exception()
        return self._hash[h]

    def pad_all(self, bit):
        for node in self.nodes:
            node.pad(bit)
    
class Node:
    def __init__(self, binary, hypercube):
        self.binary = binary
        self.hypercube = hypercube

    @property
    def string_rep(self):   
        return "".join([str(i) for i in self.binary])
    
    def pad(self, bit):
        self.binary.insert(0, bit)

    def calc_neighbors(self):
        def yield_them():
            for index in range(len(self.binary)):
                k = [i for i in self.binary]
                k[index] = flip(k[index])
                string_rep = "".join(str(m) for m in k)
                yield self.hypercube.get_node_by_hash(string_rep)
        return list(yield_them())
    
    def __repr__(self):
        return f"Node<{self.string_rep}>"
