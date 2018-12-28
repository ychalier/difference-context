import owlready2 as owl

from parser import Ontology


def common_properties(idv_a, idv_b):
    """ Returns the list of properties that two objects have in common.

    Returns a list of pairs, each pair containing the same property but
    regarding each ontology.

    """

    properties = []
    for ppt_a in idv_a.get_properties():
        for ppt_b in idv_b.get_properties():

            # TODO: maybe simple string matching is not the best
            if str(ppt_a) == str(ppt_b):
                properties.append((ppt_a, ppt_b))

    return properties


def difference(idv_a, idv_b, depth=1, keep_values=False, verbose=False):
    """ Computes the difference subgraph of two entities.

    Returns a JSON-like dictionnary. Keys are properties, and values are either
    nested elements with other entities, or a pair of "real" (string) values
    that differed from the two elements.

    The `depth` parameter controls the recursion depth of the search.

    The parameters `idv_a` and `idv_b` are objects representing individuals from
    the two ontologies considered.

    """

    if verbose:
        print("Entering difference for", idv_a,
              "and", idv_b, "width depth", depth)

    graph = {}

    # prevents infinite recursion
    if depth >= 0:

        # only consider common properties
        for ppt_a, ppt_b in common_properties(idv_a, idv_b):

            if verbose:
                print("Property:", ppt_a)

            # each property may have several values
            # TODO: maybe product comparison is not the best
            for value_a in ppt_a[idv_a]:
                for value_b in ppt_b[idv_b]:

                    if owl.ObjectProperty in ppt_a.is_a:
                        # `value_a` and `value_b` are instances of classes from
                        # the ontology, hence we go deeper in the graph
                        sub_graph = difference(value_a, value_b, depth - 1)
                        if len(sub_graph) > 0:
                            graph[str(ppt_a)] = sub_graph

                    elif owl.DataProperty in ppt_a.is_a:
                        # `value_a` and `value_b` are simple strings, so we just
                        # match them
                        if value_a != value_b:
                            if keep_values:
                                graph[str(ppt_a)] = {"a": value_a, "b": value_b}
                            else:
                                graph[str(ppt_a)] = {}

    if verbose:
        print("Exiting difference.")

    return graph


def plot(graph, prefix=""):
    """ Plots a difference graph.

    Uses tabulations to represent nesting.
    Separates different values with '//'.

    """

    for key in graph:
        if set(graph[key].keys()) != set(["a", "b"]):
            print(prefix + key)
            plot(graph[key], prefix + "\t")
        else:  # if values are kept, plot them
            value_a = graph[key]["a"][:20]
            value_b = graph[key]["b"][:20]
            print(prefix + key, "\t", value_a, "//", value_b)


# if the script is imported by another one, this will NOT be executed
if __name__ == "__main__":
    source = Ontology("000")
    target = Ontology("001")

    individual_source = source.select("botswana")
    individual_target = target.select("item1557833595821314299")

    graph = difference(individual_source, individual_target, 3)

    plot(graph)
