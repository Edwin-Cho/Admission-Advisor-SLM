# SA_SLM Gradio UI 실행 방법 (로컬 / 퍼블릭 공유 + 비밀번호)

아래 명령어는 프로젝트 루트(예: `.../SA_SLM`)에서 실행한다고 가정합니다.

## 1) 로컬(Local) 실행

### 1-1. 기본 실행 (로컬에서만)

```bash
python ui/app.py --adapter ./adapter
```

- `--adapter ./adapter`: LoRA 어댑터 폴더 경로 지정
- 접속 주소(기본): `http://127.0.0.1:7860`

### 1-2. 포트 변경

```bash
python ui/app.py --adapter ./adapter --port 7861
```

- 접속 주소: `http://127.0.0.1:7861`

### 1-3. 로컬에서 비밀번호(인증) 걸기

```bash
python ui/app.py --adapter ./adapter --auth --auth-user admin --auth-pass 'YOUR_PASSWORD'
```

- `--auth`: 접속 인증 활성화
- `--auth-user`: 사용자명 (생략 시 기본 `admin`)
- `--auth-pass`: 비밀번호 (생략 시 실행 중 터미널에서 입력 요청)

## 2) 퍼블릭(Public) 공유 링크 실행 (+ 비밀번호)

Gradio의 `share=True` 기능으로 외부 접속 가능한 공개 URL을 생성합니다.

### 2-1. 퍼블릭 공유 링크만 생성

```bash
python ui/app.py --adapter ./adapter --share
```

- 실행 로그에 `https://xxxxx.gradio.live` 형태의 URL이 출력됩니다.
- 기본적으로 인증은 걸려있지 않습니다.

### 2-2. 퍼블릭 공유 + 비밀번호(권장)

```bash
python ui/app.py --adapter ./adapter --share --auth --auth-user admin --auth-pass 'YOUR_PASSWORD'
```

- 공유 URL 접속 시 로그인해야 사용 가능합니다.

### 2-3. 환경변수로 비밀번호 숨기기(권장: 쉘 히스토리에 비번이 남지 않게)

```bash
export SA_SLM_UI_USER="admin"
export SA_SLM_UI_PASS="YOUR_PASSWORD"
python ui/app.py --adapter ./adapter --share --auth
```

## 참고(현재 `ui/app.py` 동작)

- `--share`를 켜면 UI에서 “모델 로드 탭”이 숨겨지도록 되어 있습니다. (`show_model_tab=not args.share`)
- 공유 링크는 프로세스가 살아있는 동안만 유지됩니다. (프로그램 종료/PC sleep 시 끊김)
