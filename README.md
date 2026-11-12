# まつど選挙公報ナビ

松戸市議選の選挙公報を、共通テーマ・共通形式で比べられるようにする個人プロジェクト。

## はじめかた（Claude Code）

1. このフォルダで Claude Code を起動する（`claude`）。`CLAUDE.md` と `docs/HANDOFF.md` が引き継ぎ資料。
2. 準備：`pip install pymupdf`（Python 3.10 以上）
3. 試運転：過去の公報PDFを `koho/` に置き、Claude Code で `/koho-run koho/<ファイル名>.pdf`
4. 判読不能・食い違いの一覧を見ながら `data/records/*.json` を原文と照合し、問題なければ `review.status` を `"approved"` にする
5. `python scripts/build_data.py` → `site/index.html` をブラウザで開いて確認
   （未確認分も見たいときは `--include-drafts`。公開には使わない）

`site/data.js` は最初は架空のサンプル6人分。

## 構成

- `CLAUDE.md` … Claude Code への指示（中立性ルール、構成、流れ）
- `.claude/agents/` … サブエージェント3種（書き写し・分類・照合）
- `.claude/commands/koho-run.md` … 一連の作業を回すコマンド
- `data/themes.json` … テーマと振り分け基準（仮）
- `data/schema.md` … 各ファイルのデータ形式
- `scripts/` … PDFの画像化、サイト用データの生成
- `site/` … 公開サイト
