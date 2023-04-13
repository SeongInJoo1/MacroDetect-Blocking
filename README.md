# 매크로 탐지 프로그램

jsblockv1.py 기능
- /var/log/apache2/access.log 를 실시간으로 읽어와 실시간 탐지 가능
-  GET 메소드로 자바스크립트를 요청하는 IP가 있으면 차단하고 /var/log/apache2/blocked_js.log 에 기록한다.
(매크로는 GET 메소드로 자바스크립트를 요청한다.)

pausip.py 기능
- /var/log/apache2/access.log 를 실시간으로 읽어와 실시간 탐지 가능
(실시간으로 생성되는 access.log를 50개씩 저장해서 처리하도록 만듬.)
(실시간으로 들어오는 ip의 시간내에 접속 횟수를 계산하기 위해서)
- 한 ip에서 5초이내에 10번이상 접속시 해당 ip를 10분간 차단한다.
(10분동안 프로그램이 멈추는걸 방지하기 위해 멀티스레딩 구현)

* testcode는 연습 및 시행착오 파일들을 모아놓았다.
