#!/bin/bash
# Auto-complete deployment after PYTHON_VERSION fix

set -e

echo "============================================================"
echo "JoBika Deployment Auto-Complete Script"
echo "============================================================"
echo ""
echo "This script will:"
echo "  1. Wait for the service to become healthy"
echo "  2. Verify PostgreSQL connection"
echo "  3. Run database migration"
echo "  4. Test the application"
echo ""
echo "Prerequisites:"
echo "  ✓ You have fixed PYTHON_VERSION to '3.10.12' in Render"
echo "  ✓ You have clicked 'Save, rebuild, and deploy'"
echo "  ✓ The deployment shows 'Live' status in Render Events"
echo ""
read -p "Have you completed the above steps? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "❌ Please complete the prerequisites first!"
    echo ""
    echo "Go to: https://dashboard.render.com/web/srv-d4k37pa4d50c73d82he0/env"
    echo "Fix PYTHON_VERSION to: 3.10.12"
    echo "Click: Save, rebuild, and deploy"
    echo ""
    exit 1
fi

echo ""
echo "🔄 Waiting for service to become healthy..."
echo ""

MAX_ATTEMPTS=30
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://jobika-pyt.onrender.com/health || echo "000")
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo "✅ Service is healthy!"
        break
    elif [ "$HTTP_CODE" = "500" ]; then
        echo "⏳ Attempt $((ATTEMPT+1))/$MAX_ATTEMPTS: Service returned 500 (still deploying or old version)..."
    elif [ "$HTTP_CODE" = "000" ]; then
        echo "⏳ Attempt $((ATTEMPT+1))/$MAX_ATTEMPTS: Service not reachable (deploying)..."
    else
        echo "⏳ Attempt $((ATTEMPT+1))/$MAX_ATTEMPTS: HTTP $HTTP_CODE..."
    fi
    
    ATTEMPT=$((ATTEMPT+1))
    sleep 10
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    echo ""
    echo "❌ Service did not become healthy after $MAX_ATTEMPTS attempts"
    echo ""
    echo "Please check:"
    echo "  1. Render Events page for deployment status"
    echo "  2. Render Logs for any errors"
    echo "  3. PYTHON_VERSION is exactly '3.10.12'"
    echo ""
    exit 1
fi

echo ""
echo "🔍 Running comprehensive verification..."
echo ""

python3 verify_and_migrate.py

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "✅ DEPLOYMENT COMPLETE!"
    echo "============================================================"
    echo ""
    echo "🌐 Your application is live at:"
    echo "   https://jobika-pyt.onrender.com"
    echo ""
    echo "📝 Test the application:"
    echo "   1. Register: https://jobika-pyt.onrender.com/auth.html"
    echo "   2. Login with your credentials"
    echo "   3. Upload resume and search for jobs"
    echo ""
    echo "🎉 Congratulations! Your JoBika application is fully deployed!"
    echo ""
else
    echo ""
    echo "❌ Verification failed. Please check the output above for details."
    echo ""
    exit 1
fi
