# L7 응용 계층 프로토콜

응용 계층은 OSI 7계층으로, 사용자와 가장 가까운 계층입니다.  
HTTP, DNS, SMTP 등 다양한 네트워크 서비스를 제공하는 프로토콜을 포함합니다.

---

## HTTP (HyperText Transfer Protocol)

| 항목 | 내용 |
|------|------|
| **구현 여부** | 🔶 부분 구현 |
| **소스 파일** | `Web/getflooding.py`, `Web/slowlorisattack.py`, `Web/slowreadattack.py` |
| **표준** | RFC 9110 (HTTP), RFC 9112 (HTTP/1.1) |

### 개요
HTTP는 웹의 근간이 되는 요청-응답 프로토콜입니다.  
클라이언트(브라우저)가 서버에 리소스를 요청하고 서버가 응답하는 텍스트 기반 프로토콜로,  
현재 HTTP/1.1, HTTP/2, HTTP/3(QUIC 기반)까지 발전했습니다.

### HTTP/1.1 요청 메시지 구조
```
GET /index.html HTTP/1.1\r\n
Host: example.com\r\n
User-Agent: Mozilla/5.0\r\n
Accept: text/html\r\n
\r\n
(요청 본문 - POST/PUT의 경우)
```

### 주요 메서드
| 메서드 | 설명 |
|-------|------|
| `GET` | 리소스 조회 |
| `POST` | 데이터 전송 (리소스 생성) |
| `PUT` | 리소스 대체/생성 |
| `PATCH` | 리소스 부분 수정 |
| `DELETE` | 리소스 삭제 |
| `HEAD` | 헤더만 조회 |
| `OPTIONS` | 지원 메서드 조회 |

### 주요 상태 코드
| 코드 | 의미 |
|------|------|
| `200` | OK |
| `301` | Moved Permanently |
| `400` | Bad Request |
| `401` | Unauthorized |
| `403` | Forbidden |
| `404` | Not Found |
| `500` | Internal Server Error |

### 구현 내용
- HTTP GET 요청 대량 전송 (`Web/getflooding.py`)
- Slowloris 공격: HTTP 헤더를 느리게 전송하여 연결 점유 (`Web/slowlorisattack.py`)
- Slow Read 공격: TCP Window Size를 최소화하여 서버 응답 전송 속도 저하 (`Web/slowreadattack.py`)

### 구현 계획 (미구현 부분)
- HTTP/1.1 요청/응답 파서
- 간단한 HTTP 서버 구현 (소켓 기반)
- HTTPS(TLS 위에서 동작하는 HTTP) 연동

---

## DNS (Domain Name System)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **표준** | RFC 1034, RFC 1035 |

### 개요
DNS는 도메인 이름을 IP 주소로 변환(이름 해석)하는 분산 데이터베이스 시스템입니다.  
UDP 포트 53을 사용하며(응답이 512바이트 초과 시 TCP 사용), 계층적 네임스페이스 구조를 가집니다.

### 메시지 구조
```
+---------------------------+
|       Header (12B)        |
+---------------------------+
|       Question            |
+---------------------------+
|       Answer RR           |
+---------------------------+
|       Authority RR        |
+---------------------------+
|       Additional RR       |
+---------------------------+
```

### 주요 레코드 타입
| 타입 | 설명 |
|------|------|
| `A` | IPv4 주소 |
| `AAAA` | IPv6 주소 |
| `CNAME` | 별칭(Canonical Name) |
| `MX` | 메일 서버 |
| `NS` | 네임 서버 |
| `PTR` | 역방향 조회 (IP → 도메인) |
| `TXT` | 텍스트 레코드 |

### 구현 계획
- DNS Query 메시지 생성 (A 레코드 조회)
- DNS Response 파싱
- 간단한 DNS 리졸버 구현 (재귀/반복 조회)
- DNS 증폭 공격(DNS Amplification) 패킷 생성

---

## DHCP (Dynamic Host Configuration Protocol)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **표준** | RFC 2131 |

### 개요
DHCP는 클라이언트에게 IP 주소, 서브넷 마스크, 게이트웨이, DNS 서버를 자동으로 할당하는 프로토콜입니다.  
UDP 포트 67(서버), 68(클라이언트)를 사용합니다.

### DORA 4단계 과정
```
Client                              Server
  |                                    |
  |--DHCP Discover (broadcast)-------->|
  |                                    |
  |<-DHCP Offer (unicast/broadcast)----|
  |                                    |
  |--DHCP Request (broadcast)--------->|
  |                                    |
  |<-DHCP ACK--------------------------|
  |                                    |
```

### 구현 계획
- DHCP Discover/Request 패킷 생성
- DHCP Offer/ACK 파싱
- DHCP Starvation 공격 (DHCP 주소 풀 고갈) 시뮬레이션

---

## FTP (File Transfer Protocol)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **표준** | RFC 959 |

### 개요
FTP는 파일 전송을 위한 프로토콜로, 제어 연결(TCP 21)과 데이터 연결(TCP 20)을 분리해서 사용합니다.  
Active 모드와 Passive 모드 두 가지 동작 방식이 있습니다.

### 주요 명령어
| 명령 | 설명 |
|------|------|
| `USER` | 사용자명 전송 |
| `PASS` | 비밀번호 전송 |
| `LIST` | 디렉토리 목록 |
| `RETR` | 파일 다운로드 |
| `STOR` | 파일 업로드 |
| `QUIT` | 연결 종료 |

### 구현 계획
- FTP 클라이언트 구현 (제어 채널 통신)
- Passive 모드 데이터 연결 처리
- FTP 평문 자격증명 스니핑 시뮬레이션

---

## SMTP (Simple Mail Transfer Protocol)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **표준** | RFC 5321 |

### 개요
SMTP는 이메일 전송을 위한 프로토콜입니다.  
TCP 포트 25(서버 간), 587(클라이언트→서버 제출)을 사용하며,  
수신에는 POP3(110) 또는 IMAP(143)을 사용합니다.

### 주요 명령어
| 명령 | 설명 |
|------|------|
| `EHLO` | 서버 인사 (ESMTP) |
| `MAIL FROM` | 발신자 주소 |
| `RCPT TO` | 수신자 주소 |
| `DATA` | 메일 본문 시작 |
| `QUIT` | 연결 종료 |

### 구현 계획
- SMTP 클라이언트 구현 (소켓 기반)
- 메일 헤더(From, To, Subject) 구성
- SMTP 오픈 릴레이 테스트

---

## SSH (Secure Shell)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **표준** | RFC 4251~4256 |

### 개요
SSH는 암호화된 원격 접속, 파일 전송(SCP, SFTP), 포트 포워딩을 제공하는 프로토콜입니다.  
TCP 포트 22를 사용하며, 키 교환(Diffie-Hellman), 인증(공개키/비밀번호), 암호화(AES, ChaCha20) 등을 지원합니다.

### 프로토콜 계층
```
+---------------------------+
|     SSH Connection        |  (채널, 포트포워딩)
+---------------------------+
|   SSH Authentication      |  (공개키, 비밀번호)
+---------------------------+
|     SSH Transport         |  (키 교환, 암호화)
+---------------------------+
|         TCP               |
+---------------------------+
```

### 구현 계획
- SSH 핸드셰이크 흐름 분석 (패킷 파싱)
- SSH 버전 배너 수집
- SSH 브루트포스 테스트 클라이언트 (paramiko 활용)

---

## TLS/SSL (Transport Layer Security)

| 항목 | 내용 |
|------|------|
| **구현 여부** | ❌ 미구현 |
| **소스 파일** | - |
| **표준** | RFC 8446 (TLS 1.3), RFC 5246 (TLS 1.2) |

### 개요
TLS는 TCP 위에서 암호화 통신을 제공하는 프로토콜로, SSL의 후속 표준입니다.  
HTTPS, SMTPS, IMAPS, FTPS 등의 프로토콜이 TLS를 기반으로 합니다.

### TLS 1.3 핸드셰이크 흐름
```
Client                          Server
  |                               |
  |---ClientHello---------------->|
  |                               |
  |<--ServerHello-----------------|
  |<--{EncryptedExtensions}-------|
  |<--{Certificate}---------------|
  |<--{CertificateVerify}---------|
  |<--{Finished}------------------|
  |                               |
  |---{Finished}----------------->|
  |                               |
  |<====암호화 통신 시작============>|
```

### 구현 계획
- TLS ClientHello 패킷 생성 및 파싱
- 지원 암호화 스위트 협상 분석
- 인증서 파싱 (X.509)
- TLS 다운그레이드 공격 시뮬레이션
