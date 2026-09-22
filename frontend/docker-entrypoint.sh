#!/bin/sh
API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000}"
cat > /usr/share/nginx/html/config.js <<CFG
window.__AIDOC_CONFIG__ = { apiBaseUrl: "${API_BASE_URL}" };
CFG
