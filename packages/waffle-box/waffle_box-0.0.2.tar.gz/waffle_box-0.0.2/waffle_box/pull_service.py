from maker_manager import MakerManager

from pathlib import Path

class PullService:
    """ Waffle Maker 이미지 설치

    Target Autocare-D 버전에 맞춰 Waffle Maker 이미지를 설치한다.

    # 실행 순서
    1. is_local_maker_installed
        Waffle Maker가 local pc에 설치되어 있는지 확인한다.
    2. (Optional) set_login_info
        필요하다면 docker hub에 로그인할 정보를 설정한다.
    3. pull_image_to_local
        이미지를 로컬 pc에 다운로드 한다.

    # Attributes
    - dh_id
        - docker hub id
        - 빈값일 경우 로그인 시도를 하지 않는다.
    - dh_pw
        - docker hub password
        - 빈값일 경우 로그인 시도를 하지 않는다.
    - img_tag
        - 설치할 이미지 태그
    - maker_manager
        - MakerManager

    """

    def __init__(self, workspace: Path, dx_target_version: str) -> None:
        """
        # Parameters
        - workspace
            - 작업할 경로
        - dx_target_version
            - 타겟 Autocare-D 버전

        # Raises
            - MakerManagerException

        """
        # Docker Hub
        self.dh_id: str = ''
        self.dh_pw: str = ''

        # TODO: make image tag converter
        self.img_tag = 'snuailab/trt:8.5.2.2'

        self.maker_manager = MakerManager(self.img_tag, gpu_num=0, workspace=workspace)

    def is_local_maker_installed(self) -> bool:
        """ Waffle Maker 이미지가 로컬 pc에 설치되어 있는지 확인한다.
        """
        return self.maker_manager.check_image_exist_at_local()

    def set_login_info(self, id: str, pw: str) -> None:
        """ 로그인 정보 입력

        # Parameters
        - id
            - docker hub id
        - pw
            - docker hub password

        """
        self.dh_id = id
        self.dh_pw = pw

    def pull_image_to_local(self, print_output: bool) -> None:
        """ Waffle Maker 이미지를 로컬 pc에 설치

        # Parameters
        - print_output
            - 설치 과정 출력 여부

        # Raises
        - MakerManagerException

        """
        self.maker_manager.pull_image_at_local(print_output, self.dh_id, self.dh_pw)
