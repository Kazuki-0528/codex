# Decisions (ADR-lite)

## 1. FastAPI採用
- 理由: 型ヒント/バリデーション/OpenAPI自動生成で説明しやすい。
- トレードオフ: 大規模化時の設計規律が必要。

## 2. SQLAlchemy + Alembic採用
- 理由: モデルとマイグレーションをコードで管理しやすい。
- トレードオフ: ORMの学習コスト。

## 3. Next.jsで最小CRUD
- 理由: TypeScriptで型を保ったUI実装が可能。
- トレードオフ: Node依存が増える。
