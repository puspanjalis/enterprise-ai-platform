from pathlib import Path
import html
import cairosvg

W, H = 1600, 900
bg = '#F8FAFC'
text_dark = '#0F172A'
muted = '#475569'
line = '#64748B'
light_border = '#CBD5E1'
platform_border = '#94A3B8'

boxes = [
    ('Data Sources\nAPIs • Files • CDC • SaaS', 70, 360, 200, 92, '#E0F2FE', '#38BDF8'),
    ('Ingestion & Orchestration\nBatch / Streaming Jobs', 310, 360, 240, 92, '#DBEAFE', '#60A5FA'),
    ('Raw Zone\nLanding / Audit', 590, 360, 170, 92, '#EDE9FE', '#A78BFA'),
    ('Curated Zone\nQuality Rules • Standardization', 800, 360, 260, 92, '#F3E8FF', '#C084FC'),
    ('Feature Store\nTraining / Serving Features', 1100, 360, 220, 92, '#FAE8FF', '#E879F9'),
    ('Model Training\nExperiments • Validation', 1360, 360, 220, 92, '#DCFCE7', '#4ADE80'),
    ('Model Registry\nVersioning • Approval', 1360, 520, 220, 92, '#D1FAE5', '#34D399'),
    ('Batch / API Scoring\nJobs • Endpoints', 1100, 520, 220, 92, '#ECFCCB', '#84CC16'),
    ('Monitoring & Ops\nDrift • SLAs • Alerts', 800, 520, 260, 92, '#FEF3C7', '#F59E0B'),
]

controls = [
    ('Governance\nCatalog • Policies • Lineage', 410, 130, 250, 86),
    ('CI/CD\nTests • IaC • Promotion', 690, 130, 210, 86),
    ('Security\nSecrets • RBAC • Encryption', 930, 130, 260, 86),
]

def esc(s):
    return html.escape(s)

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
svg.append(f'<rect width="100%" height="100%" fill="{bg}"/>')
svg.append('<style>'
           '.title{font:700 34px Helvetica,Arial,sans-serif; fill:#0F172A;}'
           '.section{font:700 20px Helvetica,Arial,sans-serif; fill:#0F172A;}'
           '.label{font:400 13px Helvetica,Arial,sans-serif; fill:#475569;}'
           '.box1{font:700 16px Helvetica,Arial,sans-serif; fill:#0F172A;}'
           '.box2{font:400 13px Helvetica,Arial,sans-serif; fill:#334155;}'
           '</style>')
svg.append('<defs>'
           f'<marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="{line}"/></marker>'
           f'<marker id="arrowLight" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="{platform_border}"/></marker>'
           '</defs>')

svg.append('<text x="800" y="62" text-anchor="middle" class="title">Enterprise AI Platform</text>')
svg.append('<text x="800" y="92" text-anchor="middle" class="label">Scalable data ingestion → feature engineering → model training → deployment → monitoring</text>')
svg.append(f'<rect x="365" y="108" width="860" height="130" rx="18" ry="18" fill="white" fill-opacity="0.55" stroke="{light_border}" stroke-width="1.8" stroke-dasharray="7 7"/>')
svg.append('<text x="795" y="126" text-anchor="middle" class="section">Cross-cutting controls</text>')

for title, x, y, w, h in controls:
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" ry="18" fill="#FFFFFF" stroke="{light_border}" stroke-width="1.6"/>')
    t1, t2 = title.splitlines()
    cx = x + w/2
    svg.append(f'<text x="{cx}" y="{y+34}" text-anchor="middle" class="box1" font-size="15">{esc(t1)}</text>')
    svg.append(f'<text x="{cx}" y="{y+58}" text-anchor="middle" class="box2">{esc(t2)}</text>')

svg.append(f'<rect x="40" y="300" width="1520" height="360" rx="22" ry="22" fill="#FFFFFF" fill-opacity="0.4" stroke="{platform_border}" stroke-width="1.8" stroke-dasharray="7 7"/>')
svg.append('<text x="800" y="286" text-anchor="middle" class="section" font-size="24">Reference architecture</text>')

# data flow arrows behind boxes
svg.append(f'<line x1="270" y1="406" x2="298" y2="406" stroke="{line}" stroke-width="3" marker-end="url(#arrow)"/>')
svg.append(f'<line x1="550" y1="406" x2="578" y2="406" stroke="{line}" stroke-width="3" marker-end="url(#arrow)"/>')
svg.append(f'<line x1="760" y1="406" x2="788" y2="406" stroke="{line}" stroke-width="3" marker-end="url(#arrow)"/>')
svg.append(f'<line x1="1060" y1="406" x2="1088" y2="406" stroke="{line}" stroke-width="3" marker-end="url(#arrow)"/>')
svg.append(f'<line x1="1320" y1="406" x2="1348" y2="406" stroke="{line}" stroke-width="3" marker-end="url(#arrow)"/>')
svg.append(f'<line x1="1470" y1="452" x2="1470" y2="508" stroke="{line}" stroke-width="3" marker-end="url(#arrow)"/>')
svg.append(f'<line x1="1360" y1="566" x2="1332" y2="566" stroke="{line}" stroke-width="3" marker-end="url(#arrow)"/>')
svg.append(f'<line x1="1100" y1="566" x2="1072" y2="566" stroke="{line}" stroke-width="3" marker-end="url(#arrow)"/>')

# control connectors
svg.append(f'<path d="M 535 216 L 535 272 L 930 272 L 930 348" fill="none" stroke="{light_border}" stroke-width="2" stroke-dasharray="7 7" marker-end="url(#arrowLight)"/>')
svg.append(f'<path d="M 795 216 L 795 246 L 1470 246 L 1470 348" fill="none" stroke="{light_border}" stroke-width="2" stroke-dasharray="7 7" marker-end="url(#arrowLight)"/>')
svg.append(f'<path d="M 1060 216 L 1060 246 L 1210 246 L 1210 508" fill="none" stroke="{light_border}" stroke-width="2" stroke-dasharray="7 7" marker-end="url(#arrowLight)"/>')

# feedback loop
svg.append(f'<path d="M 800 566 L 650 566 L 650 640 L 1470 640 L 1470 452" fill="none" stroke="{platform_border}" stroke-width="3" marker-end="url(#arrowLight)"/>')
svg.append('<text x="1040" y="628" text-anchor="middle" class="label">monitoring feedback loop to retraining</text>')

# boxes
for title, x, y, w, h, fill, stroke in boxes:
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" ry="18" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    t1, t2 = title.splitlines()
    cx = x + w/2
    svg.append(f'<text x="{cx}" y="{y+34}" text-anchor="middle" class="box1">{esc(t1)}</text>')
    svg.append(f'<text x="{cx}" y="{y+59}" text-anchor="middle" class="box2">{esc(t2)}</text>')

# consumers and output arrows
svg.append(f'<line x1="930" y1="612" x2="930" y2="710" stroke="{line}" stroke-width="3" marker-end="url(#arrow)"/>')
svg.append(f'<line x1="1210" y1="612" x2="1210" y2="710" stroke="{line}" stroke-width="3" marker-end="url(#arrow)"/>')
svg.append('<rect x="1060" y="720" width="300" height="92" rx="18" ry="18" fill="#FEE2E2" stroke="#F87171" stroke-width="2"/>')
svg.append('<text x="1210" y="754" text-anchor="middle" class="box1">Consumers</text>')
svg.append('<text x="1210" y="779" text-anchor="middle" class="box2">BI • Apps • Ops Teams</text>')

svg.append('<text x="90" y="854" class="label">Synthetic data • open frameworks • cloud-neutral templates • no proprietary code</text>')
svg.append('</svg>')
svg_str = ''.join(svg)
Path('/mnt/data/enterprise_ai_platform_repo/docs/architecture.svg').write_text(svg_str)
cairosvg.svg2png(bytestring=svg_str.encode(), write_to='/mnt/data/enterprise_ai_platform_repo/docs/architecture.png', output_width=1600, output_height=900)
cairosvg.svg2pdf(bytestring=svg_str.encode(), write_to='/mnt/data/enterprise_ai_platform_repo/docs/architecture.pdf')
print('done')
