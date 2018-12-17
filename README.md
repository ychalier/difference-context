# [DK914] Context of difference

The aim of this project is to propose a formal definition of the contextual difference relation between 2 URIs. A context of difference can be a subgraph of the instances description of the URIs. Then develop a tool that can extract these subgraphs for each pair of URIS.

## links

 - [project description](https://www.lri.fr/~sais/D2K/projects/index.html)
 - [IIMB datasets](http://oaei.ontologymatching.org/2010/im/iimb_large_30082010.tgz)
 
## todo list

 1. [ ] OWL parser using an OWL API for Python
 2. [ ] Difference subgraph computation, for a given pair of entities
    - use a maximum depth of exploration
    - only work on matching relations
    - *(optimization) explore nodes only once as far as possible*
 3. [ ] Main process structure (using multiprocessing)
 4. [ ] User interface to nicely plot the generated context subgraphs
 5. [ ] Evaluation
    - computation time
    - what relations are 
 
