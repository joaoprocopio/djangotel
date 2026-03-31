1. Service Health Overview
   Executive-level health metrics
   Panel Type Description
   Request Rate Stat Current requests/second
   Error Rate Stat % of requests with HTTP 4xx/5xx
   p50 Latency Stat Median latency in ms
   p95 Latency Stat 95th percentile latency
   Request Rate by Status Code Time series 2xx/4xx/5xx over time
   Latency Percentiles Over Time Time series p50/p90/p95/p99 trends
   Response Time by Status Code Pie chart Duration distribution per status
   Service Summary Table Requests, error rate, avg/p95 latency per service

---

2. HTTP/API Performance
   Endpoint-level performance analysis
   Panel Type Description
   Latency p95 by Endpoint Over Time Time series p95 latency trend per endpoint
   Throughput by Endpoint Over Time Time series Requests/second per endpoint
   Top 20 Endpoints by Request Count Table Volume, errors, latency percentiles
   Slowest Endpoints by p95 Latency Table Top 10 slowest endpoints
   Response Status Code Distribution Pie chart HTTP status breakdown
   Top HTTP Endpoints Pie chart Most trafficked endpoints

---

3. User Activity
   Authenticated user behavior analysis
   Panel Type Description
   Active Users Stat Distinct authenticated users
   Authenticated Traffic % Stat % of requests from logged-in users
   Anonymous Requests Stat Request count from unauthenticated users
   User Error Rate Stat Error rate for authenticated users
   Authenticated vs Anonymous Over Time Time series Traffic split trend
   Top Active Users Table User ID, email, requests, errors, avg duration
   Users with Highest Error Rates Table Users sorted by error %
   Latency for Authenticated Users Time series p50/p95 for logged-in users
   Top Endpoints for Authenticated Users Pie chart Endpoint distribution for auth users

---

4. Errors & Exceptions
   Error tracking and debugging
   Panel Type Description
   Total Errors (Logs) Stat ERROR level log count
   HTTP Errors (4xx/5xx) Stat Span error count
   Server Errors (5xx) Stat 5xx response count
   Warnings Stat WARN level log count
   Error Rate Over Time Time series Errors per request + rate %
   Log Volume by Severity Bar chart ERROR/WARNING/INFO over time
   Top Error Endpoints (HTTP) Table Endpoints with 4xx/5xx responses
   Top Log Errors Table Most frequent ERROR log messages
   Recent Errors (Logs) Table Last 50 ERROR logs with trace ID
   Recent HTTP Errors (Traces) Table Last 50 failed spans with details

---

5. Logs Explorer
   Log exploration and analysis
   Panel Type Description
   Log Volume Over Time Stacked bar chart ERROR/WARNING/INFO/DEBUG trends
   Log Distribution by Level Pie chart Severity breakdown
   Logs by Service Pie chart Log volume per service
   Top Services by Log Volume Bar gauge Top 5 services
   Recent Logs Logs panel Last 100 logs (all levels)
   Recent Error Logs Logs panel Last 100 ERROR logs
   Log Message Patterns Table Grouped log messages by frequency
   Errors/Warnings by Service Table Service × severity breakdown
   Traces with Most Log Errors Table Trace IDs with most error logs
