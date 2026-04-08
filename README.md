# Protocol

이 저장소는 Python으로 이더넷/ARP/IP/TCP/UDP 헤더를 직접 구성·파싱하고, 이를 기반으로 패킷 송수신 실습 및 트래픽/공격 시나리오 실험 코드를 모아둔 학습용 예제 모음이다.

## 저장소 개요

- 목적: 소켓(`AF_PACKET`, `SOCK_RAW`)과 직접 구현한 헤더 클래스를 이용해 프로토콜 동작을 실습.
- 구성: 
  - `header/`: 프로토콜 헤더 직렬화/역직렬화 유틸리티
  - 루트 스크립트: TCP 3-way handshake, TCP/UDP 패킷 송신, 스니핑, ARP 패킷 전송
  - `ServerClient/`: TCP/UDP 에코 서버/클라이언트 예제
  - `Web/`: HTTP 요청 기반 부하/지연 공격 실험 스크립트

## 실행 전 확인사항

- Python 버전: 저장소 내 `.py` 파일은 Python 3에서 문법 컴파일이 되며(`python3 -m py_compile` 기준), 별도 `requirements.txt`는 없다.
- 대부분 스크립트는 리눅스 raw socket 권한(일반적으로 root 권한)이 필요하다.
- 코드 내에 고정된 IP/MAC/인터페이스(`eth0`)가 다수 존재하므로, 실행 환경에 맞게 수동 수정이 필요하다.
- 공격성 동작(예: SYN flood, HTTP flood/slow 계열, ARP 변조성 패킷 전송)을 포함하므로, **격리된 테스트 환경에서만** 사용해야 한다.

## 소스 파일 한줄 설명

### 루트 디렉터리

- `3-way_handshake.py`: raw TCP 패킷으로 SYN → SYN/ACK 수신 → ACK 전송 흐름을 수동 구성해 3-way handshake를 실습한다.
- `SYNFlooding.py`: 출발지 IP를 임의로 바꾼 SYN 패킷을 반복 전송해 SYN backlog 고갈을 유도하는 형태의 테스트 코드를 제공한다.
- `udpflooding.py`: 고정된 UDP payload를 주기적으로 전송하는 단순 UDP flood 형태 트래픽 생성 스크립트다.
- `tcpsniffer.py`: 이더넷 프레임을 수신해 IP/TCP(및 일부 ICMP) 정보를 파싱·출력하는 간단한 스니퍼다.
- `tcppacket.py`: 사용자 입력(포트/시퀀스/플래그) 기반으로 임의 TCP 패킷 1개를 구성해 전송한다.
- `posion1.py`: ARP Request 패킷을 반복 송신하는 스크립트(파일명은 poison이나 실제 코드는 ARP request 전송 루프).
- `posion2.py`: 대상/송신 IP-MAC 조합이 다른 ARP Request 반복 송신 스크립트다.

### `header/`

- `header/eth.py`: 이더넷 헤더의 필드(MAC/type) 파싱 및 바이트 직렬화 클래스를 제공한다.
- `header/arp.py`: ARP 헤더 필드 파싱/직렬화 클래스를 제공한다.
- `header/ip.py`: IPv4 기본 헤더 필드 파싱/직렬화 클래스를 제공한다.
- `header/tcp.py`: TCP 기본 헤더 필드 파싱/직렬화 클래스를 제공한다.
- `header/udp.py`: UDP 헤더(+data) 파싱/직렬화 클래스를 제공한다.
- `header/chk.py`: 인터넷 체크섬 계산 함수(`make_chksum`)를 제공한다.

### `ServerClient/`

- `ServerClient/tcpechoserver.py`: TCP 에코 서버(수신 데이터 재전송) 예제다.
- `ServerClient/tcpechoclien.py`: TCP 에코 클라이언트 예제다(인자로 서버 IP/PORT 사용).
- `ServerClient/udpechoserver.py`: UDP 에코 서버 예제다.
- `ServerClient/udpechoclientnc.py`: UDP 에코 클라이언트 예제다(인자로 서버 IP/PORT 사용).

### `Web/`

- `Web/getflooding.py`: 동일 GET 요청을 무한 반복 전송하는 HTTP 요청 flood 형태 스크립트다.
- `Web/slowlorisattack.py`: HTTP 헤더 종료를 지연/누락하며 연결을 유지하는 slowloris 계열 실험 코드다.
- `Web/slowreadattack.py`: 큰 Content-Length 선언 후 본문 전송을 매우 느리게 지속하는 slow POST 계열 코드다.

## 제한 및 관찰 사항

- 모듈 import 경로가 `from eth import *` 형태로 작성되어 있어, 실행 위치/`PYTHONPATH`에 따라 import 실패 가능성이 있다.
- 일부 코드에는 오탈자/일관성 이슈(예: 파일명 `tcpechoclien.py`, `posion*.py`)가 존재한다.
- 본 저장소는 학습용 스크립트 집합이며, 에러 처리·재시도·로깅·테스트 자동화가 체계화된 배포용 구조는 아니다.
