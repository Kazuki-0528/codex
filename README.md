# FM Cloud Monorepo (Portfolio)

## 3行要約（何を作ったか）
- FM向けに、**BIM(ifcXML)取り込み → 部屋/外皮要素の保存 → 月次CO2簡易推計**までを動かせる最小システムを作成。
- Backend（FastAPI）/ Frontend（Next.js）/ DB（PostgreSQL）を Docker Compose で一括起動可能。
- 仕様推測と安全改修の力を示すため、`legacy-reading/` に「読解メモ + 振る舞い固定テスト + 段階的リファクタ」を同梱。

## デモ手順（5分）
1. 起動
   ```bash
   cd app
   docker compose up --build
   ```
2. 画面確認
   - Frontend: http://localhost:3000
   - Backend API Docs: http://localhost:8000/docs
3. ログイン相当（簡易RBAC）
   - 本デモは `X-Role` ヘッダーで権限制御（`admin` / `fm_manager` / `engineer` / `viewer`）。
   - Swagger UI の `Try it out` で Header を付与して操作。
4. ifcXML取り込み
   - `POST /import/ifcxml` に `tests/fixtures/minimal_ifc.xml` を multipart で送信。
   - `IfcSpace / IfcWallStandardCase / IfcWindow` を抽出してDB保存。
5. CO2推計
   - 取り込みレスポンスの `building_id` を使って
     `GET /api/v1/co2/monthly?building_id=<id>&working_days_per_month=22` を実行。
   - 部屋別・建物合計の月次推計（kg-CO2）を確認。

## 設計上の見どころ（3点）
1. **純粋関数分離**
   - ifcXMLパースとCO2推計ロジックをI/Oから分離し、単体テストしやすく設計。
2. **壊れにくい改修フロー**
   - `legacy-reading/` で、先に振る舞い固定テストを書いてから段階的に改善する手順を明示。
3. **最小でも説明可能なアーキテクチャ**
   - API/DB/フロント/CIを最小構成で通し、実装意図を `docs/` とADRで追跡可能。

## テスト / CI の見どころ
- Backend: APIテスト（CRUD / ifcXML取り込み / CO2推計）
- Unit: CO2推計の純粋関数テスト（`tests/unit`）
- Legacy: before/after の互換テスト（戻り値 + 副作用）
- CI（GitHub Actions）で backend tests / legacy tests / frontend lint を自動実行

## AI活用の方針
- AIは**下書き・叩き台・テストケース候補**の生成に利用。
- 仕様解釈、設計判断（ADR）、レビュー、最終コミット判断は人が実施。
- 「丸投げ」ではなく、差分レビューと再現テストを前提に運用。

## 今後の拡張案
- 実認証（OIDC等）とマルチテナント厳格化（Row Level Security含む）
- CO2推計の高精度化（用途係数の外部管理、季節/設備効率/実測値反映）
- 非同期ジョブ化（大容量ifcXML、再実行、監査トレース強化）
