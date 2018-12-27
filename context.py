import owlready2 as owl

from parser import Ontology


def common_properties(idv_a, idv_b):
    properties = []
    for ppt_a in idv_a.get_properties():
        for ppt_b in idv_b.get_properties():
            if str(ppt_a) == str(ppt_b):
                properties.append((ppt_a, ppt_b))
    return properties


def difference(idv_a, idv_b, depth=1, verbose=False):

    if verbose:
        print("Entering difference for", idv_a,
              "and", idv_b, "width depth", depth)

    graph = {}

    if depth >= 0:
        for ppt_a, ppt_b in common_properties(idv_a, idv_b):

            if verbose:
                print("Property:", ppt_a)

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
                            graph[str(ppt_a)] = (value_a, value_b)

    if verbose:
        print("Exiting difference.")

    return graph


def plot(graph, prefix=""):
    if type(graph) == type({}):
        for key in graph:
            print(prefix + key)
            plot(graph[key], prefix + "\t")


if __name__ == "__main__":
    source = Ontology("000")
    target = Ontology("001")

    individual_source = source.select("botswana")
    individual_target = target.select("item1557833595821314299")

    graph = difference(individual_source, individual_target, 3)

    plot(graph)
