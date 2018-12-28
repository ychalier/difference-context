import owlready2 as owl
import sys
import os


class Ontology(owl.Ontology):
    """
    Interesting methods (not complete, see documentation at
    https://owlready2.readthedocs.io/en/latest/ for more):

      # lookup
      .get_triples(s=None, p=None, o=None)
      .search()
      .search_one()

      # classes
      .classes()
      .disjoint_classes()
      .inconsistent_classes()

      # properties
      .properties()
        .data_properties()
        .object_properties()
        .annotation_properties()
      .disjoint_properties()

      # individuals
      .individuals()
      .different_individuals()

      # AllDisjoint, for classes and properties
      .disjoints()
    """

    def __init__(self, subfolder_id="000", folder="IIMB_LARGE",
                 filename="onto.owl"):
        """ Load an ontology from a given folder.

        By extracting the default folder IIMB_LARGE, subfolders are of the
        form 000, 001, 002, ..., 080. Each contains a file onto.owl with an
        ontology in XML format.

        This method intializes a Ontology object by loading the content of a
        given folder.

        """

        self.iri = os.path.join("file://", sys.path[0],
                                folder, subfolder_id, filename)
        print("Loading ontology at", self.iri)
        owl.Ontology.__init__(self, owl.World(), base_iri=self.iri+"#")
        self.load()

    def select(self, query):
        """ Selects one item based on its node name.

        If none element is found, returns None.

        """

        search = self.search(iri="*"+query)
        if len(search) > 0:
            return search[0]
        return None


# if the script is imported by another one, this will NOT be executed
if __name__ == "__main__":

    # load ontology in folder 000
    source = Ontology("000")

    # load ontology in folder 001
    target = Ontology("001")

    for individual in target.individuals():
        for property in individual.get_properties():
            for value in property[individual]:
                vstr = str(value)[:40]
                if len(str(value)) > 40:
                    vstr += " (...)"
                print("{}\t{}\t{}".format(individual, property, vstr))
        # print only first item
        break
