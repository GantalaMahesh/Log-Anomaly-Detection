# Anomaly Report

## 1. Spike Anomaly
- **type**: Spike Anomaly
- **event**: LOGIN_FAILURE
- **time_range**: 2025-09-12 10:00:05 - 2025-09-12 10:00:06
- **count**: 3
- **details**: 3 occurrences of LOGIN_FAILURE within 2 seconds
- **Explanation**: 3 occurrences of LOGIN_FAILURE within 2 seconds


## 2. Gap Anomaly
- **type**: Gap Anomaly
- **start**: 2025-09-12 10:10:10
- **end**: 2025-09-12 11:30:00
- **duration_minutes**: 79.83333333333333
- **details**: No events for 79.83 minutes between 2025-09-12 10:10:10 and 2025-09-12 11:30:00
- **Explanation**: No events for 79.83 minutes between 2025-09-12 10:10:10 and 2025-09-12 11:30:00


## 3. Gap Anomaly
- **type**: Gap Anomaly
- **start**: 2025-09-12 11:30:00
- **end**: 2025-09-12 23:45:00
- **duration_minutes**: 735.0
- **details**: No events for 735.00 minutes between 2025-09-12 11:30:00 and 2025-09-12 23:45:00
- **Explanation**: No events for 735.00 minutes between 2025-09-12 11:30:00 and 2025-09-12 23:45:00


## 4. Out-of-Hours
- **type**: Out-of-Hours
- **event**: FILE_DELETE
- **time**: 2025-09-12 23:45:00
- **details**: FILE_DELETE at 2025-09-12 23:45:00 is outside business hours (9:00-18:00)
- **Explanation**: FILE_DELETE at 2025-09-12 23:45:00 is outside business hours (9:00-18:00)


## 5. Gap Anomaly
- **type**: Gap Anomaly
- **start**: 2025-09-12 23:46:00
- **end**: 2025-09-13 08:00:00
- **duration_minutes**: 494.0
- **details**: No events for 494.00 minutes between 2025-09-12 23:46:00 and 2025-09-13 08:00:00
- **Explanation**: No events for 494.00 minutes between 2025-09-12 23:46:00 and 2025-09-13 08:00:00


## 6. Out-of-Hours
- **type**: Out-of-Hours
- **event**: LOGIN_SUCCESS
- **time**: 2025-09-12 23:46:00
- **details**: LOGIN_SUCCESS at 2025-09-12 23:46:00 is outside business hours (9:00-18:00)
- **Explanation**: LOGIN_SUCCESS at 2025-09-12 23:46:00 is outside business hours (9:00-18:00)


## 7. Gap Anomaly
- **type**: Gap Anomaly
- **start**: 2025-09-13 08:00:00
- **end**: 2025-09-13 12:00:00
- **duration_minutes**: 240.0
- **details**: No events for 240.00 minutes between 2025-09-13 08:00:00 and 2025-09-13 12:00:00
- **Explanation**: No events for 240.00 minutes between 2025-09-13 08:00:00 and 2025-09-13 12:00:00


## 8. Out-of-Hours
- **type**: Out-of-Hours
- **event**: FILE_UPLOAD
- **time**: 2025-09-13 08:00:00
- **details**: FILE_UPLOAD at 2025-09-13 08:00:00 is outside business hours (9:00-18:00)
- **Explanation**: FILE_UPLOAD at 2025-09-13 08:00:00 is outside business hours (9:00-18:00)


## 9. Gap Anomaly
- **type**: Gap Anomaly
- **start**: 2025-09-13 12:00:00
- **end**: 2025-09-13 14:40:00
- **duration_minutes**: 160.0
- **details**: No events for 160.00 minutes between 2025-09-13 12:00:00 and 2025-09-13 14:40:00
- **Explanation**: No events for 160.00 minutes between 2025-09-13 12:00:00 and 2025-09-13 14:40:00


## 10. Event Order Violation
- **type**: Event Order Violation
- **event**: LOGOUT
- **user**: X
- **time**: 2025-09-13 14:40:00
- **details**: X performed LOGOUT at 2025-09-13 14:40:00 without prior LOGIN_SUCCESS
- **Explanation**: X performed LOGOUT at 2025-09-13 14:40:00 without prior LOGIN_SUCCESS

