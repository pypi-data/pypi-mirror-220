import argparse
from .pathprocess import PathList


def main():
    parser = argparse.ArgumentParser(description='Process pathway and gene data.')
    parser.add_argument('gene_file', type=str, help='Path to gene file')
    parser.add_argument('ortholog_file', type=str, help='Path to ortholog file')
    parser.add_argument('species_file', type=str, help='Path to species file')
    parser.add_argument('abundance_file', type=str, help='Path to abundance file')
    parser.add_argument('output_file', type=str, help='Path to output file')
    args = parser.parse_args()

    path_list = PathList()
    path_list.pathway_integration(args.gene_file, args.ortholog_file, args.species_file, args.abundance_file)
    path_list.to_csv(args.output_file)


if __name__ == "__main__":
    main()
