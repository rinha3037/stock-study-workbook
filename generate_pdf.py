# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Flowable, KeepTogether, Table, TableStyle, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Malgun', r'C:\Windows\Fonts\malgun.ttf'))
pdfmetrics.registerFont(TTFont('Malgun-Bold', r'C:\Windows\Fonts\malgunbd.ttf'))

ACCENT = colors.HexColor('#1e4d7b')
ACCENT_SOFT = colors.HexColor('#e8f0f7')
INK = colors.HexColor('#1c2733')
MUTED = colors.HexColor('#767b73')
BORDER = colors.HexColor('#c9d2da')
GOLD = colors.HexColor('#9c7a35')
GOLD_SOFT = colors.HexColor('#f4ecd9')
LINE_COLOR = colors.HexColor('#b9c2ca')

STAGES = {
    1: 'STEP 1 · 종목 정하기',
    2: 'STEP 2 · 이 회사는 무슨 회사일까?',
    3: 'STEP 3 · 이 회사를 이끄는 사람',
    4: 'STEP 4 · 숫자로 확인하기',
    5: 'STEP 5 · 투자할 회사인지 판단하기',
    6: 'STEP 6 · 나만의 투자 기준 정리',
    7: 'STEP 7 · 마무리 — 오늘 얼마나 알게 됐나요?',
}

QUESTIONS = [
    dict(num=1, stage=1, title='지금 공부해볼 주식 종목을 딱 한 가지만 정해보세요.', lines=3),
    dict(num=2, stage=1, title='많은 종목 중에서 왜 이 종목을 골랐나요?',
         note='특별한 이유가 없어도 괜찮습니다. "그냥 들어봐서", "써봐서 좋아서" 도 훌륭한 시작점이에요.', lines=4),

    dict(num=3, stage=2, title='이 회사는 어떤 문제를 해결하는 회사인가요?', lines=4),
    dict(num=4, stage=2, title='이 회사는 어떻게 돈을 버나요? 가장 매출이 큰 제품이나 서비스는 무엇인가요?',
         note='경기가 좋지 않아져도 이 제품/서비스는 계속 잘 팔릴 수 있을지도 함께 생각해보세요.', lines=5),
    dict(num=5, stage=2, title='이 회사의 경쟁사는 어디인가요? (최대 3곳) 이 시장에서 이 회사의 위치(점유율)는 어느 정도인가요?',
         note='관련 기사를 찾아 함께 읽으면 더 깊이 있는 학습이 가능해요. 웹검색/AI를 활용해도 좋지만, "진짜" 믿을 수 있는 내용인지 검증해보세요.', lines=5),

    dict(num=6, stage=3, title='CEO는 누구인가요? 어떤 사람이고 왜 이 회사를 만들었는지, 장기적인 비전은 무엇인지 확인해보세요.',
         note='① 과거에 어떤 일을 했던 사람인지 ② 단기적인 돈을 보는 사람인지, 장기 비전이 있는 사람인지 ③ 함께 일하는 조력자들은 누구인지', lines=6),
    dict(num=7, stage=3, title='CEO 인터뷰 영상이 있다면 찾아서 시청해보세요. 어떤 사람으로 느껴지나요?', lines=4),
    dict(num=8, stage=3, title='회사 홈페이지에 들어가보세요. 메인 화면에는 무엇이 있는지, CEO의 기업 철학은 무엇인지 확인하고 지금까지 알아본 내용과 비교해보세요.',
         note='외국 기업이라 영어가 어렵다면 번역 시스템을 활용해보세요. 믿을 수 있는 곳인지 검증하는 연습이에요.', lines=5),

    dict(num=9, stage=4, title='매출은 늘고 있나요? 영업이익도 늘고 있나요? 빚(부채)은 얼마나 있나요?', lines=5),
    dict(num=10, stage=4, title='이 회사의 시가총액은 얼마인가요? PER은 몇인가요? 위에서 찾은 경쟁사들의 PER과 비교하면 비싼 편인가요, 싼 편인가요?', lines=5),
    dict(num=11, stage=4, title='배당을 주는 회사인가요? 배당을 준다면 어느 시기에 얼만큼의 배당금을 주는지 확인해보세요.',
         note='진짜 돈을 버는 기업인지 확인해보는 질문이에요.', lines=4),

    dict(num=12, stage=5, title='이 회사는 10년 뒤에도 살아남을 것 같나요? 만일 이 회사가 망한다면 어떤 이유일까요?', lines=5),
    dict(num=13, stage=5, title='이 회사는 위기가 닥쳤을 때 버틸 힘이 있다고 보여지나요? 위에서 살펴본 CEO의 성향을 다시 떠올리며, 어려움을 극복할 수 있는 사람인지 체크해봅시다.', lines=5),
    dict(num=14, stage=5, title='지금 이 회사의 주가 차트는 어떤 상태로 보이나요? 자유롭게 생각을 적어보세요.', lines=4),
    dict(num=15, stage=5, title='지금까지 공부해보니, 이 회사에 투자할 이유가 충분한가요? 그런 이유와, 아닌 이유를 함께 생각해봅시다.', lines=6),

    dict(num=16, stage=6, title='나는 앞으로 어떤 기업에 투자를 하고 싶은가요? 반대로 절대 투자하지 않을 기업은 어떤 곳인가요?', lines=5),
    dict(num=17, stage=6, title='어떤 CEO가 운영하는 기업에는 투자하지 않을 것인지, 나만의 기준을 적어봅시다.', lines=5),

    dict(num=18, stage=7, title='오늘 스터디를 진행하며 느낀 점, 깨달은 점, 앞으로의 방향 등 나의 생각을 자유롭게 적어보세요.', lines=6),
]


class WriteLines(Flowable):
    def __init__(self, width, n=4, gap=8.6*mm):
        Flowable.__init__(self)
        self.width = width
        self.n = n
        self.gap = gap
        self.height = gap * n

    def draw(self):
        c = self.canv
        c.setStrokeColor(LINE_COLOR)
        c.setLineWidth(0.6)
        y = self.height - self.gap
        for _ in range(self.n):
            c.line(0, y, self.width, y)
            y -= self.gap


styles = {
    'title': ParagraphStyle('title', fontName='Malgun-Bold', fontSize=22, leading=28, textColor=INK, alignment=TA_CENTER),
    'subtitle': ParagraphStyle('subtitle', fontName='Malgun', fontSize=11, leading=16, textColor=MUTED, alignment=TA_CENTER),
    'intro': ParagraphStyle('intro', fontName='Malgun', fontSize=10, leading=16, textColor=INK),
    'stage': ParagraphStyle('stage', fontName='Malgun-Bold', fontSize=14, leading=18, textColor=INK, spaceBefore=6, spaceAfter=10),
    'qtitle': ParagraphStyle('qtitle', fontName='Malgun-Bold', fontSize=10.5, leading=15, textColor=INK),
    'note': ParagraphStyle('note', fontName='Malgun', fontSize=8.7, leading=13, textColor=MUTED, spaceBefore=2, spaceAfter=4),
    'legend': ParagraphStyle('legend', fontName='Malgun', fontSize=9, leading=15, textColor=GOLD),
    'field': ParagraphStyle('field', fontName='Malgun', fontSize=10.5, leading=14, textColor=INK),
}

CONTENT_WIDTH = A4[0] - 40*mm


def stage_badge_table(stage_num):
    label = STAGES[stage_num]
    t = Table([[f'STAGE {stage_num}', label]], colWidths=[22*mm, CONTENT_WIDTH-22*mm])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, 0), 'Malgun-Bold'),
        ('FONTNAME', (1, 0), (1, 0), 'Malgun-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 8.5),
        ('FONTSIZE', (1, 0), (1, 0), 14),
        ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
        ('TEXTCOLOR', (1, 0), (1, 0), INK),
        ('BACKGROUND', (0, 0), (0, 0), ACCENT),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('TOPPADDING', (0, 0), (0, 0), 4),
        ('BOTTOMPADDING', (0, 0), (0, 0), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('LINEBELOW', (0, 0), (-1, -1), 1, BORDER),
        ('BOTTOMPADDING', (1, 0), (1, 0), 8),
    ]))
    return t


def info_box():
    rows = [
        ['종목명', '', '티커', ''],
        ['작성자', '', '작성일', ''],
    ]
    t = Table(rows, colWidths=[22*mm, 60*mm, 18*mm, 60*mm])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Malgun'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), MUTED),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.8, BORDER),
        ('LINEBELOW', (1, 0), (1, -1), 0.8, LINE_COLOR),
        ('LINEBELOW', (3, 0), (3, -1), 0.8, LINE_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t


def legend_box():
    txt = ('<b>안다의 정의</b> — 0: 들어본 적 없다 &nbsp;·&nbsp; 1: 들어본 적 있다 &nbsp;·&nbsp; '
           '2: 최근 이슈를 안다 &nbsp;·&nbsp; 3: 재무제표를 봤다 &nbsp;·&nbsp; 4: 앞으로의 방향을 안다 &nbsp;·&nbsp; '
           '5: 이 회사의 모든 걸 설명할 수 있다')
    t = Table([[Paragraph(txt, styles['legend'])]], colWidths=[CONTENT_WIDTH])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GOLD_SOFT),
        ('BOX', (0, 0), (-1, -1), 0.6, colors.HexColor('#e6d29c')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return t


def build_question_block(q):
    parts = [Paragraph(f"Q{q['num']}. {q['title']}", styles['qtitle'])]
    if q.get('note'):
        parts.append(Paragraph('💡 ' + q['note'], styles['note']))
    else:
        parts.append(Spacer(1, 4))
    parts.append(WriteLines(CONTENT_WIDTH, n=q['lines']))
    parts.append(Spacer(1, 12))
    return KeepTogether(parts)


def build_self_check_block():
    parts = [Paragraph('자기점검. 이 워크북을 채운 지금, 이 종목에 대한 나의 "안다"의 정도는 몇 점인가요?', styles['qtitle']),
             Spacer(1, 6), legend_box(), Spacer(1, 10)]
    nums = '&nbsp;&nbsp;&nbsp;'.join([f'<b>[ {n} ]</b>' for n in range(6)])
    parts.append(Paragraph('해당하는 점수에 동그라미 쳐보세요 &nbsp;&nbsp;' + nums, styles['field']))
    parts.append(Spacer(1, 8))
    parts.append(Paragraph('왜 이 점수라고 생각하나요? 더 알아야 할 부분은 무엇인가요?', styles['note']))
    parts.append(WriteLines(CONTENT_WIDTH, n=4))
    parts.append(Spacer(1, 16))
    return KeepTogether(parts)


def build():
    doc = SimpleDocTemplate(
        r'C:\Users\kiminha\Desktop\Code\260705_주식종목워크북\프리나다움_주식_스터디_워크북.pdf',
        pagesize=A4,
        topMargin=20*mm, bottomMargin=18*mm, leftMargin=20*mm, rightMargin=20*mm,
        title='프리나다움 주식 스터디 워크북'
    )
    story = []

    story.append(Paragraph('📊 프리나다움_주식 스터디 워크북', styles['title']))
    story.append(Spacer(1, 6))
    story.append(Paragraph('나만의 종목 분석 워크북 · 한 종목씩 깊게 파보기', styles['subtitle']))
    story.append(Spacer(1, 18))
    story.append(info_box())
    story.append(Spacer(1, 16))
    intro = ('이 워크북은 종목 하나를 정해 깊이 있게 공부해보는 개인 학습지입니다. '
             '정답을 맞히는 것이 목적이 아니라, 스스로 질문하고 답을 찾아가는 연습이 목적이에요. '
             '틀려도 괜찮습니다 — "잘해야지" 보다 "많이 틀려봐야지"라는 마음으로 편하게 적어보세요. '
             '새로운 종목을 공부할 때마다 이 워크북을 새로 인쇄해서 사용해보세요.')
    story.append(Paragraph(intro, styles['intro']))
    story.append(Spacer(1, 10))
    story.append(legend_box())
    story.append(PageBreak())

    last_stage = None
    for q in QUESTIONS:
        if q['stage'] != last_stage:
            if last_stage is not None:
                story.append(Spacer(1, 6))
            story.append(stage_badge_table(q['stage']))
            last_stage = q['stage']
            if q['stage'] == 7:
                story.append(build_self_check_block())
        story.append(build_question_block(q))

    doc.build(story)


if __name__ == '__main__':
    build()
    print('done')
