from fastpurge import FastPurgeClient
import click


@click.command()
@click.option('paths', '--path', '-p', multiple=True, help="A single URL to Purge (This option is repeatable for additional URLs)")
@click.option('--dryrun', '-d', is_flag=True, help="Just print the command and args that will be run and exit")

def purge(paths: list[str], dryrun: bool):
  # Omit credentials to read from ~/.edgerc
  client = FastPurgeClient()
  if dryrun:
    print('These paths will be purged:')
    for path in paths:
      click.echo(path)
  else:

    # Start purge of some URLs
    purge = client.purge_by_url(paths)
    # purge is a Future, if we want to ensure purge completed
    # we can block on the result:
    result = purge.result()
    # print("Purge completed:")
    print("Purge completed:", result)
  
if __name__ == "__main__":
  purge()
