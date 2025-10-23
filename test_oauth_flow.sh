#!/bin/bash

echo "🧪 Testing OAuth Flow"
echo "===================="
echo "" echo "Step 0: Testing server mcp endpoint..."
curl -i http://localhost:8000/mcp
echo " it will tell you are not authorized to access the resource"
echo " It will give your the resource_metadata where to authenticate"
echo "Step 1: connect to the resource_metadata""
curl -s http://localhost:8000/.well-known/oauth-protected-resource | jq
echo "Step 2: Testing OAuth authorization server..."
curl -s http://localhost:8000/.well-known/oauth-authorization-server | jq'
echo ""

