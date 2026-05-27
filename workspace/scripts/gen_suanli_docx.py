#!/usr/bin/env python3
"""生成算力服务项目招商话术手册 DOCX 版本"""

from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

# ── 颜色定义 ──
NAVY = RGBColor(0x1B, 0x2A, 0x4A)       # 深蓝主色
DARK_NAVY = RGBColor(0x0F, 0x1E, 0x3A)   # 更深蓝
ORANGE = RGBColor(0xE8, 0x6C, 0x00)       # 烤橙强调
LIGHT_ORANGE = RGBColor(0xFF, 0x9F, 0x43) # 浅橙
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF0, 0xF2, 0xF5)  # 浅灰底
MED_GRAY = RGBColor(0x99, 0x99, 0x99)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)

doc = Document()

# ── 样式设置 ──
style = doc.styles['Normal']
font = style.font
font.name = '微软雅黑'
font.size = Pt(10.5)
font.color.rgb = DARK_GRAY
style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

for level in range(1, 4):
    hs = doc.styles[f'Heading {level}']
    hf = hs.font
    hf.name = '微软雅黑'
    hf.bold = True
    hf.color.rgb = NAVY
    hf.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    if level == 1:
        hf.size = Pt(22)
    elif level == 2:
        hf.size = Pt(16)
    else:
        hf.size = Pt(13)

# ── 页面设置 ──
for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.8)
    section.right_margin = Cm(2.8)

# ══════════════════════════════════════════════
# 辅助函数
# ══════════════════════════════════════════════

def add_cover(doc):
    """封面"""
    for _ in range(6):
        doc.add_paragraph('')
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('算力服务项目\n招商转型科普及营销话术手册')
    run.font.size = Pt(28)
    run.font.bold = True
    run.font.color.rgb = NAVY
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = p2.add_run('用招商的语言说算力的事，把"卖算力"翻译成"引项目"')
    run2.font.size = Pt(13)
    run2.font.color.rgb = ORANGE
    run2.font.name = '微软雅黑'
    run2.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    
    for _ in range(4):
        doc.add_paragraph('')
    
    info_items = [
        ('适用对象', '开发区招商干部出身的人脉合作伙伴'),
        ('核心原则', '用招商的语言说算力的事'),
        ('价格数据', '2026年5月国内算力租赁行情'),
        ('版本', '修订版·价格数据修正'),
    ]
    for label, value in info_items:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p.add_run(f'{label}：')
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = NAVY
        r1.font.name = '微软雅黑'
        r1.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        r2 = p.add_run(value)
        r2.font.size = Pt(11)
        r2.font.color.rgb = DARK_GRAY
        r2.font.name = '微软雅黑'
        r2.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    
    doc.add_page_break()


def add_body(doc, text, font_size=10.5, bold=False, italic=False, color=DARK_GRAY, space_before=0, space_after=6, alignment=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if alignment:
        p.alignment = alignment
    run = p.add_run(text)
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    return p


def add_quote_box(doc, text, label='话术'):
    """话术调用框 — 灰色底色 + 橙色左边框效果"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    
    # 添加左色块（模拟边框）
    run_label = p.add_run(f'💬 {label}： ')
    run_label.font.size = Pt(10)
    run_label.font.bold = True
    run_label.font.color.rgb = ORANGE
    run_label.font.name = '微软雅黑'
    run_label.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    
    run_text = p.add_run(text)
    run_text.font.size = Pt(10)
    run_text.font.color.rgb = DARK_GRAY
    run_text.font.italic = True
    run_text.font.name = '微软雅黑'
    run_text.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    
    # 添加灰色底纹到段落
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F5F5F5" w:val="clear"/>')
    p.paragraph_format.element.get_or_add_pPr().append(shd)
    return p


def add_table_styled(doc, headers, rows, col_widths=None):
    """创建带样式的表格"""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # 设置表格样式
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else parse_xml(f'<w:tblPr {nsdecls("w")}/>')
    
    # 设置边框
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        '  <w:top w:val="single" w:sz="6" w:space="0" w:color="CCCCCC"/>'
        '  <w:left w:val="single" w:sz="6" w:space="0" w:color="CCCCCC"/>'
        '  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="CCCCCC"/>'
        '  <w:right w:val="single" w:sz="6" w:space="0" w:color="CCCCCC"/>'
        '  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="DDDDDD"/>'
        '  <w:insideV w:val="single" w:sz="4" w:space="0" w:color="DDDDDD"/>'
        '</w:tblBorders>'
    )
    tblPr.append(borders)
    
    # 表头
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(h)
        run.font.size = Pt(9)
        run.font.bold = True
        run.font.color.rgb = WHITE
        run.font.name = '微软雅黑'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # 深蓝背景
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1B2A4A" w:val="clear"/>')
        cell._tc.get_or_add_tcPr().append(shd)
    
    # 数据行
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = table.rows[ri + 1].cells[ci]
            cell.text = ''
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            run = p.add_run(str(val))
            run.font.size = Pt(9)
            run.font.color.rgb = DARK_GRAY
            run.font.name = '微软雅黑'
            run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
            
            # 首列加粗
            if ci == 0:
                run.font.bold = True
                run.font.color.rgb = NAVY
            
            # 隔行底色
            if ri % 2 == 0:
                shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F5F7FA" w:val="clear"/>')
                cell._tc.get_or_add_tcPr().append(shd)
    
    doc.add_paragraph('')  # 表后空行
    return table


def add_key_number(doc, number, label, sublabel=''):
    """突出关键数字"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(str(number))
    r1.font.size = Pt(26)
    r1.font.bold = True
    r1.font.color.rgb = ORANGE
    r1.font.name = '微软雅黑'
    r1.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(2)
    r2 = p2.add_run(label)
    r2.font.size = Pt(10)
    r2.font.color.rgb = DARK_GRAY
    r2.font.name = '微软雅黑'
    r2.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    if sublabel:
        r2b = p2.add_run(f'\n{sublabel}')
        r2b.font.size = Pt(8)
        r2b.font.color.rgb = MED_GRAY


def add_divider(doc):
    """章节分隔线"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('─' * 50)
    run.font.color.rgb = RGBColor(0xDD, 0xDD, 0xDD)
    run.font.size = Pt(8)

# ══════════════════════════════════════════════
# 正文生成
# ══════════════════════════════════════════════

add_cover(doc)

# ── 目录页 ──
doc.add_heading('目录', level=1)
toc_items = [
    '第一章　快速入门——算力是什么（三句话版）',
    '第二章　你的身份定位',
    '第三章　算力项目落地的"招商式"解读',
    '第四章　六种真实的客户场景及对应话术',
    '第五章　招商话术对照表',
    '第六章　招商金句库',
    '第七章　可转发的算力科普',
    '第八章　第一单行动清单',
    '附录　30秒自我定位',
]
for item in toc_items:
    add_body(doc, item, font_size=11, color=NAVY, space_before=4, space_after=4)
doc.add_page_break()

# ══════════════════════════════════════════════
# 第一章
# ══════════════════════════════════════════════
doc.add_heading('第一章　快速入门——算力是什么（三句话版）', level=1)

add_body(doc, '你不需要懂的细节：GPU和CPU的区别、CUDA生态、PyTorch框架、HBM带宽', bold=True, color=NAVY, space_before=8)
add_body(doc, '你需要懂的：算力这件事，用招商的思维去理解：', color=MED_GRAY, space_after=4)

add_quote_box(doc, '算力就是"电"——只不过不是给电灯用的，是给AI用的。就像开发区当年招商建电厂给企业供电，现在是建算力中心给企业"供算力"。厂还是那个厂，电表换成了服务器，电费换成了租金。', '核心比喻')

# 芯片速查表
doc.add_heading('三款芯片一句话速记', level=2)
add_table_styled(doc,
    ['芯片', '定位', '月租行情', '性能水平', '适合什么客户'],
    [
        ['B300', '🏆 最新旗舰', '15-18万/月', 'H200的4倍', '科技公司、金融、极致性能需求'],
        ['H200', '💪 中坚主力', '7.5-8.5万/月', '显存比H100多76%', '高校实验室、中型AI企业、性价比优先'],
        ['H100', '🔄 存量主流', '6-6.8万/月', '上一代标杆，够用', '预算有限的创业公司、轻量推理'],
    ]
)

# 关键数字
doc.add_heading('四个行业级数字', level=2)
add_key_number(doc, '8,351亿', '2025年中国算力市场规模', '比开发区之前招的任何一个产业都大')
add_key_number(doc, '+30%', '年增速', '连续3年30%增长，爆发式赛道')
add_key_number(doc, '+40%', 'H100半年租金涨幅', '算力租金一直在涨')
add_key_number(doc, '8-12周', '交付周期', '从签约到投产，比建厂房快10倍')

add_divider(doc)
add_quote_box(doc, '我们做的是算力项目的"项目集成商"——我们签合同、对方出钱买芯片、我们来交付和运维。相当于：你招商把企业引进来，我们帮企业的AI算力建起来。', '一句话定位')

doc.add_page_break()

# 芯片一页通
doc.add_heading('附：芯片速查一页通', level=2)
add_body(doc, '你不必全记，遇到客户问翻这页', italic=True, color=MED_GRAY, space_after=8)

doc.add_heading('B300（Blackwell Ultra）——最新旗舰  🏆', level=3)
add_table_styled(doc,
    ['维度', '数据', '招商翻译'],
    [
        ['性能', 'FP8 7,000 TFLOPS，H200的4倍', '一台顶四台'],
        ['显存', '192GB HBM3e', '跑最大的AI模型都不怕'],
        ['适合谁', 'AI训练、大规模推理、金融/医疗等', '有钱有需求的客户'],
        ['月租行情', '15-18万/月（长协15万，散单18万）', '长协相当于标准化厂房月租'],
        ['稀缺度', '🔴 全球缺货，排队到明年', '最抢手的资源'],
        ['选它理由', '每P算力成本比H200低30%', '买贵的反而省钱'],
    ]
)

doc.add_heading('H200——中坚主力  💪', level=3)
add_table_styled(doc,
    ['维度', '数据', '招商翻译'],
    [
        ['性能', 'FP8 ~1,979 TFLOPS，显存141GB', 'H100的显存翻倍版'],
        ['适合谁', '大模型训练、推理部署、中型AI企业', '性价比优先的客户首选'],
        ['月租行情', '7.5-8.5万/月（2026年已涨25%）', '半年前才6万，现在8万了'],
        ['稀缺度', '🟡 供应偏紧', '主流选择，能拿到货'],
        ['选它理由', '显存大、生态成熟、最稳妥', '开发区的"标准厂房"'],
    ]
)

doc.add_heading('H100——存量主流  🔄', level=3)
add_table_styled(doc,
    ['维度', '数据', '招商翻译'],
    [
        ['性能', 'FP8 ~1,979 TFLOPS，显存80GB', '上一代旗舰，性能够用'],
        ['适合谁', '轻量推理、预算有限创业公司、集群扩容', '预算不高的客户'],
        ['月租行情', '6-6.8万/月（半年涨了40%）', '最便宜的选择，但涨得最猛'],
        ['稀缺度', '🟢 供货好转（重回京东自营）', '货有了价格没降'],
        ['选它理由', '够用、便宜、存量生态', '经济型选择'],
    ]
)

add_quote_box(doc, '预算充足要顶配 → B300\n性价比优先 → H200\n预算有限够用就行 → H100\n不知道选什么 → 约时间让我们技术团队上门聊', '三句话选芯片')

doc.add_page_break()

# ══════════════════════════════════════════════
# 第二章
# ══════════════════════════════════════════════
doc.add_heading('第二章　你的身份定位（非常重要）', level=1)

add_body(doc, '你不是"销售"，你是"项目合伙人"', bold=True, font_size=13, color=NAVY, space_before=8)
add_body(doc, '你过去的身份是：开发区招商干部——你帮政府对接企业，促成项目落地。')
add_body(doc, '你现在的新身份是：算力项目合伙人——你帮企业对接算力资源，促成项目交付。')

add_table_styled(doc,
    ['招商干部的技能', '算力项目中的对应角色'],
    [
        ['筛项目、看资质', '筛选"强主体"客户'],
        ['谈政策、讲优惠', '聊零投入、按月付、3年不涨价'],
        ['对接局办、跑审批', '帮企业找到算力需求的关键人'],
        ['看产值、算税收', '帮老板算用算力能省多少钱'],
        ['交朋友、攒人情', '把"认识的人"变成"签合同的人"'],
    ]
)

add_quote_box(doc, '以前你帮政府招商，政府给你发工资。现在你帮企业找算力，市场给你发佣金。', '核心心态转变')

doc.add_heading('你应该见的三种人', level=2)
add_table_styled(doc,
    ['谁', '为什么', '说什么'],
    [
        ['科技公司老板/CTO', '他们是直接用户', '"你们的AI跑在哪？租还是买？"'],
        ['金融机构分管科技副总', '他们有钱+合规需求', '"B300+国产芯片双栈，合规又高效"'],
        ['高校计算机学院院长', '他们缺算力+经费周期长', '"按月付费，不走采购流程"'],
    ]
)

doc.add_heading('你不太需要见的两种人', level=2)
add_table_styled(doc,
    ['谁', '为什么'],
    [
        ['纯粹的传统制造业老板（没上AI）', '他不知道自己需要什么'],
        ['基层IT运维人员', '他做不了主、签不了合同'],
    ]
)

doc.add_page_break()

# ══════════════════════════════════════════════
# 第三章
# ══════════════════════════════════════════════
doc.add_heading('第三章　算力项目落地的"招商式"解读', level=1)

doc.add_heading('算力项目全流程', level=2)
add_table_styled(doc,
    ['传统开发区招商流程', '算力项目流程'],
    [
        ['① 接洽/拜访', '① 接洽/拜访'],
        ['② 企业考察/选址', '② 需求确认/出方案'],
        ['③ 洽谈政策/优惠', '③ 报价/算成本账'],
        ['④ 签投资协议', '④ 签租赁合同'],
        ['⑤ 建设用地/环评', '⑤ 资方订购B300芯片'],
        ['⑥ 厂房建设（6-18月）', '⑥ 等待到货（8-12周）'],
        ['⑦ 投产/达产', '⑦ 部署/交付/起租'],
        ['⑧ 持续服务', '⑧ 按月运维/到期续约'],
    ]
)
add_body(doc, '关键点：整个流程你只负责前三步——接洽、确认、签约。后面的都有专业团队做。', bold=True, color=ORANGE)

doc.add_heading('跟客户讲"时间账"', level=2)
add_quote_box(doc, '李总，知道现在市场上租一台B300什么行情吗？15-18万一个月。H200是7.5-8.5万，但B300性能是H200的4倍，算下来B300更划算。自己买呢？一台650万起步，全款预付，排队等货6-9个月。我们只要8-12周——批量定制通道，签合同、采购、到货、交付一条龙。就跟开发区卖地一样——自己买地建厂房，9个月都算快的，还得自己跑审批；租我们这种"先租后扩"的模式，开张就能开工，不用一上来就砸重金。')

doc.add_heading('跟客户算"两笔账"', level=2)

doc.add_heading('第一笔账：三款芯片行情全览', level=3)
add_body(doc, '2026年5月国内GPU租赁行情（8卡整机，含税含电）：', color=MED_GRAY, space_after=4)
add_table_styled(doc,
    ['型号', '月租金', '算力(FP8)', '显存', '性能定位', '今年涨幅', '性价比评价'],
    [
        ['H100', '6-6.8万/月', '~11 PFLOPS', '80GB HBM3', '上一代旗舰，够用', '+40%（涨最猛）', '经济型选择'],
        ['H200', '7.5-8.5万/月', '~15.8 PFLOPS', '141GB HBM3e', '中坚主力，显存多76%', '+25%', '✅ 性价比之选'],
        ['B300', '15-18万/月', '~56 PFLOPS', '192GB HBM3e', '最新旗舰，是H200的4倍', '新品上市', '✅ 每P成本最低'],
    ]
)
add_body(doc, '重点理解：B300看起来贵一倍——但性能是H200的4倍。按每P算力算，B300成本比H200低30%。', bold=True, color=ORANGE)
add_body(doc, '所有GPU都在涨价：H100半年涨40%，H200半年涨25%，整体市场春节后已涨30%。签长协就是锁价——现在签3年，不管市场涨多少，你的价格不动。', bold=True, color=ORANGE)

doc.add_heading('第二笔账：买 vs 租，三款芯片全面算', level=3)
add_table_styled(doc,
    ['项目', '自己买（任一款）', '租H100', '租H200', '租B300'],
    [
        ['首期投入', '650万全款', '零', '零', '零'],
        ['每月支出', '折旧+运维≈20万', '6-6.8万', '7.5-8.5万', '15-18万'],
        ['交付周期', '6-9个月排队', '8-12周', '8-12周', '8-12周'],
        ['资金占用', '650万一次性冻结', '按月付', '按月付', '按月付'],
        ['运维', '自己组团队（月均3-5万）', '全包', '全包', '全包'],
        ['3年总成本', '650万+运维≈900万', '≈250万', '≈300万', '≈550万'],
        ['退出', '不能退', '不续约', '不续约', '不续约'],
    ]
)

add_quote_box(doc, '赵总，市场行情摆在这——B300一台18万/月，H200要8万/月。但B300性能是H200的4倍，算下来B300更省钱。而且——你现在签合同，锁定3年价格。今年算力已经涨了25%，明年什么价没人知道。就像开发区前年地价50万一亩，去年60万，今年70万——早签就是省钱。')
add_quote_box(doc, '张总，您自己买GPU就像在开发区买地建厂房——投资大、周期长、有风险。我们这种模式就像开发区先建好标准化厂房租给企业——拎包入住，按月交租，不想租了就走。现在95%的中小企业都选第二种。')

doc.add_page_break()

# ══════════════════════════════════════════════
# 第四章
# ══════════════════════════════════════════════
doc.add_heading('第四章　六种真实的客户场景及对应话术', level=1)

# 场景一
doc.add_heading('场景一：科技公司老板（最容易成交）', level=2)
add_body(doc, '背景：朋友饭局/商会活动，对方是做AI应用的企业主', color=MED_GRAY)
add_body(doc, '你的角色：老朋友叙旧+顺带提一嘴', color=MED_GRAY, space_after=6)
add_quote_box(doc, '王总，最近AI这么火，你们公司在AI上怎么弄的？\n\n对方（大概率）：唉，别说了。阿里云上GPU租着，一个月十几万，还在涨。自建又太贵。\n\n你：那巧了。我最近正好有个项目做这块。英伟达B300、H200、H100我们都能做。B300最新旗舰，15-18万一个月，性能是H200的4倍；H200中坚主力，7.5-8.5万，性价比最高；H100够用实惠，6-6.8万。不管选哪款，都是签合同按月租，不用你掏钱买，12周到货，运维全包，3年不涨价。\n\n对方：我们跑的是xx模型，你看哪款合适？\n\n你：具体我让技术团队给你出一份对比方案——你们主要跑什么模型？训练多还是推理多？预算范围大概多少？我让他们针对你的场景推荐最合适的。先试一台也行。')
add_body(doc, '关键点：', bold=True, color=NAVY)
add_body(doc, '• 不要一上来就说"算力租赁"——说"我们有个项目"')
add_body(doc, '• 不要报价——说"让技术出方案"')
add_body(doc, '• 核心钩子——不用掏钱、按月付、3年不涨价')

# 场景二
doc.add_heading('场景二：银行/金融机构分管领导', level=2)
add_body(doc, '背景：政府关系/国企客户，你以前对接过的', color=MED_GRAY)
add_body(doc, '你的角色：以前一起办事的，现在有新项目', color=MED_GRAY, space_after=6)
add_quote_box(doc, '李行长，最近银监会在推金融科技，你们AI用得怎么样？\n\n对方：有在推进，但现在GPU不好买，国产的性能又跟不上。\n\n你：我们最近做了一个方案。你们金融场景，我们推荐H200——显存大、性能够、性价比高，7.5-8.5万一个月。如果对性能有极致要求，可以上B300，15-18万，性能是H200的4倍。如果预算有限起步，H100也能用，6-6.8万。三种方案都支持国产芯片双栈——高性能推理跑英伟达，合规要求的上华为昇腾，两套环境隔离。\n\n对方：合规能过吗？\n\n你：所以我们设计方案时可以选——合规要求高的场景走国产芯片，真正跑业务的高性能场景走英伟达。拿其中一个场景先跑试点，合规团队评估后再推广。而且不用走设备采购流程，按月走服务费就行，财务上属于运营成本，不占固定资产指标。')
add_body(doc, '关键点：', bold=True, color=NAVY)
add_body(doc, '• 金融机构最怕"不合规"——所以强调双栈')
add_body(doc, '• 金融机构最烦"走采购流程"——所以强调签合同就行')
add_body(doc, '• 用"试点"降低决策难度')

# 场景三
doc.add_heading('场景三：高校计算机学院院长/实验室负责人', level=2)
add_quote_box(doc, '刘院长，今年学校的算力够用吗？\n\n对方：别提了。申请买服务器，流程走半年。学生做毕设都排队。\n\n你：我这边有个简单的办法。不用申请设备采购，按服务费走，按月付。H200最适合高校——7.5-8.5万一个月，显存大、性价比高，跑科研AI够用了。如果预算紧张，H100也行，6-6.8万。预算充足直接上B300，15-18万，性能顶配。别的高校已经在用了，走服务采购流程就行——设备采购要招投标3个月，服务采购1周就能批。')
add_body(doc, '关键点：', bold=True, color=NAVY)
add_body(doc, '• 高校痛点不是"贵"是"流程慢"')
add_body(doc, '• 把租赁包装成"服务采购"——走不同的审批通道')
add_body(doc, '• 拿其他高校做案例背书')

# 场景四
doc.add_heading('场景四：开发区管委会/政府大数据局（远期机会）', level=2)
add_quote_box(doc, '张主任，开发区不是想搞数字经济吗？我这有个项目可以帮你们出一张"算力招商"的名片。\n\n我们现在和资方合作，可以帮开发区落地一个"小规模算力节点"——不占用地指标、不新建厂房、不增加能耗指标。机柜托管+GPU租赁，12周就能投产。开发区可以把这个节点作为"招商配套"——来开发区落户的AI企业，算力优先供给。\n\n西宁开发区已经在搞了——"1+3+X"绿色算力体系，专门出了8项政策。韶关也签了智算中心项目。这个赛道现在是"谁先布局谁占优势"。')
add_body(doc, '关键点：', bold=True, color=NAVY)
add_body(doc, '• 政府要的是"政绩"和"差异化"——算力节点是数字经济的新名片')
add_body(doc, '• 强调不占用地指标、不新建厂房、不增加能耗——这是招商干部最敏感的')
add_body(doc, '• 给开发区的企业增加招商筹码')

# 场景五
doc.add_heading('场景五：企业主朋友闲聊（最轻松的切入）', level=2)
add_quote_box(doc, '老陈，最近有个事你帮我留意一下。我这边做了个算力的项目，英伟达最新芯片，按月租，不用买。你认识的企业里有没有做AI的、或者想用AI但嫌贵的？帮我介绍一下，成了有茶水费。')
add_body(doc, '关键点：', bold=True, color=NAVY)
add_body(doc, '• 轻松、不给人压力')
add_body(doc, '• 明确"有茶水费"——每个人都知道这是什么意思')
add_body(doc, '• 不要讲技术细节')

# 场景六
doc.add_heading('场景六：微信群/朋友圈（长线铺垫）', level=2)
add_body(doc, '朋友圈文案参考：', bold=True, color=NAVY)
add_quote_box(doc, '开发区待了这么多年，第一次见到一个行业年增速30%，却不需要企业重资产投入的——AI算力按月租，签合同就上线。有需要的朋友私聊。📈')
add_body(doc, '微信群（商会/校友/企业家群）：', bold=True, color=NAVY)
add_quote_box(doc, '各位老板好，我这边对接了一个AI算力的资源——英伟达B300芯片，按月租用，不用一次性投入几百万买设备。有在跑AI模型或者想上AI但觉得算力太贵的，可以私聊聊聊。')

doc.add_page_break()

# ══════════════════════════════════════════════
# 第五章
# ══════════════════════════════════════════════
doc.add_heading('第五章　你需要掌握的"招商话术对照表"', level=1)

doc.add_heading('算力术语 → 招商语言翻译', level=2)
add_table_styled(doc,
    ['算力行业怎么说', '招商干部怎么说'],
    [
        ['GPU算力租赁', '设备融资租赁+运营服务外包'],
        ['按P/年计费', '就跟开发区按亩收税一样，按量计费'],
        ['算力项目集成', 'EPC总包+运维托管'],
        ['轻资产运营', '不搞重资产，不占用固定资产指标'],
        ['推理芯片', '"应用级芯片"——专门跑应用的，不是训练的大设备'],
        ['强主体闭口合同', '有担保的3年租赁协议'],
        ['8-12周到货', '建设周期比厂房短得多，一个季度投产'],
        ['算力券', '跟高新区的创新券一样，政府补贴'],
    ]
)

doc.add_heading('常见问题应答', level=2)
add_table_styled(doc,
    ['客户问', '你答'],
    [
        ['B300、H200、H100有什么区别？', 'B300最新旗舰，性能是H200的4倍，15-18万/月；H200中坚主力，显存141GB，7.5-8.5万/月；H100上一代，6-6.8万/月。预算够上B300，性价比选H200，省钱选H100'],
        ['为什么B300比H200贵那么多？', '看着贵一倍，但性能是4倍，每P算力成本低30%。就像买一台顶配设备顶四台普通设备，总账更划算'],
        ['我们现在用H100够不够？', '够用就先租H100。明年不够了升级H200或B300——灵活升级，不用换设备，换合同就行'],
        ['你们和阿里云有什么区别？', '阿里云是公共汽车——多人共享、随时涨价；我们是包了一辆车——数据不出门、性能独享、3年不涨价'],
        ['为什么不自己买？', '自己买650万一次性砸进去，还得养运维团队。我们相当于精装厂房+物业管理，拎包入住'],
        ['等12周太久', '自己买等6-9个月，我们批量定制通道比你快一倍。而且这段时间算力还在涨价，越早签越划算'],
        ['能不能便宜点？', '市场行情就是这样——H100半年涨了40%，H200涨了25%。我们3年不涨价就是最大的便宜'],
        ['我先想想', '行。不过B300/H200配额有限，下一批可能排到年底。而且你再等三个月，价格可能又涨了10%'],
        ['别人用了吗？', '润六尺做这个模式，去年一个季度做了2.5亿。大公司都在这么干，不是我们不靠谱，是你在犹豫'],
    ]
)

doc.add_page_break()

# ══════════════════════════════════════════════
# 第六章
# ══════════════════════════════════════════════
doc.add_heading('第六章　你的"招商金句库"', level=1)
add_body(doc, '这些句子你直接背下来，见到客户就能说。', bold=True, color=ORANGE, space_after=8)

doc.add_heading('说行业的', level=2)
add_quote_box(doc, '中国算力市场去年8351亿，增速30%，比你们开发区任何一条产业链都大。')
add_quote_box(doc, '东数西算八大枢纽，国家投了435亿撬动2000亿社会资本——这是国家级赛道。')
add_quote_box(doc, '算力被写入十五五规划建议了，国家级战略——相当于十年前的云计算、二十年前的互联网。')
add_quote_box(doc, 'H200今年涨了25%，H100一年涨了40%，B300只会更抢手——这个市场还要涨。')

doc.add_heading('说产品的', level=2)
add_quote_box(doc, '三款芯片随便选——B300最新旗舰15-18万/月，性能是H200的4倍；H200中坚主力7.5-8.5万/月，性价比最优；H100上一代6-6.8万/月，够用实惠。')
add_quote_box(doc, 'B300看着贵一倍，但每P算力成本比H200低30%——买贵的反而省钱。')
add_quote_box(doc, 'H200显存141GB，比H100多76%。跑大模型训练，H200是性价比之王。')
add_quote_box(doc, '签3年合同，3年价格不动。H100半年涨了40%，H200今年涨了25%，我们一签锁3年。')
add_quote_box(doc, '按月付费，跟付房租一样。不占你预算，不占你固定资产指标。')

doc.add_heading('说模式的', level=2)
add_quote_box(doc, '我们是项目集成商——你签合同，资方出钱，我们交付运维。所有人各赚各的。')
add_quote_box(doc, '和润六尺一样的模式，他们是上市公司，我们是小规模精耕细作。')
add_quote_box(doc, '零库存风险、零资金占用、零设备折旧压力。')

doc.add_heading('催单的', level=2)
add_quote_box(doc, 'B300全球缺货，H200供应也偏紧，我们现在报出去的都是按配额走。你这单下去，排到这批12周，排到下批可能就是半年。')
add_quote_box(doc, 'H100半年涨了40%，H200涨了25%，整个市场春节后涨了30%。你现在签3年，3年不涨价——等于把未来的涨价空间锁死。')
add_quote_box(doc, '你要不要，我先帮你锁定这个月的配额。反正是签合同我们才采购，你不签我不买，没有任何风险。')

doc.add_page_break()

# ══════════════════════════════════════════════
# 第七章
# ══════════════════════════════════════════════
doc.add_heading('第七章　你可以直接转发的"算力科普"（三句话版）', level=1)
add_body(doc, '以下内容可以直接转给客户/朋友，不需要修改。', color=MED_GRAY, space_after=8)

add_body(doc, 'AI算力是什么？', bold=True, color=NAVY, font_size=12)
add_body(doc, 'AI跑模型需要算力，就像手机需要有流量。算力越强，AI跑得越快越聪明。', space_after=8)

add_body(doc, '为什么现在大家都在租算力？', bold=True, color=NAVY, font_size=12)
add_body(doc, '因为买一台B300服务器要650万起。现在三款主流芯片都可以按月租：')
add_body(doc, '• B300：最新旗舰，15-18万/月，性能是H200的4倍')
add_body(doc, '• H200：中坚主力，7.5-8.5万/月，性价比最高')
add_body(doc, '• H100：上一代旗舰，6-6.8万/月，够用实惠')
add_body(doc, '今年所有GPU都在涨价——H100半年涨40%，H200涨25%，整个市场春节后涨了30%。不如租——签合同按月付，12周到货，运维全包，3年不涨价。润六尺做这个模式，一个季度做了2.5亿。', space_after=8)

add_body(doc, '我们有什么不一样？', bold=True, color=NAVY, font_size=12)
add_body(doc, '英伟达B300/H200/H100都能做，签强主体合同就采购。三款芯片任意选，3年锁价不涨价。适合金融机构、科技公司、高校实验室。')
add_body(doc, '感兴趣私聊，发详细方案。', bold=True, color=ORANGE)

doc.add_page_break()

# ══════════════════════════════════════════════
# 第八章
# ══════════════════════════════════════════════
doc.add_heading('第八章　你的"第一单行动清单"', level=1)
add_body(doc, '目标：30天内完成第一次有效客户沟通，90天内签下第一单。', bold=True, color=ORANGE, font_size=12, space_after=8)

add_table_styled(doc,
    ['周次', '行动', '成果'],
    [
        ['第1周', '列出通讯录里最可能用算力的10个人\n（科技公司老板/银行科技副总/高校计算机院长）', '名单'],
        ['第2周', '约3个人喝茶/吃饭——随便聊，不提算力，先了解对方在AI上干什么', '需求信息'],
        ['第3周', '针对聊过的2个人，让研墨出定制方案——不超过2页纸', '方案'],
        ['第4周', '带方案上门，按本手册话术谈', '需求确认'],
        ['第5-8周', '跟进2个重点客户，推动签合同', '签约'],
        ['第9-12周', '首单签约完成 ✅ 锁定B300配额', '第一个项目启动'],
    ]
)

doc.add_page_break()

# ══════════════════════════════════════════════
# 附录
# ══════════════════════════════════════════════
doc.add_heading('附录　30秒自我定位', level=1)
add_body(doc, '如果有人问你："你现在在做什么？"', color=MED_GRAY, space_after=6)
add_quote_box(doc, '我现在跟朋友一起做算力项目。简单说就是——帮需要AI算力的企业，对接英伟达的GPU算力。B300、H200、H100都能做，看客户需求选配置。企业不用自己花几百万买设备，签合同按月租就行，我们全包运维。帮企业省了重资产投入，我也赚点服务费。跟过去招商一样，只是从"引企业进开发区"变成了"引算力进企业"。')

add_divider(doc)

add_body(doc, '最后一句话记住就行：', bold=True, font_size=12, color=NAVY, alignment=WD_ALIGN_PARAGRAPH.CENTER)
add_quote_box(doc, '你不是在"卖算力"，你是在帮企业老板把一次性砸650万买设备，变成按月15-18万租服务。这跟你以前招商时说"来我们开发区，租厂房比买地划算"是一回事。')

# ── 保存 ──
output_path = '/root/.openclaw/workspace/deliverables/算力项目招商话术手册.docx'
doc.save(output_path)
print(f'✅ 已保存: {output_path}')
print(f'   文件大小: {os.path.getsize(output_path) / 1024:.1f} KB')
