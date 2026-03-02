#!/usr/bin/env python3
"""
팬덤 플랫폼 경쟁사 분석 대시보드 생성기

data/competitors/ 디렉토리의 JSON 파일을 읽어서
인터랙티브 HTML 대시보드를 생성합니다.

사용법: python scripts/generate-dashboard.py
결과물: reports/dashboard.html
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 프로젝트 루트 경로 설정
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data" / "competitors"
OUTPUT_PATH = PROJECT_ROOT / "reports" / "dashboard.html"


def load_competitors():
    """data/competitors/ 디렉토리의 모든 JSON 파일을 읽어서 리스트로 반환"""
    competitors = []
    for filepath in sorted(DATA_DIR.glob("*.json")):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                competitors.append(data)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"⚠️ {filepath.name} 로드 실패: {e}")
    return competitors


def get_feature_matrix(competitors):
    """기능 비교 매트릭스 데이터 생성"""
    categories = {
        "social": "커뮤니티/소셜",
        "messaging": "1:1 메시징",
        "commerce": "커머스/쇼핑",
        "live-streaming": "라이브",
        "content": "콘텐츠",
        "membership": "멤버십",
        "ai": "AI 기능",
        "platform": "플랫폼 빌더",
        "analytics": "데이터 분석",
        "integration": "외부 연동",
    }

    matrix = []
    for cat_key, cat_name in categories.items():
        row = {"category": cat_name}
        for comp in competitors:
            comp_id = comp["meta"]["id"]
            features = comp.get("product", {}).get("core_features", [])
            matching = [f for f in features if f.get("category") == cat_key]
            if matching:
                names = ", ".join(f["name"] for f in matching)
                is_paid = any(f.get("is_paid", False) for f in matching)
                row[comp_id] = {"has": True, "names": names, "paid": is_paid}
            else:
                row[comp_id] = {"has": False, "names": "", "paid": False}
        matrix.append(row)
    return matrix


def get_revenue_count(comp):
    """수익원 개수 계산"""
    return len(comp.get("business", {}).get("revenue_model", []))


def get_mau_display(comp):
    """MAU 표시용 문자열"""
    mau = comp.get("market", {}).get("mau", "미공개")
    if isinstance(mau, (int, float)):
        if mau >= 1_000_000:
            return f"{mau / 1_000_000:.0f}M"
        elif mau >= 1_000:
            return f"{mau / 1_000:.0f}K"
        return str(mau)
    return str(mau) if mau else "미공개"


def get_trends_recent(comp, limit=5):
    """최근 동향 리스트 (최신 순)"""
    trends = comp.get("trends", [])
    return sorted(trends, key=lambda t: t.get("date", ""), reverse=True)[:limit]


def generate_html(competitors):
    """HTML 대시보드 생성"""
    feature_matrix = get_feature_matrix(competitors)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 경쟁사별 색상 매핑
    colors = {
        "weverse": "#6C5CE7",
        "bubble": "#FF6B9D",
        "berries": "#FDCB6E",
        "phoning": "#00B894",
        "bemyfriends": "#E84393",
    }

    # 경쟁사 카드 HTML 생성
    cards_html = ""
    for comp in competitors:
        cid = comp["meta"]["id"]
        color = colors.get(cid, "#636e72")
        name_ko = comp["meta"]["name_ko"]
        name_en = comp["meta"]["name_en"]
        parent = comp.get("company", {}).get("parent", "")
        product_type = comp.get("product", {}).get("type", "")
        mau = get_mau_display(comp)
        revenue_count = get_revenue_count(comp)
        confidence = comp["meta"].get("data_confidence", "low")
        confidence_emoji = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(confidence, "⚪")
        status_note = comp.get("status_note", "")
        status_html = f'<div class="status-warning">{status_note}</div>' if status_note else ""

        # SWOT 요약
        strengths = comp.get("competitive_position", {}).get("strengths", [])
        weaknesses = comp.get("competitive_position", {}).get("weaknesses", [])
        top_strength = strengths[0] if strengths else "-"
        top_weakness = weaknesses[0] if weaknesses else "-"

        cards_html += f"""
        <div class="card" style="border-top: 4px solid {color}">
            <div class="card-header">
                <h3>{name_ko} <span class="name-en">{name_en}</span></h3>
                <span class="badge" style="background: {color}">{product_type}</span>
            </div>
            <div class="card-body">
                <div class="metric">
                    <span class="metric-label">모회사</span>
                    <span class="metric-value">{parent}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">MAU</span>
                    <span class="metric-value highlight">{mau}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">수익원</span>
                    <span class="metric-value">{revenue_count}개</span>
                </div>
                <div class="metric">
                    <span class="metric-label">데이터 신뢰도</span>
                    <span class="metric-value">{confidence_emoji} {confidence}</span>
                </div>
                <div class="swot-mini">
                    <div class="strength">💪 {top_strength}</div>
                    <div class="weakness">⚡ {top_weakness}</div>
                </div>
                {status_html}
            </div>
        </div>
        """

    # 기능 매트릭스 HTML
    matrix_header = "<th>기능 카테고리</th>"
    for comp in competitors:
        cid = comp["meta"]["id"]
        color = colors.get(cid, "#636e72")
        matrix_header += f'<th style="color: {color}">{comp["meta"]["name_ko"]}</th>'

    matrix_rows = ""
    for row in feature_matrix:
        matrix_rows += f"<tr><td><strong>{row['category']}</strong></td>"
        for comp in competitors:
            cid = comp["meta"]["id"]
            cell = row.get(cid, {"has": False})
            if cell["has"]:
                icon = "✅"
                paid = " 💰" if cell["paid"] else ""
                tooltip = cell["names"]
                matrix_rows += f'<td class="has-feature" title="{tooltip}">{icon}{paid}<br><small>{tooltip}</small></td>'
            else:
                matrix_rows += '<td class="no-feature">❌</td>'
        matrix_rows += "</tr>"

    # 타임라인 HTML 생성
    all_trends = []
    for comp in competitors:
        cid = comp["meta"]["id"]
        color = colors.get(cid, "#636e72")
        name = comp["meta"]["name_ko"]
        for trend in comp.get("trends", []):
            all_trends.append({
                "date": trend.get("date", ""),
                "summary": trend.get("summary", ""),
                "category": trend.get("category", ""),
                "source": trend.get("source", ""),
                "comp_name": name,
                "comp_color": color,
            })
    all_trends.sort(key=lambda t: t["date"], reverse=True)

    category_emojis = {
        "product": "📦",
        "financial": "💰",
        "milestone": "🏆",
        "partnership": "🤝",
        "user": "👥",
    }

    timeline_html = ""
    for trend in all_trends[:20]:
        emoji = category_emojis.get(trend["category"], "📌")
        timeline_html += f"""
        <div class="timeline-item">
            <div class="timeline-date">{trend['date']}</div>
            <div class="timeline-content">
                <span class="timeline-badge" style="background: {trend['comp_color']}">{trend['comp_name']}</span>
                {emoji} {trend['summary']}
                <span class="timeline-source">— {trend['source']}</span>
            </div>
        </div>
        """

    # SWOT 탭 HTML
    swot_tabs = ""
    swot_contents = ""
    for i, comp in enumerate(competitors):
        cid = comp["meta"]["id"]
        color = colors.get(cid, "#636e72")
        name = comp["meta"]["name_ko"]
        active = "active" if i == 0 else ""
        cp = comp.get("competitive_position", {})

        swot_tabs += f'<button class="swot-tab {active}" onclick="showSwot(\'{cid}\')" style="border-bottom-color: {color}">{name}</button>'

        s_items = "".join(f"<li>{s}</li>" for s in cp.get("strengths", []))
        w_items = "".join(f"<li>{w}</li>" for w in cp.get("weaknesses", []))
        o_items = "".join(f"<li>{o}</li>" for o in cp.get("opportunities", []))
        t_items = "".join(f"<li>{t}</li>" for t in cp.get("threats", []))

        display = "grid" if i == 0 else "none"
        swot_contents += f"""
        <div class="swot-content" id="swot-{cid}" style="display: {display}">
            <div class="swot-box strength-box">
                <h4>💪 강점 (Strengths)</h4>
                <ul>{s_items}</ul>
            </div>
            <div class="swot-box weakness-box">
                <h4>⚡ 약점 (Weaknesses)</h4>
                <ul>{w_items}</ul>
            </div>
            <div class="swot-box opportunity-box">
                <h4>🚀 기회 (Opportunities)</h4>
                <ul>{o_items}</ul>
            </div>
            <div class="swot-box threat-box">
                <h4>⚠️ 위협 (Threats)</h4>
                <ul>{t_items}</ul>
            </div>
        </div>
        """

    # 포지셔닝 맵 데이터
    positioning_data = []
    for comp in competitors:
        cid = comp["meta"]["id"]
        features = comp.get("product", {}).get("core_features", [])
        unique_cats = set(f.get("category") for f in features)
        feature_breadth = len(unique_cats) / 10 * 100  # 10개 카테고리 기준
        paid_count = sum(1 for f in features if f.get("is_paid"))
        total_count = len(features) if features else 1
        paid_ratio = paid_count / total_count * 100
        positioning_data.append({
            "id": cid,
            "name": comp["meta"]["name_ko"],
            "x": feature_breadth,
            "y": paid_ratio,
            "color": colors.get(cid, "#636e72"),
        })

    positioning_dots = ""
    for p in positioning_data:
        left = max(5, min(90, p["x"]))
        bottom = max(5, min(90, p["y"]))
        positioning_dots += f"""
        <div class="pos-dot" style="left: {left}%; bottom: {bottom}%; background: {p['color']}">
            <span class="pos-label">{p['name']}</span>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>팬덤 플랫폼 경쟁사 분석 대시보드</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f6fa;
            color: #2d3436;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }}
        .header h1 {{ font-size: 1.8rem; margin-bottom: 0.5rem; }}
        .header p {{ opacity: 0.8; font-size: 0.9rem; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 1.5rem; }}
        .section {{ margin-bottom: 2rem; }}
        .section-title {{
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #dfe6e9;
        }}

        /* 카드 그리드 */
        .card-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.2rem;
        }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            transition: transform 0.2s;
        }}
        .card:hover {{ transform: translateY(-3px); box-shadow: 0 4px 20px rgba(0,0,0,0.12); }}
        .card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }}
        .card-header h3 {{ font-size: 1.2rem; }}
        .name-en {{ font-size: 0.8rem; color: #636e72; font-weight: normal; }}
        .badge {{
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            color: white;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .metric {{ display: flex; justify-content: space-between; padding: 0.4rem 0; border-bottom: 1px solid #f0f0f0; }}
        .metric-label {{ color: #636e72; font-size: 0.85rem; }}
        .metric-value {{ font-weight: 600; font-size: 0.9rem; }}
        .metric-value.highlight {{ color: #e17055; font-size: 1.1rem; }}
        .swot-mini {{ margin-top: 0.8rem; }}
        .swot-mini .strength {{ color: #00b894; font-size: 0.8rem; margin-bottom: 0.3rem; }}
        .swot-mini .weakness {{ color: #e17055; font-size: 0.8rem; }}
        .status-warning {{
            margin-top: 0.8rem;
            padding: 0.5rem;
            background: #ffeaa7;
            border-radius: 6px;
            font-size: 0.8rem;
            color: #636e72;
        }}

        /* 기능 매트릭스 */
        .matrix-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }}
        .matrix-table th {{
            background: #2d3436;
            color: white;
            padding: 0.8rem;
            text-align: center;
            font-size: 0.85rem;
        }}
        .matrix-table td {{
            padding: 0.7rem;
            text-align: center;
            border-bottom: 1px solid #f0f0f0;
            font-size: 0.85rem;
        }}
        .matrix-table tr:hover {{ background: #f8f9fa; }}
        .has-feature {{ background: #f0fff4; }}
        .no-feature {{ background: #fff5f5; color: #ccc; }}
        .has-feature small {{ color: #636e72; display: block; margin-top: 2px; }}

        /* 포지셔닝 맵 */
        .positioning-map {{
            position: relative;
            width: 100%;
            height: 400px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            overflow: hidden;
        }}
        .pos-axis-x, .pos-axis-y {{
            position: absolute;
            background: #dfe6e9;
        }}
        .pos-axis-x {{ width: 80%; height: 1px; top: 50%; left: 10%; }}
        .pos-axis-y {{ width: 1px; height: 80%; top: 10%; left: 50%; }}
        .pos-label-axis {{
            position: absolute;
            font-size: 0.75rem;
            color: #636e72;
            font-weight: 600;
        }}
        .pos-dot {{
            position: absolute;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            transform: translate(-50%, 50%);
            cursor: pointer;
            z-index: 2;
        }}
        .pos-label {{
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            white-space: nowrap;
            font-size: 0.8rem;
            font-weight: 700;
            color: #2d3436;
            background: rgba(255,255,255,0.9);
            padding: 2px 6px;
            border-radius: 4px;
        }}

        /* 타임라인 */
        .timeline {{ background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }}
        .timeline-item {{
            display: flex;
            gap: 1rem;
            padding: 0.8rem 0;
            border-bottom: 1px solid #f0f0f0;
        }}
        .timeline-item:last-child {{ border-bottom: none; }}
        .timeline-date {{
            min-width: 80px;
            font-size: 0.8rem;
            color: #636e72;
            font-weight: 600;
        }}
        .timeline-content {{ font-size: 0.85rem; flex: 1; }}
        .timeline-badge {{
            display: inline-block;
            padding: 0.1rem 0.5rem;
            border-radius: 10px;
            color: white;
            font-size: 0.7rem;
            margin-right: 0.3rem;
            font-weight: 600;
        }}
        .timeline-source {{ color: #b2bec3; font-size: 0.75rem; }}

        /* SWOT */
        .swot-tabs {{ display: flex; gap: 0; margin-bottom: 0; }}
        .swot-tab {{
            padding: 0.7rem 1.5rem;
            border: none;
            background: #dfe6e9;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 600;
            border-radius: 8px 8px 0 0;
            border-bottom: 3px solid transparent;
            transition: all 0.2s;
        }}
        .swot-tab.active {{ background: white; }}
        .swot-tab:hover {{ background: #f8f9fa; }}
        .swot-content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            background: white;
            padding: 1.5rem;
            border-radius: 0 12px 12px 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }}
        .swot-box {{
            padding: 1rem;
            border-radius: 8px;
        }}
        .swot-box h4 {{ margin-bottom: 0.5rem; font-size: 0.9rem; }}
        .swot-box ul {{ list-style: none; }}
        .swot-box li {{ font-size: 0.8rem; padding: 0.3rem 0; border-bottom: 1px solid rgba(0,0,0,0.05); }}
        .strength-box {{ background: #f0fff4; }}
        .weakness-box {{ background: #fff5f5; }}
        .opportunity-box {{ background: #f0f4ff; }}
        .threat-box {{ background: #fffbf0; }}

        .footer {{
            text-align: center;
            padding: 2rem;
            color: #b2bec3;
            font-size: 0.8rem;
        }}

        @media (max-width: 768px) {{
            .card-grid {{ grid-template-columns: 1fr; }}
            .swot-content {{ grid-template-columns: 1fr; }}
            .positioning-map {{ height: 300px; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 팬덤 플랫폼 경쟁사 분석 대시보드</h1>
        <p>Platform Strategy Team | 최종 업데이트: {now}</p>
    </div>

    <div class="container">
        <!-- 1. 경쟁사 개요 카드 -->
        <div class="section">
            <h2 class="section-title">📋 경쟁사 개요</h2>
            <div class="card-grid">
                {cards_html}
            </div>
        </div>

        <!-- 2. 기능 비교 매트릭스 -->
        <div class="section">
            <h2 class="section-title">🔧 기능 비교 매트릭스</h2>
            <table class="matrix-table">
                <thead><tr>{matrix_header}</tr></thead>
                <tbody>{matrix_rows}</tbody>
            </table>
        </div>

        <!-- 3. 포지셔닝 맵 -->
        <div class="section">
            <h2 class="section-title">🗺️ 시장 포지셔닝 맵</h2>
            <div class="positioning-map">
                <div class="pos-axis-x"></div>
                <div class="pos-axis-y"></div>
                <div class="pos-label-axis" style="bottom: 5%; left: 50%; transform: translateX(-50%);">단일기능</div>
                <div class="pos-label-axis" style="top: 5%; left: 50%; transform: translateX(-50%);">슈퍼앱</div>
                <div class="pos-label-axis" style="left: 5%; top: 50%; transform: translateY(-50%);">무료 중심</div>
                <div class="pos-label-axis" style="right: 5%; top: 50%; transform: translateY(-50%);">유료 중심</div>
                {positioning_dots}
            </div>
        </div>

        <!-- 4. SWOT 분석 -->
        <div class="section">
            <h2 class="section-title">📊 SWOT 분석</h2>
            <div class="swot-tabs">{swot_tabs}</div>
            {swot_contents}
        </div>

        <!-- 5. 최근 동향 타임라인 -->
        <div class="section">
            <h2 class="section-title">📰 최근 동향 타임라인</h2>
            <div class="timeline">
                {timeline_html}
            </div>
        </div>
    </div>

    <div class="footer">
        <p>Generated by 경쟁사 분석 에이전트 | Platform Strategy Team</p>
        <p>데이터 출처: 각 경쟁사 JSON 파일 참조</p>
    </div>

    <script>
        // SWOT 탭 전환
        function showSwot(compId) {{
            // 모든 콘텐츠 숨기기
            document.querySelectorAll('.swot-content').forEach(el => el.style.display = 'none');
            // 모든 탭 비활성화
            document.querySelectorAll('.swot-tab').forEach(el => el.classList.remove('active'));
            // 선택된 콘텐츠 보이기
            document.getElementById('swot-' + compId).style.display = 'grid';
            // 선택된 탭 활성화
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>"""
    return html


def main():
    print("🚀 팬덤 플랫폼 경쟁사 분석 대시보드 생성 중...")

    # 데이터 로드
    competitors = load_competitors()
    if not competitors:
        print("❌ data/competitors/ 디렉토리에 JSON 파일이 없습니다.")
        sys.exit(1)

    print(f"📁 {len(competitors)}개 경쟁사 데이터 로드 완료")
    for comp in competitors:
        print(f"   - {comp['meta']['name_ko']} ({comp['meta']['id']})")

    # HTML 생성
    html = generate_html(competitors)

    # 파일 저장
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ 대시보드 생성 완료!")
    print(f"📄 파일: {OUTPUT_PATH}")
    print(f"💡 브라우저에서 열기: open {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
