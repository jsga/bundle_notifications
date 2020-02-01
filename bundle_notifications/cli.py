"""Console script for bundle_notifications package."""
import sys
import click
import tabulate
from .bundle_notifications import load_data, bundle_func

@click.command()
@click.option('-p','--path_csv' ,default="https://static-eu-komoot.s3.amazonaws.com/backend/challenge/notifications.csv",type=click.STRING, help='Path to csv file.',show_default=True)
@click.option('-n','--nrows_print', default=50, type=click.IntRange(min=0), help='Number of rows to print to stout',show_default=True)
def main(path_csv, nrows_print):
    """Download data, bundles notifications and prints solution to stdout
    """

    # Load dataset
    click.echo(click.style('Downloading data...', fg='green'))
    df = load_data(path_csv = path_csv)

    click.echo(click.style('Bundling notifications...', fg='green'))
    # The data needs to be sorted by date
    df.sort_values('timestamp', inplace=True)

    # Bundle notifications
    df = df.groupby('user_id').apply(bundle_func)

    # Print to stout
    click.echo(click.style('Great! Here there are the bundled notifications', fg='green'))
    click.echo(tabulate.tabulate(df.head(nrows_print), df.columns ,showindex=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

