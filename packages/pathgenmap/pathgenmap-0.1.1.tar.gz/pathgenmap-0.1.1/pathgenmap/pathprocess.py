import pandas as pd
from Bio import Entrez


class Path:
    id_path = 0

    def __init__(self, fdr, ng, pg, fe, path_name, url, genes_list):
        self.id_path = Path.id_path
        Path.id_path += 1
        self.fdr = fdr
        self.ng = ng
        self.pg = pg
        self.fe = fe
        self.path_name = path_name
        self.url = url
        self.genes_list = genes_list


class PathList:

    def __init__(self):
        self.pathways_list = []

    def pathway_integration(self, gene_path, ortholog_path, species_path, abundance_path):
        gene_data = pd.read_csv(gene_path)
        ortholog_data = pd.read_csv(ortholog_path)
        species_data = pd.read_csv(species_path)
        abundance_data = pd.read_csv(abundance_path)

        for index, row in gene_data.iterrows():
            genes = row['Genes'].split(" ")
            genes = [gene.lower() for gene in genes]

            for gene in genes:
                ortholog_row = ortholog_data[ortholog_data['Preferred_name'] == gene]
                if not ortholog_row.empty and ortholog_row.iloc[0]['Preferred_name'] != '-':
                    ortho = ortholog_row.iloc[0]['seed_ortholog']
                    species_row = species_data[species_data['orthologs'] == ortho]
                    if not species_row.empty:
                        taxo_id = species_row.iloc[0]['species'].split("(")[-1].replace(")", "")
                        abundance_row = abundance_data[abundance_data['taxonomy_id'] == int(taxo_id)]
                        if not abundance_row.empty:
                            Entrez.email = "your.email@example.com"
                            handle = Entrez.efetch(db="taxonomy", id=taxo_id, mode="text", rettype="xml")
                            records = Entrez.read(handle)
                            lineage = records[0]['Lineage']
                            reads = abundance_row.iloc[0]['new_est_reads']

                            gene_dict = {'gene_name': gene, 'taxo_id': taxo_id, 'ortho': ortho, 'lineage': lineage,
                                         'reads': reads}
                            path = Path(row['Enrichment FDR'], row['nGenes'], row['Pathway Genes'],
                                        row['Fold Enrichment'], row['Pathway'], row['URL'], [gene_dict])
                            self.pathways_list.append(path)

    def to_csv(self, output_file):
        data = []
        for path in self.pathways_list:
            for gene in path.genes_list:
                data.append(
                    [path.id_path, path.path_name, path.fdr, path.fe, gene['gene_name'], gene['taxo_id'], gene['ortho'],
                     gene['lineage'], gene['reads']])

        df = pd.DataFrame(data,
                          columns=["id_path", "pathway", "fdr", "fe", "gene", "taxonomy_id", "species_name", "lineage",
                                   "reads"])
        df.to_csv(output_file, index=False)
