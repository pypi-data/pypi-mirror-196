from parebrick.utils.data.parsers import parse_infercars_to_df
from parebrick.utils.data.stats import distance_between_blocks_distribution
from parebrick.utils.data.unique_gene_filters import filter_dataframe_unique

from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import argparse
import os


def blocks_length_dist(df):
    return [end_ - start_ for start_, end_ in zip(df['chr_beg'], df['chr_end'])]


def lengths_between(state, log):
    plt.figure()
    distance_between_2d = []
    for chr, df_chr in df.groupby('chr'):
        if state == 'after':
            df_filtered = filter_dataframe_unique(df_chr)
            ds = distance_between_blocks_distribution(df_filtered)
        else:
            ds = distance_between_blocks_distribution(df_chr)
        for d in ds:
            distance_between_2d.append([chr, d])

    distance_between_df = pd.DataFrame(data=distance_between_2d, columns=['chromosome', 'distance'])
    sns.histplot(distance_between_df, bins=50, log_scale=(False, log), x='distance', hue='chromosome', element="step", palette=['#da6f63', '#4a7ee5'])

    plt.ylabel('Number of blocks')
    plt.xlabel('Length in nucleotides')
    plt.title(f'Length of fragments not covered by {"common" if state == "after" else "any"} blocks')

    plt.tight_layout()
    plt.xlim(xmin=0)

    plt.savefig(out_folder + f'lengths_between_{state}_filtering{"_log" if log else ""}.pdf')
    # plt.show()


def get_most_probable_block(df_block):
    cnt = Counter(df_block.chr)
    if len(cnt) == 1:
        return cnt.most_common(1)[0][0]
    else:
        (most1, freq1), (most2, freq2) = cnt.most_common(2)
        return most1 + ';' + most2

def number_of_genomes_weighted(weighted, log):
    plt.figure()
    vs, ws, chroms = [], [], []

    for _, df_block in df.groupby('block'):
        # print(_, get_most_probable_block(df_block))
        vs.append(len(df_block.species.unique()))
        chroms.append(get_most_probable_block(df_block))
        lens = [e - s for s, e in zip(df_block['chr_beg'], df_block['chr_end'])]
        ws.append(np.mean(lens))

    df_draw = pd.DataFrame([[v, chr] for v, chr in zip(vs, chroms)], columns=['genomes', 'chromosome'])

    bins = 50 if max(vs) > 50 else max(vs)
    if weighted:
        # plt.hist(vs, bins=bins, weights=ws, log=log, alpha=0.7)
        sns.histplot(df_draw, x='genomes', weights=ws, hue='chromosome', bins=bins, log_scale=(False, log), element="step")
    else:
        # sns.histplot(vs, bins=bins, log_scale=(False, log), kde_kws={'alpha': 0.7})
        df_draw['chromosome'] = [c if c != '2;1' else '1;2' for c in df_draw['chromosome']]
        sns.histplot(df_draw, x='genomes', hue='chromosome', bins=bins, log_scale=(False, log), element="step",
                     palette={'1':'#da6f63', '2':'#4a7ee5', '1;2': '#a663da'})

    plt.ylabel('Length of fragments that are present\n in n genomes, nucleotides'
               if weighted else 'Number of blocks')
    plt.xlabel('Number of genomes')
    plt.title(f'{"Weighted f" if weighted else "F"}requency of synteny blocks')
    # plt.legend(loc='best')

    plt.xlim(xmin=0, xmax=max(vs))
    plt.tight_layout()
    plt.savefig(out_folder + f'blocks_frequency{"_weighted" if weighted else ""}{"_log" if log else ""}.pdf')
    # plt.show()


def block_length(log):
    plt.figure()
    df['length'] = df.chr_end - df.chr_beg

    sns.histplot(df, x='length', hue='chr', bins=50, log_scale=(False, log), element="step")

    plt.ylabel('Number of blocks')
    plt.xlabel('Length in nucleotides')
    plt.xlim(xmin=0)
    plt.title(f'Distribution of synteny blocks length')

    # plt.legend(loc=1)

    plt.tight_layout()
    plt.savefig(out_folder + f'block_lengths_distribution{"_log" if log else ""}.pdf')
    # plt.show()


def scatter_len_genomes_count():
    plt.figure()

    d2 = []
    for block, df_block in df.groupby('block'):
        lens = [row['chr_end'] - row['chr_beg'] for _, row in df_block.iterrows()]
        d2.append([len(df_block.species.unique()), np.mean(lens), get_most_probable_block(df_block)])

    draw_df = pd.DataFrame(d2, columns=['Number of genomes', 'Mean length of block', 'Chromosome'])
    sns.scatterplot(data=draw_df, x='Number of genomes', y='Mean length of block', hue='Chromosome', s=10)

    plt.title(f'Occurrence of synteny blocks vs its length')

    plt.tight_layout()
    plt.savefig(out_folder + f'scatter_number_length.pdf')


def pan_blocks(permutations=1000):
    pan_2d = []
    for chr, df_chr in df.groupby('chr'):
        block_sets = [set(df_sp.block.unique()) for _, df_sp in df_chr.groupby('species')]

        for _ in range(permutations):
            block_sets = np.random.permutation(block_sets)
            accumulate_set = set()
            accumulate_set_intersect = set(df_chr.block.unique())
            for i, bs in enumerate(block_sets):
                left = bs - accumulate_set
                accumulate_set |= bs
                accumulate_set_intersect &= bs

                pan_2d.append([chr, i + 1, len(left), len(accumulate_set), len(accumulate_set_intersect)])

    pan_df = pd.DataFrame(pan_2d, columns=['chr', 'strains', 'new blocks', 'pan blocks', 'core blocks'])

    def draw(column):
        plt.figure()
        sns.lineplot(data=pan_df, x='strains', y=column, hue="chr", ci='sd')
        plt.tight_layout()
        plt.savefig(out_folder + column.replace(' ', '_') + '.pdf')

    draw(column='new blocks')
    draw(column='pan blocks')
    draw(column='core blocks')


def pan_blocks_length(permutations=100):
    def get_genome_length(cnt):
        return sum(c * block_to_len[b] for b, c in cnt.items())

    block_to_len = {b: np.mean(df_b.chr_end - df_b.chr_beg) for b, df_b in df.groupby('block')}

    pan_2d = []
    for chr, df_chr in df.groupby('chr'):
        block_cnts = [Counter(df_sp.block.values) for _, df_sp in df_chr.groupby('species')]

        for _ in range(permutations):
            block_cnts = np.random.permutation(block_cnts)
            accumulate_cnt = Counter()
            max_occ = df_chr.groupby(['block', 'species']).size().groupby(level='block').max()
            accumulate_cnt_intersect = Counter({i: v for i, v in max_occ.items()})

            for i, bs in enumerate(block_cnts):
                left = bs - accumulate_cnt
                accumulate_cnt |= bs
                accumulate_cnt_intersect &= bs

                pan_2d.append([chr, i + 1,
                               get_genome_length(left),
                               get_genome_length(accumulate_cnt),
                               get_genome_length(accumulate_cnt_intersect)])

    pan_df = pd.DataFrame(pan_2d, columns=['chr', 'strains', 'new blocks', 'pan blocks', 'core blocks'])

    def draw(column):
        plt.figure()
        sns.lineplot(data=pan_df, x='strains', y=column, hue="chr", ci='sd')
        plt.tight_layout()
        plt.savefig(out_folder + column.replace(' ', '_') + '_length.pdf')

    draw(column='new blocks')
    draw(column='pan blocks')
    draw(column='core blocks')

def main():
    global out_folder, df

    parser = argparse.ArgumentParser(
        description='Building charts for pan-genome analysis based on synteny blocks.')

    parser.add_argument('--infercars_file', '-f', required=True,
                      help='Path to file in infercars format, can be found in main script output')

    parser.add_argument('--output', '-o', default='parebrick_charts', help='Path to output folder.')

    args = parser.parse_args()
    d = vars(args)

    file, out_folder = d['infercars_file'], d['output']

    if out_folder[-1] != '/': out_folder += '/'
    os.makedirs(out_folder, exist_ok=True)

    df = parse_infercars_to_df(file)

    sns.set(style="whitegrid", font="serif", font_scale=1.15)

    print('Plotting lengths between blocks')
    lengths_between('before', log=False)
    lengths_between('after', log=False)

    print('Plotting number of genomes in blocks')
    number_of_genomes_weighted(weighted=False, log=False)
    # number_of_genomes_weighted(weighted=True, log=False)

    print('Plotting blocks length distribution')
    block_length(log=False)

    print('Plotting scatter for occurrence of synteny blocks vs its length')
    # scatter_len_genomes_count()

    print('Plotting pan-genome plots')
    pan_blocks()
    pan_blocks_length()

if __name__ == "__main__":
    main()