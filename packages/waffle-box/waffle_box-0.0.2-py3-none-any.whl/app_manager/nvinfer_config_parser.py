from pathlib import Path
from waffle_box_exception import WaffleBoxException, ExceptionCode


class NvinferConfigParser:
    """ nvinfer config 파일 분석

    정확한 trt 엔진 변환을하기 위해 nvinfer config 파일을 읽고
    변환 설정 값을 만들기 위해 사용된다.

    설정값 접근은 get함수로 config 파일의 key 값을 입력해 찾는다.
    key값이 없을 경우 Exception을 발생한다.

    # Attributes:
    - _configs
        - config값을 저장하는 dictionary

    """

    def __init__(self, file: Path) -> None:
        """
        # Parameters
        - file
            - config 파일 위치 
            - 예) /home/yoon/.waffle_box/temp/car_make_net_v0.1.0a/infer_nvinfer_config.txt

        """
        self._configs: dict[str, str] = {}

        self._read_config_file(file)

    def _read_config_file(self, file: Path) -> None:
        """ config 파일 파싱

        config 파일을 읽고 설정 값만 _configs에 저장한다.

        # Raises
        - APP_NO_SUCH_FILE
        - APP_CONFIG_ERROR

        """
        try:
            with open(file) as f:
                lines = f.readlines()

                for l in lines:
                    sp = l.split('=')

                    if len(sp) != 2:
                        continue

                    # remove white space and new line
                    self._configs[sp[0].strip()] = sp[1].strip().replace(
                        '\n', '')
        except FileNotFoundError as e:
            raise WaffleBoxException(
                f'No infer_nvinfer_config.txt file.', ExceptionCode.APP_NO_SUCH_FILE)
        except Exception as e:
            raise WaffleBoxException(
                f'Error while reading infer_nvinfer_config.txt: {e}', ExceptionCode.APP_CONFIG_ERROR)

    def get(self, key: str) -> str | None:
        """ config 값 읽어오기

        key를 통해 config 값을 읽어온다.
        key값이 존재하지 않을경우 None을 리턴한다.

        """
        return self._configs.get(key)
