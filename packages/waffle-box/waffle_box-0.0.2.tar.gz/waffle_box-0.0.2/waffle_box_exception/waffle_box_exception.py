from enum import Enum


class ExceptionCode(Enum):
    """ Waffle Box에서 생성하는 예외 리스트

    Waffle Box에서 생성하는 예외 리스트.

    100 ~ : docker에서 발생한 예외 \n
    200 ~ : app에서 발생한 예외

    # Attributes
    - DOCKER_EXCEPTION
        - docker에서 발생한 예외
    - APP_STRUCTURE_EXCEPTION
        - app에서 발생한 예외

    """

    DOCKER_EXCEPTION = (100, 'DOCKER_EXCEPTION')
    DOCKER_IMAGE_EXCEPTION = (101, 'DOCKER_IMAGE_EXCEPTION')
    DOCKER_RUN_EXCEPTION = (102, 'DOCKER_RUN_EXCEPTION')

    MODEL_IO_EXCEPTION = (103, 'IO_EXCEPTION')
    MODEL_CONVERT_EXCEPTION = (104, 'MODEL_CONVERT_EXCEPTION')

    APP_STRUCTURE_EXCEPTION = (200, 'APP_STRUCTURE_EXCEPTION')
    APP_NO_SUCH_FILE = (201, 'APP_NO_SUCH_FILE')
    APP_FILE_ALREADY_EXIST = (202, 'APP_FILE_ALREADY_EXIST')
    APP_CONFIG_ERROR = (203, 'APP_CONFIG_ERROR')

    def __init__(self, code, desc) -> None:
        super().__init__()

        self._code: int = code
        self._desc: str = desc

    @property
    def code(self) -> int:
        return self._code

    @property
    def desc(self) -> str:
        return self._desc


class WaffleBoxException(Exception):
    def __init__(self, msg: str, code: ExceptionCode) -> None:
        super().__init__(msg)

        self._msg = msg
        self._code = code

    def __str__(self) -> str:
        return f'[{self._code.desc}]: {self._msg}'

    @property
    def code(self) -> int:
        return self._code.code
