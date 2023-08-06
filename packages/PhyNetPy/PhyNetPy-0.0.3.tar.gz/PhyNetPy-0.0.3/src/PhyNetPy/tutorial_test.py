import random
from PhyAllop import MP_ALLOP
from NetworkParser import NetworkParser
from GeneTrees import GeneTrees
from Graph import DAG

### TRIMMED SCENARIO J
# gene_trees_trimmedJ : list[DAG] = NetworkParser("/Users/mak17/Documents/PhyloGenPy/PhyNetPy/src/PhyNetPy/J_pruned.nex").get_all_networks()

### UNTRIMMED SCENARIO J
gene_trees_J : list[DAG] = NetworkParser("/Users/mak17/Documents/PhyloGenPy/PhyNetPy/src/PhyNetPy/J_nex_n1.nex").get_all_networks()

### SUBGENOME MAPPINGS
# subgenome_map_trimmedJ : dict[str, list[str]]=  {'U': ['01uA', '01uB'], 'T': ['01tA', '01tB'], 'B': ['01bA'], 'F': ['01fA'], 
#                                          'V': ['01vB', '01vA'], 'C': ['01cA'], 'A': ['01aA'], 'D': ['01dA'], 'O': ['01oA']} 
subgenome_mapJ : dict[str, list[str]]=  {'F': ['01fA'], 'T': ['01tA', '01tB'], 'W': ['01wA', '01wB'], 'B': ['01bA'], 
                   'V': ['01vA', '01vB'], 'A': ['01aA'], 'U': ['01uA', '01uB'], 'C': ['01cA'], 
                   'E': ['01eA'], 'X': ['01xA', '01xB'], 'Y': ['01yA', '01yB'], 'O': ['01oA'], 
                   'Z': ['01zB', '01zA'], 'D': ['01dA']} 

#Using mapping auto generation. Comment out if using hard coded map above
# subgenome_map_trimmedJ = GeneTrees(gene_trees_trimmedJ).mp_allop_map()

#Choose how many hill climbing runs to do. We recommend doing at least 10, but 3 is chosen here for brevity
num_hill_climbing_chains = 15

for dummy in range(num_hill_climbing_chains):
    
    #change Pathname to unpruned nexus file if doing that version.
    output_networks : dict[tuple[DAG, int]] = MP_ALLOP("/Users/mak17/Documents/PhyloGenPy/PhyNetPy/src/PhyNetPy/J_nex_n1.nex", subgenome_mapJ, iter_ct = 750, seed= random.randint(0, 1000))

    index = 0
    for net, score in output_networks.items():
        print(f"This network scored {score}!")
    
        # Do any other analysis you'd like to do here with the net object:
        #
        # INSERT STUFF HERE. 
        #
        
        #Converts network to a newick string
        print(net.to_newick())
        
        index += 1