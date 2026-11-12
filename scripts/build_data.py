"""確認済み（approved）の記録だけを集めて site/data.js を生成する。

使い方:  python scripts/build_data.py [--include-drafts] [--records DIR] [--election FILE]
  --include-drafts : 手元での表示確認用。draft も含め、画面に「未確認」と表示する。公開には使わない。
  --records / --election : 過去の選挙の記録を表示するとき（例：data/archive/2022-11-shigikai/）。

試運転でない（trial: false）公開用のビルドでは、運営者・連絡先・公報PDF・投票案内のURLが
data/election.json にそろっていないと止まる。
"""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--include-drafts", action="store_true")
    ap.add_argument("--records", default="data/records")
    ap.add_argument("--election", default="data/election.json")
    args = ap.parse_args()

    # 選挙名・投票日・試運転の表示などは data/election.json で設定する
    election = json.loads((ROOT / args.election).read_text(encoding="utf-8"))
    if not election.get("trial") and not args.include_drafts:
        missing = [k for k in ("operator", "contact", "sourceUrl", "voteInfoUrl") if not election.get(k)]
        if missing:
            sys.exit(f"{args.election}: 公開に必要な項目が空です: {', '.join(missing)}（手元の確認だけなら --include-drafts）")
    page_offset = election.get("pageOffset", 0)  # PDFの表紙の分だけ紙面のページ番号とずれる
    themes = json.loads((ROOT / "data/themes.json").read_text(encoding="utf-8"))["themes"]
    labels = {t["id"]: t["label"] for t in themes}

    candidates, skipped = [], []
    for path in sorted((ROOT / args.records).glob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        status = rec.get("review", {}).get("status")
        if status != "approved" and not args.include_drafts:
            skipped.append(rec["candidate_id"])
            continue
        policies: dict[str, list] = {}
        for p in rec.get("policies", []):
            label = labels.get(p["theme"])
            if label is None:
                sys.exit(f"{path.name}: 未定義のテーマ {p['theme']!r}")
            policies.setdefault(label, []).append(
                {
                    "s": p.get("summary") or "",
                    "h": p.get("heading") or "",
                    "q": p["verbatim"],
                    "page": p["page"] - page_offset if p.get("page") else None,
                    "achievement": bool(p.get("achievement")),
                }
            )
        candidates.append({
            "id": rec["candidate_id"],
            "order": rec.get("order"),
            "name": rec["name"],
            "kana": rec.get("kana") or "",
            "sortKana": rec.get("sort_kana") or rec.get("kana") or "",
            "party": rec.get("party") or "",
            "career": rec.get("career") or "",
            "age": rec.get("age"),
            "slogan": rec.get("slogan") or "",
            "policies": policies,
            "changes": rec.get("review", {}).get("changes", []),
            "draft": status != "approved",
        })

    data = {
        "election": election,
        "themes": [t["label"] for t in themes],
        "themeCriteria": {t["label"]: t["criteria"] for t in themes},
        "candidates": candidates,
        "preview": args.include_drafts,
    }
    out = ROOT / "site/data.js"
    out.write_text(
        "// scripts/build_data.py が生成。手で編集しない\nwindow.KOHO_DATA = "
        + json.dumps(data, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8",
    )
    print(f"{len(candidates)} 人を {out.relative_to(ROOT)} に書き出しました")
    if skipped:
        print(f"未確認のため除外: {', '.join(skipped)}")


if __name__ == "__main__":
    main()
