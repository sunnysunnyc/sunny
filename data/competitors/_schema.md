# 경쟁사 데이터 JSON 스키마

이 문서는 `data/competitors/` 디렉토리에 저장되는 경쟁사 JSON 파일의 구조를 정의합니다.

---

## 전체 구조

```json
{
  "meta": { ... },
  "company": { ... },
  "product": { ... },
  "business": { ... },
  "market": { ... },
  "trends": [ ... ],
  "competitive_position": { ... }
}
```

---

## 각 섹션 상세

### 1. meta (메타 정보)

| 필드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| `id` | string | 고유 식별자 (파일명과 동일) | `"weverse"` |
| `name_ko` | string | 한국어 이름 | `"위버스"` |
| `name_en` | string | 영어 이름 | `"Weverse"` |
| `last_updated` | string | 마지막 업데이트 날짜 (YYYY-MM-DD) | `"2026-03-01"` |
| `data_confidence` | string | 데이터 신뢰도 (high/medium/low) | `"high"` |
| `sources` | array | 참고 출처 목록 | 아래 참조 |

**sources 항목:**
```json
{
  "url": "https://example.com/article",
  "title": "기사 제목",
  "date": "2026-02-15",
  "type": "news|report|official|review|social"
}
```

### 2. company (회사 정보)

| 필드 | 타입 | 설명 |
|------|------|------|
| `parent` | string | 모회사명 |
| `subsidiary` | string | 운영 자회사/사업부 |
| `founded` | string | 설립 연도 |
| `headquarters` | string | 본사 위치 |
| `key_people` | array | 주요 인물 `[{ "name": "...", "role": "..." }]` |

### 3. product (제품/서비스)

| 필드 | 타입 | 설명 |
|------|------|------|
| `type` | string | 제품 유형 (super-app, messaging, community 등) |
| `platforms` | array | 지원 플랫폼 `["iOS", "Android", "Web"]` |
| `launch_date` | string | 출시일 (YYYY-MM) |
| `core_features` | array | 핵심 기능 목록 (아래 참조) |
| `ux_highlights` | array | UX 강점 (문자열 배열) |
| `ux_pain_points` | array | UX 약점 (문자열 배열) |

**core_features 항목:**
```json
{
  "name": "기능명",
  "category": "social|messaging|commerce|live-streaming|content|membership|ai",
  "description": "기능 설명",
  "is_paid": true/false,
  "price_usd": 5.0,
  "price_unit": "월/멤버",
  "differentiator": true/false
}
```

### 4. business (사업/재무)

| 필드 | 타입 | 설명 |
|------|------|------|
| `revenue_model` | array | 수익 모델 목록 |
| `financial_metrics` | object | 재무 지표 (자유 형식) |
| `funding` | array | 투자 유치 내역 |
| `partnerships` | array | 주요 파트너십 (문자열 배열) |
| `expansion_strategy` | array | 확장 전략 (문자열 배열) |

**revenue_model 항목:**
```json
{
  "type": "subscription|ecommerce|membership|advertising|commission",
  "name": "서비스명",
  "pricing": "가격 설명"
}
```

### 5. market (시장 지표)

| 필드 | 타입 | 설명 |
|------|------|------|
| `mau` | number | 월간 활성 사용자 수 |
| `mau_date` | string | MAU 기준 시점 |
| `total_downloads` | number | 누적 다운로드 수 |
| `total_artists` | number | 입점 아티스트 수 |
| `global_ratio` | number | 해외 사용자 비율 (0~1) |
| `primary_markets` | array | 주요 시장 (국가 목록) |
| `app_store_rating` | object | 앱스토어 평점 `{ "ios": 4.2, "android": 3.8, "review_count_estimate": "..." }` |

### 6. trends (동향 로그)

시간순으로 누적되는 동향 기록 (append-only).

```json
{
  "date": "2026-02",
  "category": "product|financial|user|partnership|milestone|regulatory",
  "summary": "동향 요약",
  "source": "출처명"
}
```

### 7. competitive_position (경쟁 포지션 - SWOT)

| 필드 | 타입 | 설명 |
|------|------|------|
| `strengths` | array | 강점 (문자열 배열) |
| `weaknesses` | array | 약점 (문자열 배열) |
| `opportunities` | array | 기회 (문자열 배열) |
| `threats` | array | 위협 (문자열 배열) |

---

## 데이터 작성 규칙

1. **출처 필수**: 정량 데이터 (MAU, 매출 등)는 반드시 `meta.sources`에 출처 기재
2. **미확인 표시**: 확인되지 않은 정보는 값 앞에 `"(미확인) "` 접두어 추가
3. **날짜 기준 명시**: 모든 수치 데이터에 기준 시점 포함
4. **append-only trends**: `trends` 배열에는 항목을 추가만 하고, 기존 항목은 수정/삭제하지 않음
5. **한국어 우선**: 설명과 요약은 한국어로 작성, 고유명사는 원어 유지
