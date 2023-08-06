from maker_manager import MakerManager, ONNXConvConfigs

from pathlib import Path


class BakeService:
    """ ONNX 모델을 trt 엔진으로 변환

    사용자가 입력한 ONNX 모델을 타겟 Autocare-D 버전에 맞춰 trt 엔진 파일로 변환한다.

    # 실행 순서
    1. is_local_maker_installed
        Waffle Maker 이미지가 로컬에 설치되어 있는지 확인한다.
    2. convert_model
        모델을 trt 엔진으로 변환한다.

    # Attributes
    - workspace
        - 작업할 경로
        - 일반적으로 ~/.waffle_box
    - origin_app_path
        - 사용자가 입력한 기존 App 경로
    - final_app_path
        - 새로운 App을 저장할 경로
    - img_tag
        - trt 변환을 위한 컨테이너 태그명
    - maker_manager
        - MakerManager

    """

    def __init__(self, workspace: Path, input: Path, output: Path, dx_target_version: str, gpu_num: int) -> None:
        """
        # Parameters
        - workspace
            - 작업할 경로
        - input
            - 변환할 모델 경로
        - output
            - 변환한 trt 엔진 파일을 저장할 경로
        - dx_target_version
            - 변환할 App의 target Autocare-D 버전
        - gpu_num
            - 작업할 GPU 번호

        # Raises
        - MakerManagerError

        """
        self.workspace: Path = workspace
        self.origin_model_path: Path = input
        self.final_model_path: Path = output

        # TODO: make image tag converter
        self.img_tag = 'snuailab/trt:8.5.2.2'

        self.maker_manager = MakerManager(self.img_tag, gpu_num=gpu_num)

    def is_local_maker_installed(self) -> bool:
        """ Waffle maker가 local에 설치되어 있는가?
        """
        return self.maker_manager.check_image_exist_at_local()

    def convert_model(self, print_output: bool, precision: str) -> None:
        """ 모델 변환

        # Parameters
        - print_output
            - 변환 과정 출력 여부
        - precision
            - 모델의 precision
            - fp32, fp16, int8 중 하나

        # Raises
        - MakerManager

        """
        onnx_config = ONNXConvConfigs(precision=precision)
        self.maker_manager.convert_onnx_to_engine_at_local(input=self.origin_model_path,
                                                           output=self.final_model_path,
                                                           convert_config=onnx_config,
                                                           print_output=print_output)
