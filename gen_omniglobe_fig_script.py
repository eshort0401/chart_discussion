import ACCESS_G_figures
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '--min', '-m', type=int, default=1,
    help='starting index')
parser.add_argument(
    '--max', '-M', type=int, default=240,
    help='starting index')

args = parser.parse_args()

ACCESS_G_figures.gen_omniglobe_figs(i_min=args.min, i_max=args.max)
