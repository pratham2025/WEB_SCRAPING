#!/bin/bash
echo "Starting GETNOTIFY API Server for Network Access..."
echo ""
echo "Server will be accessible at:"
echo "  - http://localhost:8000 (on this computer)"
echo "  - http://192.168.0.197:8000 (from mobile devices on same network)"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
uvicorn scraper_api:app --reload --host 0.0.0.0 --port 8000

