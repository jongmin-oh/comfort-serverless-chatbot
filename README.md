# AWS SAM을 활용한 카카오톡 위로 챗봇 "오복이"

***

## BackGroud
위로봇 오복이의 기존 버전은 QA쌍으로 학습된 검색 기반 모델이였습니다, <br>
성의없던 답변 문제를 공들여서 만든 2.0 버젼이 탄생했고 오복이의 답변은 훨씬 재미있고 퀄리티 높은 솔루션을 제시했습니다. <br>
하지만, [유지 비용 문제(EC2 서버 비용)]와 [대화를 이어갈 수 없는 싱글 턴의 한계]가 있었습니다.

### Solution
- 과감하게 검색 모델을 포기하고, 하이퍼클로바X 모델을 사용한 생성모델로 변경하였습니다.
- 온디멘드 인스턴스가 아닌 사용할때만 과금되는 AWS 서버리스 아키텍쳐로 새로 구현하였습니다.
- 질문/답변을 AWS DynamoDB에 저장하여 이전대화를 불러와서 생성하는 멀티턴 챗봇으로 새롭게 구현하였습니다.

## Architecture
![image](https://github.com/jongmin-oh/comfort-serverless-chatbot/assets/23625693/98c286ed-29aa-4c7e-a7c0-ac4fe1465fde)

### What is SAM?
```
AWS SAM (Serverless Application Model)은 AWS에서 서버리스 애플리케이션을 빠르고 쉽게 배포하고 관리할 수 있도록 하는 프레임워크입니다.
이를 통해 AWS Lambda, API Gateway, DynamoDB 등의 서버리스 리소스를 쉽게 정의, 배포 및 관리할 수 있습니다.
```

### Tree
```
├── events
│   └── event.json
├── samconfig.toml
├── service
│   ├── app
│   │   ├── config.py
│   │   ├── models
│   │   │   └── __init__.py
│   │   ├── resources
│   │   │   └── persona.txt
│   │   ├── secrets.yml
│   │   └── tasks
│   │       ├── __init__.py
│   │       ├── generate.py
│   │       └── record.py
│   ├── lambda_function.py
│   └── requirements.txt
└── template.yaml
```

### Deploy Steps

#### 1. Build
```
sam build
```
build 명령어를 실행하면 ".aws-sam" 파일이 생성됩니다.

#### 2. invoke
```
sam local invoke --event events/event.json
```
빌드가 된 상태에서 invoke 명령어를 사용하면 실제 Lambda 함수에 대한 테스트를 로컬에서 진행할 수 있습니다.<br>
event.json 파일에 정의된 내용이 Lambda의 event 객체로 전송되어 테스트 됩니다.

#### 3. api-test(선택사항)
```
sam local start-api
```
API gateway를 사용했을때 가능한 API 테스트 입니다, 실제 도커컨테이너로 http://localhost:3000 으로 웹서버가 실행됩니다. <br>
GET/POST 요청을 보내 테스트 할 수 있습니다.

#### 4. Deploy
```
sam deploy --guided
```
실제 AWS에 배포할 수 있습니다.


