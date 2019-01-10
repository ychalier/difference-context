import networkx as nx
import matplotlib.pyplot as plt




def build_edge_list(graph,parent_label,parent_id):
    """ Transforms dictionary graph to an edge list starting from a fictional root

    Recursively adds directed edges between a property and its object property.

    If the values of the properties are stored, they are added as leafs

    Parameters
    ----------
    graph: Dictionary
        A recuresive graph whose each key is a node label, and the value is the subgraph representing the neighbor nodes
    
    parent: string
        The label of the parent graph 
    
    parent_id: int
        the id of the parent

    Returns
    -------
    list
        A list of pairs representing the directed edges of the graph


    """
    edge_list=[]
    label_dict={}

    count=-1
    for key in graph:
        count=count+1
        id=parent_id+str(count)
        edge_list.append((parent_id,id))
        label_dict[id]=key[9:]

        # if there are no values stored
        if set(graph[key].keys()) != set(["a", "b"]):
            # recursively add the edges of the child graph
            lst,dic=build_edge_list(graph[key],key,id)
            edge_list=edge_list+lst
            label_dict.update(dic)

        else:  # if the values are kept, include them as leaves
            value_a = graph[key]["a"][:20]
            value_b = graph[key]["b"][:20]
            edge_list.append((id+"0","val1:"+value_a))
            edge_list.append((id+"1","val2:"+value_b))
            label_dict[id+"0"]="val1:"+value_a
            label_dict[id+"1"]="val2:"+value_b
        
 
    return (edge_list,label_dict)


def visualize(graph):
    """ Visualizes the differnece graph as a tree

    Generates a visualisation for a differnece graph as a tree using Networkx 

    Parameters
    ----------
    graph: Dictionary
        A recuresive graph whose each key is a node label, and the value is the subgraph representing the neighbor nodes



    """

    # Adding a fictional root labeled 'Difference'
    edge_list,label_dict=build_edge_list(graph,"Difference","0")
    label_dict["0"]="Difference"
    G=nx.DiGraph()
    for (parent,child) in edge_list:
        G.add_edge(parent,child)
    
    # Define the positions of the nodes so the graph has a top down directed tree form
    pos = hierarchy_pos(G,"0")   

    # Drawing the nodes in their predefined positions 
    # shape from ‘so^>v<dph8.
    nx.draw(G,node_size=5000, pos=pos,labels=label_dict, with_labels=True,node_shape='o')
    plt.show()

    return



def hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, 
                  pos = None, parent = None):
    """ Utiltiy function that define the positions of the nodes  of a directed acyclic graph as a tree

    """

    if pos == None:
        pos = {root:(xcenter,vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)

    neighbors = list(G.neighbors(root)) 
    if len(neighbors)!=0:
        dx = width/len(neighbors) 
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos = hierarchy_pos(G,neighbor, width = dx, vert_gap = vert_gap, 
                                vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos, 
                                parent = root)
    return pos

    