# Quick Start Deployment Script
# This script helps you prepare for deployment

echo "🚀 GETNOTIFY Deployment Preparation"
echo "===================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env template..."
    cat > .env << EOF
# Supabase Configuration
SUPABASE_URL=https://hfsazlirxtjbarftyoqh.supabase.co
SUPABASE_KEY=your-service-role-key-here

# SendGrid (Optional - for email notifications)
SENDGRID_API_KEY=your-sendgrid-api-key-here
EOF
    echo "✅ Created .env template. Please fill in your values!"
else
    echo "✅ .env file exists"
fi

# Check if requirements.txt has all dependencies
echo ""
echo "Checking dependencies..."
if grep -q "supabase" requirements.txt && grep -q "undetected-chromedriver" requirements.txt; then
    echo "✅ All required dependencies are in requirements.txt"
else
    echo "⚠️  Some dependencies might be missing"
fi

# Check Dockerfile
echo ""
echo "Checking Dockerfile..."
if [ -f dockerfile ]; then
    echo "✅ Dockerfile exists"
else
    echo "⚠️  Dockerfile not found"
fi

# Check if code is ready for production
echo ""
echo "📋 Deployment Checklist:"
echo "  [ ] Code pushed to GitHub"
echo "  [ ] Environment variables configured in deployment platform"
echo "  [ ] Supabase redirect URLs updated"
echo "  [ ] Google OAuth redirect URLs updated"
echo "  [ ] Frontend API URL configured (via meta tag or app.js)"
echo ""
echo "📖 Read DEPLOYMENT_GUIDE.md for detailed instructions"
echo ""
echo "✨ Ready to deploy!"
