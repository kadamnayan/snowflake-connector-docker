#!/bin/bash

# Build script for patched (fixed) version
echo "🔧 Building Patched (Fixed) Version..."

# Check if patched wheel exists
if [ ! -f "snowflake_connector_python-*-patched*.whl" ] && [ ! -f "snowflake_connector_python-*.whl" ]; then
    echo "⚠️  Make sure you have replaced the wheel file with your patched version"
    echo "   Current wheel: $(ls snowflake_connector_python-*.whl 2>/dev/null || echo 'None found')"
fi

echo "📋 Using current wheel file for patched build"

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t snowflake-patched .

if [ $? -eq 0 ]; then
    echo "✅ Successfully built patched container: snowflake-patched"
    echo ""
    echo "To run the container, use:"
    echo "docker run --rm snowflake-patched"
    echo ""
    echo "The PoC will auto-detect if your wheel is actually patched."
else
    echo "❌ Build failed!"
    exit 1
fi
