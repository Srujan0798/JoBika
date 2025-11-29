#!/bin/bash

# Daily Job Scraping Cron Job
# Add to crontab: 0 9 * * * /path/to/daily_scrape.sh

cd "$(dirname "$0")/.."

echo "======================================"
echo "JoBika Daily Job Scraping"
echo "Started: $(date)"
echo "======================================"

# Run scraper
node services/SimpleJobScraper.js

echo "======================================"
echo "Completed: $(date)"
echo "======================================"
