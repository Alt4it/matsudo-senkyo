---
description: 選挙公報PDFを書き起こし・分類・照合し、確認用の下書き記録を作る
argument-hint: <公報PDFのパス（例：koho/2022-shigikai.pdf）>
---

選挙公報 `$ARGUMENTS` を処理する。CLAUDE.md の最重要ルールに従うこと。

1. **ページ画像化**：`python scripts/pdf_to_pages.py $ARGUMENTS` を実行し、`work/pages/` を確認する。
2. **候補者の特定と割り当て**：ページ画像を順に開き、候補者ごとの掲載ページ・位置を把握して `work/assign.json` を作る（`data/schema.md` の形式）。書き写し担当1体あたり約5人に分ける。候補者の総数をユーザーに報告する。
3. **書き写し**：`koho-transcriber` をバッチごとに並列で起動する。各サブエージェントには担当の候補者ID・ページ画像・位置・出力先を明示する。
4. **分類**：全候補の書き起こしがそろったら、`koho-classifier` を A 用と B 用に分けて起動する（それぞれ複数体に分けてよい）。A 用には出力先 `work/classify-a/`、B 用には `work/classify-b/` を渡し、もう一方の出力先は伝えない。
5. **照合**：`koho-verifier` を起動する（1体あたり約5人）。
6. **下書き記録の作成**：照合結果を踏まえて `data/records/<id>.json` を `review.status: "draft"` で作る。照合担当が指摘した書き写しの誤りは、**画像で確認できたものだけ**直す。分類の食い違いは基準に照らして仮決めし、仮決めした箇所を一覧にする。
7. **ユーザーへの報告**：次をまとめて提示し、ここで止まる（自分で approved にしない）。
   - 処理した候補者数、問題が多い候補者
   - 判読不能・人の判断が必要な箇所の一覧（候補者ID・ブロック・画像パス付き）
   - 分類を仮決めした箇所の一覧
   - 五十音順の読み（`sort_kana`）の入力が必要な候補者の一覧（Claudeは埋めない）
8. `data/election.json`（選挙名・投票日・試運転の表示・順番の呼び名・PDFと紙面のページ差）がこの公報に合っているか確認する。本番では `trial` を false、`orderLabel` を「届出」にする。公開用のビルドは、`operator`・`contact`・`sourceUrl`・`voteInfoUrl` が空だと止まる（手元の確認は `--include-drafts`）。前回の選挙の記録は `data/archive/<選挙名>/` に移してから始める。ユーザーが確認して approved にしたら、`python scripts/build_data.py` を実行して `site/data.js` を作り、サイトをブラウザで確認する。
