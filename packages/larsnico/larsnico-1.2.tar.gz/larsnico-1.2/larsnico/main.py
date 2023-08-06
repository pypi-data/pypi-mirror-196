import click
import os

@click.command()
def main():
    # print('Hola pack larsnico')
    print(f'el path:: {os.getcwd()}')
    # open('nico.txt', 'a')
    # open('../nico.txt', 'a')
    pass

if __name__ == '__main__':
    main()