from dataclasses import dataclass
from waffle_box_exception import WaffleBoxException, ExceptionCode


@dataclass(frozen=True)
class ONNXConvConfigs:
    """ trt 엔진 변환을 위해 필요한 설정 값 정보

    # Attributes
    - precision
        - 모델의 precision
        - fp32, fp16, int8 중 하나
    - input_shape
        - 모델의 input shape
        - dynamic batch를 사용하기 위해 trtexec에 
        min, opt, max input shape을 입력할 때 사용
    - max_batch
        - 모델의 최대 batch 크기
        - min, opt, max input shape의 batch 크기를 결정할 때 사용

    """

    precision: str
    input_shapes: str
    max_batch: int

    def to_trtexec_args(self) -> list[str]:
        """ trtexec 변환에 필요한 argument 리스트로 변환

        ONNXConvConfigs의 값을 trtexec 변환에 필요한 argument 리스트로 변환한다.

        # precision
        trtexec의 precision 기본값은 fp32이므로 fp32일때는 아무런 옵션을 생성하지 않는다.
        fp16일 경우 --fp16, int8일 경우 --int8을 리턴한다.

        # input_shape & max_batch
        dynamic batch를 사용하기 위해 min, opt, max shape을 설정해야 한다.  
        모델의 input_shape은 그대로 사용하며 batch size는 min=1, opt=max_batch/2, max=max_batch로 설정한다.

        # output_name
        App의 원본 엔진파일 이름을 맞추기 위해 설정한다.
        --saveEngine=<output_name>

        """

        args: list[str] = []

        # precision
        if self.precision == 'fp16':
            args.append('--fp16')
        elif self.precision == 'int8':
            args.append('--int8')
        elif self.precision != 'fp32':
            raise WaffleBoxException(
                f'Invalid precision: {self.precision}', ExceptionCode.APP_CONFIG_ERROR)

        # dynamic batch
        # 구체적인 layer 이름이 필요하지만 현재는 inputs 레이어 한개만 있다 가정
        # min
        args.append(f'--minShapes=inputs:1x{self.input_shapes}')

        # opt
        if self.max_batch > 2:
            args.append(
                f'--optShapes=inputs:{int(self.max_batch/2)}x{self.input_shapes}')

        # max
        args.append(
            f'--maxShapes=inputs:{int(self.max_batch)}x{self.input_shapes}')

        return args
