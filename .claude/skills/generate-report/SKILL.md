---
name: generate-report
description: 경쟁사 데이터를 기반으로 다양한 형식의 리포트를 생성합니다. "리포트", "보고서", "브리핑", "요약" 요청 시 사용합니다.
argument-hint: "[리포트 유형: comparison|weekly|executive]"
---

# 리포트 생성 스킬

## 입력
- `$ARGUMENTS`: 리포트 유형
  - `comparison` - 경쟁사 비교 분석 리포트
  - `weekly` - 주간 브리핑
  - `executive` - 경영진 요약 (1-2페이지)

## 리포트 생성 프로세스

### Step 1: 데이터 수집
1. `data/competitors/` 디렉토리의 모든 JSON 파일을 읽는다 (`_schema.md` 제외)
2. 각 파일의 `meta.last_updated`를 확인한다
3. 7일 이상 오래된 데이터가 있으면 경고한다:
   "⚠️ [경쟁사명] 데이터가 [N]일 전 업데이트입니다. `/analyze-competitor [이름]`으로 갱신을 권장합니다."

### Step 2: 템플릿 로드
`templates/` 디렉토리에서 해당 유형의 템플릿을 읽는다:
- `comparison` → `templates/comparison-report.md`
- `weekly` → `templates/weekly-briefing.md`
- `executive` → `templates/executive-summary.md`

### Step 3: 리포트 작성
템플릿의 `{{placeholder}}`를 실제 데이터와 분석으로 채운다.

리포트 작성 원칙:
1. **정량 근거 우선**: 수치와 출처가 있는 정보를 먼저 제시
2. **So What 원칙**: 모든 데이터 포인트에 "그래서 우리에게 의미하는 바" 추가
3. **액션 지향**: 리포트 말미에 "권장 액션" 섹션 포함
4. **불확실성 표시**: 미확인 정보는 ⚠️로 표시
5. **한국어 작성**: 본문은 한국어, 고유명사만 원어 유지

### Step 4: 파일 저장
`reports/[유형]-[YYYY-MM-DD].md` 형식으로 저장한다.
- 예: `reports/comparison-2026-03-01.md`
- 예: `reports/weekly-2026-03-01.md`
- 예: `reports/executive-2026-03-01.md`

### Step 5: 사용자 안내
1. 생성된 리포트의 핵심 내용을 요약하여 보여준다 (전체 리포트 내용이 아닌 핵심만)
2. 리포트 파일 경로를 안내한다
3. 리포트를 열어볼 것인지 사용자에게 물어본다

## 리포트 유형별 특성

### comparison (비교 분석)
- 목적: 경쟁사 간 종합 비교
- 분량: 상세 (A4 5-7페이지 수준)
- 포함: 기능 매트릭스, 사업 모델, 시장 지표, SWOT, 포지셔닝 맵
- 대상: 팀 내부 활용

### weekly (주간 브리핑)
- 목적: 이번 주 주요 변화 요약
- 분량: 간결 (A4 2-3페이지 수준)
- 포함: 핵심 3줄 요약, 경쟁사별 움직임, 시장 트렌드
- 대상: 팀 공유

### executive (경영진 요약)
- 목적: 경영진 보고
- 분량: 핵심만 (A4 1-2페이지 수준)
- 포함: 한눈에 보기 표, Top 3 인사이트, 권장 전략
- 대상: 경영진/의사결정자

## 주의사항
- 리포트에 사용하는 모든 데이터는 JSON 파일의 출처를 기반으로 한다
- 추가 웹 검색은 하지 않는다 (데이터 갱신이 필요하면 `/analyze-competitor` 또는 `/market-update` 사용 안내)
- 이미 같은 날짜의 리포트가 있으면 덮어쓴다
