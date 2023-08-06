from app_manager import ModelInfo, AppStructure
from app_manager import NvinferConfigParser
from waffle_box_exception import WaffleBoxException, ExceptionCode

import os
import shutil
from pathlib import Path
from uuid import UUID
from zipfile import ZipFile
import json


class AppManager:
    """ Base App을 파싱하고 새로운 App을 생성

    Base App을 파싱 후 모델을 교체해 새로운 App을 생성한다.

    # Attributes
    - workspace: Path
        - 작업할 경로
        - 일반적으로 ~/.waffle_box
    - app_structure: AppStructure
        - 작업할 App의 구조

    """

    def __init__(self, workspace: Path, app_path: Path) -> None:
        """
        # Parameters
        - workspace: Path
            - 작업할 경로
        - app_path: Path
            - Base 앱 경로

        # Raises
        - IOError
            - workspace를 생성할 수 없음
        - AppParsingError
            - App parsing error

        # Raises
        - APP_STRUCTURE_EXCEPTION
        - APP_CONFIG_ERROR

        """
        self.workspace: Path = workspace

        self._app_structure: AppStructure = self._extract_app(app_path)

    def _extract_app(self, app_path: Path) -> AppStructure:
        """ App 파일을 압축 해제하고 구조를 분석한다.

        입력받은 App 파일을 workspace의 temp 폴더에 압축 해제한다.
        만약 temp 파일이 이미 존재한다면 폴더를 삭제하고 압축을 새로 해제한다.

        App 파일 내부 모델도 모두 압축 해제 후 
        model info를 담은 AppStructure를 반환한다.

        # Raises
        - APP_STRUCTURE_EXCEPTION
        - APP_CONFIG_ERROR

        """
        if not app_path.exists():
            raise WaffleBoxException('Wrong input file.', ExceptionCode.APP_NO_SUCH_FILE)
        
        # app 압축을 풀 임시 폴더
        temp_dir = self.workspace.joinpath('temp')

        if temp_dir.exists():
            shutil.rmtree(temp_dir)

        zip_file = ZipFile(app_path)
        zip_file.extractall(temp_dir)

        # read app.json
        app_json_f = open(temp_dir.joinpath('app.json'))
        app_json = json.load(app_json_f)

        app_id: UUID = UUID(app_json['id'])

        model_info_list: list[ModelInfo] = []

        if not app_json.get('models') or len(app_json['models']) == 0:
            raise WaffleBoxException(
                'There is no model in app.', ExceptionCode.APP_STRUCTURE_EXCEPTION)

        # walk models
        for model in app_json['models']:
            try:
                model_id = model['id']
                model_name = model['name']
                model_precision = model['precision']
                model_zip_path = temp_dir.joinpath(model['path'])
            except KeyError as e:
                raise WaffleBoxException(
                    f'In app.json, no such key: {e}', ExceptionCode.APP_CONFIG_ERROR)
            except Exception as e:
                raise WaffleBoxException(
                    str(e), ExceptionCode.APP_STRUCTURE_EXCEPTION)

            model_path = self._extract_model(model_zip_path)

            model_info = self._make_model_info(
                model_path=model_path, model_id=model_id,
                model_name=model_name, model_precision=model_precision
            )

            model_info_list.append(model_info)

        app_structure = AppStructure(
            id=app_id, models=model_info_list, path=temp_dir,
        )

        return app_structure

    def _extract_model(self, model_path: Path) -> Path:
        """ 모델 압축 풀기

        모델 파일은 zip 파일 이름과 동일한 이름의 폴더에 압축을 푼다.
        예) PeopleNet.zip -> PeopleNet 폴더에 압축 풀기

        압축을 풀면 zip 파일을 삭제한다.

        # Return
        - 모델 파일을 압축 푼 위치

        """
        model_dir = self._remove_extention(model_path.name)
        model_dir = model_path.parent.joinpath(model_dir)

        zip_file = ZipFile(model_path)
        zip_file.extractall(model_dir)
        zip_file.close()

        os.remove(model_path)

        return model_dir

    def _make_model_info(self, model_path: Path, model_id: UUID,
                         model_name: str, model_precision: str) -> ModelInfo:
        """ 압축 푼 모델 폴더에서 정보를 추출한다.

        압축 푼 모델 폴더의 infer_nvinfer_config.txt 파일을 읽고
        필요한 정보들을 추출한다.

        # Raises
        - APP_CONFIG_ERROR

        """
        nvinfer_parser = NvinferConfigParser(
            model_path.joinpath('infer_nvinfer_config.txt'))

        engine_file_name = nvinfer_parser.get('model-engine-file')
        if not engine_file_name:
            raise WaffleBoxException('In infer_nvinfer_config.txt, no such key model-engine-file',
                                     ExceptionCode.APP_CONFIG_ERROR)

        input_dims = nvinfer_parser.get('infer-dims')
        if not input_dims:
            raise WaffleBoxException('In infer_nvinfer_config.txt, no such key infer-dims',
                                     ExceptionCode.APP_CONFIG_ERROR)
        input_dims = input_dims.replace(';', 'x')

        batch_size = nvinfer_parser.get('batch-size')
        if not batch_size:
            raise WaffleBoxException('In infer_nvinfer_config.txt, no such key batch-size',
                                     ExceptionCode.APP_CONFIG_ERROR)
        batch_size = int(batch_size)

        return ModelInfo(
            id=model_id, name=model_name, precision=model_precision,
            engine_file_name=engine_file_name, input_dims=input_dims,
            max_batch_size=batch_size, path=model_path,
        )

    def _remove_extention(self, file_name: str) -> str:
        """ 파일 이름에서 마지막 확장자 명을 제거한다.
        """
        return file_name[:file_name.rfind('.')]

    def replace_model(self, model_id: UUID, new_model: Path) -> None:
        """ 모델의 trt 엔진 파일을 교체한다.

        입력한 id에 해당하는 모델의 trt 엔진 파일을 새로운 trt 엔진 파일로 교체한다.

        # Parameters
        - model_id
        - new_model

        # Raises
        - APP_NO_SUCH_FILE
            - 기존 모델의 엔진 파일이 존재하지 않음
            - 새로운 모델 파일이 존재하지 않음

        """
        model = self._app_structure.find_model_by_id(model_id)

        if not model:
            raise WaffleBoxException(
                f'No such model: ID - {model_id}', ExceptionCode.APP_NO_SUCH_FILE)

        # 기존 모델 파일 확인
        origin_model = model.path.joinpath(model.engine_file_name)
        if not origin_model.exists():
            raise WaffleBoxException(
                f'No such file: {origin_model}', ExceptionCode.APP_NO_SUCH_FILE)

        # 새로운 모델 파일 확인
        if not new_model.exists():
            raise WaffleBoxException(
                f'No such file: {new_model}', ExceptionCode.APP_NO_SUCH_FILE)

        # 모델 교체
        os.remove(origin_model)
        shutil.copyfile(new_model, origin_model)

    def package(self, output: Path) -> None:
        """ 새로운 App으로 생성한다.

        엔진 파일 교체가 끝나면 새로운 App으로 패키징한다.

        # Parameters
        - output
            - App 저장 경로

        # Raises
        - APP_FILE_ALREADY_EXIST
            - output 파일이 이미 존재함

        """
        if output.exists():
            raise WaffleBoxException(
                f'File already exists: {output}', ExceptionCode.APP_FILE_ALREADY_EXIST)

        for model in self._app_structure.models:
            shutil.make_archive(str(model.path), 'zip', str(model.path))
            shutil.rmtree(model.path)

        # shutil에서 .zip을 붙이므로 마지막에 .zip이 붙어있다면
        # 없앤 이름을 넣어준다.
        output_name = str(output)
        if len(output_name) > 4 and output_name[-4:] == '.zip':
            output_name = output_name[:-4]

        shutil.make_archive(output_name, 'zip', self._app_structure.path)

    @property
    def app_structure(self) -> AppStructure:
        """ App 구조를 반환한다.
        """
        return self._app_structure

    def find_model_info_by_id(self, id: UUID) -> ModelInfo | None:
        """ App의 모델 정보를 id로 찾는다.

        App의 모델 정보를 id로 찾는다. 
        만약 없다면 None을 리턴한다.

        """
        return self._app_structure.find_model_by_id(id)

    def find_model_info_by_name(self, name: str) -> ModelInfo | None:
        """ App의 모델 정보를 이름으로 찾는다.

        App의 모델 정보를 이름으로 찾는다.
        만약 없다면 None을 리턴한다.
        """
        return self._app_structure.find_model_by_name(name)

if __name__ == '__main__':
    ap = AppManager(Path('/'), Path('/'))
