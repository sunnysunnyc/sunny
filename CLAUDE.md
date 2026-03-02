# CLAUDE.md

## 사용자 프로필

- **역할**: Platform Strategy Team 리더
- **주요 업무**: 전략기획 및 사업기획
- **기술 수준**: 비개발자 (코딩 경험 없음)
- **AI Native Camp 목표**: 팬덤 커뮤니티 / 팬 소통 앱 도메인의 경쟁사 분석 에이전트 구축

## 소통 방식

- **언어**: 한국어 우선 (기술 용어는 영어 허용)
- **응답 형식**: 구조화된 분석 형태 선호 (표, 프레임워크, 비교 분석 등)
- **근거 제시**: 주장이나 분석에는 가능한 한 출처/링크를 함께 제공
- **역할 모드**: 상황에 따라 유연하게 전환
  - 전략 논의 시 → 함께 고민하는 사고 파트너
  - 실행 단계 → 빠르게 구현하는 실행 파트너
  - 새로운 도구/개념 → 단계별로 안내하는 가이드

## 경쟁사 분석 에이전트 프로젝트

### 도메인
- 팬덤 커뮤니티 및 팬 소통 앱 (Weverse, Bubble, Berries, Phoning 등)

### 핵심 분석 항목
1. **제품/기능 비교**: 앱 기능, UX, 차별화 포인트
2. **시장/사업 전략**: 수익모델, 투자유치, 사업 확장 전략
3. **사용자/커뮤니티 동향**: 팬덤 트렌드, 사용자 반응, 앱 리뷰 분석

### 기술 스택
- 비개발자이므로 Claude가 적절한 기술 스택을 추천하고 가이드
- 가능한 한 간결하고 유지보수가 쉬운 구조 선호
- 코드 작성 시 충분한 주석과 설명 포함

## Quick Commands (빠른 사용 가이드)

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `/analyze-competitor [이름]` | 특정 경쟁사 웹 검색 분석 | `/analyze-competitor weverse` |
| `/compare-competitors [이름들]` | 경쟁사 비교 분석 | `/compare-competitors all` |
| `/generate-report [유형]` | 리포트 자동 생성 | `/generate-report weekly` |
| `/market-update` | 시장 최신 동향 수집 | `/market-update` |

### 일상 워크플로우
1. **아침**: `/market-update` → 오늘 시장 동향 확인
2. **주간**: `/generate-report weekly` → 주간 브리핑 생성
3. **필요시**: 자연어로 질문 → Claude가 적절한 스킬 자동 적용
4. **월간**: `/generate-report executive` → 경영진 보고용 요약

### 경쟁사명 매핑
- 위버스/Weverse → `weverse`
- 버블/Bubble → `bubble`
- 베리즈/Berries → `berries`
- 포닝/Phoning → `phoning`

### 자연어로도 가능
스킬 명령어를 외울 필요 없이 자연어로 물어보면 Claude가 자동으로 적절한 스킬을 실행합니다.
- "위버스 최근 어때?" → `/analyze-competitor weverse` 자동 적용
- "위버스랑 버블 비교해줘" → `/compare-competitors weverse bubble` 자동 적용
- "이번 주 업계 소식 알려줘" → `/market-update` 자동 적용
- "경영진 보고용 요약 만들어줘" → `/generate-report executive` 자동 적용

### 프로젝트 파일 구조
- `data/competitors/*.json` — 경쟁사 구조화 데이터 (스킬이 자동 업데이트)
- `templates/*.md` — 리포트 템플릿
- `reports/*.md` — 생성된 리포트 (날짜별 자동 저장)

## 업무 스타일 가이드

- 분석 결과는 **의사결정에 바로 활용 가능한 형태**로 정리
- 단순 정보 나열보다 **인사이트와 시사점** 도출을 우선
- 불확실한 정보는 명확히 표시하고, 확인이 필요한 부분은 질문
- 큰 작업은 단계별로 나누어 진행하며, 각 단계마다 방향 확인
