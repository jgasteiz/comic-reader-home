#!/usr/bin/env bash
celery -A reader.tasks worker --loglevel=info --concurrency=2
