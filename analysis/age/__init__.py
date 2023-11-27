"""
공공데이터포털 API로 수집한 데이터를 분석하기 위한 패키지입니다.
"""
class BasicArgument:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
