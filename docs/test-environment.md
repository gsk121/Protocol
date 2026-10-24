# 프로토콜 헤더 개발·테스트 환경 구성 가이드

Windows에서 소스를 작성하고 Rocky Linux에서 직접 만든 Ethernet/ARP/IPv4/TCP/UDP 헤더를 검사한다. 기존 Rocky 서버가 없으면 VMware의 Rocky VM 한 대로 같은 실습을 진행한다. **저장소의 기존 Python 소스는 수정하지 않는다.**

설정 → 기본 통신 → 직접 만든 패킷 → 수신 측 캡처 순서로 확인한다. `send()` 호출 성공, 상대편 캡처, 상대 OS의 패킷 수용, TCP 연결 수립은 서로 다른 결과다.

## 1. 버전과 실습 범위

| 항목 | 기준 |
|---|---|
| Windows | VS Code, Remote - SSH, Python 확장, OpenSSH 클라이언트, Wireshark |
| Linux | 지원 중인 Rocky Linux 9.x의 최신 마이너 버전 권장. 기존 Rocky 10.x도 사용 가능 |
| Python | 이 문서의 실행기는 `/usr/bin/python3.12`로 통일 |
| 소스 문법상 최소 | Python 3.6: `0b_0000_0010` 같은 숫자 구분자 사용 |
| Python 추가 패키지 | 없음. 표준 라이브러리와 저장소의 `header/`만 사용 |
| Linux 도구 | `git`, `iproute`, `iputils`, `tcpdump`, `coreutils`, `openssh-server` |
| 권한 | 일반 계정으로 편집. 가상망 생성 및 raw socket 실행에는 `sudo` 필요 |

Rocky 9.4부터 Python 3.12가 제공된다. **9.4에 고정하라는 뜻은 아니며**, 지원 중인 최신 9.x에서 설치한다. Rocky 10에도 Python 3.12가 포함된다. 시스템의 `python3` 심볼릭 링크나 기본 버전은 바꾸지 않는다. Python 3.6은 문법 하한이며 신규 설치 권장 버전이 아니다.

Windows에서도 `header/`의 바이트 생성은 검사할 수 있다. 그러나 이 저장소의 `AF_PACKET` 송수신은 Linux 기능이므로, Windows Python과 관리자 권한만으로 raw socket 예제를 실행할 수는 없다.

### 작성 시 검증 범위

- 기준일: 2026-10-24. 기존 소스 기준 커밋: `4400cdf`.
- Windows Python 3.15.1에서 기존 소스 20개의 문법 컴파일과 헤더 관련 오프라인 검사를 수행했다.
- Python 3.6·3.12 문법 모드에서 20개 파일의 파싱을 확인했다. 해당 버전의 실제 런타임 검증과는 다르다.
- 문서의 헤더 바이트 예제를 실행하고, 원본 `tcppacket.py`를 가짜 소켓으로 실행하여 안내한 입력의 프레임·체크섬을 확인했다. 실제 패킷은 송신하지 않았다.
- Bash와 PowerShell 코드 블록은 각 셸의 구문 검사로 확인했다.
- 아래 Rocky/VMware 설치·네트워크 명령의 출력은 **정상 결과 판정 기준**이다. 이 문서 작성 과정에서 실제 Rocky 서버나 VMware VM의 종단 간 송수신을 검증하지 않았다.

## 2. 공통 구성과 실행 위치

```text
Windows PC: VS Code / Wireshark
     │ SSH: 소스 편집·터미널 / SCP: PCAP 가져오기
     ▼
Rocky Linux (실제 서버 또는 VMware VM)
     ├─ 기본 네트워크 공간: 기존 SSH 관리망
     └─ 실습망: proto-a/eth0 ═══ veth ═══ proto-b/eth0
```

네트워크 네임스페이스는 인터페이스·IP·라우팅을 나누는 Linux 기능이다. `veth`는 양끝을 연결하는 가상 이더넷 장치다. 두 끝을 각각 `proto-a`, `proto-b`에 넣으며, 실제 NIC·브리지·게이트웨이와 연결하지 않는다. 별도 서버 두 대는 필요 없다.

| 공간 | 인터페이스 | IPv4 | MAC | 기본 역할 |
|---|---|---|---|---|
| `proto-a` | `eth0` | `192.168.1.9/24` | `00:50:56:32:c2:bf` | 에코 서버 / 직접 만든 TCP 패킷 송신 |
| `proto-b` | `eth0` | `192.168.1.8/24` | `00:0c:29:cc:aa:71` | 에코 클라이언트 / TCP 패킷 수신·캡처 |

이 주소는 `ServerClient/*server.py`, `tcppacket.py`, `tcpsniffer.py`의 고정값에 맞춘 것이다. 임의의 `10.x` 주소로 대체하면 기존 소스와 맞지 않는다. MAC도 실물 NIC에 설정하지 않고 위 가상 인터페이스에만 적용한다.

실습망 안에는 기본 경로를 만들지 않는다. 관리망과 같은 IP 대역이어도 서로 다른 네임스페이스에 있어 분리되지만, 명령 실행 위치를 반드시 확인한다. **프로세스·파일·CPU·메모리는 공유**하므로 운영 서버에서 부하 실험을 하는 용도가 아니다. 아래 절차는 짧은 메시지와 단일 패킷 관찰에 한정한다.

이 문서의 `bash` 블록은 Rocky 터미널, `powershell` 블록은 Windows PowerShell에서 실행한다. `labuser`, `ROCKY_MANAGEMENT_IP`는 자신의 Linux 계정과 관리 IP로 바꾼다.

## 3. Rocky 실행 환경 준비

### 3.1 기존 서버가 있는 경우

Windows PowerShell에서 먼저 확인한다.

```powershell
ssh -V
ssh labuser@ROCKY_MANAGEMENT_IP
```

정상: OpenSSH 버전이 표시되고 Rocky 셸에 접속된다. 최초 접속 시 서버의 호스트 키 지문을 관리자 또는 서버 콘솔에서 대조한다. `ssh`가 없다면 Windows 설정의 선택적 기능에서 **OpenSSH 클라이언트**를 설치한다.

접속한 Rocky에서 확인한다.

```bash
cat /etc/os-release
uname -r
id
sudo -v
command -v python3.12 || true
```

정상: `ID="rocky"`, 지원 대상인 9.x 또는 10.x, 자신의 계정, 사용 가능한 `sudo` 권한을 확인한다. Rocky 8이거나 관리 권한이 없다면 이 문서를 이유로 서버를 업그레이드하지 말고, 관리자가 실습 환경을 제공하도록 하거나 다음 VMware 경로를 사용한다.

### 3.2 서버가 없을 때: VMware Workstation Pro

1. Windows에 [VMware Workstation Pro](https://www.vmware.com/products/desktop-hypervisor/workstation-and-fusion)를 설치한다. 호스트와 VMware 버전에 맞는 요구사항을 확인하고 CPU 가상화 기능을 활성화한다.
2. [Rocky 공식 다운로드](https://rockylinux.org/download)에서 지원 중인 Rocky 9.x x86_64 ISO와 체크섬을 받는다. 기존 Rocky 10 환경이 있다면 CPU 요구사항을 확인한 뒤 사용할 수 있다.
3. PowerShell에서 다운로드한 ISO의 SHA-256을 확인한다. 아래 파일명은 실제 이름으로 바꾼다.

   ```powershell
   Get-FileHash -Algorithm SHA256 "$env:USERPROFILE\Downloads\Rocky-9-latest-x86_64-minimal.iso"
   ```

   정상: 공식 체크섬과 일치한다.

4. 새 VM을 만들고 ISO로 설치한다. **예시 할당**은 2 vCPU, 메모리 4GB, 가상 디스크 30GB다. 이는 공식 최소 사양이 아니라 이 실습용 제안이다.
5. 가상 NIC 하나를 **NAT**에 연결한다. 패키지 다운로드와 Windows↔VM 관리 통신에 사용한다. 실제 LAN에 붙이는 Bridged 구성은 필요 없다. 실습 패킷은 이 NIC가 아니라 VM 내부의 `veth`에서 주고받는다.
6. Rocky 설치 시 일반 사용자 `labuser`를 만들고 관리자 권한을 부여한다. 설치 후 재부팅하고 ISO를 분리한다.
7. VM 콘솔에서 SSH 서버를 준비하고 관리 IP를 확인한다.

   ```bash
   sudo dnf install -y openssh-server
   sudo systemctl enable --now sshd
   systemctl is-active sshd
   ip -4 -br address
   ```

   정상: `active`와 `ens33` 등 관리 NIC의 IPv4가 표시된다. 이 주소가 `ROCKY_MANAGEMENT_IP`다. `192.168.1.9`와 `192.168.1.8`은 나중에 만들 실습용 주소이므로 SSH 접속 주소로 쓰지 않는다.

8. Windows에서 `ssh labuser@ROCKY_MANAGEMENT_IP`로 접속한다. NAT의 호스트 가상 어댑터(VMnet8)가 활성화되어 있으면 Windows 호스트에서 VM의 관리 IP로 접속할 수 있다. 방화벽으로 막혔다면 **새 VM 콘솔에서만** 다음을 확인한다.

   ```bash
   sudo firewall-cmd --get-active-zones
   ```

   관리 NIC가 속한 zone을 확인한 후, 아래 `public`을 그 zone 이름으로 맞춘다. `firewalld`가 실행 중이지 않다면 이 단계는 생략한다.

   ```bash
   SSH_ZONE=public
   sudo firewall-cmd --zone="$SSH_ZONE" --query-service=ssh
   sudo firewall-cmd --permanent --zone="$SSH_ZONE" --add-service=ssh
   sudo firewall-cmd --reload
   sudo firewall-cmd --zone="$SSH_ZONE" --query-service=ssh
   ```

   정상: 마지막 결과가 `yes`. 기존 서버는 이미 사용하는 SSH 정책을 유지한다. SELinux나 방화벽 전체를 끄지 않는다.

9. 아래 패키지와 VS Code 연결까지 준비한 뒤 VMware 스냅샷을 만든다. 이후는 실제 서버와 같은 절차다. 인터넷이 필요 없는 환경에서는 패키지를 미리 준비한 후 Host-only 관리망으로 대체할 수 있다.

### 3.3 공통 패키지와 저장소

Rocky 버전에 맞는 Python 패키지를 확인하고 설치한다. **아래 두 블록 중 자신의 OS에 해당하는 것 하나만** 실행한다.

Rocky 9.x:

```bash
sudo dnf info python3.12
sudo dnf install -y python3.12
```

Rocky 10.x: Python 3.12의 RPM 이름이 `python3`이다.

```bash
sudo dnf info python3
sudo dnf install -y python3
```

그다음 공통 도구와 실행기를 확인한다.

```bash
sudo dnf install -y git iproute iputils tcpdump coreutils openssh-server
/usr/bin/python3.12 --version
ip -Version
tcpdump --version
timeout --version
```

정상: `Python 3.12.x`와 각 도구 버전이 출력된다. 패키지를 찾지 못하면 Rocky 버전과 BaseOS/AppStream 저장소 활성 여부(`dnf repolist`)를 먼저 확인한다. 기존 서버의 저장소나 OS를 무조건 변경하지 않는다.

일반 사용자 홈 디렉터리에 저장소가 없을 때 한 번만 복제한다.

```bash
git clone https://github.com/gsk121/Protocol.git "$HOME/Protocol"
cd "$HOME/Protocol"
git rev-parse --short HEAD
git status --short
```

이미 복제했다면 다시 clone하지 않고 그 폴더를 사용한다. 아래의 `PROTOCOL_DIR`을 실제 절대 경로로 맞춘다. Windows의 `D:\git\Protocol`과 Linux 복사본은 자동 동기화되지 않는다. 이후 편집과 실행은 Linux 복사본에서 통일한다.

**새 Rocky 터미널을 열 때마다** 다음을 실행한다.

```bash
export PROTOCOL_DIR="$HOME/Protocol"
cd "$PROTOCOL_DIR"
test -f "$PROTOCOL_DIR/header/eth.py" && echo WORKSPACE_OK
```

정상: `WORKSPACE_OK`. 추가 `pip install`이나 가상환경은 이 예제 실행에 필수적이지 않다.

## 4. Windows 소스 작성 환경

1. Windows에 [VS Code](https://code.visualstudio.com/)와 [Wireshark](https://www.wireshark.org/download.html)를 설치한다. Windows에서 PCAP 파일만 열 때는 로컬 패킷 캡처 드라이버가 필수는 아니다.
2. VS Code에 Microsoft의 **Remote - SSH**와 **Python** 확장을 설치한다.
3. `Remote-SSH: Add New SSH Host...`에서 앞서 성공한 SSH 접속을 등록한다. `%USERPROFILE%\.ssh\config`의 예시는 다음과 같다. 기존 항목은 덮어쓰지 않는다.

   ```sshconfig
   Host protocol-lab
       HostName ROCKY_MANAGEMENT_IP
       User labuser
   ```

4. `Remote-SSH: Connect to Host...` → `protocol-lab`에 접속하고 `/home/labuser/Protocol`을 연다. Python 확장도 원격 Rocky 쪽에 설치한다. VS Code Server와 확장 설치에는 초기 다운로드 경로가 필요하다.
5. `Python: Select Interpreter`에서 `/usr/bin/python3.12`를 선택한다. 터미널에서 `hostname`, `pwd`, `/usr/bin/python3.12 --version`을 확인한다.

정상: 편집기가 원격 연결 상태이고, 터미널은 Rocky의 저장소 경로와 Python 3.12를 표시한다. `header/*.py`의 바이트 생성 로직은 일반 사용자 디버거로 추적한다. 패킷 예제는 아래 네임스페이스 터미널 명령으로 실행한다. IDE 전체를 root로 실행하지 않는다.

현재 루트 예제는 `from eth import *`처럼 `header/`를 직접 검색한다. 소스를 고치지 않고 실행하려면 **해당 명령에만** `PYTHONPATH="$PROTOCOL_DIR/header"`를 전달한다. `sudo`가 환경변수를 제거할 수 있으므로 아래 명령처럼 `sudo ... env PYTHONPATH=...` 순서를 유지한다.

## 5. 독립된 송신·수신 실습망 만들기

### 5.1 생성: 한 번만 실행

Rocky 관리 터미널에서 실행한다. 동일 이름이 있으면 중단하며, 다른 사람이 사용하는 네임스페이스를 자동 삭제하지 않는다. `proto-a`, `proto-b`, `proto-va`, `proto-vb`는 이 실습 전용 이름이다.

```bash
sudo bash <<'BASH'
set -eu
for ns in proto-a proto-b; do
    if ip netns list | awk '{print $1}' | grep -Fxq "$ns"; then
        echo "이미 존재하는 네임스페이스: $ns. 10절에서 상태를 확인하세요." >&2
        exit 1
    fi
done
for dev in proto-va proto-vb; do
    if ip link show dev "$dev" >/dev/null 2>&1; then
        echo "이미 존재하는 인터페이스: $dev" >&2
        exit 1
    fi
done
ip netns add proto-a
ip netns add proto-b
ip link add proto-va type veth peer name proto-vb
ip link set proto-va netns proto-a
ip link set proto-vb netns proto-b
ip -n proto-a link set proto-va name eth0
ip -n proto-b link set proto-vb name eth0
ip -n proto-a link set eth0 address 00:50:56:32:c2:bf
ip -n proto-b link set eth0 address 00:0c:29:cc:aa:71
ip -n proto-a address add 192.168.1.9/24 dev eth0
ip -n proto-b address add 192.168.1.8/24 dev eth0
for ns in proto-a proto-b; do
    ip -n "$ns" link set lo up
    ip -n "$ns" link set eth0 up
done
echo LAB_CREATED
BASH
```

정상: `LAB_CREATED`. 중간 오류가 나면 재실행부터 하지 말고 `sudo ip netns list`와 10절로 부분 생성 상태를 확인한다. 이 구성은 재부팅하면 다시 만들어야 한다.

### 5.2 주소·경로·도달성 확인

```bash
sudo ip -n proto-a -br address
sudo ip -n proto-b -br address
sudo ip -n proto-a -br link
sudo ip -n proto-b -br link
sudo ip -n proto-a route show
sudo ip -n proto-b route show
sudo ip -n proto-a route show default
sudo ip -n proto-b route show default
sudo ip netns exec proto-a ping -c 2 -W 1 192.168.1.8
```

정상: 양쪽 `eth0`에 표의 IP/MAC이 있고 인터페이스가 UP이다. 경로는 `192.168.1.0/24 dev eth0 ...`이며, 두 `route show default` 출력은 비어 있다. ping 결과는 `2 received`, `0% packet loss`다. `eth0@if...` 뒤의 번호는 환경마다 달라도 된다.

raw socket 권한도 **송신하지 않고** 확인한다.

```bash
sudo ip netns exec proto-a /usr/bin/python3.12 -c 'import socket; s=socket.socket(socket.AF_PACKET, socket.SOCK_RAW); s.bind(("eth0", 3)); print("RAW_SOCKET_OK"); s.close()'
```

정상: `RAW_SOCKET_OK`. 두 네임스페이스 모두 `lo`, `eth0` 외에 관리 NIC가 없어야 한다. 관리 NIC를 옮기거나 IP forwarding/NAT를 활성화할 필요가 없다.

## 6. 단계별 테스트

### 6.1 헤더를 바이트로 만들기: 네트워크 사용 없음

Rocky의 저장소 루트에서 실행한다. 기존 클래스의 알려진 getter 문제를 피하고, 실제 직렬화 바이트를 `struct`로 독립 확인한다.

```bash
/usr/bin/python3.12 -B - <<'PY'
from struct import unpack
from header.eth import Eth
from header.arp import Arp
from header.ip import IP
from header.tcp import Tcp
from header.udp import Udp
from header.chk import make_chksum

eth = Eth()
eth.src = '00:50:56:32:c2:bf'
eth.dst = '00:0c:29:cc:aa:71'
eth.type = 0x0800
assert len(eth.get_header()) == 14
assert unpack('!H', eth.get_header()[12:14])[0] == 0x0800
arp = Arp()
arp.opcode = 1
assert len(arp.get_header) == 28
assert unpack('!H', arp.get_header[6:8])[0] == 1
ip = IP()
ip.Ver, ip.HeaderLen, ip.TotalLen, ip.ttl, ip.Protocol = 4, 20, 40, 64, 6
ip.src, ip.dst = '192.168.1.9', '192.168.1.8'
ip.Checksum = make_chksum(ip.get_header)
assert ip.get_header[0] == 0x45 and make_chksum(ip.get_header) == 0
tcp = Tcp()
tcp.src_port, tcp.dst_port, tcp.Offset = 40000, 12000, 20
assert len(tcp.get_header) == 20 and tcp.get_header[12] == 0x50
udp = Udp()
udp.src_port, udp.dst_port, udp.Data = 10000, 20000, b'hello'
udp.HeaderLen = len(udp.get_header)
assert udp.HeaderLen == 13 and udp.get_header[8:] == b'hello'
for name, raw in [('Ethernet', eth.get_header()), ('ARP', arp.get_header),
                  ('IPv4', ip.get_header), ('TCP', tcp.get_header), ('UDP', udp.get_header)]:
    print(name, len(raw), raw.hex(' '))
print('HEADER_BYTES_OK')
PY
```

정상: 길이가 순서대로 `14`, `28`, `20`, `20`, `13`이며 마지막에 `HEADER_BYTES_OK`가 출력된다. 이 검사는 대표 필드의 바이트 배치 확인이다. 여기서 생성한 TCP/UDP 객체의 모든 필드를 채우거나 전송 체크섬까지 완성한 것은 아니므로, 이 바이트를 바로 전송하는 예제로 해석하지 않는다.

### 6.2 TCP 에코: 먼저 실습망과 일반 소켓 확인

VS Code에서 Rocky 터미널 두 개를 열고 각각 3.3절의 `PROTOCOL_DIR` 설정과 `cd`를 실행한다. `timeout`은 무한 반복 예제를 제한하며, 시간 종료 시 코드 `124`는 예상된 결과다. `-k 3s`는 종료 요청 후에도 남는 프로세스를 제한한다. 입력을 받는 예제에는 `--foreground`를 붙여 `sudo`의 터미널 설정에 따라 입력 프로세스가 정지하는 것을 피한다.

**터미널 A — 서버를 먼저 실행:**

```bash
sudo ip netns exec proto-a timeout -k 3s 90s /usr/bin/python3.12 -B -u "$PROTOCOL_DIR/ServerClient/tcpechoserver.py"
```

접속 전 출력이 없어도 정상이다. 필요하면 다른 터미널에서 `sudo ip netns exec proto-a ss -ltn 'sport = :35000'`으로 LISTEN 상태를 확인한다.

**터미널 B — 클라이언트 실행:**

```bash
sudo ip netns exec proto-b timeout --foreground -k 3s 60s /usr/bin/python3.12 -B -u "$PROTOCOL_DIR/ServerClient/tcpechoclien.py" 192.168.1.9 35000
```

`input:`에 짧은 ASCII 문자열 `hello`를 입력한다. 정상: 클라이언트에 `echo:  hello`, 서버에 `echo:  hello`와 클라이언트 IP `192.168.1.8`이 표시된다. 공백 수와 임시 클라이언트 포트는 달라도 된다.

현 서버는 연결 종료 처리가 미완성이므로 클라이언트 종료 뒤 빈 로그가 반복될 수 있다. 정상 응답 한 번을 확인하면 실습을 마치고, 제한 시간 또는 10절의 네임스페이스별 프로세스 종료로 정리한다. `Ctrl+C`만으로 서버의 모든 스레드가 끝난다고 가정하지 않는다.

### 6.3 UDP 에코

**터미널 A — 서버:**

```bash
sudo ip netns exec proto-a timeout -k 3s 90s /usr/bin/python3.12 -B -u "$PROTOCOL_DIR/ServerClient/udpechoserver.py"
```

**터미널 B — 클라이언트:**

```bash
sudo ip netns exec proto-b timeout --foreground -k 3s 60s /usr/bin/python3.12 -B -u "$PROTOCOL_DIR/ServerClient/udpechoclientnc.py" 192.168.1.9 35000
```

`hello` 입력 후 클라이언트의 `echo:  hello`, 서버의 `data: hello`를 확인한다. 이 서버들은 OS가 TCP/UDP 헤더를 만드는 일반 소켓 예제다. **에코 성공만으로 `header/tcp.py`나 `header/udp.py`가 검증된 것은 아니다.**

### 6.4 직접 만든 TCP 패킷 한 개: 기존 `tcppacket.py` 사용

상대방의 일반 TCP 서버가 없어도 패킷 도착을 관찰할 수 있다. 먼저 `proto-b`에서 캡처를 시작하고, `listening on eth0`가 나온 뒤 송신한다.

**터미널 B — 캡처:**

```bash
mkdir -p "$HOME/protocol-captures"
sudo ip netns exec proto-b timeout -k 3s 60s tcpdump -i eth0 -nn -s 0 -U -c 1 -Z root -w "$HOME/protocol-captures/tcp-syn.pcap" 'ip src 192.168.1.9 and ip dst 192.168.1.8 and tcp src port 40000 and tcp dst port 12000 and tcp[13] = 2'
```

실습에서는 제한된 캡처가 사용자 홈에 파일을 쓰도록 `-Z root`를 명시했다. 임의 인터페이스나 장시간 캡처용 명령으로 확대하지 않는다. 파일이 이미 있으면 덮어쓰므로 결과를 남기려면 다른 파일명을 사용한다.

**터미널 A — 송신:**

```bash
sudo ip netns exec proto-a timeout --foreground -k 3s 30s env PYTHONPATH="$PROTOCOL_DIR/header" /usr/bin/python3.12 -B -u "$PROTOCOL_DIR/tcppacket.py"
```

질문에 순서대로 `1`, `0`, `40000`, `12000`, `2`를 입력한다. 각각 시퀀스, ACK 번호, 출발지 포트, 목적지 포트, SYN 플래그다. 정상: 송신 스크립트가 종료되고 캡처 터미널은 `1 packet captured`로 끝난다.

캡처 종료 후 Rocky에서 읽는다.

```bash
sudo tcpdump -nn -e -S -vvv -XX -r "$HOME/protocol-captures/tcp-syn.pcap"
sudo chown "$(id -u):$(id -g)" "$HOME/protocol-captures/tcp-syn.pcap"
```

정상 필드:

| 계층 | 기대값 |
|---|---|
| Ethernet | 출발지 `00:50:56:32:c2:bf`, 목적지 `00:0c:29:cc:aa:71`, EtherType `0x0800` |
| IPv4 | `192.168.1.9` → `192.168.1.8`, IHL 20바이트, Total Length 40, TTL 64, Protocol 6 |
| TCP | `40000` → `12000`, 시퀀스 1, ACK 값 0, 헤더 20바이트, SYN만 설정, Window 65535, 데이터 0바이트 |

프레임 캡처 길이는 드라이버의 패딩 등으로 달라질 수 있다. IPv4 Total Length와 필드값을 기준으로 확인한다. 상대 포트에 리스너가 없으면 커널이 RST를 보낼 수 있지만 **이 단계의 성공 기준은 보낸 SYN 한 개가 수신 측에서 올바르게 캡처되는 것**이다.

### 6.5 기존 스니퍼와 ARP 관찰

기존 스니퍼를 `proto-b`에서 제한 시간 동안 실행한 뒤, 다른 터미널에서 6.4절 송신을 한 번 반복한다.

```bash
sudo ip netns exec proto-b timeout -k 3s 30s env PYTHONPATH="$PROTOCOL_DIR/header" /usr/bin/python3.12 -B -u "$PROTOCOL_DIR/tcpsniffer.py"
```

정상: `40000 -> 12000 Seq:1, Ack:0 Flag: 00000010` 행이 보인다. RST 등 다른 패킷 행이 추가될 수 있다. 현재 스니퍼는 기본 IPv4 헤더 중심이므로 Wireshark를 별도의 확인 수단으로 사용한다.

ARP는 캐시 변경 스크립트 대신 가상망의 정상 주소 확인 요청으로 먼저 관찰한다. `proto-b`의 별도 터미널에서:

```bash
sudo ip netns exec proto-b timeout -k 3s 30s tcpdump -i eth0 -nn -e -c 2 arp
```

`listening on eth0`가 보이면 다른 터미널에서 **실습 인터페이스의 캐시만** 비우고 ping을 한 번 보낸다.

```bash
sudo ip -n proto-a neigh flush dev eth0
sudo ip netns exec proto-a ping -c 1 -W 1 192.168.1.8
```

정상: `who-has 192.168.1.8 tell 192.168.1.9` 요청과 `192.168.1.8 is-at 00:0c:29:cc:aa:71` 응답이 보인다. 이 패킷은 OS가 생성한 ARP이며, 직접 만든 `Arp`의 바이트 배치와 비교할 기준으로 사용한다.

### 6.6 나머지 파일의 위치와 제한

| 파일 | 이 환경에서의 활용 |
|---|---|
| `header/eth.py`, `arp.py`, `ip.py`, `tcp.py`, `udp.py`, `chk.py` | 6.1절에서 직접 바이트를 생성·확인. 실제 패킷과 필드 단위로 비교 |
| `tcppacket.py` | `proto-a`에서 기존 파일 그대로 단일 패킷 전송 |
| `tcpsniffer.py` | `proto-b`의 `eth0`에서 제한된 수신 관찰 |
| `ServerClient/` | 6.2~6.3절의 소스 수정 없는 에코 실습 |
| `3-way_handshake.py` | `.9` → `.8:12000`을 가정. 상대 리스너, OS 자동 RST, 응답 선택 문제를 이해한 뒤 별도 관찰할 심화 예제 |
| `udpflooding.py` | `.8` → `.2`와 다른 MAC을 사용하며 반복 송신한다. 기본 주소표와 맞지 않아 그대로 실행하는 단계에 포함하지 않음 |
| `posion1.py`, `posion2.py` | `.23` 등 다른 주소 및 변조된 ARP 조합을 사용. 정상 ARP 관찰과 구분하며 기본 통과 조건에서 제외 |
| `SYNFlooding.py`, `Web/*.py` | 고정된 별도 대상·반복 송신 시나리오. 헤더 구현 환경 확인에 필요하지 않아 실행 절차에서 제외 |

전체 TCP 연결 성공을 환경 설치의 통과 조건으로 삼지 않는다. `3-way_handshake.py`의 수신 처리와 커널의 자동 응답 때문에, 환경이 올바르더라도 연결이 완성되지 않을 수 있다. 이 문서는 해당 소스 수정이나 호스트 전체의 방화벽/RST 차단을 요구하지 않는다.

## 7. Windows Wireshark로 결과 확인

6.4절의 캡처가 끝나고 파일 소유권을 돌려준 다음, **Windows PowerShell**에서 가져온다.

```powershell
$captureDir = Join-Path $env:USERPROFILE 'Downloads\protocol-captures'
New-Item -ItemType Directory -Force -Path $captureDir | Out-Null
scp protocol-lab:protocol-captures/tcp-syn.pcap "$captureDir\tcp-syn.pcap"
```

Wireshark에서 이 파일을 열고 표시 필터 `ip.src == 192.168.1.9 && tcp.dstport == 12000`을 적용한다. Packet Details의 Ethernet II → Internet Protocol Version 4 → Transmission Control Protocol과 Packet Bytes를 함께 본다.

- MAC·IPv4 주소·포트·길이·SYN 플래그가 6.4절 표와 같은지 확인한다.
- 상대 시퀀스 표시가 켜져 있으면 `Sequence Number`가 0처럼 보일 수 있다. `Sequence Number (raw)`가 1인지 확인하거나 TCP 환경설정에서 상대 시퀀스 표시를 해제한다.
- IPv4/TCP 체크섬 검증을 프로토콜 환경설정에서 켜고 결과를 확인한다. 검증이 꺼진 상태의 `unverified`는 통과 판정이 아니다.
- 송신 측 캡처는 체크섬 오프로딩 때문에 미완성 체크섬으로 보일 수 있다. 수신 측 캡처·실제 바이트·독립 계산을 대조하고, 모든 오류를 오프로딩 탓으로 돌리지 않는다.
- `-i any` 캡처는 Linux cooked 형식일 수 있다. Ethernet 헤더 연습에서는 **해당 네임스페이스의 `-i eth0`**로 캡처한다. Windows의 실제 LAN NIC에서는 이 `veth` 실습망을 직접 볼 수 없다.

## 8. 환경 문제와 소스 문제 구분

| 증상 | 먼저 확인할 것 / 정상 기준 |
|---|---|
| `No module named eth` 등 | 실행 명령의 `env PYTHONPATH="$PROTOCOL_DIR/header"`, 저장소 절대 경로 확인 |
| `AF_PACKET`이 없음 | Windows 실행 여부 확인. Rocky의 `/usr/bin/python3.12`로 실행 |
| `Operation not permitted` | `sudo -v`와 5.2절 raw socket 점검. 모든 Python 실행기에 전역 capability를 부여하지 않음 |
| `Cannot find device eth0` | `sudo ip -n proto-a link`, `proto-b link` 확인. 관리 공간의 `ens33`과 혼동하지 않음 |
| `Cannot assign requested address` | 에코 서버는 `.9`가 있는 `proto-a`에서 실행해야 함 |
| `Connection refused` | 서버를 먼저 실행했는지, 같은 네임스페이스의 `ss -ltn`에 35000 LISTEN이 있는지 확인 |
| `Address already in use` | 이전 실습 프로세스/소켓 확인. 10절 정리 후 가상망을 재생성하거나 소켓 해제를 기다림 |
| ping 실패 | 양쪽 `eth0` UP, 주소표, `192.168.1.0/24` 경로 확인 |
| 송신은 끝났지만 PCAP에 없음 | 캡처를 먼저 시작했는지, 수신 네임스페이스·인터페이스·MAC·BPF 필터 확인 |
| 캡처가 60초 후 코드 124로 종료 | 제한 시간 종료. `tcpdump -r`로 실제 패킷 수를 확인하고 송신/캡처 순서를 점검 |
| PCAP를 쓰거나 SCP로 읽지 못함 | 캡처 디렉터리 존재, `-Z root`, 종료 후 해당 파일 `chown` 확인. SELinux 거부는 정책 담당자와 조사 |
| 시퀀스가 0으로 표시됨 | Wireshark 상대 표시와 raw 값을 구분 |
| `NameError`, `TypeError`, 잘못된 getter 값 | 기존 헤더 구현의 제한일 수 있음. 6.1절처럼 직렬화 바이트를 독립 해석 |
| 에코 종료 후 빈 로그 반복 | 기존 TCP 서버의 종료 처리 문제. 제한 시간 또는 실습 네임스페이스의 프로세스만 종료 |
| 네임스페이스 생성 중 `mount ... Operation not permitted` | 제한된 컨테이너/호스팅 환경인지 확인. 관리자에게 요청하거나 VMware VM 사용 |

## 9. 완료 판정과 기록

다음 항목을 확인하면 기본 실습 환경이 준비된 것이다.

- [ ] Windows에서 Rocky 관리 IP로 SSH 접속되고 원격 소스를 편집할 수 있다.
- [ ] Rocky 버전·커널·`python3.12 --version`·저장소 커밋을 기록했다.
- [ ] `proto-a`, `proto-b`의 IP/MAC이 주소표와 같고 두 공간에 기본 경로가 없다.
- [ ] ping과 TCP/UDP의 짧은 ASCII 에코가 성공했다.
- [ ] 오프라인 바이트 검사가 `HEADER_BYTES_OK`를 출력했다.
- [ ] `tcppacket.py`의 단일 SYN을 수신 측에서 캡처하고 필드값을 대조했다.
- [ ] PCAP를 Windows Wireshark로 열어 raw 시퀀스와 체크섬 검증 상태를 확인했다.
- [ ] 10절 정리 후 실습 프로세스·네임스페이스가 남지 않는다.

PCAP는 `$HOME/protocol-captures`에 보관한다. 실습 날짜, 실제 서버/VM 여부, 위 버전, 사용한 명령, 예상값과 다른 필드를 함께 기록하면 환경 변경과 구현 변경을 구분하기 쉽다.

## 10. 종료·초기화

먼저 실습 터미널의 제한 시간이 끝났는지 확인한다. 다음 명령은 **이 문서에서 직접 만든 `proto-a`, `proto-b`만** 대상으로 하며, 그 안의 실습 프로세스에 종료 신호를 보낸다. 공유 서버의 다른 네임스페이스나 전체 Python 프로세스에는 적용하지 않는다.

```bash
for ns in proto-a proto-b; do
    if sudo ip netns list | awk '{print $1}' | grep -Fxq "$ns"; then
        sudo ip netns pids "$ns" | xargs -r sudo kill -TERM
        sleep 1
        if [ -n "$(sudo ip netns pids "$ns")" ]; then
            echo "$ns: 프로세스가 남아 있습니다. timeout 종료 후 다시 확인하세요."
            continue
        fi
        sudo ip netns del "$ns"
    fi
done
sudo ip netns list
```

정상: 목록에 `proto-a`, `proto-b`가 없다. 양끝이 네임스페이스 안에 있던 `veth`도 함께 제거된다. 이름을 삭제해도 프로세스가 남으면 공간이 유지될 수 있으므로 위 순서를 지킨다. PCAP와 저장소는 삭제하지 않는다.

생성 도중 실패하여 기본 공간에 `proto-va` 또는 `proto-vb`가 남았다면 `ip -d link show proto-va`와 `ip -d link show proto-vb`로 확인한다. **이번 실습에서 만든 veth임이 확인된 경우에만** `sudo ip link delete proto-va` 또는 남은 쪽을 삭제한다. 한쪽을 삭제하면 짝도 제거되므로 두 명령을 무조건 실행하지 않는다.

다음 실습은 5절부터 시작한다. 가상망을 만들기 전부터 있던 동명 자원은 이 정리 절차로 삭제하지 않는다.

## 참고 자료

- [Python 3.6 숫자 구분자](https://docs.python.org/3/whatsnew/3.6.html#pep-515-underscores-in-numeric-literals)
- [Python AF_PACKET 지원 범위](https://docs.python.org/3.12/library/socket.html#socket.AF_PACKET)
- [Rocky Linux 9.4: Python 3.12 제공](https://docs.rockylinux.org/releases/release_notes/9_4/)
- [Rocky Linux 10 릴리스 노트](https://docs.rockylinux.org/latest/releases/release_notes/10_0/)
- [RHEL 10 계열 Python 설치 패키지](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/installing_and_using_dynamic_programming_languages/installing-and-using-python)
- [VS Code Remote-SSH](https://code.visualstudio.com/docs/remote/ssh)
- [VMware NAT·Host-only·Bridged 차이](https://knowledge.broadcom.com/external/article?legacyId=1006480)
- [Linux 네트워크 네임스페이스](https://www.man7.org/linux/man-pages/man8/ip-netns.8.html)
- [Linux veth](https://man7.org/linux/man-pages/man4/veth.4.html)
- [Linux packet socket 권한](https://man7.org/linux/man-pages/man7/packet.7.html)
- [Wireshark 체크섬 검증과 오프로딩](https://www.wireshark.org/docs/wsug_html_chunked/ChAdvChecksums.html)
