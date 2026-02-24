# SA-SLM: 생기부 설계 AI | Student Record Design AI

> 🇰🇷 한국어 | [English](#english-summary)

성공 사례 기반 생기부(세특·비교과) 활동 추천 및 문장 생성 SLM  
*An SLM for recommending extracurricular activities and generating student record statements based on successful admission cases.*

---

## 🏗️ 아키텍처 | Architecture

![SA-SLM Architecture](docs/images/SA_SLM_Project_diagram.png)

<details>
<summary>상세 파이프라인 보기 | View Detailed Pipeline</summary>

![SA-SLM Detailed Pipeline](docs/images/SA_SLM_Project_overview.png)

</details>

---

## 개요 | Overview

| 항목 | 내용 |
| :--- | :--- |
| **목표** | 성적 대비 상향 진학한 학생들의 생기부 패턴을 학습하여 차별화된 활동 추천 |
| **베이스 모델** | Qwen2.5-3B-Instruct |
| **파인튜닝** | LoRA (r=16, 4-bit NF4 Quantization) |
| **학습 환경** | Google Colab (T4 GPU) |
| **추론 환경** | Colab / Local (CUDA with 4-bit quantization) |

## 프로젝트 구조 | Project Structure

```text
SA_SLM/
├── colab/
│   ├── SA_SLM_Training.ipynb   # Training notebook
│   └── SA_SLM_Inference.ipynb  # Inference notebook
├── ui/
│   └── app.py                  # Gradio UI (local)
├── data/
│   ├── examples/               # Sample/test data
│   └── schemas/                # JSON schemas for data collection
├── docs/
│   ├── images/                # Architecture diagrams
│   ├── SA_SLM_SRS.md          # Software Requirements Specification
│   └── how_to_run_directions.md
├── requirements.txt
└── README.md
```

## 빠른 시작 | Quick Start

### 1. Colab 학습 | Training on Colab

1. `data/` 폴더를 `data.zip`으로 압축 | Compress `data/` folder to `data.zip`
2. `colab/SA_SLM_Training.ipynb`를 Colab에서 열기 | Open in Colab
3. GPU 런타임(T4) 선택 → `data.zip` 업로드 → 실행 | Select T4 GPU → Upload → Run
4. 학습 완료 후 `sa_slm_adapter.zip` 다운로드 | Download adapter after training

### 2. 로컬 UI 실행 | Local UI

```bash
# Install dependencies
pip install -r requirements.txt

# Extract adapter
unzip sa_slm_adapter.zip -d ./adapter

# Run UI
python ui/app.py --adapter ./adapter

# With public share link + password protection
python ui/app.py --adapter ./adapter --share --auth
```

## 핵심 기능 | Key Features

| 기능 | 설명 | Description |
| :--- | :--- | :--- |
| **🎯 활동 추천** | 학생 프로필 기반 차별화된 활동 제안 | Personalized activity recommendations |
| **📝 세특 생성** | NEIS 형식 3인칭 서술체 문장 생성 | Generate NEIS-format statements |
| **📊 역량 평가** | 학업/진로/공동체 역량 분석 및 보완 제안 | Competency analysis & suggestions |

## UI 기능 | UI Features

- 실시간 스트리밍 출력 | Real-time streaming output
- 글자 수 카운터 | Character counter
- 복사 / 재생성 버튼 | Copy / Regenerate buttons
- 공유 링크 비밀번호 보호 | Password-protected share links (`--auth`)

## 데이터 수집 | Data Collection

`docs/data_collection_guide.md` 참고. 컨설턴트가 PDF → JSON 변환 수행.  
*Refer to the guide. Consultants perform PDF → JSON conversion.*

## 학습 결과 | Training Results

| 항목 | 값 |
| :--- | :--- |
| **학습 데이터** | 721 examples (101 student records + task templates) |
| **학습 환경** | Google Colab T4 GPU |
| **에포크** | 10 epochs |
| **최종 Training Loss** | **0.144** |
| **학습 시간** | ~39분 (2,334초) |
| **Adapter 크기** | ~50–100MB (LoRA weights only) |

### 샘플 입출력 | Sample Input/Output

**입력 (활동 추천)**:
> 계열: 공학, 성적: 3등급대, 관심: 인공지능, 데이터사이언스, 가치관: AI 윤리, 디지털 격차 해소, 목표: 컴퓨터공학

**출력 예시**:
> AI 윤리 기반 데이터 편향 탐구 보고서 작성, 디지털 리터러시 교육 봉사 기획, 오픈소스 AI 모델 활용 소규모 프로젝트 수행 등 차별화된 활동을 추천합니다.

*Note: 출력은 학습 데이터와 temperature 설정에 따라 달라질 수 있습니다.*

---

## 주의사항 | Disclaimer

- 이 시스템은 **보조 도구**입니다. 최종 생기부 확정은 컨설턴트가 수행합니다.  
  *This is an **assistive tool**. Final decisions are made by consultants.*
- 모든 데이터는 비식별 처리 후 내부 환경에서만 사용됩니다.  
  *All data is de-identified and used only in internal environments.*
- `adapter/` 폴더는 Git에 포함되지 않습니다 (용량 문제).  
  *The `adapter/` folder is not included in Git (file size).*

---

[English](#english-summary)

## English Summary

**SA-SLM** is a Small Language Model fine-tuned for Korean student record ("생기부") consulting. It analyzes successful university admission cases and provides:

- **Activity Recommendations**: Suggests differentiated extracurricular activities based on student profiles
- **Statement Generation**: Creates NEIS-format third-person narrative statements
- **Competency Evaluation**: Analyzes academic, career, and community competencies

### Technical Stack

- **Base Model**: Qwen2.5-3B-Instruct
- **Fine-tuning**: LoRA (r=16) with 4-bit NF4 quantization
- **Training**: Google Colab (T4 GPU)
- **Inference**: Local (CUDA with 4-bit quantization) or Colab
- **UI**: Gradio with streaming output

### Architecture

![SA-SLM Architecture](docs/images/SA_SLM_Project_diagram.png)

<details>
<summary>View Detailed Pipeline</summary>

![SA-SLM Detailed Pipeline](docs/images/SA_SLM_Project_overview.png)

</details>

### License

Apache License 2.0
