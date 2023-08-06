import os
import click
import cv2
from dtais.AugTools import img_aug_tools

root_path = 'C://dtais/data/'


def get_files(input_file):
    if os.path.isabs(input_file):
        path = input_file
    else:
        path = root_path + input_file

    if os.path.isfile(path):
        return [path]
    else:
        files = os.listdir(path)
        for file in files:
            abs_file = os.path.abspath(file)
            print(abs_file)
        return files


@click.group()
def dtais():
    pass


@dtais.command()
@click.option('--input', '-i', 'input_file', required=True, type=str)
@click.option('--output', '-o', 'output', required=False, type=str)
@click.option('--percentage', 'percentage', required=True, type=float)
def saltAndPepper(input_file, output, percentage):
    files = get_files(input_file)
    click.echo('img aug function')
    if output is None:
        output = root_path + input_file + '_aug_by_saltAndPepper'
    else:
        output = root_path + input_file + output

    if not os.path.exists(output):
        os.mkdir(output)

    for file in files:
        file_path = root_path + input_file + '/' + file
        img = cv2.imread(file_path)
        img_salt = img_aug_tools.SaltAndPepper(img, percentage)
        cv2.imwrite(output + '/' + file[:-4] + '_salt.jpg', img_salt)


@dtais.command()
@click.option('--input', '-i', 'input_file', required=True, type=str)
@click.option('--output', '-o', 'output', required=False, type=str)
@click.option('--percentage', 'percentage', required=True, type=float)
def GaussianNoise(input_file, output, percentage):
    files = get_files(input_file)
    click.echo('img aug function')
    if output is None:
        output = root_path + input_file + '_aug_by_GaussianNoise'
    else:
        output = root_path + input_file + output

    if not os.path.exists(output):
        os.mkdir(output)

    for file in files:
        file_path = root_path + input_file + '/' + file
        img = cv2.imread(file_path)
        img_gauss = img_aug_tools.addGaussianNoise(img, percentage)
        cv2.imwrite(output + '/' + file[:-4] + '_gauss.jpg', img_gauss)


@dtais.command()
@click.option('--input', '-i', 'input_file', required=True, type=str)
@click.option('--output', '-o', 'output', required=False, type=str)
@click.option('--percentage', 'percentage', required=True, type=float)
def darker(input_file, output, percentage):
    files = get_files(input_file)
    click.echo('img aug function')
    if output is None:
        output = root_path + input_file + '_aug_by_darker'
    else:
        output = root_path + input_file + output

    if not os.path.exists(output):
        os.mkdir(output)

    for file in files:
        file_path = root_path + input_file + '/' + file
        img = cv2.imread(file_path)
        img_darker = img_aug_tools.darker(img, percentage)
        cv2.imwrite(output + '/' + file[:-4] + '_darker.jpg', img_darker)


@dtais.command()
@click.option('--input', '-i', 'input_file', required=True, type=str)
@click.option('--output', '-o', 'output', required=False, type=str)
@click.option('--percentage', 'percentage', required=True, type=float)
def brighter(input_file, output, percentage):
    files = get_files(input_file)
    click.echo('img aug function')
    if output is None:
        output = root_path + input_file + '_aug_by_brighter'
    else:
        output = root_path + input_file + output

    if not os.path.exists(output):
        os.mkdir(output)

    for file in files:
        file_path = root_path + input_file + '/' + file
        img = cv2.imread(file_path)
        img_brighter = img_aug_tools.brighter(img, percentage)
        cv2.imwrite(output + '/' + file[:-4] + '_brighter.jpg', img_brighter)


@dtais.command()
@click.option('--input', '-i', 'input_file', required=True, type=str)
@click.option('--output', '-o', 'output', required=False, type=str)
@click.option('--angle', 'angle', required=True, type=float)
def rotate(input_file, output, angle):
    files = get_files(input_file)
    click.echo('img aug function')
    if output is None:
        output = root_path + input_file + '_aug_by_rotate'
    else:
        output = root_path + input_file + output

    if not os.path.exists(output):
        os.mkdir(output)

    for file in files:
        file_path = root_path + input_file + '/' + file
        img = cv2.imread(file_path)
        img_rotate = img_aug_tools.rotate(img, angle)
        cv2.imwrite(output + '/' + file[:-4] + '_rotate.jpg', img_rotate)


@dtais.command()
@click.option('--input', '-i', 'input_file', required=True, type=str)
@click.option('--output', '-o', 'output', required=False, type=str)
def flip(input_file, output):
    files = get_files(input_file)
    click.echo('img aug function')
    if output is None:
        output = root_path + input_file + '_aug_by_flip'
    else:
        output = root_path + input_file + output

    if not os.path.exists(output):
        os.mkdir(output)

    for file in files:
        file_path = root_path + input_file + '/' + file
        img = cv2.imread(file_path)
        img_flip = img_aug_tools.flip(img)
        cv2.imwrite(output + '/' + file[:-4] + '_flip.jpg', img_flip)


if __name__ == '__main__':
    dtais()
