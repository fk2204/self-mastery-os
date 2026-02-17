# Quick Start - Mobile API Integration

## 5-Minute Setup

### 1. Verify Server is Running
```bash
cd /home/user/self-mastery-os
python server.py
# Server running at: http://localhost:8080
```

### 2. Test Endpoints (Terminal 2)
```bash
python test_server_endpoints.py
# Should show: Total: 8/8 tests passed
```

### 3. React Native Integration (Copy-Paste Ready)

#### Base Configuration
```javascript
const API_BASE = 'http://localhost:8080'; // Change for production

// Helper function with error handling
const apiCall = async (endpoint, data) => {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Call Failed:', error);
    throw error;
  }
};
```

#### Morning Check-in
```javascript
const saveMorningCheckin = async () => {
  return apiCall('/api/checkin/morning', {
    sleep_hours: 7.5,
    energy_level: 8,
    top_3_priorities: [
      'Hit 10 sales calls',
      '2hr deep work block',
      'Read 30 minutes'
    ],
    win_definition: 'Close 1 deal and stay focused'
  });
};

// Usage
saveMorningCheckin().then(result => {
  console.log('Morning saved:', result);
  // result.status === 'success'
  // result.date === '2026-02-17'
});
```

#### Evening Reflection
```javascript
const saveEveningReflection = async () => {
  return apiCall('/api/checkin/evening', {
    wins: [
      'Closed 2 deals',
      '3.5 hours deep work',
      'Read entire chapter'
    ],
    challenges: [
      'Too many email interruptions',
      'One call cancelled'
    ],
    deep_work_hours: 3.5,
    day_score: 8,
    lessons: 'Batching emails works better. Need earlier call scheduling.'
  });
};
```

#### Complete Habit
```javascript
const completeHabit = async (habitId) => {
  return apiCall(`/api/habits/${habitId}/complete`, {});
};

// Usage
completeHabit('deep_work_90').then(result => {
  console.log('Habit completed:', result.habit_id);
});

// All valid habit IDs:
const HABITS = [
  'morning_routine',
  'deep_work_90',
  'sales_outreach',
  'objection_practice',
  'finance_review',
  'skill_learning',
  'journaling',
  'reading',
  'networking',
  'social_interaction',
  'inbox_zero',
  'no_phone_morning'
];
```

#### Journal Entry
```javascript
const saveJournalEntry = async () => {
  return apiCall('/api/journal', {
    content: 'Long form thoughts about today. What I learned, what went well, what to improve.',
    mood: 'energized',
    tags: ['sales', 'learning', 'psychology']
  });
};
```

#### Fetch with Caching
```javascript
let etag = null;
let cachedData = null;

const getDataWithCache = async () => {
  const headers = {
    'Accept-Encoding': 'gzip'
  };

  if (etag) {
    headers['If-None-Match'] = etag;
  }

  const response = await fetch(`${API_BASE}/api/data`, { headers });

  if (response.status === 304) {
    console.log('Using cached data');
    return cachedData;
  }

  cachedData = await response.json();
  etag = response.headers.get('ETag');

  return cachedData;
};
```

---

## API Endpoints Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /api/checkin/morning | Save morning check-in |
| POST | /api/checkin/evening | Save evening reflection |
| POST | /api/habits/{id}/complete | Mark habit complete |
| POST | /api/journal | Save journal entry |
| GET | /api/data | Get dashboard data |
| GET | /api/wisdom | Get daily wisdom |
| GET | /api/habits | Get habits list |

---

## Request Examples

### cURL - Morning Check-in
```bash
curl -X POST http://localhost:8080/api/checkin/morning \
  -H "Content-Type: application/json" \
  -H "Accept-Encoding: gzip" \
  -d '{
    "sleep_hours": 7.5,
    "energy_level": 8,
    "top_3_priorities": ["Task 1", "Task 2", "Task 3"],
    "win_definition": "Hit targets"
  }'
```

### Python - Complete Habit
```python
import requests

response = requests.post(
    'http://localhost:8080/api/habits/deep_work_90/complete',
    headers={'Accept-Encoding': 'gzip'}
)

print(response.json())
```

### JavaScript - Journal Entry
```javascript
fetch('http://localhost:8080/api/journal', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Accept-Encoding': 'gzip'
  },
  body: JSON.stringify({
    content: 'My journal entry...',
    mood: 'focused',
    tags: ['work', 'learning']
  })
})
.then(r => r.json())
.then(data => console.log(data))
```

---

## Response Format

### Success Response
```json
{
  "status": "success",
  "message": "Morning check-in saved",
  "date": "2026-02-17",
  "data": {
    "timestamp": "2026-02-17T08:30:00",
    ...
  }
}
```

### Error Response
```json
{
  "status": "error",
  "code": 400,
  "message": "Invalid JSON: Expecting value"
}
```

---

## Common HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Data saved successfully |
| 304 | Not Modified | Use cached data (ETag match) |
| 400 | Bad Request | Check input validation |
| 403 | Forbidden | Path traversal blocked |
| 404 | Not Found | Check endpoint URL |
| 413 | Payload Too Large | Request exceeds 1MB |
| 500 | Server Error | Check server logs |

---

## Input Validation Rules

### Morning Check-in
```javascript
{
  sleep_hours: Number,           // 0-16, defaults to 0
  energy_level: Number,          // 1-10, defaults to 0
  top_3_priorities: [String],    // Max 3 items, 500 chars each
  win_definition: String         // Max 500 characters
}
```

### Evening Reflection
```javascript
{
  wins: [String],                // Max 5 items, 500 chars each
  challenges: [String],          // Max 5 items, 500 chars each
  deep_work_hours: Number,       // 0-24, defaults to 0
  day_score: Number,             // 1-10, defaults to 0
  lessons: String                // Max 1000 characters
}
```

### Complete Habit
```javascript
{
  date: String                   // Optional, format: YYYY-MM-DD
  // Defaults to today if not provided
}
```

### Journal Entry
```javascript
{
  content: String,               // Required, max 10,000 chars
  mood: String,                  // Optional, max 50 chars
  tags: [String]                 // Optional, max 10 items
}
```

---

## Performance Tips for Slow Networks

### 1. Enable Compression
Always include the header:
```javascript
headers: { 'Accept-Encoding': 'gzip' }
```
**Result:** 60-80% bandwidth savings

### 2. Use ETag Caching
Send previous ETag to avoid re-downloading:
```javascript
headers: { 'If-None-Match': previousETag }
```
**Result:** 95% bandwidth savings for static data

### 3. Batch Requests
Send multiple habits at once instead of one by one:
```javascript
// Good: Multiple operations in parallel
Promise.all([
  completeHabit('habit1'),
  completeHabit('habit2'),
  completeHabit('habit3')
])

// Avoid: Sequential one at a time
await completeHabit('habit1');
await completeHabit('habit2');
await completeHabit('habit3');
```

### 4. Check Connectivity
```javascript
const isOnline = navigator.onLine;
if (!isOnline) {
  // Store locally and retry when online
  storeLocally(data);
}
```

---

## Troubleshooting

### Connection Refused
```
Error: Could not connect to http://localhost:8080
```
**Solution:** Make sure server is running: `python server.py`

### 400 Bad Request
```json
{"status": "error", "code": 400, "message": "Invalid JSON"}
```
**Solution:** Check JSON syntax. Validate all required fields.

### 413 Payload Too Large
```json
{"status": "error", "code": 413, "message": "Payload too large"}
```
**Solution:** Journal entries max 10,000 chars. Reduce content size.

### Path Not Found (404)
```json
{"status": "error", "code": 404, "message": "Endpoint not found"}
```
**Solution:** Check URL spelling. Valid endpoints:
- `/api/checkin/morning`
- `/api/checkin/evening`
- `/api/habits/{id}/complete`
- `/api/journal`

### Timeout on Slow Network
**Solution:**
1. Increase fetch timeout
2. Check gzip compression is enabled
3. Check ETag caching is working
4. Split large requests

---

## Complete Integration Example

```javascript
import React, { useState } from 'react';
import { Button, TextInput, ScrollView } from 'react-native';

const SelfMasteryApp = () => {
  const [sleepHours, setSleepHours] = useState('7.5');
  const [energyLevel, setEnergyLevel] = useState('8');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const API_BASE = 'http://localhost:8080';

  const apiCall = async (endpoint, data) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept-Encoding': 'gzip'
        },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      setResult(result);
      return result;
    } catch (error) {
      setResult({ status: 'error', message: error.message });
    } finally {
      setLoading(false);
    }
  };

  const submitMorning = () => {
    apiCall('/api/checkin/morning', {
      sleep_hours: parseFloat(sleepHours),
      energy_level: parseInt(energyLevel),
      top_3_priorities: ['Task 1', 'Task 2', 'Task 3'],
      win_definition: 'Hit daily targets'
    });
  };

  return (
    <ScrollView>
      <TextInput
        placeholder="Sleep hours"
        value={sleepHours}
        onChangeText={setSleepHours}
      />
      <TextInput
        placeholder="Energy level"
        value={energyLevel}
        onChangeText={setEnergyLevel}
      />
      <Button
        title={loading ? 'Saving...' : 'Save Morning Check-in'}
        onPress={submitMorning}
        disabled={loading}
      />
      {result && (
        <Text>{JSON.stringify(result, null, 2)}</Text>
      )}
    </ScrollView>
  );
};

export default SelfMasteryApp;
```

---

## Next Steps

1. **Test locally:** Run `python test_server_endpoints.py`
2. **Integrate with mobile app:** Use code examples above
3. **Deploy to production:** Update API_BASE URL
4. **Monitor:** Check server logs for errors
5. **Scale:** Consider database migration for production

---

## Documentation Files

- **API_MOBILE_ENDPOINTS.md** - Complete API reference
- **ENHANCEMENT_SUMMARY.md** - Technical implementation details
- **test_server_endpoints.py** - Test suite
- **server.py** - Implementation

---

## Support

Check server logs for debugging:
```bash
python server.py 2>&1 | tee server.log
```

All errors include descriptive messages in JSON format for easy debugging.
