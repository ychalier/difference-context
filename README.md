# [DK914] Context of difference

The aim of this project is to propose a formal definition of the contextual difference relation between 2 URIs. A context of difference can be a subgraph of the instances description of the URIs. Then develop a tool that can extract these subgraphs for each pair of URIS.

## links

 - [project description](https://www.lri.fr/~sais/D2K/projects/index.html)
 - [IIMB datasets](http://oaei.ontologymatching.org/2010/im/iimb_large_30082010.tgz)

## virtual environment

The following setup is done for **Python v3.5.2**.

### initial setup

If not done already, install the `virtualenv` package from Python. You should be able to do it with:

    pip3 install virtualenv

However, some distributions may require the installation of a dedicated package (`sudo apt-get install python3-virtualenv` or equivalent). See what's best for yourself.

From the root directory of this repository, initiate the virtual environment with the following command:

    virtualenv venv

That will create a local folder `venv/` that will contain the Python installation. *If anything goes wrong, delete this folder and retry the procedure.*

### usage

Active it with

    source venv/bin/activate

Install the packages from `requirements.txt` with

    pip install -r requirements.txt

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
