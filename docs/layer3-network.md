# L3 네트워크 계층 프로토콜

네트워크 계층은 OSI 3계층으로, 서로 다른 네트워크 간의 패킷 라우팅과 논리 주소(IP) 지정을 담당합니다.

---

## IPv4 (Internet Protocol version 4)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ✅ 구현됨 |
| **소스 파일** | `header/ip.py`, `header/chk.py` |
| **표준** | RFC 791 |

### 개요
IPv4는 인터넷의 기반이 되는 네트워크 계층 프로토콜입니다.  
32비트 주소 체계를 사용하며, 패킷 분할(Fragmentation), TTL, 헤더 체크섬 등의 기능을 제공합니다.

### 헤더 구조
```
 0               1               2               3
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |    DSCP   |ECN|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |         Header Checksum       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### 주요 Protocol 번호
| 값 | 프로토콜 |
|----|---------|
| `1` | ICMP |
| `6` | TCP |
| `17` | UDP |
| `89` | OSPF |

### 구현 내용
- `struct.pack`을 이용한 IP 헤더 직렬화 (`header/ip.py`)
- 인터넷 체크섬 계산 (`header/chk.py`)
- TTL, 프로토콜 필드, 출발지/목적지 IP 설정

---

## ICMPv4 (Internet Control Message Protocol)

| 항목 | 내용 |
|------|------|
| **구현 여부** | 🔶 부분 구현 |
| **소스 파일** | `tcpsniffer.py` (파싱만 구현) |
| **표준** | RFC 792 |

### 개요
ICMP는 네트워크 오류 보고 및 진단을 위한 프로토콜입니다.  
`ping`(Echo Request/Reply), 목적지 도달 불가, TTL 초과 등의 메시지를 전달합니다.

### 헤더 구조
```
+--------+--------+------------------+
|  Type  |  Code  |    Checksum      |
| (1B)   | (1B)   |    (2 bytes)     |
+--------+--------+------------------+
|         Rest of Header            |
|         (4 bytes)                 |
+-----------------------------------+
|              Data                 |
+-----------------------------------+
```

### 주요 Type 값
| Type | Code | 의미 |
|------|------|------|
| `0` | `0` | Echo Reply (ping 응답) |
| `3` | `0~15` | Destination Unreachable |
| `8` | `0` | Echo Request (ping 요청) |
| `11` | `0` | TTL Exceeded |

### 구현 내용
- `tcpsniffer.py`에서 ICMP 헤더 Type/Code 파싱 구현

### 구현 계획 (미구현 부분)
- ICMP Echo Request/Reply 전송 (ping 구현)
- ICMP Destination Unreachable 생성
- Traceroute 구현 (TTL Exceeded 활용)

---

## IPv6 (Internet Protocol version 6)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **표준** | RFC 8200 |

### 개요
IPv6는 IPv4 주소 고갈 문제를 해결하기 위한 차세대 인터넷 프로토콜입니다.  
128비트 주소 체계를 사용하며, 헤더를 단순화하고 확장 헤더(Extension Header) 체계를 도입했습니다.

### 기본 헤더 구조 (40바이트 고정)
```
 0               1               2               3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version| Traffic Class |            Flow Label                 |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Payload Length        |  Next Header  |   Hop Limit   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
+                       Source Address (128 bits)               +
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
+                    Destination Address (128 bits)             +
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### IPv4 vs IPv6 비교
| 항목 | IPv4 | IPv6 |
|------|------|------|
| 주소 길이 | 32비트 | 128비트 |
| 헤더 크기 | 가변(20~60B) | 고정(40B) |
| 체크섬 | 있음 | 없음 |
| 브로드캐스트 | 있음 | 없음 (멀티캐스트로 대체) |
| ARP | ARP | NDP (ICMPv6) |

### 구현 계획
- IPv6 기본 헤더 직렬화/파싱
- 확장 헤더 처리 (Hop-by-Hop, Routing, Fragment)
- IPv6 주소 표기법 변환

---

## ICMPv6

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **표준** | RFC 4443 |

### 개요
ICMPv6는 IPv6 환경에서 오류 보고, 진단, 이웃 탐색(NDP)을 담당합니다.  
IPv4의 ARP, IGMP, ICMP 기능을 통합한 프로토콜입니다.

### 주요 Type 값
| Type | 의미 |
|------|------|
| `1` | Destination Unreachable |
| `128` | Echo Request |
| `129` | Echo Reply |
| `133` | Router Solicitation (NDP) |
| `134` | Router Advertisement (NDP) |
| `135` | Neighbor Solicitation (NDP, ARP 대체) |
| `136` | Neighbor Advertisement (NDP, ARP Reply 대체) |

### 구현 계획
- ICMPv6 Echo Request/Reply
- NDP (Neighbor Discovery Protocol) - Neighbor Solicitation/Advertisement

---

## OSPF (Open Shortest Path First)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **표준** | RFC 2328 (OSPFv2), RFC 5340 (OSPFv3) |

### 개요
OSPF는 링크 상태 라우팅 프로토콜로, 자율 시스템(AS) 내부에서 사용됩니다.  
Dijkstra 알고리즘으로 최단 경로를 계산하며, Area 개념으로 네트워크를 계층화합니다.

### 패킷 타입
| Type | 이름 | 설명 |
|------|------|------|
| `1` | Hello | 이웃 라우터 탐색 및 유지 |
| `2` | DBD | 라우터 데이터베이스 요약 교환 |
| `3` | LSR | 링크 상태 요청 |
| `4` | LSU | 링크 상태 업데이트 |
| `5` | LSAck | 링크 상태 확인 응답 |

### 구현 계획
- OSPF Hello 패킷 생성 및 파싱
- LSA(Link State Advertisement) 생성
- SPF(Dijkstra) 알고리즘으로 라우팅 테이블 계산

---

## RIP (Routing Information Protocol)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **표준** | RFC 2453 (RIPv2) |

### 개요
RIP는 거리 벡터 라우팅 프로토콜로, 홉 카운트(최대 15)를 메트릭으로 사용합니다.  
구현이 단순하지만 대규모 네트워크에는 적합하지 않습니다.

### 구현 계획
- RIP Request/Response 패킷 생성
- 라우팅 테이블 업데이트 로직
- 벨만-포드 알고리즘으로 경로 계산

---

## BGP (Border Gateway Protocol)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **표준** | RFC 4271 |

### 개요
BGP는 인터넷 AS 간의 라우팅을 담당하는 외부 게이트웨이 프로토콜입니다.  
TCP 포트 179를 사용하며, 경로 정책 기반으로 라우팅을 결정합니다.

### 메시지 타입
| Type | 이름 | 설명 |
|------|------|------|
| `1` | OPEN | BGP 세션 수립 |
| `2` | UPDATE | 라우팅 정보 교환 |
| `3` | NOTIFICATION | 오류 통보 및 세션 종료 |
| `4` | KEEPALIVE | 세션 유지 |

### 구현 계획
- BGP OPEN/KEEPALIVE 메시지 생성
- UPDATE 메시지 파싱 (NLRI, Path Attributes)
- 간단한 BGP 세션 상태 머신 구현
