import click
import pandas as pd
from main import run
from ..util.cli import *

@click.command()

@optgroup.group('I/O')
@fasta 
@input_dir
@opt_out_dir
@opt_library

@optgroup.group('Selection')
@coords
@primers
@fill

@optgroup.group('Clustering')
@opt_max_clusters
@min_iter
@signal_thresh
@info_thresh
@include_g_u
@include_del
@min_reads
@convergence_cutoff
@num_runs
@max_procs

@optgroup.group('Miscellaneous')
@verbose


def cli(**args):
    run(**args)

if __name__ == '__main__':
    run()
