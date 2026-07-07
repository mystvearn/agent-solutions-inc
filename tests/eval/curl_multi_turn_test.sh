#!/bin/bash
# Multi-turn evaluation using CURL to measure system performance

SERVER_URL="http://localhost:8001"
USER_ID="curl_eval_user"
APP_NAME="app"

echo "Creating session..."
SESSION_RESPONSE=$(curl -s -X POST "$SERVER_URL/apps/$APP_NAME/users/$USER_ID/sessions" \
    -H "Content-Type: application/json" \
    -d '{}')

SESSION_ID=$(echo "$SESSION_RESPONSE" | jq -r '.id')
if [ -z "$SESSION_ID" ] || [ "$SESSION_ID" == "null" ]; then
    echo "Failed to create session. Response: $SESSION_RESPONSE"
    exit 1
fi

function send_message() {
    local turn=$1
    local query=$2
    
    echo "========================================================="
    echo "Turn $turn"
    echo "User Query: $query"
    echo "---------------------------------------------------------"
    
    # Construct the JSON payload
    local payload=$(cat <<EOF
{
    "appName": "$APP_NAME",
    "userId": "$USER_ID",
    "sessionId": "$SESSION_ID",
    "newMessage": {
        "role": "user",
        "parts": [{"text": "$query"}]
    }
}
EOF
)

    # Track time and send request
    start_time=$(date +%s)
    response=$(curl -s -X POST "$SERVER_URL/run" \
        -H "Content-Type: application/json" \
        -d "$payload")
    end_time=$(date +%s)
    
    elapsed=$((end_time - start_time))
    
    # Parse the agent's response from the ADK Event output format using jq
    # We look for events with content.parts and extract text
    agent_text=$(echo "$response" | jq -r '.[]? | select(.content != null and .content.parts != null) | .content.parts[0].text // empty' | tail -n 1)
    
    if [ -z "$agent_text" ] || [ "$agent_text" == "null" ]; then
       # Maybe the agent returned an output dictionary (like status: wait)
       agent_text=$(echo "$response" | jq -r '.[]? | select(.output != null) | .output | to_entries | map("\(.key): \(.value)") | join(", ")')
    fi
    
    echo "Agent Response:"
    echo "$agent_text"
    echo "---------------------------------------------------------"
    echo "Time taken: ${elapsed}s"
    echo "========================================================="
    echo ""
}

echo "Starting Multi-turn CURL Evaluation..."
echo "Using Session ID: $SESSION_ID"
echo ""

# Turn 1
send_message 1 "I am a new retail startup with no existing processes. I want to build an AI agent for customer support."

# Turn 2
send_message 2 "Yes, the goal is to resolve customer complaints instantly and save money on hiring support staff. We use Zendesk."
