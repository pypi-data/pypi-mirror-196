# Python wrapper to have available all the scoring classes in one place and
# merge the results

import sys
import csv
import json
import argparse
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .rrm_rna_functions import RNAScoring, HMMScanner, LogoGenerator

__version__ = "1.0.6"

def main():
    print("Executing rrmscorer version %s." % __version__)
    usr_input = UserInput()
    manager = Manager(usr_input)
    manager.input_handler()


class Manager():
    # This is the general input manager of the scoring framework
    def __init__(self, usr_input):
        self.rna_scoring = RNAScoring()
        self.rna_scoring.__init__()
        self.hmm_scan = HMMScanner()
        self.hmm_scan.__init__()
        self.usr_input = usr_input
        self.logo_gen = LogoGenerator()
        self.standard_amino_acids = {
            "A", "C", "D", "E", "F", "G", "H", "I", "K",
            "L", "M", "N", "P", "Q", "R", "S", "T", "V",
            "W", "Y"}
        self.standard_RNA_nucleotides = {"A", "C", "G", "U"}

    def input_handler(self):
        if self.usr_input.fasta_file:
            seqs_dict = self.hmm_scan.hmmalign_RRMs(
                fasta_file=self.usr_input.fasta_file)

        elif self.usr_input.UP_id:
            seqs_dict = self.hmm_scan.get_UP_seq(
                UP_id=self.usr_input.UP_id)

        for seq_id, seq in seqs_dict.items():
            set_seq = set(seq.upper())
            set_seq.remove("-")
            if set_seq.issubset(self.standard_amino_acids):
                pass
            else:
                print("\033[91m[ERROR] The protein sequence contains"
                      " non-standard amino acids.\033[0m")
                sys.exit()
            seq_id = seq_id.replace("/", "_").replace("|", "_")
            print("Running predictions for {}...".format(seq_id))
            if self.usr_input.top:
                top_scores = self.rna_scoring.find_best_rna(rrm_seq=seq)

                if self.usr_input.json:
                    json_path = self.usr_input.json + seq_id + "_top_scorers.json"
                    with open(json_path, "w") as fp:
                        json.dump(top_scores, fp, indent=2)
                        print("Json file succesfully saved in {}".format(
                            json_path))

                if self.usr_input.plot:
                    for n_mers in [10, 50, 100, 250]:
                        plot_path = self.usr_input.plot + seq_id + \
                                    "_top_{}_logo.png".format(n_mers)
                        ppm = self.logo_gen.generate_PPM(
                            rna_scores=top_scores, n_mers=n_mers,
                            ws=self.usr_input.window_size)
                        bits_df = self.logo_gen.ppm_to_bits(ppm=ppm)
                        self.logo_gen.generate_logo(bits_df=bits_df, id=seq_id)
                        plt.savefig(plot_path, dpi=300)
                        print("Plot succesfully saved in {}".format(
                            plot_path))

            elif self.usr_input.rna_seq:
                if set(self.usr_input.rna_seq).issubset(
                        self.standard_RNA_nucleotides):
                    pass
                else:
                    print("\033[91m[ERROR] The RNA sequence contains"
                          " non-standard RNA nucleotides.\033[0m")
                    sys.exit()
                self.rna_scoring.score_out_seq(
                    rrm_seq=seq, rna_seq=self.usr_input.rna_seq,
                    rna_pos_range=self.usr_input.rna_pos_range)

                for key, score in self.rna_scoring.scores_dict.items():
                    print(key, score)

                if self.usr_input.json:
                    json_path = self.usr_input.json + seq_id + ".json"
                    with open(json_path, "w") as fp:
                        json.dump(
                            self.rna_scoring.scores_dict, fp, indent=2)
                        print("Json file succesfully saved in {}".format(json_path))

                if self.usr_input.csv:
                    csv_path = self.usr_input.csv + seq_id + ".csv"
                    with open(csv_path, 'w') as csv_file:
                        writer = csv.writer(csv_file)
                        for key, value in self.rna_scoring.scores_dict.items():
                            writer.writerow([key, value])
                        print("CSV file succesfully saved in {}".format(csv_path))

                if self.usr_input.plot:
                    print(seq_id)
                    plot_path = self.usr_input.plot + seq_id + ".png"
                    self.rna_scoring.plot_rna_kde(seq_id=seq_id,
                                                  rna_seq=self.usr_input.rna_seq,
                                                  scores_dict=self.rna_scoring.scores_dict,
                                                  window_size=self.usr_input.window_size)
                    plt.savefig(plot_path, dpi=300)
                    print("Plot succesfully saved in {}".format(plot_path))


class UserInput():
    def __init__(self):
        # Input files parser
        args = sys.argv[1:]
        parser = argparse.ArgumentParser(
            description='RRM-RNA scoring framework')

        input_arg = parser.add_mutually_exclusive_group(required=True)
        input_arg.add_argument('-u', '--uniprot',
                               help='UniProt identifier')
        input_arg.add_argument('-f', '--fasta',
                               help='Fasta file path')

        feat_arg = parser.add_mutually_exclusive_group(required=True)
        feat_arg.add_argument('-r', '--rna',
                              help='RNA sequence')
        feat_arg.add_argument('-t', '--top', action="store_true",
                              help='To find the top scoring RNA fragments')

        parser.add_argument('-w', '--window_size', required=False,
                            help='')

        parser.add_argument('-j', '--json', help='Store the results in a json file on the declared directory path')
        parser.add_argument('-c', '--csv', help='Store the results in a CSV file')
        parser.add_argument('-p', '--plot', help='Store the plots in [path]')

        self.input_files = parser.parse_args(args)

        self.fasta_file = self.input_files.fasta
        self.UP_id = self.input_files.uniprot

        self.rna_seq = self.input_files.rna
        self.top = self.input_files.top

        # User defined outputs
        self.json = self.input_files.json
        self.csv = self.input_files.csv
        self.plot = self.input_files.plot

        # Default window size
        if self.input_files.window_size:
            self.window_size = int(self.input_files.window_size)
            if self.window_size == 3:
                self.rna_pos_range = (3, 6)

            elif self.window_size == 5:
                self.rna_pos_range = (2, 7)

        else:  # Default ws=5 if not in input
            self.window_size = 5
            self.rna_pos_range = (2, 7)


if __name__ == '__main__':
    usr_input = UserInput()
    manager = Manager(usr_input)
    manager.input_handler()
