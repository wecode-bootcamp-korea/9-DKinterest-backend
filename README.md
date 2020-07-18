# introduction

* 핀터레스트(Pinterest)는 이용자가 스크랩하고자 하는 이미지를 포스팅하고 다른 이용자와 공유하는 소셜 네트워크 서비스이다.
핀터레스트의 가장 큰 특징은 이미지 보드에 핀으로 사진을 꽂는 것과 비슷한 개념으로 이미지 파일을 모으고 관리할 수 있다는 점이다. 사이트의 특징을 최대한 살려 클론을 진행했다.
* 개발기간 : 2020.07.06 ~ 2020.07.17(약 2주)
* 개발인원 : 3 Front-end(이재준, 이호균, 한수민), 3 Back-end(김동건, 류제승, 이유진)
* [Front-end Github](https://github.com/wecode-bootcamp-korea/9-DKinterest-frontend)
* [Back-end Github](https://github.com/wecode-bootcamp-korea/9-DKinterest-backend)

# Model

![Model](https://images.velog.io/images/dgk089/post/1615a138-ba46-4ae6-a29e-50bc18c12750/%ED%95%80%ED%84%B0%EB%A0%88%EC%8A%A4%ED%8A%B8_20200717_02_08.png)

# Technologies

* Python
* Django
* Beautifulsoup, Selenium
* Bcrypt
* JWT
* Unittest
* MySQL
* AWS S3
* CORS headers
* Git, Github

# Features

* Account
   - 유저정보저장
   - 회원가입 / 로그인
     - 회원가입시 유효성 검사
     - 회원가입시 패스워드 암호화
     - 로그인시 JWT Access 토큰 발행
   - 로그인 상태인지 확인하는 데코레이터 함수
   - 카카오톡 소셜 로그인 기능 구현
   - 관심사 저장하는 기능 구현
   - unittest
   
* Boardpin
   - 마이페이지 계정 정보 보여주는 기능 구현
   - 마이페이지 저장한 보드 정보 보여주는 기능 구현
   - 마이페이지 저장한 핀 정보 보여주는 기능 구현
   - 선택한 관심사 사진을 메인 페이지에 리스트하는 기능 구현
   - 선택한 관심사의 이미지를 랜덤으로 전송하는 기능 구현
   - 핀 상세 페이지 구현
   - 보드 생성 기능 구현
   - 핀 생성 기능 구현
   - 핀 생성 시 원하는 이미지 파일을 선택해 AWS S3로 이미지 업로드 기능 구현
   - unittest
   
