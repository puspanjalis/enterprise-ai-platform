from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pathlib import Path

out = Path('/mnt/data/enterprise_ai_platform_repo/docs/one_page_summary.pdf')
arch = Path('/mnt/data/enterprise_ai_platform_repo/docs/architecture.png')

W, H = letter
c = canvas.Canvas(str(out), pagesize=letter)

# Background
c.setFillColor(colors.HexColor('#F8FAFC'))
c.rect(0, 0, W, H, fill=1, stroke=0)

# Header band
c.setFillColor(colors.HexColor('#0F172A'))
c.rect(0, H-92, W, 92, fill=1, stroke=0)

c.setFillColor(colors.white)
c.setFont('Helvetica-Bold', 24)
c.drawString(42, H-50, 'Enterprise AI Platform Demo')
c.setFont('Helvetica', 11)
c.drawString(42, H-68, 'Snowflake + MLOps example • synthetic data • cloud-neutral architecture patterns')

# Summary paragraph
c.setFillColor(colors.HexColor('#1E293B'))
c.setFont('Helvetica-Bold', 14)
c.drawString(42, H-120, 'Overview')
text = c.beginText(42, H-142)
text.setFont('Helvetica', 10.5)
text.setFillColor(colors.HexColor('#334155'))
summary = (
    'This case study shows an end-to-end enterprise AI platform: data ingestion, curated data zones, feature engineering, '
    'model training, deployment, and monitoring. The repo includes runnable Python code, CI/CD templates, infrastructure stubs, '
    'and stakeholder-ready architecture collateral.'
)
for line in [
    'This case study shows an end-to-end enterprise AI platform: data ingestion, curated data zones,',
    'feature engineering, model training, deployment, and monitoring. The repo includes runnable',
    'Python code, CI/CD templates, infrastructure stubs, and stakeholder-ready architecture collateral.'
]:
    text.textLine(line)
c.drawText(text)

# Capability pills
pill_y = H-205
pill_specs = [
    ('1. Ingest', '#E0F2FE', '#38BDF8', 42),
    ('2. Curate', '#F3E8FF', '#C084FC', 145),
    ('3. Train', '#DCFCE7', '#4ADE80', 248),
    ('4. Monitor', '#FEF3C7', '#F59E0B', 351),
]
for label, fill, stroke, x in pill_specs:
    c.setFillColor(colors.HexColor(fill))
    c.setStrokeColor(colors.HexColor(stroke))
    c.roundRect(x, pill_y, 88, 26, 10, fill=1, stroke=1)
    c.setFillColor(colors.HexColor('#0F172A'))
    c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(x+44, pill_y+8, label)

# Architecture block
c.setFillColor(colors.white)
c.setStrokeColor(colors.HexColor('#CBD5E1'))
c.roundRect(42, 245, 330, 285, 16, fill=1, stroke=1)
c.setFillColor(colors.HexColor('#0F172A'))
c.setFont('Helvetica-Bold', 13)
c.drawString(58, 508, 'Reference architecture')
c.setFont('Helvetica', 9.5)
c.setFillColor(colors.HexColor('#475569'))
c.drawString(58, 492, 'Flow: sources → ingest → curate → features → train → serve → monitor')
c.drawImage(ImageReader(str(arch)), 56, 276, width=302, height=198, preserveAspectRatio=True, mask='auto')

# Metrics block
c.setFillColor(colors.white)
c.setStrokeColor(colors.HexColor('#CBD5E1'))
c.roundRect(392, 390, 178, 140, 16, fill=1, stroke=1)
c.setFillColor(colors.HexColor('#0F172A'))
c.setFont('Helvetica-Bold', 13)
c.drawString(408, 508, 'Demo KPIs')
metrics = [
    ('120k', 'records processed'),
    ('92%', 'model accuracy'),
    ('Green', 'drift status'),
]
y = 475
for value, label in metrics:
    c.setFillColor(colors.HexColor('#0F172A'))
    c.setFont('Helvetica-Bold', 18)
    c.drawString(408, y, value)
    c.setFillColor(colors.HexColor('#475569'))
    c.setFont('Helvetica', 10)
    c.drawString(465, y+2, label)
    y -= 34

# Repo assets block
c.setFillColor(colors.white)
c.setStrokeColor(colors.HexColor('#CBD5E1'))
c.roundRect(392, 245, 178, 125, 16, fill=1, stroke=1)
c.setFillColor(colors.HexColor('#0F172A'))
c.setFont('Helvetica-Bold', 13)
c.drawString(408, 348, 'Included assets')
assets = [
    'README + runnable pipeline',
    'Sample ETL and training code',
    'CI/CD + IaC stubs',
    'Architecture PNG/PDF',
    'System overview slide deck',
]
y = 330
c.setFont('Helvetica', 9.5)
c.setFillColor(colors.HexColor('#334155'))
for a in assets:
    c.drawString(410, y, f'• {a}')
    y -= 18

# IP checklist block
c.setFillColor(colors.white)
c.setStrokeColor(colors.HexColor('#CBD5E1'))
c.roundRect(42, 88, 528, 132, 16, fill=1, stroke=1)
c.setFillColor(colors.HexColor('#0F172A'))
c.setFont('Helvetica-Bold', 13)
c.drawString(58, 198, 'IP and publication checklist')
items = [
    'Public cloud or open frameworks only',
    'Synthetic dataset only; no customer data',
    'Abstract environment and company names',
    'Architecture patterns emphasized over proprietary code',
]
y = 176
c.setFont('Helvetica', 10)
c.setFillColor(colors.HexColor('#334155'))
for i in items:
    c.drawString(60, y, f'• {i}')
    y -= 20

# Footer
c.setFillColor(colors.HexColor('#64748B'))
c.setFont('Helvetica', 8.5)
c.drawString(42, 40, 'Deliverables: repo + architecture diagram + slide deck + one-page summary. Demo video optional and not included.')

c.showPage()
c.save()
print(out)
