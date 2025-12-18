from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import requests, uuid, os

prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)


def clamp_text(text, max_chars):
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "…"


def create_slide(prs, slide_data):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0),
        prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(3, 7, 18)
    bg.line.fill.background()
    slide.shapes._spTree.remove(bg._element)
    slide.shapes._spTree.insert(2, bg._element)

    for x, y, size, color, t in [
        (-3, -3, 10, RGBColor(17, 24, 39), 0.5),
        (5, -2, 8, RGBColor(30, 41, 59), 0.6),
        (3, 4, 9, RGBColor(15, 23, 42), 0.7),
    ]:
        orb = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(x), Inches(y),
            Inches(size), Inches(size)
        )
        orb.fill.solid()
        orb.fill.fore_color.rgb = color
        orb.fill.transparency = t
        orb.line.fill.background()

    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.8),
        Inches(9), Inches(1.0)
    )
    tf = title_box.text_frame
    tf.clear()
    title = tf.paragraphs[0]
    title.text = slide_data["title"].upper()
    title.font.size = Pt(40)
    title.font.bold = True
    title.font.color.rgb = RGBColor(255, 255, 255)
    title.alignment = PP_ALIGN.LEFT

    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.5), Inches(1.85),
        Inches(3.5), Pt(4)
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = RGBColor(96, 165, 250)
    accent.line.fill.background()

    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.35), Inches(2.3),
        Inches(5.7), Inches(5.2)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(15, 23, 42)
    card.fill.transparency = 0.35
    card.line.fill.background()

    content_box = slide.shapes.add_textbox(
        Inches(0.7), Inches(2.6),
        Inches(5.0), Inches(4.8)
    )
    tf = content_box.text_frame
    tf.word_wrap = True
    tf.clear()

    points = slide_data["points"][:4]
    explanations = slide_data["explanation"][:4]

    if len(points) <= 3:
        point_size = Pt(26)
        exp_size = Pt(16)
        exp_spacing = Pt(10)
    else:
        point_size = Pt(21)
        exp_size = Pt(13)
        exp_spacing = Pt(6)

    for i, point in enumerate(points):
        bullet = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        bullet.text = "◆ " + clamp_text(point, 60)
        bullet.font.size = point_size
        bullet.font.bold = True
        bullet.font.color.rgb = RGBColor(255, 255, 255)
        bullet.space_after = Pt(3)

        exp = tf.add_paragraph()
        exp.text = clamp_text(explanations[i], 120)
        exp.font.size = exp_size
        exp.font.color.rgb = RGBColor(203, 213, 225)
        exp.line_spacing = 1.15
        exp.space_after = exp_spacing

    frame = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.15), Inches(2.25),
        Inches(3.6), Inches(4.9)
    )
    frame.fill.solid()
    frame.fill.fore_color.rgb = RGBColor(10, 15, 30)
    frame.line.color.rgb = RGBColor(96, 165, 250)
    frame.line.width = Pt(2)

    img_bytes = requests.get(slide_data["image"]).content
    img_path = f"{uuid.uuid4()}.jpg"
    with open(img_path, "wb") as f:
        f.write(img_bytes)

    slide.shapes.add_picture(
        img_path,
        Inches(6.25), Inches(2.35),
        width=Inches(3.4),
        height=Inches(4.7)
    )
    os.remove(img_path)






