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
![image](https://github.com/jongmin-oh/comfort-serverless-chatbot/assets/23625693/ca1c51e8-fc41-46de-81f8-051d26ae70e9)

## What is AWS SAM(Serverless Application Model)
```
AWS SAM (Serverless Application Model)은 AWS에서 서버리스 애플리케이션을 빠르고 쉽게 배포하고 관리할 수 있도록 하는 프레임워크입니다.
이를 통해 AWS Lambda, API Gateway, DynamoDB 등의 서버리스 리소스를 쉽게 정의, 배포 및 관리할 수 있습니다.
```
