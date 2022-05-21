import datetime
import numpy as np

class Vertex:
    def __init__(self, vertex_id, level=-1):
        self.vertex_id = vertex_id
        self.level = level
        
class Edge:
    def __init__(self, edge_from, edge_to, edge_wt):
        self.edge_from = edge_from
        self.edge_to = edge_to
        self.edge_wt = edge_wt
        
class ListNode:
    def __init__(self):
        self.prev = None
        self.next = None
        self.is_head = False
    
    def insert_node(self, node):
        while(not self.is_head):
            self = self.prev
        node.prev = self
        node.next = self.next
        if self.next is None:
            self.next = node
        else:
            self.next.prev = node
            self.next = node
    
    def delete_node(self):
        if self.next is not None:
            self.next.prev = self.prev
            self.prev.next = self.next
        else:
            self.prev.next = None

class VertexToEdgeListNode(ListNode):
    def __init__(self):
        super(VertexToEdgeListNode, self).__init__()
        self.edge = None
        self.belong_to_vertex = None
    
    def set_vertex(self, belong_to_vertex):
        self.belong_to_vertex = belong_to_vertex
        self.is_head = True
    
    def insert_edge(self, edge):
        temp = VertexToEdgeListNode()
        temp.edge = edge
        self.insert_node(temp)
        
class WeightToEdgeListNode(ListNode):
    def __init__(self):
        super(WeightToEdgeListNode, self).__init__()
        self.edge = None
        self.weight = -1
    
    def set_weight(self, weight):
        self.weight = weight
        self.is_head = True
    
    def insert_edge(self, edge):
        temp = WeightToEdgeListNode()
        temp.edge = edge
        self.insert_node(temp)
        
class Graph:
    def __init__(self, img):
        self.img = img.astype(np.int32)
        self.img_height, self.img_width = self.img.shape[0], self.img.shape[1]
        self.vertex_num = self.img_height * self.img_width
        self.create_vertices()
        self.create_adjacent_edges()
        
    def create_adjacent_edges(self):
        print(datetime.datetime.now().strftime('%F %T') + ' Creating graph ...')
        for i in range(self.vertex_num):
            if (i - self.img_width >= 0):
                self.insert_edge(i, i-self.img_width, self.get_weight(i, i-self.img_width))
            if (i % self.img_width < self.img_width-1):
                self.insert_edge(i, i+1, self.get_weight(i, i+1))
            if (i + self.img_width < self.vertex_num):
                self.insert_edge(i, i+self.img_width, self.get_weight(i, i+self.img_width))
            if (i % self.img_width > 0):
                self.insert_edge(i, i-1, self.get_weight(i, i-1))

    def create_vertices(self):
        self.vertex_pool = []
        self.vertex_to_edge = []
        for i in range(self.vertex_num):
            self.vertex_pool.append(Vertex(i))
            self.vertex_to_edge.append(VertexToEdgeListNode())
            self.vertex_to_edge[i].set_vertex(self.vertex_pool[i]) 
    
    def get_weight(self, i, j):
        ax, ay = i // self.img_width, i % self.img_width
        bx, by = j // self.img_width, j % self.img_width
        return np.max(np.abs(self.img[ax, ay] - self.img[bx, by]), axis=-1)
    
    def insert_edge(self, from_vertex_id, to_vertex_id, edge_weight=-1):
        self.vertex_to_edge[from_vertex_id].insert_edge(Edge(from_vertex_id, to_vertex_id, edge_weight))

