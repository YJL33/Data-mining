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

def getbetweenness(edges_list):
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
    class Node(object):
        """
        Class of a Node
        """
        def __init__(self, node):
            self.value = node
            self.parent = []        # Node's Parents
            self.children = []      # Node's Children
            self.p_val = 0          # Node's p-value (pass through)

        def __repr__(self):
            return 'Node:%s' % (self.value)

    class Tree(object):
        """                                       *   - Root, tier 0
        Class of a DAG graph                     /|\
        Nodes are constructed as Node()         1 2 3       - tier 1
                                                   / \
                                                  4   5     - tier 2
        """
        def __init__(self, root, edges_list, nodes_list):
            """
            Initialize a tree,
            root = root,
            edges_list: given json file, indicate edge and nodes at both side.
            """
            self.size = 1
            self.root = Node(root)                      # Create a tree beginning from the root
            self.root.parent = None
            self.root.path = 1
            self.root.tier = 0

            self.tiers = {}                             # key = Tier, value = Nodes
            self.tiers[0] = [self.root]

            self.node = []                              # Nodes
            self.node.append(self.root)

            tier = 0

            while self.size < len(nodes_list):          # Grow a single DAG tree
                for i in self.tiers[tier]:
                    edges_list = self.grow_one_tier(i, edges_list)
                tier += 1

        def __repr__(self):
            return 'Root:\n%s' % self.root

        def add_child(self, prnt, chld, new_node=True):
            """ Add a child. prnt, chld are Nodes. """
            nd_values = [i.value for i in self.node]
            if chld.value in nd_values and chld.tier != prnt.tier+1:
                return                  # => node seen in higher tier, not belong to this tier
            chld.parent.append(prnt)
            chld.path = sum([p.path for p in chld.parent])
            chld.tier = prnt.tier + 1
            prnt.children.append(chld)              # build the relationship
            if new_node:
                if chld.tier not in self.tiers.keys():      # ... the first node in this tier
                    self.tiers[chld.tier] = [chld]
                else:                                       # ... already other nodes in this tier
                    self.tiers[chld.tier].append(chld)
                self.node.append(chld)                      # a new node on this tree
            return

        def grow_one_tier(self, node, data):
            """ Grow a tier based on "node of interest" in DAG graph, data: edges data """
            #print "Grow tree: from", node, "   - Tier", tier+1
            edge_to_be_removed = [True]*len(data)
            nd_values = [i.value for i in self.node]        # Value of all existing nodes
            for i in xrange(len(data)):                     # For all edges ...
                if node.value in data[i]:                   # ... a edge has "node of interest"
                    edge_to_be_removed[i] = False           # ... this edge can be removed
                    counterpart = [c for c in data[i] if c != node.value]   # the other end of edge
                    assert len(counterpart) == 1
                    if counterpart[0] not in nd_values:     # never seen it in previous grow
                        child = Node(counterpart[0])            # ... make a new node.
                        self.size += 1
                        self.add_child(node, child)             # ... and build relationship
                    else:                                   # already seen it in earlier grow
                        existing_nd = [i for i in self.node if i.value == counterpart[0]]
                        assert len(existing_nd) == 1
                        child = self.node[self.node.index(existing_nd[0])]
                        self.add_child(node, child, False)      # ... just update relationship
                else: continue
            rmdata = [i for i in data if edge_to_be_removed[data.index(i)]]
            return rmdata

        def get_p(self, node):
            """ Given a single node, calculate its P value. """
            p_from_children = 0             # parts of p-value (contributed by children)
            for i in node.children:         # ( p_from_children = 0 if no children)
                if len(i.parent) == 1:
                    p_from_children += i.p_val
                else:
                    p_from_children += (float(node.path)/sum([p.path for p in i.parent]))*i.p_val
            p_value = 1 + p_from_children   # Here use 1 (contributed by self) rather than p.path
            return p_value

        def get_q(self, one, another):
            """ Given two node, check whether the edge is valid, return Q(e) if yes"""
            eoi = [i for i in self.node if i.value == one or i.value == another]
            assert len(eoi) == 2 
            q_value = 0                     # if no parent-children relationship => return 0
            if eoi[0] in eoi[1].parent:
                q_value += float(eoi[0].path*eoi[1].p_val)/(sum([p.path for p in eoi[1].parent]))
            elif eoi[1] in eoi[0].parent:
                q_value += float(eoi[1].path*eoi[0].p_val)/(sum([p.path for p in eoi[0].parent]))
            return q_value

    def get_all_nodes(edges):
        """Get all nodes as a list"""
        nodes_list = []
        for link in edges:
            for node in link:
                if node not in nodes_list:
                    nodes_list.append(node)
        return nodes_list

    def get_trees_dict(e_list, n_list):
        """
        Construct ALL possible DAG trees, e_list = edges, n_lists = nodes
        nd_dict: key = root, value = tree grow from that root
        """
        nd_dict = {}                        # key: root node, value: DAG Tree
        for node in n_list:                                 # For every node...
            nd_dict[node] = Tree(node, e_list, n_list)      # ...grow a Tree with this node as root
            assert nd_dict[node].size == len(n_list)
        #for nd in nd_dict[node].node: print node, nd.value, nd.path, nd.parent
        return nd_dict

    def update_p_value(n_dict):
        """
        Get p-value for all nodes in all trees
        n_dict: key = root, value = trees
        """
        for tree in n_dict.values():                                # For each tree ...
            for tier in sorted(tree.tiers.keys(), reverse=True):    # (bottom-up)
                for node in tree.tiers[tier]:                       # ... and for its each node ...
                    node.p_val = tree.get_p(node)                   # ... update the p-value!
                    #print tree.root, node.value, node.p_val
        return n_dict

    def get_edges_dict(e_list, n_dict):
        """
        Get q-value for all edges in all trees
        n_dict: refer to get_trees_dict(), e_list: all edges
        """
        e_dict = {}                     # key: edge, value: list of Q values
        for edge in e_list:                             # For each edge ...
            e_dict[json.dumps(sorted(edge))] = []
            for tree in n_dict.values():                # ... seek its q-value in every tree!
                e_dict[json.dumps(sorted(edge))].append(tree.get_q(edge[0], edge[1]))
        return e_dict

    ################################################################################################
    # Below this line are the main part.

    nodes_list = get_all_nodes(edges_list)              # All nodes are extracted in a list
    nodes_dict = get_trees_dict(edges_list, nodes_list) # A1. Use a dictionary to save all trees
    update_p_value(nodes_dict)                          # A2. Update p-value of all node
    edges_dict = get_edges_dict(edges_list, nodes_dict) # A3. Get all edge's q-value in all trees

    for k, trees in sorted(edges_dict.items()):
        print "%s: %.1f" % (k, float(sum(trees))/2)    # B

# Do not modify below this line
# =============================
if __name__ == '__main__':
    FILE = open(sys.argv[1])      # json file that containing data points
    DATA_POINTS = []                     # data points
    for l in FILE:                # Read them all
        DATA_POINTS.append(json.loads(l))
    getbetweenness(DATA_POINTS)
