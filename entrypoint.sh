#!/bin/bash

chmod +x backend/wait_for_postgres.sh
./backend/wait_for_postgres.sh
alembic upgrade head || exit 1
exec uvicorn backend.main:app --host 0.0.0.0 --port 8000

# for future me, make this executable - chmod +x entrypoint.sh
