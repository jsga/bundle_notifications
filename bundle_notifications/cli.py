"""Console script for bundle_notifications package."""
import sys
import click
import tabulate
from .bundle_notifications import load_data, bundle

@click.command()
@click.option('-p','--path_input_csv' ,default = "https://static-eu-komoot.s3.amazonaws.com/backend/challenge/notifications.csv", type = click.STRING, help='Input path to csv file.',show_default = True)
@click.option('-o','--path_output_csv' ,default = "bundle_notifications.csv", type = click.STRING, help='Output path to csv file.', show_default = True)
@click.option('-n','--nrows_print', default = 50, type = click.IntRange(min=0), help = 'Number of rows to print to stout', show_default = True)
def main(path_input_csv, path_output_csv, nrows_print):
    """Download data, bundles notifications and prints solution to stdout
    """

    # Load dataset
    click.echo(click.style('Downloading data...', fg = 'green'))
    df = load_data(path_csv = path_input_csv)

    # Give an approximate execution time
    approx_time = df.shape[0]*(60*6)/330000
    approx_text = f"Bundling notifications... (Estimated time: {approx_time:.2f} seconds for {df.shape[0]} rows)"
    click.echo(click.style(approx_text, fg='green'))

    # The data needs to be sorted by date. Then bundle.
    df.sort_values('timestamp', inplace=True)
    df = bundle(df)

    # Save to csv
    click.echo(click.style(f'Saving to csv: {path_output_csv}', fg='green'))
    df.to_csv(path_output_csv, index=False)

    # Print to stout
    click.echo(click.style(f'Great! Here there are the first {nrows_print} bundled notifications', fg='green'))
    click.echo(tabulate.tabulate(df.head(nrows_print), df.columns ,showindex=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

