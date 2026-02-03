## 1. 개요 (Overview)

### 1.1 시스템 목적

- 학원 내부에서 사용할 **Small Language Model(SLM) 기반 진로·전공 로드맵 및 생활기록부(세특·비교과) 설계 AI**를 구축한다.  
- 목표는  
  - 학생 개개인의 전공 관심 + 사회·산업·윤리 관점을 반영한 **융복합 인재용 서사**를 만들고,  
  - 일반 LLM이 찍어내는 획일적 활동·문장을 피하며,  
  - 입학사정관 관점에서 “개별성·진정성·전공·사회 연결”이 드러나는 생기부를 설계하는 것이다.[1][2][3][4][5]

### 1.2 범위

- 1차 타깃 도메인  
  - AI/컴퓨터공학 계열  
  - 경영/경제 계열  
- 향후 패치 버전  
  - 인문·사회, 자연과학, 예체능 등 **다른 메이저 도메인으로 확장**.  
- 1차 목표  
  - **학원 서버 상시 서비스가 아니라**,  
  - Apple Silicon Mac(M4 Pro)에서 동작하는 **로컬 프로토타입** 구축 및 품질 검증.[6][7]

***

## 2. 기능 요구사항 (Functional Requirements)

### 2.1 진로·전공 로드맵 생성

**FR-1. 로드맵 생성**

- 입력  
  - 학생 프로필  
    - 학년, 계열(문과/이과/통합), 희망 전공군(AI/컴공, 경영/경제 등)  
    - 사회 관심 키워드(노동, 불평등, 기후, 인권, 복지, 도시 등)  
    - 가치관(공정성, 효율, 지속가능성, 포용 등)  
  - 학교·지역 자원  
    - 사용 가능한 동아리, 탐구반, 프로젝트, 기관, 온라인 리소스 등  
  - 제약조건  
    - 시간, 예산, 이동, 학교 규정 등  

- 출력  
  - 1~3학년(또는 최소 1년) 기준 **학기별 활동 로드맵**  
    - 활동 유형: 교과탐구, 동아리, 프로젝트, 독서, 발표, 봉사, 대회, 현장 체험 등  
    - 각 활동에 대해  
      - 활동 설명  
      - 어떤 전공 지식/관심과 연결되는지  
      - 어떤 사회·산업·윤리 이슈와 연결되는지  
      - 학업역량/진로역량/공동체역량 중 무엇을 드러내는지 태그[2][3][4][1]

**FR-2. 도메인별 색채 반영**

- AI/컴공 로드맵  
  - AI/데이터/알고리즘/자동화 키워드 + 사회·윤리(노동, 편향, 개인정보 등) 결합.[8][9][10][11]
- 경영/경제 로드맵  
  - 마케팅/재무/ESG/플랫폼/행동경제 등 + 사회문제(불평등, 지역경제, 노동 등) 결합.[12][13][14][15]

***

### 2.2 생기부 문장(세특·비교과) 생성·리라이팅

**FR-3. 세특/비교과 문장 초안 생성**

- 입력  
  - 과목 또는 활동 타입(수업, 동아리, 프로젝트, 봉사, 독서, 대회 등)  
  - 활동 상세(raw_activity): 학생이 실제로 수행한 내용, 역할, 과정, 느낀 점  
  - 학생 프로필: 희망 전공, 사회 관심 키워드, 가치관  
- 출력  
  - NEIS 형식과 호환되는 **1~3문장 세특/비교과 초안**  
  - 문장에는  
    - 구체적인 활동 내용(과정)  
    - 전공적합성 및 융합/사회 관점  
    - 자기주도성, 협업, 성찰 등이 자연스럽게 드러나야 한다.[16][17][18]

**FR-4. 할루시네이션·과장 방지**

- 모델은 입력에 없는 활동/성과를 새로 만들어 내지 않는다.  
- instruction 및 학습 데이터에서  
  - “입력에 없는 활동이나 과장된 표현을 추가하지 말 것”을 명시한다.[19][20][21]

***

### 2.3 역량·융합성 평가 및 피드백

**FR-5. 역량 평가**

- 입력  
  - 이미 작성된 세특/비교과 문장.  
- 출력  
  - 학업역량, 진로역량, 공동체역량 별 코멘트.  
  - 전공+사회·윤리·산업과의 연결 정도에 대한 평가.[3][4][5][1][2]

**FR-6. 보완 제안**

- 융복합/사회 관점에서  
  - 어떤 요소(문제의식, 과정 설명, 사회적 의미 등)를 보완하면 좋은지 제안.  
  - 필요한 경우, **추가 활동 아이디어**도 제시(실제 수행 전제).[11][22][23][24]

***

## 3. 데이터 요구사항 및 전처리 (Data Requirements)

### 3.1 데이터 종류

**DR-1. 학원 내부 데이터**

- 비식별 처리된 과거 생활기록부 텍스트  
  - 세특, 창체, 자율, 진로 항목 등 텍스트 파트.  
- 학생 활동 로그  
  - 프로젝트, 동아리, 독서, 봉사, 대회 및 그에 대응하는 최종 생기부 문장.  
- 입시 결과 정보(가능 시)  
  - 지원 대학, 전형, 전공, 합불 결과.[25][3]
- 컨설턴트/교사 피드백  
  - “좋은 표현 vs 과장/허위 가능성 vs 규정 위반 가능성” 등 코멘트.[20][21][19]

### 3.2 비식별·가명화

**DR-2. 직접 식별자 처리**

- 이름, 학부모·교사 이름, 학교명, 학급, 학번, 연락처, 상세 주소, 구체 기관명은 모두 제거 또는 토큰 치환.  
- 예시: `[학생A]`, `[일반고]`, `[대학A]`, `[대기업A]` 등.  
- 국내 개인정보 비식별 조치 가이드라인 수준을 준수.[26][27][28][29]

**DR-3. 간접 식별자 범주화**

- 지역 정보: “서울시 강남구 ○○동” → “서울시” 수준.  
- 성적: “전교 1등” → “상위 1%” 등 구간화.  
- 대학/기업: 실명 대신 등급·유형으로 표현.  

**DR-4. 전처리 파이프라인**

- 규칙 기반 치환 스크립트(파이썬 등) + 수동 샘플 검수.  
- 비식별 전후 샘플을 점검해 재식별 위험을 최소화.[30][31][32][33]

### 3.3 구조화 스키마

**DR-5. 공통 JSON 구조**

```json
{
  "student_profile": {
    "grade": 2,
    "track": "문과/이과/통합",
    "interest_domains": ["AI", "경영"],
    "social_topics": ["노동", "불평등"],
    "values": ["공정성", "효율"]
  },
  "context": {
    "subject": "수학",
    "year": 2025,
    "activity_type": "수업탐구/동아리/프로젝트/봉사/독서/대회",
    "role": "리더/참여/기획",
    "environment": "학교내/지역사회/온라인"
  },
  "raw_activity": "활동 상세 기술",
  "teacher_comment_final": "최종 생기부 문장",
  "outcome": {
    "admission_result": "합격/불합격/미응시",
    "target_major": "컴퓨터공학/경영학/경제학 등",
    "evaluation_tags": ["학업역량", "진로역량", "공동체역량"]
  }
}
```

**DR-6. 도메인별 필드**

- AI/컴공: `tech_keywords`(예: 머신러닝, 알고리즘 등), `project_type`(모델구현, 데이터수집 등).[34][35]
- 경영/경제: `biz_keywords`(마케팅, ESG 등), `data_context`(시장조사, 설문 등).[13][15][12]

***

## 4. 모델·학습·기술 스택 요구사항 (Model & Tech Stack)

### 4.1 프레임워크 및 포맷

**TR-1. 프레임워크**

- 기본 딥러닝 프레임워크는 **PyTorch**로 한다.[36]
- 언어 모델 관련 작업(로딩, 토크나이징, 파인튜닝)은 **HuggingFace Transformers 생태계**를 우선 사용한다.[37][38]
- TensorFlow/Keras(.h5) 기반 모델은 1차 구현 범위에서 제외(필요 시 별도 패치로 검토).  

**TR-2. 모델 포맷**

- 학습/파인튜닝 기본 포맷: **PyTorch/HF 포맷(.bin 또는 .safetensors)**.[38][39][37]
- 로컬·온프레미스 추론 최적화용: 필요 시 **양자화 포맷(예: .gguf)** 으로 변환해 별도 배포.[7][6]
- “모델을 하나의 파일로 저장해 로컬에서 로드한다”는 요구는 위 포맷들로 충족하며, `.h5`는 필수 조건이 아니다.[37][38]

### 4.2 모델 스케일 및 구조

**TR-3. 모델 크기**

- 파라미터 규모: **3B~8B급 한국어 지원 LLM**을 SLM 후보로 선정.  
- 구조:  
  - 멀티 도메인 코어 SLM (학업·진로·공동체·융합 프레임 공통 학습).  
  - 도메인별 LoRA/QLoRA 어댑터(AI/컴공, 경영/경제 등).[40][41][42]

**TR-4. 태스크 학습 (SFT)**

- 태스크 1: 로드맵 생성  
- 태스크 2: 세특/비교과 문장 생성·리라이팅  
- 태스크 3: 역량·융합성 평가 및 피드백  
- 인스트럭션 튜닝 스타일(JSON 기반 instruction/input/output)로 통일.[41][43]

### 4.3 학습·추론 운영

**TR-5. 학습**

- 파인튜닝은 **Apple Silicon M4 Pro 로컬 환경**에서 QLoRA 등 경량 튜닝 기법으로 수행 가능한 수준을 목표로 한다.[6][7]
- 학습은 상시가 아닌, **필요 시 배치성 작업**으로만 실행한다.  

**TR-6. 추론**

- 파인튜닝 완료 후  
  - 모델 가중치를 배포용 파일(또는 파일 세트)로 저장하고,  
  - 로컬 애플리케이션(스크립트 또는 간단 UI)에서 이를 로드하여 **추론 전용**으로 사용한다.[7][6]
- 운영 단계에서는 **온라인 continual learning 없음**.  
- 신규 데이터 반영은  
  - 재튜닝 → 새 버전 모델 파일 생성 → 로컬에서 교체  
  방식의 버전업으로 처리한다.[44][45][46]

***

## 5. 인프라·보안·규제 요구사항 (Infra & Governance)

### 5.1 인프라

**IR-1. 개발/테스트 환경**

- OS/하드웨어: Apple Silicon M4 Pro 기반 macOS.  
- 요구사항:  
  - 해당 환경에서 모델 로딩·추론·간단 UI 테스트가 가능해야 함.[47][6][7]

**IR-2. 향후 운영(선택 사항)**

- 향후 학원 서버/전용 VPC 배포 가능성을 고려해  
  - 모델 파일 포맷  
  - 의존 라이브러리  
  - 리소스 요구(메모리/스토리지) 문서화.[47][6]

### 5.2 보안·프라이버시

**GR-1. 데이터 유출 방지**

- 학습 데이터는 모두 비식별 처리 후 내부 환경에서만 사용.  
- 외부 SaaS/클라우드 API로 학습 데이터 또는 추론 로그 전송 금지.[31][32][30]

**GR-2. 규제·책임**

- “학생부 작성에 생성형 AI 활용 가능, 책임은 교사”라는 교육부 기조를 전제로 한다.[21][20]
- 시스템은 **보조 도구**이며, 최종 생기부 확정은 교사가 수행한다는 점을 UI·문서에 명시한다.  
- 허위·과장 표현을 권장하지 않고, 입력 사실을 기반으로 한 정리·구조화에 초점을 둔다.[48][19]

***

## 6. UX/제품 요구사항 (UX & Product)

**UX-1. 사용자**

- 1차 타깃: 학원 컨설턴트, 담임/과목 교사.

**UX-2. 인터페이스 (1차 로컬 프로토타입)**

- 최소 요구  
  - CLI 또는 간단 웹 UI(예: 로컬 Gradio/Streamlit 수준)를 통해  
    - 학생 프로필/활동 입력  
    - 로드맵/세특 문장/피드백 출력 확인 가능.  

**UX-3. 메시지**

- “AI가 대신 써주는 도구”가 아니라  
  - **교사의 관찰과 학생의 실제 경험을 구조화·정리·확장해 주는 도구**라는 메시지를 문서와 화면에 명확히 표현.[22][23][11][19][48]

***

필요하면 이 SRS 위에 바로 붙일 수 있는 **Vibe-Coding용 메타 프롬프트 버전**도, 지금 구조를 유지한 채로 한 번 더 정제해서 만들어 드릴 수 있습니다.

[1](https://www.01consulting.co.kr/admissionsInfo/detail/23/11404)
[2](https://nojaesu.com/678)
[3](https://www.jinhak.com/jh/high3/univ-entrance-info/ipsi-analysis/ipsi-strategy/100000139)
[4](https://blog.naver.com/doshin38/223382028383)
[5](https://blog.naver.com/doshin38/223390605501)
[6](https://aws.amazon.com/blogs/compute/running-and-optimizing-small-language-models-on-premises-and-at-the-edge/)
[7](https://www.anaconda.com/blog/small-language-models-efficient-future-ai)
[8](https://ai.kisdi.re.kr/aieth/main/contents.do?menuNo=400040)
[9](https://ksp.etri.re.kr/ksp/article/file/70466.pdf)
[10](https://www.korea.kr/news/contributePolicyView.do?newsId=148955467)
[11](https://happyedu.moe.go.kr/happy/bbs/selectHappyArticle.do?bbsId=BBSMSTR_000000000191&nttId=41321)
[12](https://downloads.hindawi.com/journals/sp/2022/4478115.pdf)
[13](https://pmc.ncbi.nlm.nih.gov/articles/PMC9732559/)
[14](https://www.mdpi.com/2076-3387/14/7/157/pdf?version=1721694763)
[15](https://journals.icapsr.com/index.php/ijgasr/article/download/50/115)
[16](https://www.youtube.com/watch?v=p88imSNif8I)
[17](https://blog.naver.com/PostView.naver?blogId=auraedu&logNo=223522119964)
[18](https://www.mk.co.kr/news/economy/9410180)
[19](https://www.donga.com/news/Society/article/all/20250703/131929611/2)
[20](https://thetibs.co.kr/?p=3859)
[21](https://www.hankyung.com/article/2025081018181)
[22](https://www.ktv.go.kr/content/view?content_id=742818)
[23](https://blog.naver.com/moeblog/224071134610)
[24](https://spri.kr/posts/view/22756)
[25](https://v.daum.net/v/f4ga2NP3Nt)
[26](https://blog.softcamp.co.kr/204)
[27](https://blog.skby.net/wp-content/uploads/2019/03/%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4-%EB%B9%84%EC%8B%9D%EB%B3%84-%EC%A1%B0%EC%B9%98-%EA%B0%80%EC%9D%B4%EB%93%9C%EB%9D%BC%EC%9D%B8.pdf)
[28](https://www.korea.kr/archive/expDocView.do?docId=37095)
[29](https://koreascience.kr/article/JAKO202405955800395.pdf)
[30](https://murjet.muet.edu.pk/index.php/home/article/view/292)
[31](https://www.mdpi.com/2071-1050/13/16/9206/pdf)
[32](https://www.mdpi.com/2076-3417/11/18/8506/pdf?version=1631687734)
[33](https://arxiv.org/pdf/2501.01786.pdf)
[34](https://josephlee54.tistory.com/366)
[35](https://pitapatseul.tistory.com/33)
[36](https://deepsense.ai/blog/keras-or-pytorch-as-your-first-deep-learning-framework/)
[37](https://huggingface.co/blog/ngxson/common-ai-model-formats)
[38](https://learnopencv.com/model-weights-file-formats-in-machine-learning/)
[39](https://stackoverflow.com/questions/78019134/how-to-properly-save-the-finetuned-transformer-model-in-safetensors-without-losi)
[40](https://www.nature.com/articles/s41524-025-01564-y)
[41](https://www.arxiv.org/pdf/2510.02347.pdf)
[42](https://www.meegle.com/en_us/topics/supervised-fine-tuning/supervised-fine-tuning-for-cross-domain-learning)
[43](https://arxiv.org/html/2510.02347v1)
[44](http://arxiv.org/pdf/2408.10691.pdf)
[45](https://arxiv.org/pdf/2312.15603.pdf)
[46](http://arxiv.org/pdf/2406.10288.pdf)
[47](https://www.reddit.com/r/LocalLLaMA/comments/1nig0zp/hardware_and_model_recommendations_for_onprem_llm/)
[48](https://www.chosun.com/national/education/2025/09/06/P4DLCQD3DRHAVE6PGMMTPRNP74/)

---

## 1. Vibe-Coding용 메타 프롬프트 – 목적

> 이 프롬프트는 “대입 학원 전용 SLM 기반 진로·로드맵·생기부 설계 AI”를 같이 설계·구현하기 위한 **Vibe-Coding 세션용 요구 명세 프롬프트**입니다.  
> SLM은 로컬(Apple Silicon 맥)에서 동작하는 **소형·도메인 특화 모델**을 지향하며, 교육 도메인에서 SLM이 충분한 성능과 효율성을 낼 수 있다는 최근 연구·사례와도 맞닿아 있습니다.[1][2][3][4][5]

***

## 2. 역할/컨텍스트 지정 블록

```text
당신은 대한민국 대입 학원 전용 AI 솔루션을 설계·구현하는 **수석 머신러닝 엔지니어**입니다.

우리가 만들고 싶은 것은, 일반 LLM이 찍어내는 획일적인 활동·문장이 아니라,
학생의 전공 관심 + 사회·산업·윤리 관점을 반영한 **융복합 인재용 진로·전공 로드맵 및 생활기록부(세특/비교과) 설계 SLM**입니다.

이 SLM은 다음 특징을 가집니다.
- 학원 내부 전용, 프라이버시 중시
- Small Language Model(3B~8B급) 위에 학원 데이터를 얇게 입힌 도메인 특화 모델
- Apple Silicon Mac(M4 Pro)에서 로컬 실행 가능한 규모와 구조
- “AI가 대신 써주는 도구”가 아니라, 교사/컨설턴트의 관찰과 학생의 실제 경험을 구조화·정리·확장해 주는 보조 도구
- 상시 재학습 서비스가 아니라, 한 번 파인튜닝한 모델 파일을 로컬에서 로드하여 추론 전용으로 쓰는 구조
```

***

## 3. 전제 조건/제약사항 블록

```text
[전제 조건]

1) 도메인/타깃
- 1차 타깃 전공군: AI/컴퓨터공학, 경영/경제
- 향후 패치 버전으로 인문·사회, 자연과학, 예체능 등 메이저 도메인 확장
- 평가 프레임은 공통적으로 "학업역량·진로역량·공동체역량" 3축을 사용

2) 데이터/전처리
- 학원 내부 데이터:
  - 비식별 처리된 과거 생활기록부 텍스트(세특/창체/자율/진로)
  - 학생 활동 로그(동아리, 프로젝트, 독서, 봉사, 대회 등) + 이에 대응하는 최종 생기부 문장
  -(가능하다면) 지원 대학/전형/전공/합불 결과, 컨설턴트/교사 피드백
- 비식별/가명화:
  - 이름, 학교명, 학번, 연락처, 상세 주소, 구체 기관명 등 직접 식별자는 모두 제거/치환
  - 지역, 성적, 학교 유형, 대학/기업 이름 등은 범주화(수도권/지방, 상위 1%, 대학A 등)
  - 국내 개인정보 비식별 조치 가이드라인 수준을 목표로 함
- 구조화(JSON 스키마):
  - student_profile: 학년, 계열, 희망 전공군, 사회 관심 키워드, 가치관 등
  - context: 과목/활동 유형, 역할, 환경(학교/지역/온라인) 등
  - raw_activity: 활동 상세
  - teacher_comment_final: 최종 생기부 문장
  - outcome: target_major, admission_result, evaluation_tags(학업/진로/공동체 역량)

3) 모델/기술 스택
- 기본 프레임워크: PyTorch
- LLM 스택: HuggingFace Transformers 기반
- 모델 포맷:
  - 학습/튜닝: PyTorch/HF 포맷(.bin 또는 .safetensors)
  - 추론 최적화: 필요 시 양자화(.gguf 등)로 변환하여 별도 배포
  - TensorFlow/Keras(.h5)는 1차 구현 범위에서 제외 (필요 시 이후 별도 패치로 검토)
- 모델 크기:
  - 3B~8B급 한국어 지원 오픈소스 LLM을 SLM 후보로 선정
  - 멀티 도메인 코어 + 도메인별 LoRA/QLoRA 어댑터 구조
- 실행 환경:
  - 1차 개발/테스트는 Apple Silicon M4 Pro 맥에서 로컬로 수행
  - 파인튜닝은 필요 시 배치성으로만 실행하고, 운영 단계는 추론 전용

4) 운영/보안/규제
- 로컬 프로토타입 단계:
  - 학원 서버나 지점 배포보다 "내 맥에서 제대로 동작하는지" 검증이 우선 목표
- 향후 운영:
  - 온프레미스 또는 전용 VPC 기반 학원 내부 전용 서비스로 확장 가능성을 열어둠
- 프라이버시:
  - 학습/테스트 데이터는 모두 비식별 처리 후 내부 환경에서만 사용
  - 외부 SaaS/클라우드 API로 학습 데이터/로그를 보내지 않음
- 규제:
  - 교육부 기조: "생성형 AI 활용은 허용 가능하나, 책임은 교사에게 있음"을 전제로 함
  - 시스템은 보조 도구이며, 최종 생기부 확정은 교사가 담당해야 함
```

***

## 4. 모델 기능/태스크 정의 블록

```text
[모델이 지원해야 할 핵심 태스크]

1) 진로·전공 로드맵 생성
- 입력:
  - student_profile (학년, 계열, 희망 전공군, 사회 관심 키워드, 가치관 등)
  - school_resources (동아리, 탐구반, 프로젝트, 지역 기관, 온라인 리소스 등)
  - constraints (시간, 예산, 이동, 학교 규정 등)
- 출력:
  - 1~3년(또는 최소 1년) 단위 학기별 활동 로드맵
  - 각 활동에 대해:
    - 활동 설명
    - 어떤 전공 지식/관심과 연결되는지
    - 어떤 사회·산업·윤리 이슈와 연결되는지
    - 학업역량·진로역량·공동체역량 중 무엇을 드러내는지 태그

2) 세특/비교과 문장 생성·리라이팅
- 입력:
  - subject 또는 activity_type
  - raw_activity (학생 실제 활동 로그, 역할, 과정, 느낀 점 등)
  - target_major, social_topics, values 등
- 출력:
  - NEIS 형식과 호환되는 1~3문장 세특/비교과 초안
- 제약:
  - 입력에 없는 활동/성과를 새로 만들어 내지 말 것
  - 과장/허위 표현을 피하고, 관찰 가능한 행동과 구체적 과정 중심으로 기술할 것

3) 역량·융합성 평가 및 피드백
- 입력:
  - 이미 작성된 세특/비교과 문장
- 출력:
  - 학업역량, 진로역량, 공동체역량에 대한 평가 코멘트
  - 전공+사회·산업·윤리 관점에서 드러나는 강점·약점
  - 필요한 경우, 융복합적 관점에서의 보완 아이디어/추가 활동 제안
```

***

## 5. Vibe-Coding에서 우선 해줬으면 하는 일 (질문/산출물 지시)

```text
[당신에게 요청하는 작업]

위 전제를 바탕으로, 지금 단계에서 우리가 Vibe-Coding으로 먼저 확인하고 싶은 것은
"이 SLM을 실제로 만들고 배포하는 데 있어, 빠져 있는 요구사항·리스크·구현 난이도 포인트"입니다.

1. 데이터 관점
   - 위에 정리된 JSON 스키마/비식별 규칙/데이터 종류만으로,
     진로 로드맵/세특 생성/역량 평가 3태스크를 학습하기에 무엇이 부족한지 정리해 주세요.
   - 추가로 필요한 필드나 라벨(예: 활동 난이도, 학생 성향 타입 등)이 있다면 제안해 주세요.

2. 모델·학습 관점
   - 3B~8B급 한국어 SLM + LoRA/QLoRA 구조를 전제로 할 때,
     Apple Silicon M4 Pro 로컬 환경에서 현실적으로 가능한:
       - 데이터량/시퀀스 길이,
       - 학습 시간/배치 크기,
       - 추론 속도 수준을 대략 범위로 설명해 주세요.
   - 로드맵 생성/세특 생성/역량 평가 세 태스크를
     하나의 멀티태스크로 묶을지, 별도 헤드/체크포인트로 나눌지에 대한 권장안을 제시해 주세요.

3. 인프라·운영 관점
   - "로컬 프로토타입" 기준에서 필요한 최소 구성 요소(스크립트, 간단 UI, 로그 저장 방식 등)를 정리해 주세요.
   - 추후 온프레미스/전용 VPC 배포를 생각했을 때, 지금 설계에서 미리 고려해 두면 좋은 점(모델 포맷, 모듈화 등)을 알려 주세요.

4. UX/제품 관점
   - 학원 컨설턴트/교사가 실제로 쓸 때,
     첫 화면에서 어떤 입력을 받는 것이 좋을지(필수/선택 필드 구분) 제안해 주세요.
   - "AI가 대신 써준다"가 아니라
     "교사의 관찰과 학생의 실제 경험을 정리·확장해 준다"는 메시지를 UX적으로 구현하는 아이디어를 간단히 제안해 주세요.

5. 리스크·추가 질문
   - 프라이버시/규제/입학사정관 관점에서
     이 설계가 가질 수 있는 주요 리스크를 3~5개 정도로 정리해 주세요.
   - 당신이 보기에, 이 SRS에서 아직 모호하거나 빠져 있다고 느끼는 지점이 있으면
     "추가로 물어봐야 할 질문 리스트" 형태로 정리해 주세요.

[응답 형식]

- 각 번호(1~5)에 대해
  - 요약 bullet
  - 필요한 경우 짧은 예시
- 가능한 한 구체적으로, 바로 다음 Vibe-Coding 턴에서
  - "데이터 스키마 수정"
  - "프롬프트 템플릿 설계"
  - "파이썬 코드 틀 작성"
  으로 이어질 수 있을 정도의 레벨까지 내려가 주세요.
```

***

이 메타 프롬프트를 그대로 복붙해서 쓰시면,  
- 당신이 원하는 **SLM·교육·로컬·프라이버시·융복합 인재** 조건이 한 번에 전달되고,  
- 다음 단계부터는 이 위에 구체적인 **프롬프트 템플릿, 데이터 예시, 코드 스켈레톤**을 Vibe-Coding 스타일로 쌓아갈 수 있습니다.[6][7][8][9][10]

다음 턴에서는  
- ① 이 메타 프롬프트에 맞춰 나올 답변을 “예상 형태”로 미리 시뮬레이션해 보거나,  
- ② 바로 “세특 리라이팅 태스크”용 구체 프롬프트/데이터 예시/코드 틀까지 내려가 볼 수도 있습니다.  
어느 쪽부터 진행하고 싶으신지 한 가지만 골라 주시면 거기에 맞춰 이어가겠습니다.

[1](https://arxiv.org/abs/2510.02347)
[2](https://chatpaper.com/paper/195801)
[3](https://www.arxiv.org/abs/2510.02347)
[4](https://edtechmagazine.com/k12/article/2025/03/small-language-models-slm-perfcon)
[5](https://bostoninstituteofanalytics.org/blog/weekly-wrap-up-25th-oct-1st-nov-how-small-language-models-slms-are-outperforming-giants-in-2025/)
[6](https://www.distillabs.ai/blog/vibe-tuning-the-art-of-fine-tuning-small-language-models-with-a-prompt)
[7](https://huggingface.co/learn/cookbook/prompt_tuning_peft)
[8](https://ai-infrastructure.org/how-to-fine-tune-hugging-face-transformers-on-a-custom-dataset/)
[9](https://cloud.google.com/discover/what-is-vibe-coding)
[10](https://almcorp.com/blog/vibe-coding-complete-guide/)
[11](https://link.springer.com/10.1007/s10844-025-00963-3)
[12](https://arxiv.org/abs/2509.09356)
[13](https://arxiv.org/abs/2503.15426)
[14](https://onlinelibrary.wiley.com/doi/10.1111/jcal.13060)
[15](https://link.springer.com/10.1007/s00146-025-02403-w)
[16](https://arxiv.org/abs/2507.10628)
[17](https://arxiv.org/abs/2504.10179)
[18](https://www.semanticscholar.org/paper/395553f7790e6965a2dbbd9ed89755a81e50647f)
[19](https://arxiv.org/abs/2506.13186)
[20](http://arxiv.org/pdf/2407.10194.pdf)
[21](https://aclanthology.org/2023.conll-babylm.10.pdf)
[22](http://arxiv.org/pdf/2503.04267.pdf)
[23](https://arxiv.org/pdf/2311.08886.pdf)
[24](https://arxiv.org/pdf/2311.05943.pdf)
[25](https://arxiv.org/pdf/2307.16364.pdf)
[26](http://arxiv.org/pdf/2502.20527.pdf)
[27](https://dl.acm.org/doi/pdf/10.1145/3626252.3630909)
[28](https://huggingface.co/learn/cookbook/fine_tuning_llm_to_generate_persian_product_catalogs_in_json_format)