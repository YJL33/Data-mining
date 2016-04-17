"""
USC INF553 Sp. 2016
Assignment 5
Problem 1: Find betweenness

<Input>
The input graph will be provided in a JSON file where each line represents an edge in the graph.

<Output>
Stdout the betweenness of edges in a format as follows:
   ["a", "b"]: 5.0
   ["a", "c"]: 1.0
   ["b", "c"]: 5.0
   ["b", "d"]: 12.0
   ...

Sort every edge (i.e. node pair) in alphabetic order. 
e.g. print out ["a", "b"] instead of ["b", "a"].

<Execute>
python firstname_lastname_betweenness.py input.json
"""
import sys
import json

def getBetweenness(edges_list):
    """
    Input:
    edges_list: a list of edges, e.g., [[1,2],[1,3]]

    Steps of GN algorithm:
    [Step A] for each node X in the graph G,
        1. Run BFS, starting at the node X;
           form a DAG graph G' that contains edges between different levels of BFS.
        2. For each node Y in the graph, compute the number of shortest paths from X to Y.
           Recall that this is done by a top-down traversal of G'.
        3. Based on the results in step 2, for each edge e in G',
           compute the sum of the fraction of shortest paths from X that pass through e.
           Recall that this is done by a bottom-up traversal of G'.
    [Step B] for each edge e in the graph G,
        1. Sum up the fractions obtained in Step A for e.
        2. Divide the sum by 2 to give the betweeneness of e.

    Output:
    Stdout the betweenness of edges.
    """
    class Node():
        """
        Class of a Node
        """
        def __init__(self, node):
            self.value = node
            self.parent = []        # Parents
            self.children = []      # Children
            self.p_val = 0

        def __repr__(self):
            return 'Node:%s' % (self.value)

    class Tree():
        """
        Class of a DAG graph
        """
        def __init__(self, root, data_points):
            """
            Initialize a tree
            """
            nodes_list = []
            for edges in data_points:
                for node in edges:
                    if node not in nodes_list: nodes_list.append(node)
            limitation = len(nodes_list)
            tierseries = [x for x in range(limitation)]

            self.tiers = {}#{t:[] for t in tierseries}     # key = Tier, value = Nodes
            self.nd = []                                # Nodes
            self.size = 0
            self.root = Tree.create_tree(self, root)        # Create a tree beginning from the root

            tier = 0

            while (self.size < limitation):
                for i in self.tiers[tier]:
                    data_points = self.grow_one_tier(tier, i, data_points)
                tier += 1

        def __repr__(self):
            return 'Root:\n%s' % self.root

        def create_tree(self, rootnode):
            """
            Create a new tree
            """
            root = Node(rootnode)
            root.parent = None
            root.path = 1
            root.tier = 0
            self.tiers[0] = [root]
            self.nd.append(root)
            self.size += 1
            return root

        def add_child(self, pr, ch, new_node=True):
            """
            Add a child. pr, ch are Nodes.
            """
            nd_values = [i.value for i in self.nd]
            if ch.value in nd_values and ch.tier != pr.tier+1: return # Element seen in higher tier
            #print "add", ch.value, "to", pr.value
            ch.parent.append(pr)
            ch.path = sum([p.path for p in ch.parent])
            ch.tier = pr.tier + 1
            pr.children.append(ch)
            if new_node:
                if ch.tier not in self.tiers.keys(): self.tiers[ch.tier]=[ch]
                else: self.tiers[ch.tier].append(ch)
                self.nd.append(ch)
            return

        def grow_one_tier(self, tier, node, data):
            """
            Grow a tier of node in DAG graph
            """
            #print "Grow tree: from", node, "   - Tier", tier+1
            rm = [True]*len(data)
            nd_values = [i.value for i in self.nd]      # Value of all existing nodes
            for i in xrange(len(data)):
                if node.value in data[i]:
                    rm[i] = False
                    counterpart = [c for c in data[i] if c != node.value]
                    assert len(counterpart) == 1
                    if counterpart[0] not in nd_values:
                        child = Node(counterpart[0])
                        self.size += 1
                        self.add_child(node, child)
                    else:
                        existing_nd = [i for i in self.nd if i.value == counterpart[0]]
                        assert len(existing_nd) == 1
                        child = self.nd[self.nd.index(existing_nd[0])]
                        self.add_child(node, child, False)
                else: continue
            rmdata = [i for i in data if rm[data.index(i)]]
            return rmdata

        def getP(self, node):
            """
            Given a node, calculate its P value.
            """
            p_from_children = 0
            for i in node.children:
                if len(i.parent) == 1: p_from_children += i.p_val
                else: p_from_children += (float(node.path)/sum([p.path for p in i.parent]))*i.p_val
            p_value = 1 + p_from_children                   # Here use 1 rather than p.path
            return p_value

        def getQ(self, parent, child):
            """
            Given two node, judge whether there's a edge in the DAG tree. If yes, return Q(e)
            """
            eoi = [i for i in self.nd if i.value == parent or i.value == child]
            assert (len(eoi) == 2)
            q_value = 0
            if eoi[0] in eoi[1].parent: q_value += float(eoi[0].path*eoi[1].p_val)/(sum([p.path for p in eoi[1].parent]))
            elif eoi[1] in eoi[0].parent: q_value += float(eoi[1].path*eoi[0].p_val)/(sum([p.path for p in eoi[0].parent]))
            return q_value
            
    ################################################################################################
    # Below this line are the main part.

    nodes_list = []                 # Get all nodes
    for edges in edges_list:
        for node in edges:
            if node not in nodes_list: nodes_list.append(node)
    #print json.dumps(sorted(nodes_list))
    #print edges_list

    dag_node_dict = {}                          # key: root node, value: DAG Tree
    for node in nodes_list:
        dag_node_dict[node] = Tree(node, edges_list)                            # A-1
        assert dag_node_dict[node].size == len(nodes_list)
        #for nd in dag_node_dict[node].nd: print node, nd.value, nd.path, nd.parent
    for dag_tree in dag_node_dict.values():
        for t in sorted(dag_tree.tiers.keys(), reverse=True):       # Bottom-up
            for node in dag_tree.tiers[t]:
                node.p_val = dag_tree.getP(node)                                # A-2
                #print dag_tree.root, node.value, node.p_val

    edge_dict = {}                          # key: edge, value: list of Q values
    for edge in edges_list:
        edge_dict[json.dumps(sorted(edge))] = []
        for dag_tree in dag_node_dict.values():
            edge_dict[json.dumps(sorted(edge))].append(dag_tree.getQ(edge[0], edge[1]))      # A-3
    
    for k,v in edge_dict.items(): print "%s: %.1f" %(k, float(sum(v))/2)                     # B

# Do not modify below this line
# =============================
if __name__ == '__main__':
    f = open(sys.argv[1])   # json file that containing data points
    dp = []                 # data points
    for l in f:             # Read them all
        dp.append(json.loads(l))
    getBetweenness(dp)
