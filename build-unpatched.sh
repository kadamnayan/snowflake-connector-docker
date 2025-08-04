#!/bin/bash

# Build script for unpatched (vulnerable) version
echo "🔧 Building Unpatched (Vulnerable) Version..."

# Check if unpatched wheel exists
if [ ! -f "snowflake_connector_python-*-unpatched*.whl" ] && [ ! -f "snowflake_connector_python-*.whl" ]; then
    echo "⚠️  Make sure you have replaced the wheel file with your unpatched version"
    echo "   Current wheel: $(ls snowflake_connector_python-*.whl 2>/dev/null || echo 'None found')"
fi

echo "📋 Using current wheel file for unpatched build"

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t snowflake-unpatched .

if [ $? -eq 0 ]; then
    echo "✅ Successfully built unpatched container: snowflake-unpatched"
    echo ""
    echo "To run the container, use:"
    echo "docker run --rm snowflake-unpatched"
    echo ""
    echo "The PoC will auto-detect if your wheel is actually vulnerable."
else
    echo "❌ Build failed!"
    exit 1
fi
