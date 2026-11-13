# データ形式

候補者ID（`candidate_id`）は届出順の番号を3桁にしたもの（例：届出1番 → `c001`）。届出順が不明な試運転では公報の掲載順を使う。

## work/assign.json（割り当て）

```json
{
  "election": "2026-matsudo-shigikai",
  "source_pdf": "koho/2026-shigikai.pdf",
  "batches": [
    {"agent": "transcriber-1", "candidates": [
      {"candidate_id": "c001", "pages": ["work/pages/page-01.png"]},
      {"candidate_id": "c002", "pages": ["work/pages/page-01.png"]}
    ]}
  ]
}
```

1ページに複数の候補者が載る場合は、同じ画像を複数の候補者に割り当て、`position`（例：「上段左」）を添える。

## work/transcripts/<candidate_id>.json（書き写し担当の出力）

```json
{
  "candidate_id": "c001",
  "source": {"pdf": "koho/2026-shigikai.pdf", "pages": [1], "position": "上段左"},
  "name": "氏名（公報の表記どおり）",
  "kana": "公報から分かる読み（下記）。分からなければ null",
  "party": "党派（公報の表記どおり。なければ null）",
  "age": 42,
  "career": "議員歴（公報の語句をそのまま。下記。なければ null）",
  "slogan": "スローガン（下記の基準。該当がなければ null）",
  "blocks": [
    {"block_id": "b01", "kind": "policy", "heading": "見出し（なければ null）", "verbatim": "箇条や文を1つ、公報のまま", "page": 1},
    {"block_id": "b02", "kind": "policy", "heading": "同じ見出し", "verbatim": "同じ見出しの次の箇条", "page": 1},
    {"block_id": "b03", "kind": "profile", "heading": null, "verbatim": "経歴などそのまま", "page": 1}
  ],
  "issues": ["読めなかった箇所や判断に迷った点"]
}
```

`kind`：`policy`（政策・公約・実績）／`profile`（経歴・プロフィール）／`message`（政策以外の訴え・決意）／`other`

**ブロックの区切り（`kind: "policy"`）**
- 紙面の箇条1つ、または文1つを1ブロックにする。1つの文の途中では分けない。
- 同じ見出しの下の箇条には、それぞれ同じ `heading` を付ける。`heading` は公報の見出しそのまま。
- 見出しは独立したブロックにしない（配下の箇条にない主張を含む場合も同じ。原文欄に `heading` として表示される）。配下に箇条も文もない見出しだけは、`heading: null` の policy ブロックにする。
- 図の中の文字など、切り離すと意味が通じないまとまりは分けない。
- 過去の実績も `policy` とする。
- 箇条の行頭記号（・●など）は `verbatim` に含めない。

**`name`**：最も大きく書かれた氏名の表記を採る（漢字の併記などは profile ブロックに残す）。

**`age`**：年齢欄がなくても、本人の年齢が本文に数字で書かれていれば採る（例：「25歳の挑戦！」→ 25）。生年月日から計算しない。

**`party`**：党名だけを採る。「市民力代表／公認」のような党名でない表示は入れない。氏名の横に党名がなく、欄内のロゴにだけあるときはロゴから採る。

**`kana`**：氏名のかな部分とふりがなを、氏名の順につなぐ（例：いとう＋えいいち → `いとうえいいち`）。読みが分かるのが姓だけならそこまで（例：`すずき`）。姓の読みが分からなければ `null`。公報にない読みは補わない。

**`career`**：議員歴を示す公報の語句を、そのまま抜き出す（例：`市議3期`、`現職3期`）。「現職」「新人」などに言い換えない。期数を計算しない。元の文は `profile` ブロックにも残す。

**`slogan`**：氏名・党名・見出しを除き、候補者の主張として読める文言のうち最も大きいもの。同じ大きさなら紙面の上にあるものを採る。該当がなければ `null`（サイトでは全員同じ形で「スローガンの記載なし」と表示する）。「実現しました！」「5つの柱」のように内容を束ねる見出しは採らない。政策の箇条の1つや、本文と同程度の大きさの吹き出しも採らない（本文より明らかに大きく掲げられた文言に限る）。

**政策に含めないもの（`kind` を `profile` か `message` にする）**
- 受賞歴、本人の活動や経歴の説明、候補者自身の選挙運動の方法。
- 施策のない現状説明や経過の説明。ただし、同じ見出しの下に施策の文がなく、外すとその主張が消える場合は残す。
- 同じ語句の重複は1回だけ政策にする。スローガンと同じ語句でも、具体的な主張なら政策に残す。

**番号**：箇条の行頭の番号は `verbatim` に含めない。**`party`**：「公認」は含めず党名だけにする（「推薦」は残す）。

## work/classify-a|b/<candidate_id>.json（分類担当の出力）

```json
{
  "candidate_id": "c001",
  "classifier": "A",
  "themes_version": "draft-2",
  "items": [
    {"block_id": "b01", "themes": ["kosodate"], "achievement": false, "summary": "原文の言い換え（40字以内）", "confidence": "high"}
  ],
  "notes": ["分類に迷った理由など"]
}
```

`kind` が `policy` のブロックだけ分類する。`confidence`：`high`／`low`。

テーマの付け方：2つ目のテーマは、本文に明記があるときだけ付ける。公報にない知識や見出しからの推測で足さない。同じ文面は、どの候補者でも同じテーマと要約にする。抽象的な公約（具体的な施策・対象・数値・期限のどれも書かれていないもの）、図の解釈に頼る箇所、項目が多く選ぶと印象が変わる箇所は、要約せず原文だけにする（`summary` は空文字）。サイトは原文を主、要約を従として表示する。

`achievement`：公報が過去の実績として書いているブロックは `true`（例：見出しが「実現しました！」「実績」、文末が「導入！」「削減できました！」）。実績と今後の話が同じ文に混ざる場合は `false` にして `notes` に書く。要約の頭に「実績：」とは書かない（サイトが印を付ける）。

## work/review/<candidate_id>.md（照合担当の出力）

Markdown。見出し「書き写しの問題」「分類の食い違い」「要約の問題」「人に判断してほしいこと」。問題がなければ「問題なし」と書く。

## data/records/<candidate_id>.json（確定記録）

```json
{
  "candidate_id": "c001",
  "order": 1,
  "name": "...", "kana": "...", "sort_kana": null, "party": "...", "career": "市議3期", "age": 42,
  "slogan": "...",
  "policies": [
    {"block_id": "b01", "theme": "kosodate", "achievement": false, "summary": "...", "heading": "...", "verbatim": "...", "page": 1}
  ],
  "review": {
    "status": "draft",
    "checked_by": null,
    "checked_at": null,
    "changes": []
  }
}
```

テーマが2つのブロックは、同じ内容の行をテーマごとに1行ずつ `policies` に持つ。

`sort_kana`：五十音順の並べ替えだけに使う読み。**ユーザーが選管の資料などで確かめて入力する。Claudeは自分の知識で埋めない。** 画面には表示しない。`null` のときは `kana` で並べ、どちらもなければ末尾に置く。

`review.status`：`draft`（Claudeが作成）→ `approved`（ユーザーが原文と照合済み）。公開後に訂正したら `changes` に `{"date": "...", "what": "...", "reason": "..."}` を追記する（訂正履歴としてサイトに表示）。
