up:
	docker compose up --build

test:
	cd backend && pytest
	cd .. && python -m pytest legacy-reading/test_legacy.py

lint:
	cd backend && python -m compileall app
	cd frontend && npm install && npm run lint
