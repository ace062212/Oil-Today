# Oil Today®

## 프로젝트 소개
Oil Today는 사용자 위치 기반으로 주변 주유소의 유가 정보를 제공하는 웹 서비스입니다. 이 프로젝트는 사용자가 현재 위치를 기반으로 가장 저렴한 주유소를 찾고, 최신 석유 관련 뉴스를 확인할 수 있는 서비스를 제공합니다.

## 주요 기능
- 사용자 위치 기반 주변 주유소 정보 제공
- 휘발유, 경유 등 다양한 유종별 가격 정보 확인
- 석유 관련 최신 뉴스 제공
- 7일간의 유가 데이터 분석 및 시각화

## 기술 스택
- **프론트엔드**: HTML, CSS, JavaScript
- **백엔드**: Flask (Python)
- **데이터 처리**: Python

## 설치 및 실행 방법
1. 저장소 클론하기
```bash
git clone https://github.com/your-username/oil-today.git
cd oil-today
```

2. 필요한 패키지 설치하기
```bash
pip install -r backend/requirements.txt
```

3. 서버 실행하기
```bash
python app.py
```

4. 웹 브라우저에서 접속하기
```
http://localhost:5000
```

## 프로젝트 구조
```
oil-today/
├── app.py                # Flask 애플리케이션 서버
├── index.html            # 메인 웹페이지
├── api_test.ipynb        # API 테스트용 Jupyter 노트북
├── js/                   # JavaScript 파일
├── css/                  # CSS 스타일시트
├── api/                  # API 관련 코드
├── data/                 # 데이터 파일
├── backend/              # 백엔드 코드
│   └── requirements.txt  # 필요한 Python 패키지 목록
└── pages/                # 추가 웹페이지
```

## 스크린샷
(프로젝트 스크린샷을 여기에 추가하세요)

## 기여 방법
1. 이 저장소를 포크합니다.
2. 새로운 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다.

## 라이센스
이 프로젝트는 MIT 라이센스 하에 있습니다 - 자세한 내용은 LICENSE 파일을 참조하세요.

## 연락처
- 이메일: your-email@example.com
- 깃허브: [your-username](https://github.com/your-username) 