import owlready2 as owl
import sys
import os


class Ontology(owl.Ontology):
    """
    Interesting methods (not complete):

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

    def __init__(self, subfolder_id="000", folder="IIMB_LARGE", filename="onto.owl"):
        self.iri = os.path.join("file://", sys.path[0], folder, subfolder_id, filename)
        print("Loading ontology at", self.iri)
        owl.Ontology.__init__(self, owl.World(), base_iri=self.iri+"#")
        self.load()

    def select(self, query):
        search = self.search(iri="*"+query)
        if len(search) > 0:
            return search[0]
        return None

    def demo(self):
        print("\n----- CLASSES -----")
        for class_ in self.classes():
            print(class_, end=" ")
        print("\n\n----- PROPERTIES -----")
        for property in self.properties():
            print(property, end=" ")
        print()

if __name__ == "__main__":

    # load ontology in folder 000
    source = Ontology("000")
    source.demo()

    # load ontology in folder 001
    target = Ontology("001")
    target.demo()

    print("\n----- FIRST INDIVIDUAL DEMO -----")
    for individual in target.individuals():
        for property in individual.get_properties():
            for value in property[individual]:
                print("{} {} {}".format(individual, property, value))
        break
