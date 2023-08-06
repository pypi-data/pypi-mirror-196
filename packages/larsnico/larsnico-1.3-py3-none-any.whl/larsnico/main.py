import os
import time
import click

@click.command()
@click.option('--file', '-f', help='Name of the file', required=True)
def main(file):
    s_i = os.path.getsize(file)

    while True:
        s_n = os.path.getsize(file)
        if s_i != s_n:
            # run prog
            os.system('clear')
            print(f'Running: {file} - {s_i} bytes.')
            print(f'>>>\n')
            os.system(f'python3 {file}')
        s_i = os.path.getsize(file)
        time.sleep(1)


if __name__ == '__main__':
    main()