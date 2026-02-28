# FM Cloud Monorepo (Portfolio)

受託開発会社向けの採用ポートフォリオとして、要件定義・設計・実装の最小動作例をまとめたモノレポです。

## セットアップ

### 前提
- Docker / Docker Compose
- (ローカル実行時) Python 3.11+, Node 20+

### 起動
```bash
cd app
make up
```

- Backend: http://localhost:8000/docs
- Frontend: http://localhost:3000

### テスト
```bash
cd app
make test
```

### Lint
```bash
cd app
make lint
```

## 構成
- `docs/`: 要件・設計・意思決定記録
- `app/backend`: FastAPI + SQLAlchemy + Alembic + pytest
- `app/frontend`: Next.js + TypeScript の最小CRUD
- `legacy-reading`: レガシー読解・安全改修サンプル

## 認可モデル（最小）
Backend APIは `X-Role` ヘッダーにより簡易RBACを行います。
- `admin`, `fm_manager`: 書き込み可
- `engineer`, `viewer`: 読み取りのみ
