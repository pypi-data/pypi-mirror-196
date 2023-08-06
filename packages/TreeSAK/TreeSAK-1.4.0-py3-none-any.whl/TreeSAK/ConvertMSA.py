import os
import argparse
from Bio import SeqIO
from Bio import AlignIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


ConvertMSA_usage = '''
================================ ConvertMSA example commands ===============================

# convert alignment in fasta format to phylip-relaxed format
TreeSAK ConvertMSA -in NorthSea.aln -inf fasta -out NorthSea.phylip -outf phylip-relaxed

# Alignment format:
  clustal, emboss, fasta, fasta-m10, ig, maf, mauve, nexus, 
  phylip, phylip-sequential, phylip-relaxed, stockholm

# More details about alignment format is here: 
  https://biopython.org/wiki/AlignIO

======================================================================================================
'''


def ConvertMSA(args):

    aln_in =            args['i']
    aln_in_format =     args['fi']
    aln_out =           args['o']
    aln_out_format =    args['fo']
    AlignIO.convert(aln_in, aln_in_format, aln_out, aln_out_format)

if __name__ == '__main__':

    # initialize the options parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',      required=True,   help='input alignment')
    parser.add_argument('-fi',     required=True,   help='format of input alignment')
    parser.add_argument('-o',      required=True,   help='output alignment')
    parser.add_argument('-fo',     required=True,   help='format of output alignment')
    args = vars(parser.parse_args())
    ConvertMSA(args)
