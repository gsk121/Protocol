# 보안/공격 기법 구현

> **주의**: 이 저장소의 공격 코드는 교육 목적으로만 사용하며, 반드시 격리된 테스트 환경에서만 실행해야 합니다.  
> 허가받지 않은 시스템에 대한 공격은 불법입니다.

---

## 구현 현황 요약

| 공격 기법 | 계층 | 구현 여부 | 소스 파일 |
|----------|------|-----------|----------|
| SYN Flooding | L4 (TCP) | ✅ 구현됨 | `SYNFlooding.py` |
| UDP Flooding | L4 (UDP) | ✅ 구현됨 | `udpflooding.py` |
| ARP Poisoning | L2 (ARP) | ✅ 구현됨 | `posion1.py`, `posion2.py` |
| HTTP GET Flooding | L7 (HTTP) | ✅ 구현됨 | `Web/getflooding.py` |
| Slowloris | L7 (HTTP) | ✅ 구현됨 | `Web/slowlorisattack.py` |
| Slow Read | L7 (HTTP) | ✅ 구현됨 | `Web/slowreadattack.py` |
| ICMP Flooding | L3 (ICMP) | ❌ 미구현 | - |
| DNS Amplification | L7 (DNS) | ❌ 미구현 | - |
| DHCP Starvation | L7 (DHCP) | ❌ 미구현 | - |
| TCP RST Injection | L4 (TCP) | ❌ 미구현 | - |
| VLAN Hopping | L2 (802.1Q) | ❌ 미구현 | - |

---

## SYN Flooding

| 항목 | 내용 |
|------|------|
| **구현 여부** | ✅ 구현됨 |
| **소스 파일** | `SYNFlooding.py` |
| **대상 계층** | L4 (TCP) |

### 개요
SYN Flood는 TCP 3-way handshake 취약점을 이용한 DoS 공격입니다.  
공격자가 위조된(스푸핑된) 출발지 IP로 대량의 SYN 패킷을 전송하면,  
서버는 SYN-ACK를 보내고 반쪽 열린 연결(half-open connection)을 백로그 큐에 쌓습니다.  
큐가 가득 차면 정상 연결 요청을 처리하지 못하게 됩니다.

### 동작 원리
```
공격자 (스푸핑 IP)          서버
  |                          |
  |--SYN (src=1.2.3.4)------>|  (가짜 IP)
  |--SYN (src=5.6.7.8)------>|  (가짜 IP)
  |--SYN (src=9.10.11.12)--->|  (가짜 IP)
  |  ... (수천~수만 개)       |
  |                          |
  |  서버 백로그 큐 포화 →     |
  |  정상 연결 거부됨          |
```

### 방어 기법
- **SYN Cookies**: 백로그 큐 없이 쿠키로 상태 추적
- **방화벽 임계치**: 동일 출발지 SYN 수 제한
- **IPS/IDS**: 이상 트래픽 감지

---

## UDP Flooding

| 항목 | 내용 |
|------|------|
| **구현 여부** | ✅ 구현됨 |
| **소스 파일** | `udpflooding.py` |
| **대상 계층** | L4 (UDP) |

### 개요
UDP Flood는 대상 서버의 임의 포트로 대량의 UDP 패킷을 전송하는 DoS 공격입니다.  
서버는 수신한 UDP 패킷에 대해 해당 포트의 응용프로그램이 없으면 ICMP Destination Unreachable을 반환하므로,  
네트워크 대역폭 및 CPU 자원을 소모합니다.

### 방어 기법
- 불필요한 UDP 포트 방화벽 차단
- 대역폭 임계치 설정
- 업스트림 클리닝 센터(DDoS 방어 서비스)

---

## ARP Poisoning (ARP Cache Poisoning)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ✅ 구현됨 |
| **소스 파일** | `posion1.py`, `posion2.py` |
| **대상 계층** | L2 (ARP) |

### 개요
ARP Poisoning은 ARP 프로토콜의 인증 없는 신뢰 특성을 악용한 공격입니다.  
공격자가 가짜 ARP Reply를 브로드캐스트하여 피해자의 ARP 테이블을 오염시킵니다.  
이를 통해 Man-in-the-Middle(MITM) 공격으로 트래픽을 가로채거나, 트래픽을 차단할 수 있습니다.

### 동작 원리
```
정상 상태:
  호스트 A (192.168.1.1)  ←→  게이트웨이 (192.168.1.254)

ARP Poisoning 후:
  호스트 A의 ARP 테이블:
    192.168.1.254 → [공격자 MAC]  ← 오염됨

  호스트 A의 트래픽이 공격자를 경유하게 됨
```

### 구현 내용
- `posion1.py`: 단방향 ARP Poisoning (호스트 A 오염)
- `posion2.py`: 양방향 ARP Poisoning (호스트 A + 게이트웨이 동시 오염) → 완전한 MITM

### 방어 기법
- **Dynamic ARP Inspection (DAI)**: 스위치에서 ARP 패킷 검증
- **Static ARP 엔트리**: 중요 호스트는 정적 ARP 설정
- **ARP 감시 도구**: `arpwatch`, `XArp` 등

---

## HTTP GET Flooding

| 항목 | 내용 |
|------|------|
| **구현 여부** | ✅ 구현됨 |
| **소스 파일** | `Web/getflooding.py` |
| **대상 계층** | L7 (HTTP) |

### 개요
HTTP GET Flood는 유효한 HTTP GET 요청을 대량으로 전송하는 L7 DoS 공격입니다.  
일반 네트워크 방화벽은 정상 HTTP 요청으로 보여 차단하기 어렵습니다.  
서버의 CPU, 메모리, 데이터베이스 자원을 소모시킵니다.

### 방어 기법
- CAPTCHA, 레이트 리미팅
- CDN/WAF(Web Application Firewall) 활용
- 요청 패턴 분석 및 IP 차단

---

## Slowloris Attack

| 항목 | 내용 |
|------|------|
| **구현 여부** | ✅ 구현됨 |
| **소스 파일** | `Web/slowlorisattack.py` |
| **대상 계층** | L7 (HTTP) |

### 개요
Slowloris는 적은 대역폭으로 웹 서버의 동시 연결 수를 고갈시키는 공격입니다.  
HTTP 요청 헤더를 의도적으로 매우 느리게 전송하여 서버가 연결을 닫지 못하도록 합니다.  
Apache 같은 스레드 기반 서버에 효과적이며, nginx 같은 이벤트 기반 서버에는 영향이 적습니다.

### 동작 원리
```
공격자                              서버
  |                                   |
  |--TCP 연결 수립 (수백 개)----------->|
  |                                   |
  |--GET / HTTP/1.1\r\n-------------->|  (헤더 시작)
  |--X-Header: value\r\n------------->|  (헤더 계속)
  |                                   |  (15초 대기)
  |--X-Header2: value\r\n------------>|  (헤더 유지)
  |                                   |  (15초 대기)
  |  ...무한 반복...                   |
  |                                   |
  |  서버 연결 풀 고갈 → 정상 요청 거부  |
```

### 방어 기법
- 연결별 헤더 수신 타임아웃 설정
- 최대 헤더 크기 제한
- 동일 IP 동시 연결 수 제한

---

## Slow Read Attack

| 항목 | 내용 |
|------|------|
| **구현 여부** | ✅ 구현됨 |
| **소스 파일** | `Web/slowreadattack.py` |
| **대상 계층** | L7 (HTTP) / L4 (TCP) |

### 개요
Slow Read Attack은 TCP의 수신 윈도우 크기(Window Size)를 매우 작게 설정하여  
서버가 응답 데이터를 매우 느리게 전송하도록 강제하는 공격입니다.  
서버는 응답을 보내는 동안 연결을 유지해야 하므로 자원이 고갈됩니다.

### 동작 원리
```
공격자                              서버
  |                                   |
  |--GET /large-file HTTP/1.1-------->|
  |                                   |
  |<--HTTP 200 OK (데이터 전송 시작)---|
  |                                   |
  |  [TCP Window Size = 1 byte]       |
  |  서버는 1바이트씩만 전송 가능      |
  |                                   |
  |  연결 수백 개 유지 → 자원 고갈    |
```

### 방어 기법
- 전송 완료 타임아웃 설정
- 최소 TCP Window Size 임계치 강제
- 연결별 응답 전송 속도 모니터링

---

## ICMP Flooding (미구현)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **대상 계층** | L3 (ICMP) |

### 개요
ICMP Flood(ping flood)는 대량의 ICMP Echo Request를 전송하여 대역폭을 포화시키는 공격입니다.  
Smurf Attack은 브로드캐스트 주소에 스푸핑된 IP로 ICMP Request를 보내 피해자에게 증폭 응답을 유발합니다.

### 구현 계획
- ICMP Echo Request 대량 전송 구현
- Smurf Attack 패킷 생성 (브로드캐스트 + 스푸핑)

---

## DNS Amplification (미구현)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **대상 계층** | L7 (DNS) |

### 개요
DNS 증폭 공격은 공개 DNS 서버를 악용하여 트래픽을 증폭시키는 DDoS 공격입니다.  
작은 DNS Query(~40B)로 큰 DNS Response(수 KB)를 피해자 IP로 유도합니다.  
증폭 배율은 최대 70배 이상일 수 있습니다.

### 구현 계획
- 스푸핑된 출발지 IP로 ANY/TXT 레코드 DNS Query 전송
- 증폭 배율 측정

---

## TCP RST Injection (미구현)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **대상 계층** | L4 (TCP) |

### 개요
TCP RST Injection은 기존 TCP 연결에 위조된 RST 패킷을 삽입하여 강제로 연결을 끊는 공격입니다.  
시퀀스 번호를 정확히 맞춰야 효과가 있으며, 인터넷 검열이나 세션 하이재킹에 악용될 수 있습니다.

### 구현 계획
- 스니핑으로 시퀀스 번호 파악
- 정확한 시퀀스 번호의 RST 패킷 생성 및 삽입
