"""
SA_SLM Gradio UI

Colab에서 학습한 LoRA adapter를 로컬에서 사용하는 UI입니다.
sa_slm_adapter.zip 압축 해제 후 adapter 폴더 경로를 지정하세요.

Usage:
    python ui/app.py --adapter ./sa_slm_adapter
"""

import argparse
import getpass
import os
from pathlib import Path
from typing import Iterator, List, Optional, Tuple
from threading import Thread

import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TextIteratorStreamer
from peft import PeftModel


# 전역 변수
model = None
tokenizer = None
is_loaded = False


def load_model(adapter_path: str) -> str:
    """모델 및 LoRA adapter 로드 (Colab 코드와 동일)"""
    global model, tokenizer, is_loaded
    
    if not adapter_path.strip():
        return "❌ adapter 경로를 입력하세요"
    
    adapter_path = Path(adapter_path)
    if not adapter_path.exists():
        return f"❌ 경로가 존재하지 않습니다: {adapter_path}"
    
    try:
        BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"
        
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
        
        model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )
        model = PeftModel.from_pretrained(model, str(adapter_path))
        model.eval()
        
        is_loaded = True
        return f"✅ 모델 로드 완료: {adapter_path}"
    
    except Exception as e:
        return f"❌ 로드 실패: {str(e)}"


def get_runtime_info() -> str:
    lines = ["### Runtime / Device 정보"]

    try:
        lines.append(f"- **Python**: {__import__('sys').version.split()[0]}")
    except Exception:
        pass

    try:
        lines.append(f"- **torch**: {torch.__version__}")
        lines.append(f"- **mps available**: {torch.backends.mps.is_available()}")
    except Exception as e:
        lines.append(f"- **torch 확인 실패**: {e}")

    lines.append(f"- **model loaded**: {is_loaded}")

    if is_loaded and model is not None:
        try:
            param = next(model.parameters())
            lines.append(f"- **model.device**: {getattr(model, 'device', 'N/A')}")
            lines.append(f"- **param.device**: {param.device}")
            lines.append(f"- **param.dtype**: {param.dtype}")
        except Exception as e:
            lines.append(f"- **model 파라미터 확인 실패**: {e}")
    else:
        lines.append("- **model/param device**: (모델 로드 후 확인 가능)")

    return "\n".join(lines)


def ask(prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str: # max_tokens를 500으로 수정
    """추론 함수 (Colab 코드와 동일)"""
    if not is_loaded:
        return "⚠️ 먼저 모델을 로드하세요"
    
    msgs = [
        {"role": "system", "content": "생기부 설계 전문가. 성공 사례 기반 차별화된 활동 추천."},
        {"role": "user", "content": prompt}
    ]
    
    txt = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    inp = tokenizer(txt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        out = model.generate(
            **inp,
            max_new_tokens=max_tokens,
            temperature=temperature,
            do_sample=True,
            top_p=0.9
        )
    
    return tokenizer.decode(out[0][inp["input_ids"].shape[1]:], skip_special_tokens=True)


def ask_stream(
    prompt: str,
    max_tokens: int = 800,  # max_tokens를 800으로 증가
    temperature: float = 0.7,
) -> Iterator[Tuple[str, str]]:
    if not is_loaded:
        yield "⚠️ 먼저 모델을 로드하세요", ""
        return

    yield "입력 구성 중...", ""

    msgs = [
        {"role": "system", "content": "생기부 설계 전문가. 성공 사례 기반 차별화된 활동 추천."},
        {"role": "user", "content": prompt},
    ]

    txt = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    inp = tokenizer(txt, return_tensors="pt").to(model.device)

    try:
        streamer = TextIteratorStreamer(
            tokenizer,
            skip_special_tokens=True,
            timeout=120,  # timeout을 120초로 증가
            skip_prompt=True,
        )
    except TypeError:
        streamer = TextIteratorStreamer(
            tokenizer,
            skip_special_tokens=True,
            timeout=120,  # timeout을 120초로 증가
        )

    gen_kwargs = {
        **inp,
        "streamer": streamer,
        "max_new_tokens": max_tokens,
        "temperature": temperature,
        "do_sample": True,
        "top_p": 0.9,
    }

    thread = Thread(target=model.generate, kwargs=gen_kwargs)
    thread.start()

    text = ""
    yield "생성 중...", text
    for token_text in streamer:
        text += token_text
        yield "생성 중...", text

    thread.join()
    yield "완료", text


def recommend_activities(track: str, grade_tier: str, interests: str, values: str, target_major: str) -> str:
    """활동 추천"""
    profile = f"""계열: {track}
성적: {grade_tier}
관심: {interests}
가치관: {values}
목표: {target_major}"""

    return ask(f"차별화된 활동을 추천하세요.\n\n{profile}")


def recommend_activities_stream(
    track: str,
    grade_tier: str,
    interests: str,
    values: str,
    target_major: str,
) -> Iterator[Tuple[str, str]]:
    profile = f"""계열: {track}
성적: {grade_tier}
관심: {interests}
가치관: {values}
목표: {target_major}"""
    yield from ask_stream(f"차별화된 활동을 추천하세요.\n\n{profile}")


def generate_statement(subject: str, activity: str) -> str:
    """세특 문장 생성"""
    return ask(f"NEIS 세특 문장으로 작성. 3인칭 서술체.\n\n과목: {subject}\n활동: {activity}", max_tokens=250) # max_tokens를 250으로 수정


def generate_statement_stream(subject: str, activity: str) -> Iterator[Tuple[str, str]]:
    yield from ask_stream(
        f"NEIS 세특 문장으로 작성. 3인칭 서술체.\n\n과목: {subject}\n활동: {activity}",
        max_tokens=200, # max_tokens를 200으로 수정
    )


def evaluate_statement(statement: str, target_major: str) -> str:
    """역량 평가"""
    return ask(f"역량 평가 및 보완 제안.\n\n문장: {statement}\n전공: {target_major}")


def evaluate_statement_stream(statement: str, target_major: str) -> Iterator[Tuple[str, str]]:
    yield from ask_stream(f"역량 평가 및 보완 제안.\n\n문장: {statement}\n전공: {target_major}")


# 마지막 생성 입력 저장 (재생성용)
last_inputs: dict = {"recommend": {}, "statement": {}, "evaluate": {}}


def copy_to_clipboard(text: str) -> str:
    """복사 완료 메시지 반환 (JS에서 실제 복사 수행)"""
    if not text.strip():
        return "⚠️ 복사할 내용이 없습니다"
    char_count = len(text)
    return f"✅ 복사됨 ({char_count}자)"


def create_ui(show_model_tab: bool = True):
    """Gradio UI 생성"""
    with gr.Blocks(title="SA_SLM") as app:
        gr.Markdown("""
        # 🎓 SA_SLM: 생기부 설계 AI
        
        성공 사례 기반으로 차별화된 활동을 추천하고 세특 문장을 생성합니다.
        
        > ⚠️ 이 시스템은 **보조 도구**입니다. 최종 생기부 확정은 컨설턴트가 수행해야 합니다.
        """)
        
        if show_model_tab:
            # 모델 로드 탭
            with gr.Tab("🔧 모델 설정"):
                gr.Markdown("### LoRA Adapter 로드")
                gr.Markdown("Colab 학습에서 다운로드한 `sa_slm_adapter.zip`을 압축 해제한 경로를 입력하세요.")
                
                adapter_input = gr.Textbox(
                    label="Adapter 경로",
                    placeholder="./adapter",
                    value="./adapter"
                )
                load_btn = gr.Button("모델 로드", variant="primary")
                load_status = gr.Textbox(label="상태", interactive=False)
                
                load_btn.click(load_model, inputs=[adapter_input], outputs=[load_status])

                gr.Markdown("### 실행 환경 확인")
                runtime_btn = gr.Button("실행 환경 확인")
                runtime_output = gr.Markdown()
                runtime_btn.click(get_runtime_info, outputs=[runtime_output])
        
        # 활동 추천 탭
        with gr.Tab("🎯 활동 추천"):
            gr.Markdown("### 학생 프로필 기반 활동 추천")
            
            with gr.Row():
                with gr.Column():
                    track_input = gr.Dropdown(
                        label="계열",
                        choices=["자연", "인문", "예체능"],
                        value="자연"
                    )
                    grade_tier_input = gr.Dropdown(
                        label="성적",
                        choices=["1등급대", "2등급대", "3등급대", "4등급대", "5등급대"],
                        value="2등급대"
                    )
                    target_major_input = gr.Textbox(
                        label="목표 전공",
                        placeholder="컴퓨터공학",
                        value="컴퓨터공학"
                    )
                
                with gr.Column():
                    interests_input = gr.Textbox(
                        label="관심 분야 (쉼표로 구분)",
                        placeholder="AI, XAI, AGI, 빅데이터, 데이터사이언스",
                        value="AI, XAI, AGI, 빅데이터, 데이터사이언스",
                    )
                    values_input = gr.Textbox(
                        label="가치관/사회 관심 (쉼표로 구분)",
                        placeholder="AI 윤리, 디지털 격차 해소",
                        value="AI 윤리, 디지털 격차 해소"
                    )
            
            with gr.Row():
                recommend_btn = gr.Button("활동 추천", variant="primary")
                recommend_regen_btn = gr.Button("🔄 재생성", variant="secondary")
                recommend_copy_btn = gr.Button("📋 복사")
            recommend_status = gr.Textbox(label="상태", interactive=False)
            recommend_output = gr.Textbox(label="추천 결과", lines=10, interactive=False)
            
            def recommend_with_save(*args):
                last_inputs["recommend"] = {
                    "track": args[0], "grade_tier": args[1], "interests": args[2],
                    "values": args[3], "target_major": args[4]
                }
                for status, text in recommend_activities_stream(*args):
                    yield status, text
            
            def recommend_regenerate():
                inp = last_inputs["recommend"]
                if not inp:
                    yield "⚠️ 먼저 추천을 실행하세요", ""
                    return
                for status, text in recommend_activities_stream(
                    inp["track"], inp["grade_tier"], inp["interests"], inp["values"], inp["target_major"]
                ):
                    yield status, text
            
            recommend_btn.click(
                recommend_with_save,
                inputs=[track_input, grade_tier_input, interests_input, values_input, target_major_input],
                outputs=[recommend_status, recommend_output]
            )
            recommend_regen_btn.click(
                recommend_regenerate,
                outputs=[recommend_status, recommend_output]
            )
            recommend_copy_btn.click(
                None,
                inputs=[recommend_output],
                js="(text) => { navigator.clipboard.writeText(text); }"
            )
        
        # 세특 문장 생성 탭
        with gr.Tab("📝 세특 문장 생성"):
            gr.Markdown("### 활동 → NEIS 세특 문장")
            
            subject_input = gr.Textbox(
                label="과목",
                placeholder="정보",
                value="정보"
            )
            activity_input = gr.Textbox(
                label="활동 내용",
                placeholder="이미지 분류 데이터셋 클래스 불균형 문제 탐구. 언더/오버샘플링 직접 구현하여 비교 실험.",
                lines=3
            )
            
            with gr.Row():
                statement_btn = gr.Button("문장 생성", variant="primary")
                statement_regen_btn = gr.Button("🔄 재생성", variant="secondary")
                statement_copy_btn = gr.Button("📋 복사")
            statement_status = gr.Textbox(label="상태", interactive=False)
            statement_output = gr.Textbox(label="생성된 문장", lines=5, interactive=False)
            
            def statement_with_save(subject, activity):
                last_inputs["statement"] = {"subject": subject, "activity": activity}
                for status, text in generate_statement_stream(subject, activity):
                    yield status, text
            
            def statement_regenerate():
                inp = last_inputs["statement"]
                if not inp:
                    yield "⚠️ 먼저 문장 생성을 실행하세요", ""
                    return
                for status, text in generate_statement_stream(inp["subject"], inp["activity"]):
                    yield status, text
            
            statement_btn.click(
                statement_with_save,
                inputs=[subject_input, activity_input],
                outputs=[statement_status, statement_output]
            )
            statement_regen_btn.click(
                statement_regenerate,
                outputs=[statement_status, statement_output]
            )
            statement_copy_btn.click(
                None,
                inputs=[statement_output],
                js="(text) => { navigator.clipboard.writeText(text); }"
            )
        
        # 역량 평가 탭
        with gr.Tab("📊 역량 평가"):
            gr.Markdown("### 세특 문장 역량 평가")
            
            eval_statement_input = gr.Textbox(
                label="평가할 문장",
                placeholder="코딩 동아리에서 프로그래밍을 배우고 간단한 프로젝트를 수행함.",
                lines=3
            )
            eval_major_input = gr.Textbox(
                label="목표 전공",
                placeholder="컴퓨터공학",
                value="컴퓨터공학"
            )
            
            with gr.Row():
                evaluate_btn = gr.Button("평가하기", variant="primary")
                evaluate_regen_btn = gr.Button("🔄 재생성", variant="secondary")
                evaluate_copy_btn = gr.Button("📋 복사")
            evaluate_status = gr.Textbox(label="상태", interactive=False)
            evaluate_output = gr.Textbox(label="평가 결과", lines=10, interactive=False)
            
            def evaluate_with_save(statement, major):
                last_inputs["evaluate"] = {"statement": statement, "major": major}
                for status, text in evaluate_statement_stream(statement, major):
                    yield status, text
            
            def evaluate_regenerate():
                inp = last_inputs["evaluate"]
                if not inp:
                    yield "⚠️ 먼저 평가를 실행하세요", ""
                    return
                for status, text in evaluate_statement_stream(inp["statement"], inp["major"]):
                    yield status, text
            
            evaluate_btn.click(
                evaluate_with_save,
                inputs=[eval_statement_input, eval_major_input],
                outputs=[evaluate_status, evaluate_output]
            )
            evaluate_regen_btn.click(
                evaluate_regenerate,
                outputs=[evaluate_status, evaluate_output]
            )
            evaluate_copy_btn.click(
                None,
                inputs=[evaluate_output],
                js="(text) => { navigator.clipboard.writeText(text); }"
            )
        
        gr.Markdown("""
        ---
        **SA_SLM** | Colab 학습 결과를 로컬에서 사용
        """)
    
    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", type=str, default="", help="LoRA adapter 경로")
    parser.add_argument("--port", type=int, default=7860, help="서버 포트")
    parser.add_argument("--share", action="store_true", help="공유 링크 생성")
    parser.add_argument("--auth", action="store_true", help="접속 인증 사용")
    parser.add_argument("--auth-user", type=str, default="", help="접속 사용자명")
    parser.add_argument("--auth-pass", type=str, default="", help="접속 비밀번호")
    args = parser.parse_args()
    
    # 시작 시 adapter 자동 로드
    if args.adapter:
        print(load_model(args.adapter))

    app = create_ui(show_model_tab=not args.share)

    auth: Optional[list[Tuple[str, str]]] = None
    if args.auth:
        user = args.auth_user.strip() or os.environ.get("SA_SLM_UI_USER", "").strip() or "admin"
        password = args.auth_pass.strip() or os.environ.get("SA_SLM_UI_PASS", "").strip()
        if not password:
            try:
                password = getpass.getpass("SA_SLM UI password: ")
            except Exception:
                password = ""
        if not password:
            raise SystemExit("--auth 사용 시 비밀번호가 필요합니다. --auth-pass 또는 SA_SLM_UI_PASS를 설정하세요.")
        print(f"Auth enabled. Username: {user}")
        auth = [(user, password)]

    app.queue().launch(server_port=args.port, share=args.share, auth=auth)
