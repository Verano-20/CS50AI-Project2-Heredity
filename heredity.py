import csv
import itertools
import sys
import pandas as pd

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Calculate the matrix of probabilities for gene inheritance
    gene_matrix = gene_matrix()
    
    # create list to store all probabilities to be multiplied
    joint_prob = []

    # Loop through people and create dictionary of who has what genes and trait
    ref = dict()
    for person in people:
        # Get number of genes
        if person in one_gene:
            genes = 1
        elif person in two_genes:
            genes = 2
        else:
            genes = 0
        # Get trait
        if person in have_trait:
            trait = True
        else:
            trait = False
        # Add info to ref
        ref[person] = {'genes': genes, 'trait': trait}

    # Begin looping through people
    for person in people:
       
        # Check if the person has parents
        if people[person]['mother'] == None and people[person]['father'] == None:
            # If no parents, take values straight from dict
            gene_prob = PROBS['gene'][ref[person]['genes']]    
            trait_prob = PROBS['trait'][ref[person]['genes']][ref[person]['trait']]
            joint_prob.append(gene_prob * trait_prob)
        else:
            # Calculate prob of getting number of genes from mother and father
            for parent in ['mother', 'father']:
                if ref[person[parent]]['genes'] == 2:
                    gene_prob = 1 - PROBS['mutation']
                elif ref[person[parent]]['genes'] == 1:
                    gene_prob = 0.5 - PROBS['mutation']
                elif ref[person[parent]]['genes'] == 0:
                    gene_prob = PROBS['mutation']
                
                inherited_prob = 



            # Calculate prob of getting number of genes from father



        # Calculate total probability for this person
        total_prob = gene_prob * trait_prob
        joint_prob.append(total_prob)


def gene_matrix():
    """ 
    Calculate a 3 x 3 x 3 matrix of probabilities for inherting any number of genes from parents with any number of genes.
    x, y = parents
    z = child
    Values taken from PROBS dict.
    """


    


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]['gene'][1] += p
        if person in two_genes:
            probabilities[person]['gene'][2] += p
        if person in have_trait:
            probabilities[person]['trait'][True] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # Get sums as given
    for person in probabilities:
        gene_total = sum(probabilities[person]['gene'][n] for n in range(3))
        trait_total = sum(probabilities[person]['trait'][t] for t in [True, False])
        # Calculate alpha(gene) and beta(trait) normalisation factors
        alpha = 1 / gene_total
        beta = 1 / trait_total
        # Apply normalisation
        for n in range (3):
            probabilities[person]['gene'][n] *= alpha
        for t in [True, False]:
            probabilities[person]['trait'][t] *= beta 
        

if __name__ == "__main__":
    main()
