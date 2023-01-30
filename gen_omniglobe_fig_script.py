import ACCESS_G_figures
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '--min', '-m', type=int, default=1,
    help='starting index')
parser.add_argument(
    '--max', '-M', type=int, default=240,
    help='starting index')
parser.add_argument(
    '--max', '-M', type=int, default=240,
    help='starting index')
parser.add_argument(
    '-w', '--winds', action='store_true', help='create wind plot')

args = parser.parse_args()

if args.winds:
    ACCESS_G_figures.gen_omniglobe_wind_mslp(i_min=args.min, i_max=args.max)
else:
    ACCESS_G_figures.gen_omniglobe_mslp_prcp_temp(
        i_min=args.min, i_max=args.max)
