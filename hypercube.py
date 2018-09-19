import pygame
from pygame import gfxdraw
import itertools

def flip(bit):
    return 1 if bit == 0 else 0

class HypercubeGenerator:
    def __init__(self, i_x=50, i_y=600):
        self._hash = {}
        self.n = 2
        
        self.nodes = [Node([0], self, i_x, i_y), Node([1], self, i_x, i_y + 250)]
        
        for node in self.nodes:
            node.hypercube = self
            self._hash[node.string_rep] = node
    
    def split(self):
        self._hash = {}
        copies = [node.copy().pad(1) for node in self.nodes]
        self.nodes = [node.pad(0) for node in self.nodes]
        dx = 1
        dy = 0
        if self.n == 3:
            dy = -0.7
            dx = 0.5
        elif self.n == 4:
            dx = 0.8
            dy = -0.4
        elif self.n == 5:
            dx = 0.4
            dy = -0.3
        for node in self.nodes:
            node.set_velo(0, 0)
            self._hash[node.string_rep] = node
        for node in copies:
            node.set_velo(dx, dy)
            self._hash[node.string_rep] = node
        self.nodes.extend(copies)
        self.n += 1
    
    def get_node_by_hash(self, h):
        if h not in self._hash:
            print(f"Invalid hash '{h}'")
            print(self._hash)
            raise Exception()
        return self._hash[h]
    
    def __repr__(self):
        return f"Hypercube<{self.n}>"
    
class Node:
    count = 0
    registry = []

    def __init__(self, binary, hypercube, x, y):
        Node.count += 1
        Node.registry.append(self)
        self.binary = binary
        self.hypercube = hypercube
        self._x = x
        self._y = y
        self.dx = 0
        self.dy = 0
        self.moving = False
    
    @property
    def x(self):
        return int(self._x)
    
    @property
    def y(self):
        return int(self._y)

    def step(self):
        self._x += self.dx
        self._y += self.dy

    def set_velo(self, x, y):
        self.dx = x
        self.dy = y

    def copy(self):
        return Node([k for k in self.binary], self.hypercube, self._x, self._y)

    @property
    def string_rep(self):   
        return "".join([str(i) for i in self.binary])
    
    def pad(self, bit):
        self.binary.insert(0, bit)
        return self

    def calc_neighbors(self):
        def yield_them():
            for index in range(len(self.binary)):
                k = [i for i in self.binary]
                k[index] = flip(k[index])
                string_rep = "".join(str(m) for m in k)
                yield self.hypercube.get_node_by_hash(string_rep)
        return list(yield_them())
    
    def __repr__(self):
        return f"Node<{self.string_rep}, ({self.x}, {self.y})>"

pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption("hypercube fuckery")

screen = pygame.display.set_mode(
    (1600, 900))
pygame.display.update()

h = HypercubeGenerator()
ticks = 0

white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.SysFont('monospace', 30)

translate_steps = 250
current_step = 0

print(f"Num nodes: {Node.count}")

h.split()

final_dimension = 5

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    screen.fill(white)
    
    for node in h.nodes:
        node.step()
        gfxdraw.aacircle(screen, node.x, node.y, 5, black)
        gfxdraw.filled_circle(screen, node.x, node.y, 5, black)
        label = font.render(node.string_rep, True, black)
        screen.blit(label, (node.x + 10, node.y + 10))


    for node in h.nodes:
        for nb in node.calc_neighbors():
            pygame.draw.lines(screen, black, False, [
                (node.x, node.y),
                (nb.x, nb.y)
            ], 1)

    current_step += 1
    if current_step >= translate_steps:
        if h.n <= final_dimension:
            h.split()
        else:
            for node in h.nodes:
                node.set_velo(0, 0)
        current_step = 0
    

    ticks += 1
    pygame.display.update()
    clock.tick(60)
