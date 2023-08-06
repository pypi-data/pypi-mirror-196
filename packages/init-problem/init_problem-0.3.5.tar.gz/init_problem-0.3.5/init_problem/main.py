import click
import os
import time


from .chapters import chapters_list
from .problem import Problem
from .choice_option import ChoiceOption

path_parent = os.environ["TEX_PARENT_PATH"] 

eqn_number_without_database = f'{int(time.strftime("%H%M%S%d%m%Y")):14}'


size_square = f'\\geometry{{\npaperwidth=5in, \npaperheight=5in, \ntop=15mm, \nbottom=15mm, \nleft=10mm, \nright=10mm\n}}\n\n'
size_h_rectangle = f'\\geometry{{\npaperwidth=8in, \npaperheight=4.5in, \ntop=15mm, \nbottom=15mm, \nleft=10mm, \nright=10mm\n}}\n\n'
size_v_rectangle = f'\\geometry{{\npaperwidth=4.5in, \npaperheight=8in, \ntop=15mm, \nbottom=15mm, \nleft=10mm, \nright=10mm\n}}\n\n'

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(
        context_settings = CONTEXT_SETTINGS,
        help="Creates problem format tex file"
        )
@click.option(
        '-c',
        '--chapter',
        prompt='Chapters',
        type=click.Choice(
            chapters_list,
            case_sensitive=False),
        cls=ChoiceOption,
        help="Chapter name",
        )
@click.option(
        '-f',
        '--format_problem',
        prompt='Format',
        default=1,
        type=click.Choice(['JEE', 'IIT-JEE', 'NEET', 'BOOK', 'MINE']),
        cls=ChoiceOption,
        help='Format of the problem'
        )
@click.option(
        '-s',
        '--size',
        prompt='Size',
        default=1,
        type=click.Choice(['square', 'h-rectangle', 'v-rectangle']),
        cls=ChoiceOption,
        show_default=True,
        help="Size of the canvas"
        )
@click.option(
        '-n',
        '--problem_number',
        type=click.INT
        )
@click.option(
        '-a',
        '--append_to_database',
        is_flag=True,
        default=True,
        prompt=True,
        help="flag (-a turns-on) appends the equation to database"
        )
def main(chapter, format_problem, size, problem_number, append_to_database):
    problem = Problem(format_problem.lower(), chapter, path_parent)
    if append_to_database:
        try:
            problem_number = problem.get_data(1)[0][0] + 1
        except:
            problem_number = 1
        problem.insert_data()
    else:
        problem_number = eqn_number_without_database

    path_problem= os.path.join(
            problem.path_problem_format(),
            f'problem-{problem_number:02}'
            )


    os.makedirs(path_problem, exist_ok=True)
    main_tex = os.path.join(path_problem, 'main.tex')
    with open(main_tex, 'w') as file:
        file.write(f'\\documentclass{{article}}\n')
        file.write(f'\\usepackage{{v-problem}}\n')
        if size == 'square':
            file.write(size_square)
        elif size == 'h-rectangle':
            file.write(size_h_rectangle)
        elif size == 'v-rectangle':
            file.write(size_v_rectangle)

        file.write(f'\\begin{{document}}\n')
        file.write(f'\\vtitle[{chapter.upper()}]\n\n')
        file.write(f'\\vproblem[{problem_number}][This is a problem.][2022]\n\n')
        file.write(f'\\vspace*{{\\fill}}\n\n')
        file.write(f'\\begin{{center}}\n')
        file.write(f'\\begin{{tikzpicture}}\n')
        file.write(f'\t\\pic at (0, 0){{frame=8cm}};\n')
        file.write(f'\\end{{tikzpicture}}\n')
        file.write(f'\\end{{center}}\n\n')
        file.write(f'\\vspace*{{\\fill}}\n\n')
        file.write(f'\\voption[\n\\begin{{tasks}}(2)\n\\task\n\\task\n\\task\n\\task\n\\end{{tasks}}\n]\n\n')
        file.write(f'\\end{{document}}\n')


    os.system(f'bat {main_tex}')
    time.sleep(1)
    os.system(f'open -a texmaker {main_tex}')
    print('\n\topening texmaker ...\n')
    time.sleep(1)



