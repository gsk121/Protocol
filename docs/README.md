# 프로토콜 구현 현황

이 문서는 본 저장소에서 다루는 네트워크 프로토콜 전체 목록과 각 프로토콜의 개요, Python 소스 구현 여부를 정리합니다.

---

## 구현 현황 요약

| 계층 | 프로토콜 | 구현 여부 | 소스 파일 |
|------|---------|-----------|----------|
| **L2 데이터링크** | Ethernet II | ✅ 구현됨 | `header/eth.py` |
| **L2 데이터링크** | ARP | ✅ 구현됨 | `header/arp.py`, `posion1.py`, `posion2.py` |
| **L2 데이터링크** | IEEE 802.1Q (VLAN) | ❌ 미구현 | - |
| **L2 데이터링크** | PPP | ❌ 미구현 | - |
| **L2 데이터링크** | STP | ❌ 미구현 | - |
| **L3 네트워크** | IPv4 | ✅ 구현됨 | `header/ip.py` |
| **L3 네트워크** | IPv6 | ❌ 미구현 | - |
| **L3 네트워크** | ICMPv4 | 🔶 부분 구현 | `tcpsniffer.py` (파싱만) |
| **L3 네트워크** | ICMPv6 | ❌ 미구현 | - |
| **L3 네트워크** | OSPF | ❌ 미구현 | - |
| **L3 네트워크** | RIP | ❌ 미구현 | - |
| **L3 네트워크** | BGP | ❌ 미구현 | - |
| **L4 전송** | TCP | ✅ 구현됨 | `header/tcp.py`, `3-way_handshake.py`, `tcppacket.py`, `tcpsniffer.py` |
| **L4 전송** | UDP | ✅ 구현됨 | `header/udp.py`, `udpflooding.py` |
| **L4 전송** | SCTP | ❌ 미구현 | - |
| **L7 응용** | HTTP | 🔶 부분 구현 | `Web/getflooding.py` (공격용) |
| **L7 응용** | DNS | ❌ 미구현 | - |
| **L7 응용** | DHCP | ❌ 미구현 | - |
| **L7 응용** | FTP | ❌ 미구현 | - |
| **L7 응용** | SMTP | ❌ 미구현 | - |
| **L7 응용** | SSH | ❌ 미구현 | - |
| **L7 응용** | TLS/SSL | ❌ 미구현 | - |
| **보안/공격** | SYN Flooding | ✅ 구현됨 | `SYNFlooding.py` |
| **보안/공격** | UDP Flooding | ✅ 구현됨 | `udpflooding.py` |
| **보안/공격** | ARP Poisoning | ✅ 구현됨 | `posion1.py`, `posion2.py` |
| **보안/공격** | HTTP GET Flooding | ✅ 구현됨 | `Web/getflooding.py` |
| **보안/공격** | Slowloris | ✅ 구현됨 | `Web/slowlorisattack.py` |
| **보안/공격** | Slow Read | ✅ 구현됨 | `Web/slowreadattack.py` |

---

## 계층별 상세 문서

- [L2 데이터링크 계층 프로토콜](layer2-datalink.md)
- [L3 네트워크 계층 프로토콜](layer3-network.md)
- [L4 전송 계층 프로토콜](layer4-transport.md)
- [L7 응용 계층 프로토콜](layer7-application.md)
- [보안/공격 기법 구현](security-attacks.md)

---

## 범례

| 기호 | 의미 |
|------|------|
| ✅ | Python 소스로 완전 구현됨 |
| 🔶 | 부분적으로 구현됨 (일부 기능만) |
| ❌ | 미구현 (향후 구현 대상) |
