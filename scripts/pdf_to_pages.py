"""公報PDFをページごとのPNG画像に変換する。

使い方:  python scripts/pdf_to_pages.py koho/2022-shigikai.pdf [--dpi 200]
出力先:  work/pages/page-01.png, page-02.png, ...
必要:    pip install pymupdf
"""
import argparse
import pathlib
import sys

try:
    import pymupdf
except ImportError:
    sys.exit("PyMuPDF がありません。`pip install pymupdf` を実行してください。")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--dpi", type=int, default=200, help="小さい文字が読めなければ 300 に上げる")
    ap.add_argument("--out", default="work/pages")
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(args.pdf)
    width = max(2, len(str(doc.page_count)))
    for i, page in enumerate(doc, start=1):
        path = out / f"page-{i:0{width}d}.png"
        page.get_pixmap(dpi=args.dpi).save(path)
        print(path)
    print(f"{doc.page_count} ページを {out} に保存しました")


if __name__ == "__main__":
    main()
