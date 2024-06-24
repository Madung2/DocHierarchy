# DocHierarchy
![image](https://github.com/Madung2/DocHierarchy/assets/104334219/20832d05-657d-47b3-8de7-3b595eedb513)

## 목표: 
* docx파일을 만들면 그 hierarchy에 맞는 json파일을 리턴한다.

## 조건

1순위: 폰트 사이즈
2순위: justify-center면 타이틀로 간주
3순위: 볼드 텍스트

(모든 문서에 제너럴하게 작업이 되려면 조건이 간단하게 되어야 함으로 조건을 무겁게 두지 않았습니다.
세부적인 처리가 필요할시 조건을 다르게 작성해야하는 점 말씀드립니다.)
***

## FASTAPI 어플리케이션 실행
```
# 루트 디렉토리로 이동
$ poetry run uvicorn app.main:app --reload
```

## STREAMLIT어플리케이션 실행
```
$ poetry run streamlit run streamlit/main.py
```

#### 라이브러리 추가
```
poetry add python-docx
```

#### 테스트 환경 설정
```
poetry add --dev pytest
```




### 본 프로그램은 테스트용이며 하기의 기능은 따로 모듈로 추가해야하는 점 안내드립니다.
### * 번호매기기 처리 모듈
### * 세부처리는 내부 llm을 사용해 작업할 예정
dfdviolet910714