#!/usr/bin/env python3
"""
합성 학생 데이터 100개 생성 스크립트
Schema v2 기준
"""

import json
import random
import os

# 기본 설정
REGIONS = ["서울", "경기", "수도권", "비수도권"]
SCHOOL_TYPES = ["평준화", "비평준화", "자사고", "특목고", "영재고"]
TRACKS = ["인문", "사회", "자연", "공학", "의약", "예체능"]
GRADE_TIERS = ["1등급대", "2등급대", "3등급대", "4등급대", "5등급대이하"]
ADMISSION_TYPES = ["학종", "교과", "논술", "실기"]
PERFORMANCE_LEVELS = ["상향", "적정", "하향"]
UNIVERSITY_TIERS = ["최상위권", "상위권", "중상위권", "중위권"]

# 계열별 세부 전공
MAJORS = {
    "인문": ["국어국문학", "영어영문학", "사학", "철학", "심리학", "문헌정보학"],
    "사회": ["경영학", "경제학", "법학", "행정학", "정치외교학", "사회학", "미디어커뮤니케이션"],
    "자연": ["수학", "물리학", "화학", "생명과학", "지구과학", "통계학"],
    "공학": ["컴퓨터공학", "전기전자공학", "기계공학", "화학공학", "건축공학", "산업공학", "신소재공학"],
    "의약": ["의예과", "치의예과", "한의예과", "약학", "간호학", "수의예과"],
    "예체능": ["미술", "음악", "체육교육", "디자인", "연극영화", "무용"]
}

# 계열별 관심사
INTERESTS = {
    "인문": ["문학", "언어학", "역사", "철학", "번역", "글쓰기", "비평", "고전"],
    "사회": ["경영전략", "마케팅", "금융", "회계", "법률", "정책", "국제관계", "사회문제"],
    "자연": ["수리논증", "실험설계", "데이터분석", "자연현상", "과학철학", "연구방법론"],
    "공학": ["프로그래밍", "인공지능", "로봇공학", "IoT", "빅데이터", "시스템설계", "알고리즘"],
    "의약": ["의료윤리", "생명과학", "임상연구", "공중보건", "헬스케어", "의료AI"],
    "예체능": ["창작", "공연", "전시기획", "스포츠과학", "예술경영", "미디어아트"]
}

# 계열별 가치관
VALUES = {
    "인문": ["문화다양성", "인권", "역사의식", "비판적사고", "인문정신"],
    "사회": ["ESG", "사회적기업", "공정무역", "지속가능발전", "사회혁신"],
    "자연": ["과학윤리", "환경보전", "기초과학발전", "객관성", "진리탐구"],
    "공학": ["기술윤리", "지속가능기술", "디지털격차해소", "접근성", "혁신"],
    "의약": ["생명존중", "의료형평성", "환자중심", "공중보건", "의료봉사"],
    "예체능": ["예술의사회적역할", "문화민주주의", "창의성", "다양성존중", "표현의자유"]
}

# 계열별 과목
SUBJECTS = {
    "인문": ["국어", "문학", "영어", "제2외국어", "윤리와사상", "한국사"],
    "사회": ["사회문화", "경제", "정치와법", "세계사", "윤리와사상", "영어"],
    "자연": ["수학", "물리학", "화학", "생명과학", "지구과학", "정보"],
    "공학": ["수학", "물리학", "정보", "기술가정", "화학", "영어"],
    "의약": ["생명과학", "화학", "수학", "영어", "보건", "윤리와사상"],
    "예체능": ["미술", "음악", "체육", "미술창작", "음악실기", "국어"]
}

# 활동 유형
ACTIVITY_TYPES = ["탐구프로젝트", "실험연구", "독서토론", "발표", "동아리활동", "봉사활동", "현장체험", "경시대회", "작품창작", "팀프로젝트"]
ROLES = ["연구자", "팀장", "발표자", "참가자", "기획자", "진행자"]

# 계열별 활동 템플릿
ACTIVITY_TEMPLATES = {
    "인문": [
        {"desc": "{subject} 시간에 {topic}에 관한 비평 에세이 작성", "neis": "{topic}에 대한 심층적 분석을 통해 비판적 사고력을 발휘하며, 논리적인 글쓰기 능력을 보여줌."},
        {"desc": "고전 문학 작품 {work} 분석 및 현대적 재해석 발표", "neis": "{work}를 현대적 관점에서 재해석하여 발표하며, 시대를 초월한 인문학적 통찰력을 보여줌."},
        {"desc": "{language} 원서 강독 스터디 운영", "neis": "{language} 원서를 직접 읽고 해석하며 언어 능력과 문화 이해도를 높이는 자기주도적 학습 태도를 보임."},
    ],
    "사회": [
        {"desc": "{topic} 관련 사회문제 분석 및 정책 제안 보고서 작성", "neis": "{topic} 문제의 원인을 다각도로 분석하고 실현 가능한 정책 대안을 제시하며 사회적 통찰력을 보여줌."},
        {"desc": "모의 UN 대회 참가, {country} 대표로 {issue} 의제 토론", "neis": "{country}의 입장에서 {issue} 문제를 분석하고 외교적 협상 능력을 발휘하며 국제적 시각을 넓힘."},
        {"desc": "사회적 기업 {company} 사례 연구 및 비즈니스 모델 분석", "neis": "사회적 가치와 경제적 지속가능성의 균형을 고민하며 혁신적인 비즈니스 모델에 대한 이해를 보여줌."},
    ],
    "자연": [
        {"desc": "{topic} 관련 가설 설정 및 실험 설계, 데이터 분석", "neis": "{topic}에 대한 과학적 호기심을 바탕으로 체계적인 실험을 설계하고 데이터를 분석하는 탐구 역량을 보여줌."},
        {"desc": "수학적 모델링으로 {phenomenon} 현상 분석", "neis": "수학적 도구를 활용하여 {phenomenon}을 모델링하고 예측하며 수리적 사고력과 응용 능력을 보여줌."},
        {"desc": "{subject} 심화 개념 탐구 및 학급 내 멘토링 활동", "neis": "{subject}의 심화 개념을 스스로 탐구하고 동료 학생들에게 설명하며 지식 나눔의 자세를 보여줌."},
    ],
    "공학": [
        {"desc": "{tech}를 활용한 {project} 프로젝트 개발", "neis": "{tech} 기술을 활용하여 {project}를 구현하며 문제 해결 능력과 공학적 사고력을 보여줌."},
        {"desc": "알고리즘 문제 해결 및 {language} 코딩 역량 강화", "neis": "다양한 알고리즘 문제를 해결하며 논리적 사고력과 프로그래밍 역량을 꾸준히 발전시킴."},
        {"desc": "{issue} 문제 해결을 위한 기술적 솔루션 설계", "neis": "{issue} 문제에 대해 기술적 관점에서 접근하여 실현 가능한 솔루션을 설계하는 창의적 문제 해결력을 보여줌."},
    ],
    "의약": [
        {"desc": "{disease} 관련 의학 논문 리뷰 및 발표", "neis": "{disease}에 관한 최신 연구 동향을 파악하고 비판적으로 분석하며 의학적 탐구심을 보여줌."},
        {"desc": "의료 봉사 활동 참여 및 환자 케어 경험", "neis": "의료 현장에서 환자를 돌보며 생명 존중의 가치와 의료인으로서의 사명감을 체득함."},
        {"desc": "{topic} 관련 생명윤리 토론 참여", "neis": "{topic}에 관한 생명윤리적 쟁점을 다각도로 분석하고 균형 잡힌 시각으로 토론에 참여함."},
    ],
    "예체능": [
        {"desc": "{medium}을 활용한 {theme} 주제 작품 창작", "neis": "{medium}을 통해 {theme}를 표현하며 독창적인 예술적 감성과 기술적 완성도를 보여줌."},
        {"desc": "{event} 대회 참가 및 입상", "neis": "꾸준한 연습과 노력으로 {event}에서 우수한 성과를 거두며 예술적/체육적 역량을 인정받음."},
        {"desc": "{field} 분야 전문가 멘토링 및 진로 탐색", "neis": "{field} 분야 전문가의 조언을 통해 진로에 대한 구체적인 비전을 수립하고 전문성 개발에 힘씀."},
    ],
}

# 템플릿 변수
TEMPLATE_VARS = {
    "인문": {
        "topic": ["실존주의", "포스트모더니즘", "페미니즘 문학", "동서양 비교철학", "언어와 권력", "기억과 역사"],
        "work": ["햄릿", "파우스트", "죄와 벌", "변신", "이방인", "노인과 바다"],
        "language": ["영어", "일본어", "중국어", "프랑스어", "독일어", "스페인어"],
    },
    "사회": {
        "topic": ["청년실업", "주거불평등", "기후변화 대응", "디지털 격차", "저출산 고령화", "플랫폼 노동"],
        "country": ["한국", "미국", "중국", "EU", "개발도상국"],
        "issue": ["기후변화", "난민", "핵비확산", "무역분쟁", "인권"],
        "company": ["그라민은행", "파타고니아", "탐스슈즈", "소셜벤처"],
    },
    "자연": {
        "topic": ["효소 반응 속도", "빛의 회절", "유전자 발현", "화학 평형", "천체 운동", "생태계 균형"],
        "phenomenon": ["인구 증가", "전염병 확산", "기후 변화", "주가 변동"],
        "subject": ["미적분", "역학", "유기화학", "분자생물학", "확률통계"],
    },
    "공학": {
        "tech": ["Python", "Arduino", "React", "TensorFlow", "Unity", "라즈베리파이"],
        "project": ["챗봇", "IoT 센서 시스템", "웹 앱", "게임", "데이터 시각화 대시보드"],
        "language": ["Python", "Java", "C++", "JavaScript"],
        "issue": ["교통 혼잡", "에너지 효율", "정보 접근성", "노인 돌봄"],
    },
    "의약": {
        "disease": ["암", "치매", "당뇨", "감염병", "희귀질환", "정신건강"],
        "topic": ["안락사", "유전자 편집", "임상시험 윤리", "장기이식", "AI 진단"],
    },
    "예체능": {
        "medium": ["유화", "수채화", "디지털아트", "조각", "설치미술", "영상"],
        "theme": ["정체성", "자연", "도시", "관계", "시간", "기억"],
        "event": ["전국대회", "지역대회", "공모전", "전시회", "연주회"],
        "field": ["순수미술", "디자인", "클래식", "실용음악", "스포츠"],
    },
}

# 행특 템플릿
BEHAVIORAL_TEMPLATES = [
    {"neis": "타인의 의견을 경청하며 협력적으로 문제를 해결하는 자세가 돋보이며, 학급 활동에 적극적으로 참여함.", "traits": ["협업", "경청", "적극성"]},
    {"neis": "자기주도적으로 학습 계획을 세우고 실천하며, 어려운 상황에서도 포기하지 않는 끈기를 보여줌.", "traits": ["자기주도성", "끈기", "성실성"]},
    {"neis": "학급 임원으로서 구성원들의 다양한 의견을 조율하고, 갈등 상황을 원만하게 해결하는 리더십을 발휘함.", "traits": ["리더십", "조정력", "책임감"]},
    {"neis": "다른 학생들의 학습을 돕는 멘토 활동에 적극 참여하며, 지식 나눔의 가치를 실천함.", "traits": ["나눔", "배려", "협동"]},
    {"neis": "창의적인 아이디어를 제시하고 이를 구체화하는 과정에서 주도적인 역할을 수행함.", "traits": ["창의성", "주도성", "실행력"]},
]

def fill_template(template, track):
    """템플릿 변수 채우기"""
    result = template
    vars_dict = TEMPLATE_VARS.get(track, {})
    for key, values in vars_dict.items():
        placeholder = "{" + key + "}"
        if placeholder in result:
            result = result.replace(placeholder, random.choice(values))
    return result

def generate_activity(track, category, subject=None):
    """활동 생성"""
    templates = ACTIVITY_TEMPLATES.get(track, ACTIVITY_TEMPLATES["공학"])
    template = random.choice(templates)
    
    return {
        "category": category,
        "subject": subject,
        "activity_type": random.choice(ACTIVITY_TYPES),
        "role": random.choice(ROLES),
        "description": fill_template(template["desc"], track),
        "neis_statement": fill_template(template["neis"], track),
        "major_connection": f"{track} 계열 핵심 역량 연결",
        "uniqueness_score": random.randint(3, 5),
        "effectiveness_score": random.randint(3, 5),
        "tags": random.sample(INTERESTS.get(track, [])[:6], min(3, len(INTERESTS.get(track, []))))
    }

def generate_student(student_id, track):
    """학생 레코드 생성"""
    region = random.choice(REGIONS)
    school_type = random.choice(SCHOOL_TYPES)
    
    # 학교 유형에 따른 성적 분포 조정
    if school_type in ["자사고", "특목고", "영재고"]:
        grade_weights = [0.3, 0.4, 0.2, 0.1, 0.0]
    else:
        grade_weights = [0.1, 0.2, 0.3, 0.25, 0.15]
    
    overall_tier = random.choices(GRADE_TIERS, weights=grade_weights)[0]
    major_tier = random.choices(GRADE_TIERS, weights=grade_weights)[0]
    
    specific = random.choice(MAJORS[track])
    interests = random.sample(INTERESTS[track], min(3, len(INTERESTS[track])))
    values = random.sample(VALUES[track], min(2, len(VALUES[track])))
    subjects = SUBJECTS[track]
    
    # 교과 활동 (세특)
    curricular = []
    for subj in random.sample(subjects, min(3, len(subjects))):
        curricular.append(generate_activity(track, "세특", subj))
    
    # 비교과 활동
    extracurricular = []
    extra_categories = ["동아리", "진로", "봉사", "독서"]
    for cat in random.sample(extra_categories, min(3, len(extra_categories))):
        extracurricular.append(generate_activity(track, cat))
    
    # 세특
    subject_specific = []
    for act in curricular:
        subject_specific.append({
            "subject": act["subject"],
            "neis_statement": act["neis_statement"],
            "major_connection": act["major_connection"],
            "uniqueness_score": act["uniqueness_score"]
        })
    
    # 행특
    behavioral = random.choice(BEHAVIORAL_TEMPLATES)
    
    # 입시 결과 (성적에 따른 대학 티어 조정)
    tier_idx = GRADE_TIERS.index(overall_tier)
    if tier_idx <= 1:
        uni_weights = [0.4, 0.4, 0.15, 0.05]
    elif tier_idx == 2:
        uni_weights = [0.1, 0.3, 0.4, 0.2]
    else:
        uni_weights = [0.0, 0.1, 0.3, 0.6]
    
    university_tier = random.choices(UNIVERSITY_TIERS, weights=uni_weights)[0]
    
    # 상향 여부 결정
    grade_rank = GRADE_TIERS.index(overall_tier)
    uni_rank = UNIVERSITY_TIERS.index(university_tier)
    if uni_rank < grade_rank:
        performance = "상향"
    elif uni_rank == grade_rank:
        performance = "적정"
    else:
        performance = "하향"
    
    # 전형 유형 (계열별 가중치)
    if track == "예체능":
        admission_type = random.choices(ADMISSION_TYPES, weights=[0.2, 0.1, 0.1, 0.6])[0]
    elif track == "의약":
        admission_type = random.choices(ADMISSION_TYPES, weights=[0.4, 0.3, 0.3, 0.0])[0]
    else:
        admission_type = random.choices(ADMISSION_TYPES, weights=[0.5, 0.3, 0.2, 0.0])[0]
    
    # 서사 생성
    narrative = f"{overall_tier} 성적으로 '{specific}' 진학을 목표로, {', '.join(interests[:2])}에 대한 일관된 관심을 세특과 비교과 전반에 녹여냄. {', '.join(values)}라는 가치관을 바탕으로 차별화된 스토리를 구축하여 {performance} 진학에 성공."
    
    return {
        "student_id": student_id,
        "school_info": {
            "region": region,
            "school_type": school_type
        },
        "grades": {
            "overall_tier": overall_tier,
            "major_subjects_tier": major_tier,
            "career_selection_ratio": f"A {random.choice([60, 70, 80, 90, 100])}%"
        },
        "target_major": {
            "track": track,
            "specific": specific,
            "interests": interests,
            "values": values
        },
        "activities": {
            "curricular": curricular,
            "extracurricular": extracurricular
        },
        "special_notes": {
            "subject_specific": subject_specific,
            "behavioral": {
                "neis_statement": behavioral["neis"],
                "key_traits": behavioral["traits"]
            }
        },
        "admission_result": {
            "university_tier": university_tier,
            "major": specific,
            "admission_type": admission_type,
            "performance_level": performance
        },
        "consultant_notes": {
            "key_strengths": [f"{interests[0]} 분야 심화 탐구", f"{values[0]} 관련 사회적 관점", "일관된 스토리라인"],
            "winning_activities": [curricular[0]["description"][:30] + "...", extracurricular[0]["description"][:30] + "..."],
            "narrative_summary": narrative
        }
    }

def main():
    """100개 학생 데이터 생성"""
    os.makedirs("./data/raw/students", exist_ok=True)
    
    students = []
    
    # 계열별 분포 (공학/의약 조금 더 많이)
    track_counts = {
        "인문": 12,
        "사회": 15,
        "자연": 15,
        "공학": 25,
        "의약": 18,
        "예체능": 15
    }
    
    idx = 1
    for track, count in track_counts.items():
        for _ in range(count):
            student_id = f"STU_2024_{idx:03d}"
            student = generate_student(student_id, track)
            students.append(student)
            
            # 개별 파일 저장
            filepath = f"./data/raw/students/{student_id}.json"
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(student, f, ensure_ascii=False, indent=2)
            
            idx += 1
    
    print(f"Generated {len(students)} student records")
    
    # 통계 출력
    print("\n=== 생성 통계 ===")
    print(f"계열별: {track_counts}")
    
    region_counts = {}
    school_counts = {}
    grade_counts = {}
    perf_counts = {}
    
    for s in students:
        r = s["school_info"]["region"]
        region_counts[r] = region_counts.get(r, 0) + 1
        
        sc = s["school_info"]["school_type"]
        school_counts[sc] = school_counts.get(sc, 0) + 1
        
        g = s["grades"]["overall_tier"]
        grade_counts[g] = grade_counts.get(g, 0) + 1
        
        p = s["admission_result"]["performance_level"]
        perf_counts[p] = perf_counts.get(p, 0) + 1
    
    print(f"지역별: {region_counts}")
    print(f"학교유형별: {school_counts}")
    print(f"성적별: {grade_counts}")
    print(f"진학결과: {perf_counts}")

if __name__ == "__main__":
    main()
