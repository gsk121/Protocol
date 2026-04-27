# L4 전송 계층 프로토콜

전송 계층은 OSI 4계층으로, 종단 간(end-to-end) 통신을 담당합니다.  
포트 번호로 프로세스를 식별하며, 신뢰성 있는 전송(TCP) 또는 비연결 전송(UDP)을 제공합니다.

---

## TCP (Transmission Control Protocol)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ✅ 구현됨 |
| **소스 파일** | `header/tcp.py`, `3-way_handshake.py`, `tcppacket.py`, `tcpsniffer.py` |
| **표준** | RFC 793, RFC 9293 |

### 개요
TCP는 연결 지향(Connection-Oriented) 프로토콜로, 데이터의 신뢰성 있는 전송을 보장합니다.  
3-way handshake로 연결을 수립하고, 4-way handshake로 연결을 종료합니다.  
흐름 제어, 혼잡 제어, 오류 검출 및 재전송 기능을 제공합니다.

### 헤더 구조 (최소 20바이트)
```
 0               1               2               3
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |       |C|E|U|A|P|R|S|F|                               |
| Offset|Reserv.|W|C|R|C|S|S|Y|I|            Window            |
|       |       |R|E|G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options (if Data Offset > 5)               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### 제어 플래그 (Control Bits)
| 플래그 | 이름 | 설명 |
|-------|------|------|
| `SYN` | Synchronize | 연결 요청 |
| `ACK` | Acknowledge | 수신 확인 |
| `FIN` | Finish | 연결 종료 요청 |
| `RST` | Reset | 연결 강제 종료 |
| `PSH` | Push | 버퍼 즉시 전달 |
| `URG` | Urgent | 긴급 데이터 |

### 3-Way Handshake
```
Client                          Server
  |                               |
  |------SYN (seq=x)------------->|
  |                               |
  |<-----SYN-ACK (seq=y, ack=x+1)-|
  |                               |
  |------ACK (ack=y+1)----------->|
  |                               |
  |       [연결 수립됨]            |
```

### 구현 내용
- TCP 헤더 직렬화 및 의사 헤더(pseudo header) 포함 체크섬 계산 (`header/tcp.py`)
- Raw socket을 이용한 수동 3-way handshake (`3-way_handshake.py`)
- 커스텀 TCP 패킷 생성 및 전송 (`tcppacket.py`)
- Ethernet/IP/TCP/ICMP 계층 파싱 패킷 스니퍼 (`tcpsniffer.py`)
- TCP 에코 서버/클라이언트 (`ServerClient/tcpechoserver.py`, `ServerClient/tcpechoclien.py`)

---

## UDP (User Datagram Protocol)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ✅ 구현됨 |
| **소스 파일** | `header/udp.py`, `udpflooding.py`, `ServerClient/udpechoserver.py`, `ServerClient/udpechoclientnc.py` |
| **표준** | RFC 768 |

### 개요
UDP는 비연결(Connectionless) 프로토콜로, 신뢰성보다 속도를 우선합니다.  
연결 수립 없이 데이터를 즉시 전송하며, 재전송·흐름제어·혼잡제어가 없습니다.  
DNS, DHCP, 실시간 스트리밍, 게임 등에 사용됩니다.

### 헤더 구조 (8바이트 고정)
```
 0               1               2               3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|             Length            |            Checksum           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### TCP vs UDP 비교
| 항목 | TCP | UDP |
|------|-----|-----|
| 연결 | 연결 지향 | 비연결 |
| 신뢰성 | 보장 (재전송) | 미보장 |
| 순서 보장 | 보장 | 미보장 |
| 속도 | 느림 | 빠름 |
| 오버헤드 | 높음 (20B 헤더) | 낮음 (8B 헤더) |
| 용도 | HTTP, FTP, SSH | DNS, DHCP, 스트리밍 |

### 구현 내용
- UDP 헤더 직렬화 (`header/udp.py`)
- UDP Flooding 공격 (대량 UDP 패킷 전송) (`udpflooding.py`)
- UDP 에코 서버/클라이언트 (`ServerClient/udpechoserver.py`, `ServerClient/udpechoclientnc.py`)

---

## SCTP (Stream Control Transmission Protocol)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **표준** | RFC 4960 |

### 개요
SCTP는 TCP와 UDP의 장점을 결합한 전송 계층 프로토콜입니다.  
멀티호밍(다중 IP 주소), 멀티스트리밍, 메시지 경계 보존, 4-way handshake(TCP와 달리 연결 시 쿠키 교환으로 SYN Flood 방어) 등의 특징이 있습니다.  
VoIP, 통신 신호 전달(SS7/SIGTRAN)에 주로 사용됩니다.

### 구현 계획
- SCTP 청크(Chunk) 구조 직렬화/파싱
- INIT / INIT ACK / COOKIE ECHO / COOKIE ACK 4-way handshake
- 멀티스트리밍 데이터 전송 시뮬레이션
