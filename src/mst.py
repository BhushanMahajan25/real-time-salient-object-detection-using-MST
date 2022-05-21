import copy
from pickle import FALSE
import numpy as np
import datetime

from graph import *

class MinimumSpanningTree(Graph):
    def __init__(self, img):
        super(MinimumSpanningTree, self).__init__(img)
        self.parent_edge = []
        self.has_chosen = []
        self.weight_bset = []
        self.weight_to_edge = []
        self.child_edge = []
        for i in range(self.vertex_num):
            self.parent_edge.append(Edge(-1, -1, -1))
            self.has_chosen.append(False)
            self.child_edge.append(VertexToEdgeListNode())
            self.child_edge[i].set_vertex(self.vertex_pool[i])
        for i in range(256):
            self.weight_bset.append(False)
            self.weight_to_edge.append(WeightToEdgeListNode())
            self.weight_to_edge[i].set_weight(i)
        self.prims_algorithm()
    
    def expand_front(self, cur_vertex_id):
        self.has_chosen[cur_vertex_id] = True
        cur_edge_list = self.vertex_to_edge[cur_vertex_id]
        while cur_edge_list.next is not None:
            cur_edge_list = cur_edge_list.next
            vertex_id = cur_edge_list.edge.edge_to
            if not self.has_chosen[vertex_id]:
                edge_weight = cur_edge_list.edge.edge_wt
                self.weight_to_edge[edge_weight].insert_edge(cur_edge_list.edge)
                self.weight_bset[edge_weight] = True

    def prims_algorithm(self, root_id=0):
        print(datetime.datetime.now().strftime('%F %T') + ' Prims algorithm ...')
        self.expand_front(root_id)
        while True:
            if True in self.weight_bset:
                firstOne = self.weight_bset.index(True)
                pListNode = self.weight_to_edge[firstOne].next
            else:
                break
            to_vertex_id = pListNode.edge.edge_to
            if not self.has_chosen[to_vertex_id]:
                from_vertex_id = pListNode.edge.edge_from
                self.child_edge[from_vertex_id].insert_edge(pListNode.edge)
                self.parent_edge[to_vertex_id] = pListNode.edge
                self.weight_to_edge[firstOne].next.delete_node()
                self.expand_front(to_vertex_id)
            else:
                self.weight_to_edge[firstOne].next.delete_node()
            if self.weight_to_edge[firstOne].next is None:
                self.weight_bset[firstOne] = False


class MinBarrierDistMST(MinimumSpanningTree):
    def __init__(self, img):
        super(MinBarrierDistMST, self).__init__(img)
        self.has_visited = []
        self.inque = []
        self.min_barrier_dist = []
        self.is_seed = []
        self.vertex_value = copy.deepcopy(self.img).reshape(-1, 3)
        self.max_value_along_path = copy.deepcopy(self.vertex_value)
        self.min_value_along_path = copy.deepcopy(self.vertex_value)  
        for i in range(self.vertex_num):
            self.has_visited.append(False)
            self.inque.append(False)
            self.min_barrier_dist.append(-1)
            self.is_seed.append(False)
        
    def computer_level(self, root_id=0):
        que = [root_id]
        while que:
            u_id = que[-1]
            que.pop()
            pListNode = self.child_edge[u_id]
            while pListNode.next is not None:
                v_id = pListNode.next.edge.edge_to
                if not self.has_visited[v_id]:
                    self.vertex_pool[v_id].level = self.vertex_pool[u_id].level + 1
                    self.has_visited[v_id] = True
                    que.insert(0, v_id)
                pListNode = pListNode.next
    
    def bottom_up(self):
        self.computer_level()
        vec = []
        for i in range(self.vertex_num):
            vec.append(self.vertex_pool[i].level)
        vec_sorted_index = sorted(range(len(vec)), key=lambda k: vec[k], reverse=True)
        for i in range(self.vertex_num):
            v_id = vec_sorted_index[i]
            u_id = self.parent_edge[v_id].edge_from
            if u_id == -1:
                break
            if self.min_barrier_dist[v_id] != -1:
                tmp_min = np.min(np.stack((self.vertex_value[u_id], self.min_value_along_path[v_id])), axis=0)
                tmp_max = np.max(np.stack((self.vertex_value[u_id], self.max_value_along_path[v_id])), axis=0)
                tmp_dist = np.min(tmp_max - tmp_min)
                if self.min_barrier_dist[u_id] == -1 or tmp_dist < self.min_barrier_dist[u_id]:
                    self.min_barrier_dist[u_id] = tmp_dist
                    self.min_value_along_path[u_id] = tmp_min
                    self.max_value_along_path[u_id] = tmp_max

    def top_down(self, root_id=0):
        que = [root_id]
        self.inque[root_id] = True
        while que:
            v_id = que[-1]
            que.pop()
            pListNode = self.child_edge[v_id].next
            while pListNode is not None:
                u_id = pListNode.edge.edge_to
                if self.min_barrier_dist[v_id] != -1:
                    tmp_min = np.min(np.stack((self.vertex_value[u_id], self.min_value_along_path[v_id])), axis=0)
                    tmp_max = np.max(np.stack((self.vertex_value[u_id], self.max_value_along_path[v_id])), axis=0)
                    tmp_dist = np.min(tmp_max - tmp_min)
                    if self.min_barrier_dist[u_id] == -1 or tmp_dist < self.min_barrier_dist[u_id]:
                        self.min_barrier_dist[u_id] = tmp_dist
                        self.min_value_along_path[u_id] = tmp_min
                        self.max_value_along_path[u_id] = tmp_max
                    if not self.inque[u_id]:
                        que.insert(0, u_id)
                        self.inque[u_id] = True
                pListNode = pListNode.next
    
    def calculate_minimum_barrier_distance(self):
        for i in range(self.vertex_num):
            if self.is_seed[i]:
                self.min_barrier_dist[i] = 0
        print(datetime.datetime.now().strftime('%F %T') + ' Bottom to up ...')
        self.bottom_up()
        print(datetime.datetime.now().strftime('%F %T') + ' Top to down ...')
        self.top_down()
        result = np.array(self.min_barrier_dist)
        result = result.reshape(self.img_height, self.img_width)
        print(datetime.datetime.now().strftime('%F %T') + ' Done.')
        return result