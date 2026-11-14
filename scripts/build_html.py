# -*- coding: utf-8 -*-
"""把《六祖坛经·自性五句与风幡公案（存疑稿）》编译成单文件 HTML。
用法：python3 scripts/build_html.py    （需 pandoc）
输入：book/润泽说 道可道之六祖坛经·自性五句与风幡公案（存疑稿）.md
输出：book/坛经·存疑稿·阅读版.html
"""
import pathlib, re, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import daokedao_book as kit

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOK = ROOT / "book"
MD = BOOK / "润泽说 道可道之六祖坛经·自性五句与风幡公案（重校本）.md"
OUT = BOOK / "坛经·阅读版.html"
TMP = pathlib.Path("/tmp/liuzu_src.md")
BODY_TMP = pathlib.Path("/tmp/liuzu_body.html")

src = MD.read_text(encoding="utf-8")
src = re.sub(r"^---\n.*?\n---\n", "", src, count=1, flags=re.S)
src = src.replace("# 润泽说 道可道之六祖坛经\n## 自性五句与风幡公案（重校本）\n", "")

TMP.write_text(src, encoding="utf-8")

subprocess.run(["pandoc", str(TMP), "-f", "markdown+hard_line_breaks",
                "-t", "html5", "--no-highlight", "-o", str(BODY_TMP)], check=True)
body = BODY_TMP.read_text(encoding="utf-8")
body = re.sub(r"<h([234])\s*\n\s*", r"<h\1 ", body)

heads = re.findall(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', body, flags=re.S)
nav = "\n".join('<li class="wide"><a href="#%s"><i>·</i><span>%s</span></a></li>'
                % (hid, re.sub(r"<[^>]+>", "", raw).strip())
                for hid, raw in heads)
body = body.replace("<blockquote>", '<blockquote class="sutra">')
body = body.replace("<table>", '<table class="t">')
body = body.replace("<!-- FIG:fengfan -->", kit.fig_svg(BOOK/"figures/图2-风幡阴阳太和.svg", "风幡阴阳太和", "幡为阴、风为阳、心为涵摄阴阳之太和；此心非心，故名此心。"))

FAVICON = ("<link rel=\"icon\" type=\"image/svg+xml\" href=\"data:image/svg+xml,"
           "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Crect width='64' height='64' fill='%237C6D5C'/%3E"
           "%3Ctext x='32' y='46' font-size='30' text-anchor='middle' "
           "fill='%23F7F4EE' font-family='serif'%3E%E8%97%E4%3C/text%3E%3C/svg%3E\">")

SHELL = pathlib.Path(__file__).parent.joinpath("_shell.html").read_text(encoding="utf-8")
SHELL = SHELL.replace("__KIT_CSS__", kit.COVER_CSS + kit.FIG_CSS).replace("__KIT_MQ__", kit.COVER_MQ)
out = (SHELL.replace("__NAV__", nav).replace("__BODY__", body)
       .replace("__FAVICON__", FAVICON))
OUT.write_text(out, encoding="utf-8")
print("ok", len(out), "chars |", len(heads), "toc items |", OUT)
