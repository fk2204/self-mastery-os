# Self-Mastery OS - Mobile API Endpoints

## Overview
Enhanced `server.py` with POST endpoints for React Native mobile app integration. All endpoints support gzip compression and ETag caching for optimal performance on slow networks.

## Features
- **POST Endpoints**: 4 new endpoints for mobile data submission
- **Gzip Compression**: Automatic compression for responses >500 bytes
- **ETag Caching**: HTTP 304 Not Modified support for static data
- **Input Validation**: Type checking and constraint validation on all inputs
- **Security**: Path traversal prevention, content-length limits, sanitized inputs

## Endpoints

### 1. POST /api/checkin/morning
Save morning check-in data.

**Request:**
```json
{
  "sleep_hours": 7.5,
  "energy_level": 8,
  "top_3_priorities": [
    "Sales call with prospect A",
    "Deep work on module refactor",
    "Read 30 min"
  ],
  "win_definition": "10 sales touches and 2hrs focused work"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Morning check-in saved",
  "date": "2026-02-17",
  "data": {
    "timestamp": "2026-02-17T08:30:00",
    "sleep_hours": 7.5,
    "energy_level": 8,
    "top_3_priorities": [...],
    "win_definition": "..."
  }
}
```

**Validation Rules:**
- `sleep_hours`: 0-16, defaults to 0
- `energy_level`: 1-10, defaults to 0 (invalid inputs)
- `top_3_priorities`: Array of strings, max 3 items, 500 chars each
- `win_definition`: String, max 500 characters

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "code": 400,
  "message": "Invalid JSON: ..."
}
```

---

### 2. POST /api/checkin/evening
Save evening reflection data.

**Request:**
```json
{
  "wins": [
    "Closed 2 deals",
    "3.5 hours deep work",
    "Read entire chapter"
  ],
  "challenges": [
    "Lost focus on emails",
    "Missed one follow-up"
  ],
  "deep_work_hours": 3.5,
  "day_score": 8,
  "lessons": "Email batching works. Need to schedule calls earlier."
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Evening reflection saved",
  "date": "2026-02-17",
  "data": {
    "timestamp": "2026-02-17T20:45:00",
    "wins": [...],
    "challenges": [...],
    "deep_work_hours": 3.5,
    "day_score": 8,
    "lessons": "..."
  }
}
```

**Validation Rules:**
- `wins`: Array of strings, max 5 items
- `challenges`: Array of strings, max 5 items
- `deep_work_hours`: 0-24, defaults to 0
- `day_score`: 1-10, defaults to 0 if invalid
- `lessons`: String, max 1000 characters

---

### 3. POST /api/habits/{id}/complete
Mark a habit complete for a specific date.

**Request:**
```json
{
  "date": "2026-02-17"
}
```

Or for today (date is optional):
```json
{}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Habit 'deep_work_90' marked complete",
  "habit_id": "deep_work_90",
  "date": "2026-02-17"
}
```

**Validation Rules:**
- `habit_id`: Alphanumeric + underscore, max 100 characters (checked in path)
- `date`: Optional, format YYYY-MM-DD, defaults to today

**Valid Habit IDs (from habits.json):**
- `morning_routine`
- `deep_work_90`
- `sales_outreach`
- `objection_practice`
- `finance_review`
- `skill_learning`
- `journaling`
- `reading`
- `networking`
- `social_interaction`
- `inbox_zero`
- `no_phone_morning`

**Error Example (404):**
```json
{
  "status": "error",
  "code": 404,
  "message": "Endpoint not found"
}
```

---

### 4. POST /api/journal
Save a journal entry.

**Request:**
```json
{
  "content": "Today was about focused execution. Practiced objection handling with 5 prospects. Key insight: objections early in conversation are often requests for more info.",
  "mood": "energized",
  "tags": ["sales", "learning", "psychology"]
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Journal entry saved",
  "date": "2026-02-17",
  "entry_id": 0
}
```

**Validation Rules:**
- `content`: Required, max 10,000 characters
- `mood`: Optional, max 50 characters
- `tags`: Optional array of strings, max 10 tags, 100 chars each
- Multiple entries per day supported (limit 100 per day)

---

## GET Endpoints (Enhanced)

### GET /api/data
Dashboard data with stats, habits, and profile.

**Response includes ETags and caching headers:**
```
ETag: "a1b2c3d4e5f6g7h8"
Cache-Control: public, max-age=3600
```

**Subsequent request with If-None-Match:**
```
If-None-Match: "a1b2c3d4e5f6g7h8"
Response: 304 Not Modified
```

### GET /api/wisdom
Daily wisdom with ETags support (cached per date).

### GET /data/{filename}.json
Secure file serving with path traversal prevention.

---

## Performance Optimizations

### 1. Gzip Compression
Automatically applied to responses >500 bytes when client sends:
```
Accept-Encoding: gzip
```

**Response headers:**
```
Content-Encoding: gzip
Vary: Accept-Encoding
```

**Size reduction:** Typically 60-80% for JSON data.

### 2. ETag Caching
Static data (wisdom, habits, user profile) includes ETags:
```
ETag: "abc123def456"
Cache-Control: public, max-age=3600
```

Client sends on subsequent requests:
```
If-None-Match: "abc123def456"
Response: 304 Not Modified (no body sent)
```

**Bandwidth saved:** ~95% for cached content.

### 3. Content-Length Validation
Maximum payload: **1MB** (1,048,576 bytes)

Requests exceeding this size return:
```json
{
  "status": "error",
  "code": 413,
  "message": "Payload too large"
}
```

---

## Security Features

### 1. Path Traversal Prevention
Blocks attempts to access files outside `/data` directory:

```
GET /data/../server.py          → 403 Forbidden
GET /data/..%2F..%2Fpasswd      → 403 Forbidden
GET /data/../../etc/passwd      → 403 Forbidden
```

**Validation:**
- Filename sanitized (alphanumeric, hyphen, underscore, dot only)
- `.json` extension required
- Real path verified with `os.path.realpath()`

### 2. Input Validation
All user inputs are validated and constrained:

```
sleep_hours: 7.5 → constrained to [0, 16]
energy_level: 99 → constrained to [1, 10]
win_definition: 5000 chars → truncated to 500 chars
priorities array: 10 items → limited to 3 items
```

### 3. JSON Parsing
Strict JSON validation:

```json
// Invalid JSON returns 400
Invalid input → {"status": "error", "code": 400, "message": "Invalid JSON: ..."}
```

### 4. Type Checking
All fields type-checked before processing:

```python
# Whitelist approach - only safe fields accepted
am_checkin = {
    "timestamp": datetime.now().isoformat(),
    "sleep_hours": self._validate_number(data.get("sleep_hours"), 0, 16),
    ...
}
```

---

## Error Responses

### 400 Bad Request
Invalid input, missing required fields, malformed JSON.

```json
{
  "status": "error",
  "code": 400,
  "message": "Invalid JSON: Expecting value"
}
```

### 403 Forbidden
Path traversal or access denied.

```json
{
  "status": "error",
  "code": 403,
  "message": "Access denied"
}
```

### 404 Not Found
Endpoint not found.

```json
{
  "status": "error",
  "code": 404,
  "message": "Endpoint not found"
}
```

### 413 Payload Too Large
Request body exceeds 1MB.

```json
{
  "status": "error",
  "code": 413,
  "message": "Payload too large"
}
```

### 500 Internal Server Error
Server-side error during processing.

```json
{
  "status": "error",
  "code": 500,
  "message": "Error saving morning check-in: ..."
}
```

---

## Mobile App Integration Examples

### React Native with Fetch API

```javascript
// Morning check-in
const submitMorningCheckin = async (data) => {
  try {
    const response = await fetch('http://localhost:8080/api/checkin/morning', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip'
      },
      body: JSON.stringify(data)
    });

    if (response.status === 304) {
      console.log('Cached data, no update needed');
      return;
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Error:', error);
  }
};

// Complete habit with caching
const completeHabit = async (habitId) => {
  const response = await fetch(
    `http://localhost:8080/api/habits/${habitId}/complete`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip'
      }
    }
  );

  return response.json();
};
```

### Python Requests

```python
import requests
import gzip

# Morning check-in with gzip
response = requests.post(
    'http://localhost:8080/api/checkin/morning',
    json={
        "sleep_hours": 7.5,
        "energy_level": 8,
        "top_3_priorities": ["Task 1", "Task 2", "Task 3"],
        "win_definition": "Hit targets"
    },
    headers={
        'Accept-Encoding': 'gzip'
    }
)

print(response.json())

# Habit completion
response = requests.post(
    'http://localhost:8080/api/habits/deep_work_90/complete',
    json={
        "date": "2026-02-17"
    }
)

print(response.json())
```

---

## Data Storage

All POST data is stored in JSON files:

```
/data/
├── logs/
│   ├── 2026-02-17.json      (morning check-in + evening reflection)
│   ├── 2026-02-16.json
│   └── ...
├── habits.json               (habit completions tracked here)
└── user_profile.json         (user settings)
```

### Log File Structure

```json
{
  "date": "2026-02-17",
  "created_at": "2026-02-17T06:00:00",
  "am_checkin": {
    "timestamp": "2026-02-17T06:00:00",
    "sleep_hours": 7.5,
    "energy_level": 8,
    ...
  },
  "pm_reflection": {
    "timestamp": "2026-02-17T20:30:00",
    "wins": [...],
    "challenges": [...],
    ...
  },
  "journal_entries": [
    {
      "timestamp": "2026-02-17T14:00:00",
      "content": "...",
      "mood": "energized",
      "tags": [...]
    }
  ]
}
```

---

## Testing

Run the included test suite:

```bash
# Terminal 1: Start server
python server.py

# Terminal 2: Run tests
python test_server_endpoints.py
```

**Test Coverage:**
- Morning check-in POST
- Evening reflection POST
- Habit completion POST
- Journal entry POST
- Gzip compression
- ETag caching
- Path traversal prevention
- Input validation

---

## Performance Metrics

On slow mobile networks (3G/4G):

| Feature | Benefit | Savings |
|---------|---------|---------|
| Gzip Compression | Reduce data transfer | 60-80% smaller |
| ETag Caching | Avoid redundant transfers | 95% bandwidth saved (cached) |
| Content-Length Limit | Prevent memory exhaustion | Max 1MB payloads |
| Input Validation | Prevent large entries | Caps on text fields |

**Example:**
- Uncompressed `/api/data`: ~15KB
- Gzip compressed: ~3KB
- With ETag (304): 0KB

---

## Version History

### v2.0 (Current - Feb 2026)
- Added 4 POST endpoints for mobile
- Gzip compression support
- ETag caching headers
- Enhanced security (path traversal prevention)
- Comprehensive input validation
- Error responses as JSON
- Test suite included

### v1.0 (Original)
- GET endpoints only
- No compression
- No caching headers
- Basic file serving
