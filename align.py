import click
from gently.aligner import align_csv

@click.command()
@click.option('--filename', '-f')
@click.option('--delim', '-d', default='\t')
def main(filename, delim):
    align_csv(filename, delim)


if __name__ == "__main__":
    main()