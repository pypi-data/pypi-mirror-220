import click
import os
import glob
from gptask.conf import setup, load_prompts
from gptask.git_checker import is_staged
from gptask.openai_gptask import run


def check_file_staged_status(file, force):
    if not force and is_staged(file.name):
        click.echo(f"File {file.name} has staged changes. Please unstage the file before running gptask.")
        return False
    return True


def get_files_to_process(recursive, file):
    if file:
        return [file]
    if recursive:
        return [open(f, 'r') for f in glob.glob(recursive, recursive=True)]
    click.echo("Either a file or directory must be provided.")
    return []


def get_prompt_contents(prompt, all_prompts):
    if(".gptask" in prompt):
        return all_prompts[prompt[:-7]]
    else:
        return all_prompts[prompt]


@click.command()
@click.option('-p', '--prompt', help='Prompts in ~/.gptask/prompts')
@click.option('-f', '--force', is_flag=True, help='Force execution even if conditions are not met')
@click.option('-r', '--recursive', type=click.STRING, help='Directory with files to be processed')
@click.argument('file', type=click.File('r'), required=False)
def main(prompt, force, recursive, file):
    setup()

    files_to_process = get_files_to_process(recursive, file)
    if not files_to_process:
        return

    if not all(check_file_staged_status(f, force) for f in files_to_process):
        return

    click.echo(f"The following files will be processed: {[f.name for f in files_to_process]}")
    if not click.confirm("Do you want to continue?", default=True):
        return

    all_prompts = load_prompts()
    if prompt not in all_prompts:
        click.echo(f"Prompt {prompt} not found")
        return

    prompt_contents = get_prompt_contents(prompt, all_prompts)

    for file in files_to_process:
        click.echo(f"Formatting file: {file.name}")
        file_contents = file.read()
        res = run(prompt_contents, file.name, file_contents)
        with open(file.name, 'w') as f:
            f.write(res)
        file.close()


if __name__ == '__main__':
    main()
