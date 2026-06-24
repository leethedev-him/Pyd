import re
import os
import zipfile
from lxml import etree
import latex2mathml.converter
import mathml2omml

NS_W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS_M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
NS_XML = 'http://www.w3.org/XML/1998/namespace'

etree.register_namespace('m', NS_M)

W_P = f'{{{NS_W}}}p'
W_R = f'{{{NS_W}}}r'
W_T = f'{{{NS_W}}}t'
W_RPR = f'{{{NS_W}}}rPr'
M_OMATH = f'{{{NS_M}}}oMath'
M_OMATHPARA = f'{{{NS_M}}}oMathPara'

RPR_FIELDS = {
    f'{{{NS_W}}}rStyle', f'{{{NS_W}}}b', f'{{{NS_W}}}i',
    f'{{{NS_W}}}caps', f'{{{NS_W}}}smallCaps', f'{{{NS_W}}}strike',
    f'{{{NS_W}}}dstrike', f'{{{NS_W}}}sz', f'{{{NS_W}}}szCs',
    f'{{{NS_W}}}color', f'{{{NS_W}}}highlight', f'{{{NS_W}}}vertAlign',
    f'{{{NS_W}}}u', f'{{{NS_W}}}effect', f'{{{NS_W}}}ltr',
}

RE_DISPLAY = re.compile(r'\$\$(.+?)\$\$', re.DOTALL)
RE_INLINE = re.compile(r'(?<!\$)\$(.+?)\$(?!\$)', re.DOTALL)
RE_TRIPLE_BS = re.compile(r'\\{3,}')
RE_NUMERIC = re.compile(r'^[\d.,\s]+$')


def strip_artifacts(text):
    return RE_TRIPLE_BS.sub('', text)


def looks_real(content):
    content = content.strip()
    if not content:
        return False
    return not RE_NUMERIC.match(content)


def latex_to_omml(latex, display):
    mathml = latex2mathml.converter.convert(latex, display=display)
    omml_str = mathml2omml.convert(mathml)
    wrapped = f'<root xmlns:m="{NS_M}">{omml_str}</root>'
    root = etree.fromstring(wrapped)
    return root[0]


def copy_props(target, props):
    if not props:
        return
    existing = target.find(W_RPR)
    if existing is not None:
        target.remove(existing)
    rpr = etree.SubElement(target, W_RPR)
    for p in props:
        rpr.append(p)


def text_run(parent, text, props=None):
    r = etree.SubElement(parent, W_R)
    copy_props(r, props)
    t = etree.SubElement(r, W_T)
    t.text = text
    t.set(f'{{{NS_XML}}}space', 'preserve')


def para_text(para):
    return ''.join((t.text or '') for t in para.iter(W_T))


def find_matches(full_text):
    dm = list(RE_DISPLAY.finditer(full_text))
    dr = [(m.start(), m.end()) for m in dm]
    im = [
        m for m in RE_INLINE.finditer(full_text)
        if not any(ds <= m.end() and de >= m.start() for ds, de in dr)
    ]
    out = [(m.start(), m.end(), m.group(1), 'display') for m in dm]
    out.extend((m.start(), m.end(), m.group(1), 'inline') for m in im)
    out.sort(key=lambda x: x[0])
    return out


def run_props(r):
    rpr = r.find(W_RPR)
    if rpr is None:
        return None
    return [c for c in rpr if c.tag in RPR_FIELDS]


def process_para(para):
    full = para_text(para)
    if '$' not in full:
        return 0

    matches = find_matches(full)
    if not matches:
        return 0

    first = para.find(W_R)
    props = run_props(first) if first is not None else None

    for child in list(para):
        para.remove(child)

    pos = 0
    count = 0
    for start, end, content, kind in matches:
        if start > pos:
            text_run(para, full[pos:start], props)
        cleaned = strip_artifacts(content)
        if cleaned and looks_real(cleaned):
            count += 1
            omml = latex_to_omml(
                cleaned, 'block' if kind == 'display' else 'inline'
            )
            if kind == 'display':
                wrapper = etree.SubElement(para, M_OMATHPARA)
                wrapper.append(omml)
            else:
                para.append(omml)
        else:
            text_run(para, full[start:end], props)
        pos = end

    if pos < len(full):
        text_run(para, full[pos:], props)

    return count


def fix_docx(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f'File not found: {path}')

    out = os.path.join(
        os.path.dirname(path),
        f'{os.path.splitext(os.path.basename(path))[0]}_fixed.docx',
    )

    with zipfile.ZipFile(path, 'r') as z:
        if 'word/document.xml' not in z.namelist():
            raise ValueError('Invalid DOCX: word/document.xml not found')
        data = z.read('word/document.xml')

    root = etree.fromstring(data)

    total = 0
    for para in root.iter(W_P):
        total += process_para(para)

    modified = etree.tostring(
        root, xml_declaration=True, encoding='UTF-8', standalone=True
    )

    with zipfile.ZipFile(path, 'r') as z_in:
        with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z_out:
            for item in z_in.namelist():
                z_out.writestr(
                    item,
                    modified if item == 'word/document.xml' else z_in.read(item),
                )

    return out, total
