#!/usr/bin/env bash

PORT="${PORT:-13456}"
HOST="${HOST:-0.0.0.0}"
uvicorn main:app --host "$HOST" --port "$PORT" --forwarded-allow-ips '*'
