import pandas as pd
from typing import List
from pathprocess import PathGen


class PathGen:
    def __init__(self):
        self.pathgen = PathGen()

    def read_pathway(self, file: str) -> pd.DataFrame:
        """
        Reads the Pathway CSV file and returns it as a DataFrame.
        """
        return pd.read_csv(file)

    def read_annotation(self, file: str) -> pd.DataFrame:
        """
        Reads the Annotation CSV file and returns it as a DataFrame.
        """
        return pd.read_csv(file)

    def read_orthologs(self, file: str) -> pd.DataFrame:
        """
        Reads the Orthologs CSV file and returns it as a DataFrame.
        """
        return pd.read_csv(file)

    def read_abundance(self, file: str) -> pd.DataFrame:
        """
        Reads the Abundance CSV file and returns it as a DataFrame.
        """
        return pd.read_csv(file)

    def main(self, files: List[str]) -> None:
        """
        Reads data from four files, integrates them, and writes the result to a new CSV file.
        """
        pathways = self.read_pathway(files[0])
        annotations = self.read_annotation(files[1])
        orthologs = self.read_orthologs(files[2])
        abundance = self.read_abundance(files[3])

        self.pathgen.pathway_integration(pathways, annotations, orthologs, abundance)
