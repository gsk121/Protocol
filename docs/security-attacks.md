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
| ICMP Flooding / Smurf | L3 (ICMP) | ❌ 미구현 | - |
| DNS Amplification | L7 (DNS) | ❌ 미구현 | - |
| NTP Amplification | L7 (NTP) | ❌ 미구현 | - |
| DHCP Starvation | L7 (DHCP) | ❌ 미구현 | - |
| TCP RST Injection | L4 (TCP) | ❌ 미구현 | - |
| Session Hijacking | L4 (TCP) | ❌ 미구현 | - |
| IP Spoofing | L3 (IP) | ❌ 미구현 | - |
| MAC Flooding | L2 (Ethernet) | ❌ 미구현 | - |
| VLAN Hopping | L2 (802.1Q) | ❌ 미구현 | - |
| Ping of Death | L3 (ICMP) | ❌ 미구현 | - |
| Teardrop Attack | L3 (IP) | ❌ 미구현 | - |
| Land Attack | L4 (TCP) | ❌ 미구현 | - |
| HTTP POST Flooding | L7 (HTTP) | ❌ 미구현 | - |

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

---

## DHCP Starvation (미구현)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **대상 계층** | L7 (DHCP) |

### 개요
DHCP Starvation은 위조된 MAC 주소로 DHCP Discover를 대량 전송하여 DHCP 서버의 주소 풀을 고갈시키는 공격입니다.  
주소 풀이 고갈되면 이후 정상 클라이언트는 IP를 할당받지 못합니다.  
DHCP Starvation 이후 공격자가 가짜 DHCP 서버를 올려 MITM 공격으로 이어지기도 합니다(DHCP Spoofing).

### 동작 원리
```
공격자                              DHCP 서버
  |                                    |
  |--DHCP Discover (MAC=AA:BB:CC:...)-->|
  |--DHCP Discover (MAC=DD:EE:FF:...)-->|
  |  ... (수천 개의 가짜 MAC)            |
  |                                    |
  |  DHCP 주소 풀 고갈 →               |
  |  정상 클라이언트 IP 할당 불가         |
```

### 구현 계획
- 랜덤 MAC 주소로 DHCP Discover 대량 전송
- DHCP Spoofing (가짜 DHCP 서버 응답) 연계

---

## VLAN Hopping (미구현)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **대상 계층** | L2 (802.1Q) |

### 개요
VLAN Hopping은 VLAN 격리를 우회하여 다른 VLAN의 트래픽에 접근하는 공격입니다.  
두 가지 방식이 있습니다.

1. **Switch Spoofing**: 공격자가 트렁크 포트 협상 프로토콜(DTP)을 흉내내어 스위치와 트렁크 링크 수립
2. **Double Tagging**: 802.1Q 태그를 이중으로 붙여 내부 태그의 VLAN으로 패킷 도달

### Double Tagging 동작 원리
```
공격자 (VLAN 10)                스위치 A         스위치 B
  |                                |                |
  |--[Tag:10][Tag:20] 프레임------>|                |
  |                                |  외부 Tag:10  |
  |                                |  제거 후 전달-->|
  |                                |                | Tag:20 패킷이
  |                                |                | VLAN 20으로 도달
```

### 구현 계획
- Double Tagging 프레임 생성 (Ethernet + 이중 802.1Q 태그)
- DTP 협상 패킷 생성 (Switch Spoofing)

---

## Session Hijacking (미구현)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **대상 계층** | L4 (TCP) |

### 개요
세션 하이재킹은 합법적인 TCP 세션을 가로채는 공격입니다.  
패킷 스니핑으로 시퀀스/ACK 번호를 파악한 뒤, 서버에 위조된 패킷을 주입하여 클라이언트인 척 통신합니다.  
ARP Poisoning을 선행하면 MITM 위치에서 더 쉽게 수행 가능합니다.

### 동작 원리
```
클라이언트 ←-- ARP Poisoning --→ 공격자 ←--→ 서버

1. ARP Poisoning으로 트래픽 경유
2. TCP 시퀀스 번호 파악
3. 클라이언트를 RST로 연결 끊음
4. 파악한 시퀀스 번호로 서버에 위조 패킷 전송
```

### 구현 계획
- 스니퍼로 TCP 시퀀스/ACK 번호 추출
- 위조 패킷 주입 (ARP Poisoning 연계)

---

## IP Spoofing (미구현)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **대상 계층** | L3 (IP) |

### 개요
IP Spoofing은 IP 헤더의 출발지 주소를 위조하는 기법입니다.  
그 자체로는 공격이라기보다 SYN Flood, DNS/NTP 증폭, Smurf 등 다른 공격의 기반 기법으로 사용됩니다.  
Raw Socket을 사용하면 OS가 자동으로 채우는 출발지 IP를 임의로 설정할 수 있습니다.

### 구현 계획
- Raw Socket으로 출발지 IP를 임의로 설정한 IP 패킷 전송
- 다른 공격 기법(SYN Flood, ICMP Flood)과의 연계 시연

---

## MAC Flooding (CAM Table Overflow) (미구현)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **대상 계층** | L2 (Ethernet) |

### 개요
MAC Flooding은 스위치의 CAM(Content Addressable Memory) 테이블을 위조된 MAC 주소로 가득 채우는 공격입니다.  
CAM 테이블이 포화되면 스위치는 학습 불가 상태가 되어 모든 포트로 프레임을 플러딩(허브처럼 동작)합니다.  
이를 이용해 공격자는 자신이 연결된 포트로 다른 호스트의 트래픽을 수신할 수 있습니다.

### 동작 원리
```
공격자가 수만 개의 가짜 MAC 주소로 프레임 전송
→ 스위치 CAM 테이블 포화
→ 스위치가 허브처럼 모든 포트로 플러딩
→ 공격자가 타 호스트 트래픽 도청 가능
```

### 구현 계획
- 랜덤 출발지 MAC 주소로 Ethernet 프레임 대량 생성·전송
- 스위치 CAM 테이블 포화 확인

---

## Ping of Death (미구현)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **대상 계층** | L3 (ICMP / IP) |

### 개요
Ping of Death는 IPv4 최대 패킷 크기(65,535바이트)를 초과하는 ICMP Echo Request를 단편화하여 전송하는 공격입니다.  
수신 측에서 단편을 재조합하면 버퍼 오버플로우가 발생하여 시스템이 충돌(BSOD, 재부팅)할 수 있습니다.  
현대 OS는 대부분 패치되어 있으나, 임베디드/구형 장비에서는 여전히 유효할 수 있습니다.

### 구현 계획
- 65,535바이트를 초과하는 ICMP 페이로드를 IP 단편화하여 전송
- 재조합 시 오버플로우 유발 구조 시연

---

## Teardrop Attack (미구현)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **대상 계층** | L3 (IP) |

### 개요
Teardrop Attack은 IP 단편화(Fragmentation) 메커니즘의 취약점을 이용하는 공격입니다.  
단편 오프셋 값을 조작하여 단편들이 서로 겹치거나(overlap) 불완전하게 재조합되도록 유도합니다.  
취약한 시스템에서는 재조합 중 커널 패닉이나 충돌이 발생합니다.

### 동작 원리
```
정상 단편:   [0~100] [101~200] [201~300]
Teardrop:   [0~100] [50~150]  ← 오프셋 조작으로 겹침 발생
             → 재조합 로직 오류 → 시스템 충돌
```

### 구현 계획
- IP Fragment Offset을 겹치도록 조작한 패킷 쌍 생성
- 불완전 단편(마지막 단편 없음) 전송으로 재조합 대기 자원 고갈

---

## Land Attack (미구현)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **대상 계층** | L4 (TCP) |

### 개요
Land Attack은 출발지 IP/포트와 목적지 IP/포트를 동일하게 설정한 SYN 패킷을 전송하는 공격입니다.  
취약한 시스템은 자기 자신에게 SYN-ACK를 보내는 무한 루프에 빠져 CPU 자원이 고갈됩니다.

### 동작 원리
```
패킷: src IP = dst IP = 피해자 IP
      src Port = dst Port = 피해자 포트
→ 피해자가 자신에게 SYN-ACK 전송 → 무한 루프
```

### 구현 계획
- 출발지=목적지로 설정된 TCP SYN 패킷 생성 (IP Spoofing 활용)

---

## NTP Amplification (미구현)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **대상 계층** | L7 (NTP) |

### 개요
NTP 증폭 공격은 공개 NTP 서버의 `monlist` 명령을 악용하는 반사·증폭 DDoS 공격입니다.  
소량의 요청(~46B)으로 최대 206배까지 증폭된 응답(~46KB)을 피해자에게 유도할 수 있습니다.  
현재 대부분의 NTP 서버는 `monlist` 비활성화로 패치되어 있습니다.

### 동작 원리
```
공격자 (스푸핑: src=피해자IP)    NTP 서버       피해자
  |                                |               |
  |--monlist 요청 (46B)----------->|               |
  |                                |--응답(~46KB)->|
  |                                |  (증폭 최대 206배)
```

### 구현 계획
- 스푸핑된 IP로 NTP monlist 요청 전송
- 증폭 배율 측정

---

## HTTP POST Flooding (미구현)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **대상 계층** | L7 (HTTP) |

### 개요
HTTP POST Flood는 대용량 본문(body)을 가진 POST 요청을 대량 전송하는 L7 DoS 공격입니다.  
GET Flooding에 비해 서버의 처리 비용이 더 높으며(파싱, DB 쓰기 등),  
Slow POST는 본문을 아주 느리게 전송하여 Slowloris와 유사하게 연결을 장시간 점유합니다.

### 구현 계획
- Content-Length를 크게 선언하고 본문을 느리게 전송 (Slow POST)
- 대용량 POST 요청 대량 전송
