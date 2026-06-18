from __future__ import annotations

from pathlib import Path
from typing import Iterable
import re

from PIL import Image, ImageDraw, ImageFilter, ImageFont


REPO_ROOT = Path("/private/tmp/basionmy")
CONTEST_DIR = REPO_ROOT / "oj-contests-17"
OUT_DIR = CONTEST_DIR / "assets" / "learning-posters"
README_PATH = CONTEST_DIR / "README.md"

W, H = 1440, 1800
FONT_REG = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


FONTS = {
    "eyebrow": font(34, True),
    "title": font(88, True),
    "subtitle": font(34),
    "badge": font(28, True),
    "section": font(40, True),
    "body": font(30),
    "small": font(25),
    "tiny": font(21),
    "icon": font(26, True),
}


POSTERS = [
    {
        "letter": "A",
        "title": "密码校验",
        "difficulty": "难度 ★☆☆☆☆",
        "gesp": "GESP 1级",
        "topic": "条件判断",
        "accent": "#3b82f6",
        "background": "/Users/mac01/.codex/generated_images/019edad7-4c40-7623-ba0f-52573e965e80/ig_0af1550a2ccf9023016a33f24ddedc81978953b769b4ab83fe.png",
        "story": "古堡大门只认“左右对称”的四位密码，孩子要学会把数字拆开逐位检查。",
        "summary": "这题把神秘门锁变成清晰规则：先提取千百十个位，再判断两组数字是否对称相等。",
        "real": "理解门禁码、编号、车牌里常见的对称识别规则。",
        "logic": "训练“先拆成部分，再逐条判断”的分析习惯。",
        "code": "整数取位、if 条件判断、T 组输入输出。",
        "parent": "给家长看的总结：题目很短，但它在练孩子最关键的程序思维起点，先拆解对象，再根据条件做判断。",
    },
    {
        "letter": "B",
        "title": "宝藏众数",
        "difficulty": "难度 ★★☆☆☆",
        "gesp": "GESP 2级",
        "topic": "统计与比较",
        "accent": "#f59e0b",
        "background": "/Users/mac01/.codex/generated_images/019edad7-4c40-7623-ba0f-52573e965e80/ig_0af1550a2ccf9023016a33f2ac0c9c819793e6d05d663a7afd.png",
        "story": "古堡宝库里有许多编号宝藏，探险者要找出出现次数最多、最值得优先寻找的一类。",
        "summary": "孩子会从一堆数据里先做“出现次数统计”，再按题目要求处理“次数相同取最小值”的细节规则。",
        "real": "对应投票计票、销售统计、错题高频项分析等真实场景。",
        "logic": "学会先统计，再比较，最后处理并列情况的规则优先级。",
        "code": "计数数组、遍历求最大值、按顺序确定众数。",
        "parent": "给家长看的总结：这类题帮助孩子建立数据观察能力，不只会算，还会从数据中找出最常见的现象。",
    },
    {
        "letter": "C",
        "title": "卷宗整理",
        "difficulty": "难度 ★★★☆☆",
        "gesp": "GESP 3级",
        "topic": "结构体与排序",
        "accent": "#0f766e",
        "background": "/Users/mac01/.codex/generated_images/019edad7-4c40-7623-ba0f-52573e965e80/ig_0af1550a2ccf9023016a33f2ddfa348197acc9075be09699bd.png",
        "story": "古堡图书馆里堆满卷宗，孩子要筛出密级为 A 的资料，并按案件编号整理成清楚目录。",
        "summary": "这题让孩子感受到“信息记录”不是只放在数组里，还能把多个属性打包后筛选、排序、输出。",
        "real": "对应档案整理、学生名单筛选、图书目录排序等管理任务。",
        "logic": "先按条件过滤，再按关键字排序，还要考虑没有结果时输出 none。",
        "code": "结构体存信息、条件筛选、sort 自定义比较。",
        "parent": "给家长看的总结：孩子开始接触“复杂数据管理”，这是从单一变量走向真实项目思维的重要一步。",
    },
    {
        "letter": "D",
        "title": "山峰统计",
        "difficulty": "难度 ★★★★☆",
        "gesp": "GESP 4级",
        "topic": "二维遍历",
        "accent": "#06b6d4",
        "background": "/Users/mac01/.codex/generated_images/019edad7-4c40-7623-ba0f-52573e965e80/ig_0af1550a2ccf9023016a33f32087f8819792088213a946f864.png",
        "story": "古堡地图是一张高度网格，探险者必须逐格比较四周，找出真正高过邻居的山峰。",
        "summary": "孩子会把一张地图拆成一格一格来分析，并理解边界格子和中间格子的判断方式为什么不同。",
        "real": "对应地图高点识别、区域监测、游戏地形分析等问题。",
        "logic": "对每个格子检查上下左右四邻居，严格比较并处理边界。",
        "code": "二维数组、方向数组、嵌套循环、边界判断。",
        "parent": "给家长看的总结：这类题明显提升空间想象和规则执行力，孩子不再只看一个数，而是开始观察局部关系。",
    },
    {
        "letter": "E",
        "title": "大数相减",
        "difficulty": "难度 ★★★★★",
        "gesp": "GESP 5级",
        "topic": "高精度运算",
        "accent": "#8b5cf6",
        "background": "/Users/mac01/.codex/generated_images/019edad7-4c40-7623-ba0f-52573e965e80/ig_0af1550a2ccf9023016a33f35c24088197bcdb5ae2623f9d49.png",
        "story": "古堡宝库记录的是超大数字，普通整数装不下，孩子要像手算一样完成逐位借位减法。",
        "summary": "这题把“计算器做不到”的感觉转成程序步骤：倒着存数字、逐位相减、借位、去前导零。",
        "real": "适合理解金融大额数据、库存统计、科学计数等超长数字处理场景。",
        "logic": "按照从低位到高位的顺序处理，任何一步都不能漏掉借位状态。",
        "code": "字符串转数字数组、高精度减法、借位与结果整理。",
        "parent": "给家长看的总结：高精度题训练的是耐心和步骤意识，孩子会更清楚“复杂问题其实是很多小步骤的组合”。",
    },
    {
        "letter": "F",
        "title": "地下密道",
        "difficulty": "难度 ★★★★★",
        "gesp": "GESP 6级",
        "topic": "BFS 最短路",
        "accent": "#ef4444",
        "background": "/Users/mac01/.codex/generated_images/019edad7-4c40-7623-ba0f-52573e965e80/ig_0af1550a2ccf9023016a33f399c01481978ed15f43695ae670.png",
        "story": "古堡地下密室彼此连通，探险者要从 1 号密室出发，用最少步数找到终点房间。",
        "summary": "孩子会第一次真正理解“最短路径”不是猜出来的，而是用一层一层扩展的方法稳定找出来。",
        "real": "对应导航寻路、地铁换乘、校园路线规划、游戏关卡探索。",
        "logic": "按层搜索能保证第一次到达就是最短，并能清楚判断是否不可达。",
        "code": "邻接表建图、队列 BFS、dist 距离数组。",
        "parent": "给家长看的总结：这是很经典的算法入门题，孩子会开始理解‘搜索策略’如何决定效率和正确性。",
    },
]


def rgb(hex_value: str) -> tuple[int, int, int]:
    hex_value = hex_value.lstrip("#")
    return tuple(int(hex_value[i : i + 2], 16) for i in (0, 2, 4))


def measure(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill, outline=None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        current = ""
        for ch in paragraph:
            trial = current + ch
            if measure(draw, trial, fnt)[0] <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = ch
        if current:
            lines.append(current)
        elif paragraph == "":
            lines.append("")
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill,
    max_width: int,
    line_gap: int = 10,
) -> int:
    x, y = xy
    for line in wrap_text(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += measure(draw, line or "一", fnt)[1] + line_gap
    return y


def crop_background(path: Path) -> Image.Image:
    src = Image.open(path).convert("RGB")
    scale = max(W / src.width, H / src.height)
    resized = src.resize((int(src.width * scale), int(src.height * scale)), Image.LANCZOS)
    left = max(0, (resized.width - W) // 2)
    top = max(0, (resized.height - H) // 2)
    return resized.crop((left, top, left + W, top + H)).convert("RGBA")


def apply_overlays(base: Image.Image) -> Image.Image:
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rectangle((0, 0, W, 450), fill=(5, 10, 24, 132))
    d.rounded_rectangle((50, 960, 1390, 1735), radius=56, fill=(250, 250, 248, 245), outline=(229, 231, 235, 255), width=2)
    d.ellipse((1080, -80, 1480, 320), fill=(255, 255, 255, 18))
    d.ellipse((-80, 1340, 220, 1640), fill=(255, 255, 255, 22))
    return Image.alpha_composite(base, overlay.filter(ImageFilter.GaussianBlur(0)))


def draw_badges(draw: ImageDraw.ImageDraw, item: dict[str, str]) -> None:
    x = 88
    labels = [
        (item["difficulty"], rgb(item["accent"]), (255, 255, 255, 255)),
        (item["gesp"], (15, 23, 42), (255, 255, 255, 255)),
        (item["topic"], (255, 255, 255), (15, 23, 42, 255)),
    ]
    for text, fill, fg in labels:
        tw, th = measure(draw, text, FONTS["badge"])
        rounded(draw, (x, 322, x + tw + 42, 378), 26, (*fill, 236) if len(fill) == 3 else fill)
        draw.text((x + 21, 336), text, font=FONTS["badge"], fill=fg)
        x += tw + 58


def draw_cards(draw: ImageDraw.ImageDraw, item: dict[str, str]) -> None:
    cards = [
        ("现实意义", item["real"], "#0f766e"),
        ("逻辑思维", item["logic"], "#4f46e5"),
        ("编程知识点", item["code"], "#be123c"),
    ]
    x = 110
    for title, body, color in cards:
        rounded(draw, (x, 1292, x + 388, 1602), 34, (255, 255, 255, 255), outline=(224, 229, 236, 255), width=2)
        draw.ellipse((x + 30, 1325, x + 88, 1383), fill=rgb(color))
        draw.text((x + 59, 1336), title[0], font=FONTS["icon"], fill=(255, 255, 255, 255), anchor="ma")
        draw.text((x + 106, 1327), title, font=FONTS["badge"], fill=(17, 24, 39, 255))
        draw_wrapped(draw, (x + 30, 1410), body, FONTS["small"], (71, 85, 105, 255), 328, 9)
        x += 416


def poster_filename(item: dict[str, str]) -> str:
    return f"周赛17-{item['letter']}-{item['title']}-学习价值海报.png"


def render_poster(item: dict[str, str]) -> Path:
    poster = crop_background(Path(item["background"]))
    poster = apply_overlays(poster)
    draw = ImageDraw.Draw(poster)

    white = (255, 255, 255, 255)
    navy = (15, 23, 42, 255)
    slate = (51, 65, 85, 255)

    draw.text((88, 74), f"周赛17 · {item['letter']}题", font=FONTS["eyebrow"], fill=(223, 235, 255, 255))
    draw.text((88, 128), item["title"], font=FONTS["title"], fill=white)
    draw_wrapped(draw, (92, 244), item["story"], FONTS["subtitle"], (235, 241, 255, 246), 1160, 8)
    draw_badges(draw, item)

    draw.text((110, 1036), "故事背景", font=FONTS["section"], fill=navy)
    draw_wrapped(draw, (110, 1092), item["summary"], FONTS["body"], slate, 1180, 10)
    draw_cards(draw, item)

    draw.line((110, 1628, 1330, 1628), fill=(222, 226, 232, 255), width=2)
    draw.text((110, 1655), "给家长看的总结", font=FONTS["badge"], fill=navy)
    draw_wrapped(draw, (110, 1700), item["parent"], FONTS["small"], (100, 116, 139, 255), 1210, 8)

    out_path = OUT_DIR / poster_filename(item)
    poster.convert("RGB").save(out_path, "PNG")
    return out_path


def update_readme(files: Iterable[Path]) -> None:
    text = README_PATH.read_text(encoding="utf-8").rstrip() + "\n"
    section = ["## 学习价值海报", ""]
    for file in files:
        rel = file.relative_to(CONTEST_DIR).as_posix()
        section.append(f"- [{file.name}](./{rel})")
    section_text = "\n".join(section).rstrip() + "\n"

    pattern = re.compile(r"\n## 学习价值海报\n.*\Z", re.S)
    if pattern.search(text):
        text = pattern.sub("\n" + section_text, text)
    else:
        text = text + "\n" + section_text
    README_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = [render_poster(item) for item in POSTERS]
    update_readme(outputs)
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
