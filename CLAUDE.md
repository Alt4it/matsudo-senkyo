# まつど選挙公報ナビ — Claude Code 向け指示書

松戸市議会議員選挙の**選挙公報**を、全候補者で共通の形式・テーマに整理し、比べやすいWebサイトとして公開する個人プロジェクト。
背景・これまでの検討・決定事項は `docs/HANDOFF.md` を必ず最初に読むこと。

## 最重要ルール（中立性と正確さ）

1. **情報源は選挙公報のみ。** 候補者のSNS・Webサイト・報道・AIの知識など、公報以外の情報を一切加えない。唯一の例外は、五十音順に使う読み（`sort_kana`）で、ユーザーが選管の資料などで確かめて入力する。画面には表示せず、Claudeは自分の知識で埋めない。
2. **原文を改変しない。** `verbatim`（原文）は公報の文字をそのまま写す。誤字があっても直さない。読めない文字は `〓` とし、`issues` に記録する。
3. **要約は原文の言い換えのみ。** 原文にない数値・固有名詞・評価語（「画期的」「現実的でない」など）を足さない。迷ったら要約せず原文だけにする。
4. **評価・推薦・当落予想をしない。** 候補者の比較で優劣を示す表現、並び順による誘導も避ける（サイトの初期表示はシャッフル）。
5. **全候補者を同じ手順・同じ項目で扱う。** 特定の候補者だけ手厚く／薄くしない。
6. **人の最終確認が済んでいない記録は公開しない。** `status: "approved"` の記録だけがサイトに反映される（`scripts/build_data.py` が保証）。
7. 公職選挙法上の注意：サイトの印刷配布、有権者への一斉メール案内をする機能・手順は作らない。

## ディレクトリ構成

```
koho/            公報PDFの置き場（ユーザーが選管サイトから入手して置く。Git管理しない）
work/pages/      PDFをページ画像に変換したもの（scripts/pdf_to_pages.py）
work/assign.json 担当割り当て（どの書き写し担当がどの候補者・ページを扱うか）
work/transcripts/<candidate_id>.json   書き写し担当の出力
work/classify-a/<candidate_id>.json    分類担当Aの出力
work/classify-b/<candidate_id>.json    分類担当Bの出力
work/review/<candidate_id>.md          照合担当の出力（要確認リスト）
data/themes.json        テーマ定義と振り分け基準
data/schema.md          各ファイルのデータ形式
data/records/<candidate_id>.json      人が確認した最終記録（status を持つ）
site/index.html          公開サイト（試作版をベース）
site/data.js             build_data.py が生成。手で編集しない
```

## 作業の流れ（詳細は `.claude/commands/koho-run.md`）

1. 公報PDF → ページ画像化
2. 候補者と担当の割り当て（書き写し担当1体あたり約5人）
3. `koho-transcriber` が原文を書き起こす（並列）
4. `koho-classifier` を **A・Bの2体、互いの結果を見せずに** 実行（並列）
5. `koho-verifier` が原文画像と突き合わせ、誤り・食い違いを `work/review/` にまとめる
6. メインのClaudeが確定案（`data/records/`、`status: "draft"`）を作る
7. **ユーザー（こばやしさん）が原文と照合し、`approved` にする**
8. `python scripts/build_data.py` → `site/data.js` を生成し、ブラウザで確認

## サブエージェント

| 名前 | 役割 | 書き込み先 |
| --- | --- | --- |
| koho-transcriber | 公報画像から原文を書き起こす | work/transcripts/ |
| koho-classifier | 書き起こしにテーマを付ける（A/Bで独立実行） | work/classify-a/, work/classify-b/ |
| koho-verifier | 画像・書き起こし・分類A/Bを突き合わせて問題を列挙 | work/review/ |

サブエージェントには、担当範囲（候補者ID・ページ画像のパス）と出力先を必ず明示して渡す。分類担当には、もう一方の出力ファイルの場所を教えない。

## コーディング方針

- サイトはビルド不要の静的ファイル（HTML + 1つのdata.js）。外部APIへの通信、アクセス解析、Cookieは使わない。
- 日本語UI。スマホで読める幅を優先する。
- アクセシビリティ：候補者名のふりがな表示、文字サイズ、スクリーンリーダーでの読み上げに配慮する。

## ユーザーについて

- 松戸市の有権者。React の経験が少しある。最終的な公開判断はユーザーが行う。
- 会話は日本語で。
