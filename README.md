# 다양성 평가 리포트 웹사이트 - 뉴웨이즈
<!-- # 깃헙은 최종일에 제출 필요!
- 팀별 GitHub repository 링크 및 발표 자료 Slack으로 제출
- GitHub 포함 사항
  - 재현 가능한 전체 개발 코드
  - README.md
    - 간단한 문제 정의와 해결책 설명
    - 사용 가능한 데모 링크 (웹사이트 링크나 실행가능한 Google colab 파일 등)
    - 설치 및 실행 과정 설명
    - 팀 및 팀원 소개
    - (선택 사항) 데모 영상 -->
## 프로젝트 개요
프로젝트 이름  다양성 평가 리포트 웹사이트 - 뉴웨이즈
기간          23 가을-겨울

## 설치 및 실행 과정
1. 파이썬 가상환경 생성
    - 아래 명령을 실행하여 파이썬 가상환경을 생성합니다.
    ```bash
    cd ~ && virtualenv newways --python=3.10
    ```
2. 가상환경 활성화
    - 아래 명령을 실행하여 가상환경을 활성화합니다.
    ```bash
    source ~/newways/bin/activate
    ``` 
3. 레포지토리 클론
   - 아래 명령을 실행하여 레포지토리를 클론합니다.
   ```bash
    git clone https://github.com/NewWays-TechForImpactKAIST/API-scrap-and-analysis.git
    ```
4. 필요한 패키지 설치
   - requirements.txt에 명시된 패키지를 설치합니다.
   ```bash
    pip install -r requirements.txt
    ```
5. 환경 변수 설정
   - `.env.example` 파일을 복사하여 `.env` 파일을 생성합니다.
   ```bash
    cp .env.example .env
    ```
    - `.env` 파일을 열어 환경 변수의 값을 필요에 따라 바꾸어줍니다. 
6. 예제 코드 실행
   - 이 프로젝트는 여러 개의 파이썬 패키지로 구성되어 있습니다.
   - 각각의 패키지는 독립적으로 실행할 수 있습니다. 단, 실행 시 python -m 옵션(module을 의미)을 사용해야 합니다.
   - 크롤링 및 데이터베이스 저장 예제 코드를 실행하려면, 아래 명령을 실행합니다.
    ```bash
      # scrap/local_councils/seoul/junggu.py 파일을 실행합니다.
      python -m scrap.local_councils.seoul.junggu
      # scrap/examples/database.py 파일을 실행합니다.
      python -m scrap.examples.database
      ```