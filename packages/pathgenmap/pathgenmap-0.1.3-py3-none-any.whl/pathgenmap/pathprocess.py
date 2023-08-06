import pandas as pd
from Bio import Entrez
from typing import List


class Path:
    id_counter = 1

    def __init__(self, fdr, ng, pg, fe, path_name, url):
        self.id_path = Path.id_counter
        Path.id_counter += 1
        self.fdr = fdr
        self.ng = ng
        self.pg = pg
        self.fe = fe
        self.path_name = path_name
        self.url = url
        self.genes_list = []


class PathList:
    def __init__(self):
        self.pathways_list = []

    def pathway_integration(self, pathways, annotations, orthologs, abundance) -> None:
        """
        Integrates data from four DataFrames and populates the Pathways list.
        """
        for _, pathway in pathways.iterrows():
            path = Path(pathway['Enrichment FDR'], pathway['nGenes'], pathway['Pathway Genes'],
                        pathway['Fold Enrichment'], pathway['Pathway'], pathway['URL'])
            genes = pathway['Genes'].split()

            for gene in genes:
                gene = gene.lower()
                annotation = annotations[annotations['Preferred_name'] == gene]
                ortho = annotation['seed_ortholog'].values[0] if len(annotation) > 0 else None

                if ortho:
                    ortholog = orthologs[orthologs['orthologs'] == ortho]
                    taxo_id = ortholog['species'].values[0].split('(')[-1][:-1] if len(ortholog) > 0 else None

                    if taxo_id:
                        abund = abundance[abundance['taxonomy_id'] == int(taxo_id)]
                        reads = abund['new_est_reads'].values[0] if len(abund) > 0 else None

                        lineage = None
                        if taxo_id:
                            handle = Entrez.efetch(db="taxonomy", id=taxo_id, retmode="xml")
                            records = Entrez.read(handle)
                            lineage = records[0]["Lineage"]

                        gene_dict = {
                            "gene_name": gene,
                            "taxo_id": taxo_id,
                            "ortho": ortho,
                            "lineage": lineage,
                            "reads": reads
                        }
                        path.genes_list.append(gene_dict)

            self.pathways_list.append(path)

        self.write_to_csv()

    def write_to_csv(self) -> None:
        """
        Writes the Pathways list to a new CSV file.
        """
        data = []
        for path in self.pathways_list:
            for gene in path.genes_list:
                data.append([
                    path.id_path,
                    path.path_name,
                    path.fdr,
                    path.fe,
                    gene['gene_name'],
                    gene['taxo_id'],
                    gene['ortho'],
                    gene['lineage'],
                    gene['reads']
                ])

        df = pd.DataFrame(data, columns=['id_path', 'pathway', 'fdr', 'fe', 'gene', 'taxonomy_id', 'ortho', 'lineage',
                                         'reads'])
        df.to_csv('pathway_gene_species.csv', index=False)
