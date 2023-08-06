import typer
from typing_extensions import Annotated
from pathlib import Path

from waffle_box.convert_service import ConvertService
from waffle_box.pull_service import PullService
from waffle_box_exception.waffle_box_exception import WaffleBoxException

app = typer.Typer()

# subcommand에 option 값 전달을 위한 dictionary
options = {
    'dx_target_version': '1.6.2',
    'gpu_num': 0,
}


@app.command('convert')
def cli_make_new_app(input: Annotated[str, typer.Argument(help="Base app file.")],
                     output: Annotated[str, typer.Option('-O', help="Output app file.")],
                     queit: Annotated[bool, typer.Option(help="Do not print anything.")] = False):
    """
    Make a new app from base app with input models.
    """
    home_dir = Path.home()
    workspace = home_dir.joinpath('.waffle_box')

    try:
        cv = ConvertService(workspace, Path(input), Path(
            output), options["dx_target_version"], options['gpu_num'])
    except WaffleBoxException as e:
        print(e)
        raise typer.Exit(-1)

    # Waffle maker가 설치되어 있는지 확인
    if not cv.is_local_maker_installed():
        print('Waffle maker is not installed.\nPlease execute wb pull first.')
        raise typer.Exit(-1)

    # 모델 정보 받아오기
    try:
        model_list = cv.get_model_info()
    except WaffleBoxException as e:
        print(e)
        raise typer.Exit(-1)
    except Exception as e:
        print(e)
        raise typer.Exit(-1)

    print('----- Model list -----')
    for model in model_list:
        print(f'ID: {model.id}')
        print(f'Name: {model.name}')
        new_model: str = typer.prompt(
            'Pass or Change [Pass(Enter)/Path]', default='')
        new_model = new_model.strip().replace('\n', '')

        if len(new_model) == 0:
            continue

        new_model_path = Path(new_model)

        if not new_model_path.exists():
            print('Wrong file. Please check again...')
            raise typer.Exit(-1)

        cv.add_convert_info(model.id, new_model_path)
        print()

    # start convert
    try:
        cv.convert_models(not queit)
    except WaffleBoxException as e:
        print(e)
        raise typer.Exit(-1)

    # make output app
    try:
        cv.package_app()
    except WaffleBoxException as e:
        print(e)
        raise typer.Exit(-1)

    print('Finished!')


@app.command('bake')
def cli_convert_onnx_to_engine(input: Annotated[str, typer.Argument(help="ONNX model input file.")],
                               output: Annotated[str, typer.Option('-O', help='TensorRT engine output file.')],
                               queit: Annotated[bool, typer.Option(help="Do not print anything.")] = False):
    """
    Convert ONNX file to TensorRT engine file.
    """
    print('Not implemented yet...')
    raise typer.Exit(-1)


@app.command('pull')
def cli_pull_waffle_maker_image(login: Annotated[bool, typer.Option(help="Login to docker hub.")] = False,
                                queit: Annotated[bool, typer.Option(help="Do not print anything.")] = False):
    """
    Pull waffle maker image.
    """
    home_dir = Path.home()
    workspace = home_dir.joinpath('.waffle_box')

    ps = PullService(workspace, options['dx_target_version'])

    # 이미지 설치 확인
    if ps.is_local_maker_installed():
        print("Waffle Maker is already installed.")
        raise typer.Exit()

    # 로그인 정보 입력
    if login:
        print('Docker Hub Login')
        id = typer.prompt('ID', show_choices=False)
        pw = typer.prompt('Password', hide_input=True, show_choices=False)
        ps.set_login_info(id, pw)

    # 이미지 다운로드
    try:
        ps.pull_image_to_local(not queit)
    except WaffleBoxException as e:
        print(e)
        raise typer.Exit(-1)


@app.callback()
def main(dx_target_version: Annotated[str, typer.Option('--dx-version',
                                                        help='Target Autocare-D version.')] = '1.6.2',
         gpu_num: Annotated[int, typer.Option('-G', help='GPU number to use.')] = 0):
    if dx_target_version:
        options['dx_target_version'] = dx_target_version

    options['gpu_num'] = gpu_num


if __name__ == '__main__':
    app()
