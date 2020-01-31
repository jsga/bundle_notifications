"""Console script for bundle_notifications package.______"""
import sys
import click
from .bundle_notifications import load_data, bundle_func

@click.command()
@click.option('--path', '-p',default="https://static-eu-komoot.s3.amazonaws.com/backend/challenge/notifications.csv",type=click.STRING, help='Path to csv file.')
@click.option('--nrows','-n', default=50, type=click.int, help='Number of rows to print to stout')
def main(path_csv, nrows):
    """ Download data and bundles notifications

    Parameters
    ----------
    path_csv : str
        path to csv file. Could be a url.

    nrows : int
        Number of rows to print to stout. Default = 50

    """

    # Load dataset
    click.echo(click.style('Dwnloading data...', fg='green'))
    df = load_data(path_csv = path_csv)

    click.echo(click.style('Bundling notifications...', fg='green'))
    # The data needs to be sorted by date
    df.sort_values('timestamp', inplace=True)

    # Bundle notifications
    df = df.groupby('user_id').apply(bundle_func)

    # Print to stout
    click.echo(click.style('Great! Here there are the bundled notifications', fg='green'))
    click.echo(df.head(nrows))

    return 0


if __name__ == "__main__":
    #sys.exit(main())  # pragma: no cover
    main()
