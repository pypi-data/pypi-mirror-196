# Inhibitory Drug Target Analyzer of Viruses
Viruses, in particular, RNA viruses show increased drug resistance to antivirals that directly act on viral proteins. IDTA module aims to find the candidate drugs/antivirals by using /high-throughput screening of FDA approved drug databases to target historically conserved sequences (HCS) of a given virus.

## Getting Started

### Prerequisites

To use this program, you will need:

- Python 3.8 and above version should be installed in your machine.
- Only Unix based OS' are supported.

### Requirements

- [Biopython](https://biopython.org/)
- [Pandas](https://pandas.pydata.org/)
- [Numpy](https://numpy.org/)
- [Subprocess](https://docs.python.org/3/library/subprocess.html)
- [Json](https://docs.python.org/3/library/json.html)
- [Urllib](https://docs.python.org/3/library/urllib.html)
- [Math](https://docs.python.org/3/library/math.html)
- [Nglview](https://github.com/nglviewer/nglview)
- [Local BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download)
- [P2Rank](https://github.com/rdk/p2rank)
- [Open Babel](https://openbabel.org/docs/dev/Installation/install.html)
- [Autodock Vina](https://autodock-vina.readthedocs.io/en/latest/)

### Installation

1. Install the package by running `pip3 install idta`
2. Additionaly, you need to install `P2Rank`, `Open Babel`, `Autodock Vina` manually to run the codes successfully. You can install those packages using your favorite package manager in Unix based OS'. Only `P2Rank` should be install from the github repository using source files.

### Usage

Import the Class

    from idta.Drug_module import Drug_module

Create an object of the Drug_module class
    
    obj = Drug_module()

Pass fasta file or json file as a parameter of read_hcs method.
    
    obj.read_hcs(fasta_file|json_file)

Blast your HCS' with pdb database using your taxid of your host and decide the output name.

    obj.do_pdb_blast(taxid, output_filename)

Filter your blast output for further analysis.

    obj.filtering_blast_output()

Download pdb files that is present in your blast result.

    obj.get_pdb_files()

Search for binding pockets of your downloaded pdb files using `p2rank`.

    obj.pocket_control(p2rank_path)

Calculate the center of HCS' and use as a box of docking analysis.

    obj.calculate_center_of_box()

You can look your protein and your HCS using `NGL Viewer`.

    obj.show_nglview()

Perform a docking analysis to find an inhibitor of your target protein with vina.

    obj.do_docking_with_vina()

Parse the result and get your top 3 candidates.

    obj.parsing_docking_results()

### License

This project is licensed under the MIT License - see the `LICENSE` file for details.

### Acknowledgments

- This project was inspired by the need for effective treatments for viral infections, especially in light of the COVID-19 pandemic.
- The FDA-approved drug database was obtained from ZINC (https://zinc.docking.org/organisms/viruses/substances/subsets/fda/).