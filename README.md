# Observe Insurance AI Claims Support API

FastAPI-based backend service for an AI-powered voice assistant that handles insurance claims inquiries, provides customer support, and logs post-call interactions.

## Architecture

This API serves as the backend for a VAPI (Voice AI Platform) integration, providing:
- **Claim Status Lookup**: Retrieves claim information based on phone number authentication
- **Interaction Logging**: Records post-call summaries with sentiment analysis and escalation flags
- **VAPI Integration**: Custom middleware to handle VAPI's tool call format

### Tech Stack
- **Framework**: FastAPI (Python 3.9.6)
- **Database**: Google Cloud Firestore (NoSQL)
- **Deployment**: Google Cloud Run
- **Voice AI**: VAPI (Voice AI Platform)
- **Logging**: Google Cloud Logging (via stdout)

---

## Database Schema

### Firestore Collections

#### **claims** Collection
Stores customer claim information indexed by phone number.

```json
{
  "phone": "5551234567",        
  "first_name": "John",
  "last_name": "Doe",
  "claim_status": "approved",      // approved | pending | requires_documentation
  "claim_id": "CLM-2024-001",
  "email": "john.doe@example.com"
}
```


#### **interactions** Collection
Logs all customer interaction summaries from completed calls.

```json
{
  "caller_name": "John Doe",       // "Unknown" if not authenticated
  "phone": "5551234567",           // Optional - may be null
  "summary": "Customer called to check claim status and was satisfied with the information provided.",
  "sentiment": "positive",         // positive | neutral | negative
  "needs_handoff": false,          // true if escalation required
  "timestamp": "2025-11-24T10:30:00Z"
}
```

**Fields:**
- `caller_name` (string, optional): Full name or "Unknown"
- `phone` (string, optional): Caller's phone number
- `summary` (string, required): One neutral sentence describing the interaction
- `sentiment` (string, required): positive/neutral/negative classification
- `needs_handoff` (boolean, default: false): Escalation indicator
- `timestamp` (string, optional): ISO 8601 timestamp

---

## Implementation Details

### VAPI Integration

The API uses custom middleware (`VAPISerializer`) to parse VAPI's tool call format:

**VAPI Request Format:**
```json
{
  "message": {
    "toolCalls": [
      {
        "id": "call_abc123",
        "function": {
          "name": "lookupClaim",
          "arguments": {
            "phone": "5551234567"
          }
        }
      }
    ]
  }
}
```

**VAPI Response Format:**
```json
{
  "results": [
    {
      "toolCallId": "call_abc123",
      "result": {
        // Data here
      }
    }
  ]
}
```

### Middleware Flow

1. **VAPISerializer** (First Layer)
   - Parses `message.toolCalls[0].function.arguments`
   - Extracts `toolCallId` from `message.toolCalls[0].id`
   - Normalizes data and stores in `request.state`
   - Provides helper functions for routes

2. **CORS Middleware** (Second Layer)
   - Handles cross-origin requests
   - Configured for all origins in development

### API Endpoints

#### `GET /`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

#### `POST /claims/lookup`
Lookup claim by phone number.

**VAPI Tool Call:**
```json
{
  "message": {
    "toolCalls": [{
      "id": "call_xyz",
      "function": {
        "name": "lookupClaim",
        "arguments": {
          "phone": "5551234567"
        }
      }
    }]
  }
}
```

**Success Response (200):**
```json
{
  "results": [{
    "toolCallId": "call_xyz",
    "result": {
      "found": true,
      "claim": {
        "phone": "5551234567",
        "first_name": "John",
        "last_name": "Doe",
        "claim_status": "approved",
        "claim_id": "CLM-2024-001",
        "email": "john.doe@example.com"
      }
    }
  }]
}
```

**Not Found Response (200):**
```json
{
  "results": [{
    "toolCallId": "call_xyz",
    "result": {
      "found": false,
      "message": "No claim found for this phone number"
    }
  }]
}
```

#### `POST /interactions/log`
Log post-call interaction summary.

**VAPI Tool Call:**
```json
{
  "message": {
    "toolCalls": [{
      "id": "call_abc",
      "function": {
        "name": "logInteraction",
        "arguments": {
          "caller_name": "John Doe",
          "phone": "5551234567",
          "summary": "Customer inquired about claim status and received confirmation.",
          "sentiment": "positive",
          "needs_handoff": false,
          "timestamp": "2025-11-24T10:30:00Z"
        }
      }
    }]
  }
}
```

**Response (200):**
```json
{
  "results": [{
    "toolCallId": "call_abc",
    "result": {
      "success": true,
      "message": "Interaction logged successfully"
    }
  }]
}
```

---

## Project Structure

```
observe-agent-api/
├── main.py                          # FastAPI app initialization
├── requirements.txt                 # Python dependencies
├── DockerFile                       # Container configuration
├── README.md                        # This file
└── app/
    ├── core/
    │   ├── config.py                # Settings & environment variables
    │   ├── logger.py                # Cloud Logging integration
    │   └── vapi_serializer.py       # VAPI middleware
    ├── models/
    │   ├── claim.py                 # Claim Pydantic models
    │   └── interaction.py           # InteractionLog Pydantic model
    ├── routes/
    │   ├── claims.py                # Claim lookup endpoint
    │   └── interactions.py          # Interaction logging endpoint
    └── services/
        ├── claim_service.py         # Firestore claim repository
        └── interaction_service.py   # Firestore interaction repository
```

---

## Logging & Monitoring

All logs are automatically sent to Google Cloud Logging via stdout/stderr capture.

**Log Levels:**
- `INFO`: Request/response logging, successful operations
- `WARNING`: Missing data, fallback scenarios
- `ERROR`: Exceptions, failed operations

**Example Log Entry:**
```
[INFO] Received VAPI request: {"message": {"toolCalls": [...]}}
[INFO] Parsed VAPI - body: {"phone": "5551234567"}, toolCallId: call_xyz
[INFO] Claim found for phone: 5551234567
```

---

## Testing

Use the included Postman collection:
1. Import `Observe_Insurance_API.postman_collection.json`
2. Set `base_url` variable to the Cloud Run URL
3. Test all three endpoints:
   - Health Check
   - Lookup Claim (VAPI format)
   - Log Interaction (VAPI format)

---

## Assignment Context

This project is part of the Observe.AI Take-Home Assessment for building an AI-powered voice assistant for insurance claims support. The assistant handles:

1. **Greeting & Authentication**: Voice-based caller identification
2. **Claim Status Lookup**: Phone-authenticated claim retrieval
3. **FAQ Support**: Common insurance questions
4. **Escalation**: Human handoff when needed
5. **Call Summary**: Post-call interaction logging

**Key Features Implemented:**
- Phone-based authentication via VAPI
- Real-time claim status retrieval from Firestore
- Post-call sentiment analysis & escalation tracking
- Cloud-native deployment on GCP
- Comprehensive logging for debugging

---

## Author

Chase Moffat
- GitHub: [@Chasem11](https://github.com/Chasem11)
- Cloud Run URL: `https://observe-agent-api-863068629828.us-east1.run.app`
