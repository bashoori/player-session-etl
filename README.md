# Player Session ETL Pipeline

Gaming analytics platform: extract raw player session data, transform into behavioral insights, and generate real-time dashboards for game studios.

## Overview

Game studios generate massive amounts of session data—login, gameplay events, item purchases, quest completions. Without structure, it's noise. With structure, it answers: Which levels are frustrating? Where do players quit? What drives engagement?

**Key Topics**
- Session-based data aggregation
- Player behavior analysis
- Real-time pipeline (Airflow)
- Gaming metrics (engagement, retention, monetization)
- Player segmentation and cohort analysis

## Problem It Solves

A game studio collects:
- **Session events** (login, logout, timestamp, duration)
- **In-game actions** (level completed, item purchased, quest started)
- **Player profiles** (account age, country, device)

**Questions they ask:**
- Which levels have the highest abandonment rate?
- Are new players more likely to quit after level 3?
- What's the LTV (lifetime value) by player cohort?
- Are players engaging more/less over time?

**Before this pipeline:** Manual SQL queries, inconsistent metrics, no dashboards.  
**After:** Automated daily updates, consistent definitions, real-time insights.

## Architecture

### Data Ingestion
- Game client sends events to backend (login, action, logout)
- Events stored in raw logs or event streaming platform
- Timestamp every event for replay/validation

### Transformation (Airflow DAG)
1. **Extract sessions** — group events by player + session window
2. **Calculate metrics** — session duration, actions per session, monetization
3. **Segment players** — cohort by registration date, behavior patterns
4. **Aggregate dashboards** — daily/weekly summaries

### Output
- **Session facts** — one row per session (duration, actions, revenue)
- **Player summaries** — one row per player (LTV, engagement score, churn risk)
- **Daily dashboards** — top metrics, trends, anomalies

## Key Metrics

### Engagement
- **Session length** — how long do players play per session?
- **Actions per session** — how active are they?
- **Session frequency** — how often do they return?

### Retention
- **D1, D7, D30 retention** — % returning after 1, 7, 30 days
- **Churn rate** — % who never return
- **Cohort retention** — compare retention by signup date

### Monetization
- **ARPU** (Average Revenue Per User) — revenue ÷ active players
- **ARPPU** (Average Revenue Per Paying User) — revenue ÷ paying players
- **LTV** (Lifetime Value) — total revenue per player

### Game Design
- **Level abandonment** — % quitting at each level
- **Quest completion rate** — % finishing quests
- **Feature adoption** — % using new features

## Project Structure

```
player-session-etl/
├── airflow/
│   └── dags/
│       └── player_analytics_dag.py
├── sql/
│   ├── session_facts.sql
│   ├── player_summaries.sql
│   └── engagement_metrics.sql
├── src/
│   ├── extract_sessions.py
│   ├── calculate_metrics.py
│   └── aggregate_dashboards.py
├── data/
│   └── sample_events.csv
├── requirements.txt
└── README.md
```

## Enhanced Features

### 1. Session Reconstruction
Raw events → complete sessions with:
- Session ID (player + timestamp window)
- Duration (logout timestamp - login timestamp)
- Actions (count of events)
- Monetization (in-session purchases)

### 2. Behavioral Segmentation
Players categorized by engagement + spending:
- **Whales**: high spending, high engagement
- **Engaged free-to-play**: high engagement, no spending
- **Casual**: low engagement, any spending
- **At-risk**: no recent sessions, used to be active

### 3. Cohort Analysis
Compare players by signup cohort:
- Week 1 retention by signup week
- LTV progression over time
- Feature adoption curves

### 4. Real-time Alerting
Monitor for anomalies:
- Sudden drop in session length (game crash? bug?)
- Churn rate spike (new patch broke something?)
- Revenue drop (payment processing issue?)

### 5. Player Journey Mapping
Track individual players through:
- Tutorial completion
- First purchase (if any)
- Level progression
- Churn point

## Running It

### Local
```bash
pip install -r requirements.txt
python src/extract_sessions.py --date 2026-05-20
python src/calculate_metrics.py --date 2026-05-20
python src/aggregate_dashboards.py --date 2026-05-20
```

### Production (Airflow)
```bash
airflow dags trigger player_analytics_dag -e 2026-05-20
```

## Sample Outputs

### Session Facts
| session_id | player_id | start_time | duration_min | actions | revenue |
|---|---|---|---|---|---|
| S001 | P123 | 2026-05-20 19:00 | 45 | 127 | $2.99 |
| S002 | P124 | 2026-05-20 19:15 | 12 | 23 | $0 |
| S003 | P125 | 2026-05-20 19:30 | 120 | 450 | $9.99 |

### Daily Dashboard
- **Active sessions today**: 12,450
- **Avg session duration**: 38 minutes
- **Engagement trend**: ↑ 3% vs yesterday
- **Revenue today**: $15,230
- **At-risk players**: 340 (no session in 7 days)

## What This Demonstrates

**Gaming Analytics Thinking**
- Understood session-based data structure
- Designed metrics that drive game design decisions
- Built insights tied to business outcomes (engagement, monetization)

**Pipeline Skills**
- Session reconstruction (complex logic)
- Aggregation and rollups
- Real-time processing with Airflow
- Monitoring and alerting

**Data Engineering Judgment**
- Chose appropriate aggregation levels (session → player → cohort)
- Thought about data quality (anomaly detection)
- Designed for both exploratory (SQL) and operational (dashboards) use

## Enhanced Features Added

✓ **Session reconstruction** — from raw events  
✓ **Behavioral segmentation** — player classification  
✓ **Cohort analysis** — group-level trends  
✓ **Real-time alerting** — anomaly detection  
✓ **Player journey mapping** — progression tracking  

## What I'd Do Differently

1. **Real-time streaming** (Kafka) instead of batch (Airflow)
   - Player events processed instantly
   - Alerts fired in real-time, not overnight

2. **Machine learning**
   - Churn prediction (predict who will quit)
   - Lookalike modeling (find new players like your whales)
   - Personalized recommendations (optimize per-player engagement)

3. **A/B testing framework**
   - Test level design changes on player cohorts
   - Measure impact on engagement and LTV
   - Statistical rigor (power, significance)

4. **Attribution modeling**
   - Which features drive engagement?
   - Which in-game monetization triggers work best?

5. **Graph analysis**
   - Social networks (which players influence each other)
   - Feature dependencies (what unlocks what)

## Next Steps

- Add ML churn prediction model
- Build real-time leaderboards
- Implement A/B testing framework
- Migrate to real-time streaming
- Add player recommendation engine

---

**The point:** Gaming is data-driven. This pipeline shows how raw events become strategic insights. That's analytics engineering with impact.
