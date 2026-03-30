# Operational Runbook

## Overview

This runbook provides procedures for operating the Enterprise AI Platform in production. It covers deployment, monitoring, incident response, maintenance, and on-call responsibilities.

## Table of Contents

1. [Platform Architecture](#platform-architecture)
2. [Deployment Procedures](#deployment-procedures)
3. [Monitoring and Alerting](#monitoring-and-alerting)
4. [Incident Response](#incident-response)
5. [Maintenance Windows](#maintenance-windows)
6. [Disaster Recovery](#disaster-recovery)
7. [On-Call Guide](#on-call-guide)
8. [Common Issues](#common-issues)
9. [Escalation Paths](#escalation-paths)

## Platform Architecture

### Component Overview

```
Enterprise AI Platform
├── Data Ingestion Layer
│   ├── API connectors
│   ├── Database connections
│   ├── File watchers
│   └── Validation gates
├── Processing Layer
│   ├── Feature engineering
│   ├── ETL pipelines
│   └── Data quality checks
├── ML Lifecycle Layer
│   ├── Training orchestration
│   ├── Model registry
│   └── Evaluation framework
├── Monitoring Layer
│   ├── Data quality metrics
│   ├── Model drift detection
│   └── System health checks
└── Infrastructure Layer
    ├── Kubernetes cluster
    ├── Object storage
    ├── Metadata database
    └── Message queue
```

### Key Services

**Critical Services (15-minute SLA)**
- Pipeline orchestrator (Airflow)
- Metadata database (PostgreSQL)
- Object storage (S3/GCS/Azure Blob)
- Monitoring system (Prometheus/Grafana)

**Important Services (1-hour SLA)**
- Model registry
- Feature store
- CI/CD system
- Documentation portal

**Supporting Services (4-hour SLA)**
- Development environments
- Experiment tracking
- Cost monitoring dashboard

### Dependencies

**External Dependencies**
- Cloud provider infrastructure
- Data source systems (databases, APIs)
- Authentication provider (SSO)
- Alerting services (PagerDuty, Slack)

**Internal Dependencies**
- Corporate network and VPN
- DNS and certificate management
- Monitoring and logging infrastructure
- Backup systems

## Deployment Procedures

### Standard Deployment

**Deployment Schedule**
- Production: Tuesdays and Thursdays, 10 AM - 2 PM
- Avoid: Fridays, weekends, holidays, critical business periods
- Emergency deployments: Anytime with approval

**Pre-Deployment Checklist**

```bash
# 1. Verify all tests pass
pytest tests/ --cov=pipeline

# 2. Check code review approvals
git log --oneline -n 5

# 3. Review CHANGELOG
cat CHANGELOG.md

# 4. Backup current state
./scripts/backup_metadata.sh

# 5. Notify stakeholders
# Post in #ml-platform: "Deploying version X.Y.Z at HH:MM"
```

**Deployment Steps**

```bash
# 1. Set environment
export ENV=production
export VERSION=v1.2.0

# 2. Pull latest code
git fetch origin
git checkout tags/${VERSION}

# 3. Build and push Docker image
docker build -t enterprise-ai-platform:${VERSION} .
docker push enterprise-ai-platform:${VERSION}

# 4. Update Kubernetes deployment
kubectl set image deployment/ml-pipeline \
  pipeline=enterprise-ai-platform:${VERSION} \
  -n ai-platform

# 5. Watch rollout
kubectl rollout status deployment/ml-pipeline -n ai-platform

# 6. Verify health
./scripts/health_check.sh

# 7. Monitor for 15 minutes
# Watch Grafana dashboard, check logs, verify pipeline executions
```

**Post-Deployment Validation**

```bash
# Run smoke tests
pytest tests/smoke/ --env=production

# Verify key metrics
curl -s http://platform.internal/metrics | grep "pipeline_success_rate"

# Check recent pipeline executions
./scripts/check_recent_pipelines.sh

# Confirm no new errors
./scripts/check_error_rate.sh
```

**Rollback Procedure**

```bash
# If issues detected within 15 minutes:

# 1. Rollback deployment
kubectl rollout undo deployment/ml-pipeline -n ai-platform

# 2. Verify rollback
kubectl rollout status deployment/ml-pipeline -n ai-platform

# 3. Run health check
./scripts/health_check.sh

# 4. Investigate root cause
kubectl logs deployment/ml-pipeline -n ai-platform --tail=100

# 5. Document incident
# Create postmortem in docs/incidents/YYYY-MM-DD-issue.md
```

### Emergency Hotfix Deployment

**When to Use**
- Critical production bug affecting users
- Security vulnerability requiring immediate patch
- Data integrity issue

**Process**

```bash
# 1. Create hotfix branch
git checkout -b hotfix/critical-issue main

# 2. Make minimal fix
# Edit only necessary files

# 3. Fast-track review
# Get approval from on-call lead

# 4. Deploy to staging first
./scripts/deploy.sh staging

# 5. Validate on staging
./scripts/smoke_test.sh staging

# 6. Deploy to production with monitoring
./scripts/deploy.sh production --monitor

# 7. Document and follow up
# Create incident report
# Schedule proper fix for next release
```

## Monitoring and Alerting

### Key Metrics

**System Health Metrics**

```
Platform Uptime
- Target: 99.7%
- Measurement: Synthetic health checks every 60 seconds
- Alert: <99.5% over 5-minute window

Pipeline Success Rate
- Target: 99%
- Measurement: Successful / Total pipeline runs
- Alert: <95% over 1-hour window

Pipeline Execution Time
- Target: P95 < 30 minutes for standard pipelines
- Measurement: Time from trigger to completion
- Alert: P95 > 45 minutes over 1-hour window

Resource Utilization
- CPU: Target 60-80%, Alert >90% for 10 minutes
- Memory: Target 70-85%, Alert >90% for 5 minutes
- Disk: Target <80%, Alert >85%
```

**Data Quality Metrics**

```
Data Freshness
- Target: Data less than 2 hours old
- Alert: Data older than 4 hours

Validation Failure Rate
- Target: <0.1%
- Alert: >1% over 1-hour window

Missing Data Rate
- Target: <0.5%
- Alert: >2% for critical fields
```

**Model Performance Metrics**

```
Prediction Drift
- Target: PSI < 0.2
- Alert: PSI > 0.2 for any feature

Model Latency (if serving)
- Target: P95 < 100ms
- Alert: P95 > 200ms for 5 minutes

Model Accuracy (with ground truth)
- Target: >90% (baseline dependent)
- Alert: Drop >5% from baseline
```

### Alert Severity Levels

**Critical (Page On-Call)**
- Platform down (health check failing)
- Database connection lost
- Critical pipeline failing >3 times
- Data integrity issue detected
- Security incident

**High (Notify Team, Create Ticket)**
- Pipeline success rate <95%
- Significant performance degradation
- Data validation failure rate >1%
- Model drift detected

**Medium (Daily Digest)**
- Individual pipeline failure
- Resource utilization trending up
- Minor data quality issues

**Low (Weekly Report)**
- Optimization opportunities
- Usage pattern changes
- Documentation gaps identified

### Monitoring Dashboards

**Platform Health Dashboard**
- URL: https://grafana.internal/d/platform-health
- Metrics: Uptime, success rate, latency, resource utilization
- Refresh: 30 seconds
- Check: Every morning, before deployments, during incidents

**Pipeline Execution Dashboard**
- URL: https://grafana.internal/d/pipeline-execution
- Metrics: Success/failure by pipeline, execution time trends
- Refresh: 1 minute
- Check: When investigating pipeline issues

**Cost Dashboard**
- URL: https://grafana.internal/d/cost-tracking
- Metrics: Daily spend, cost per pipeline, cost per team
- Refresh: 1 hour
- Check: Weekly for review, monthly for reporting

## Incident Response

### Incident Classification

**Severity 1 (Critical)**
- Platform completely unavailable
- Data loss or corruption
- Security breach
- Response Time: 15 minutes
- Resolution Time: 4 hours target

**Severity 2 (High)**
- Major functionality impaired
- Multiple teams affected
- Workaround available
- Response Time: 30 minutes
- Resolution Time: 8 hours target

**Severity 3 (Medium)**
- Limited functionality affected
- Single team impacted
- Workaround available
- Response Time: 2 hours
- Resolution Time: 24 hours target

**Severity 4 (Low)**
- Minor issue, no business impact
- Response Time: Next business day
- Resolution Time: 1 week target

### Incident Response Workflow

```
1. Detection
   ├── Alert fires (PagerDuty/Slack)
   ├── User report (Slack/email)
   └── Monitoring dashboard anomaly

2. Assessment (5 minutes)
   ├── Acknowledge alert
   ├── Determine severity
   ├── Check dashboards
   └── Review recent changes

3. Communication (10 minutes)
   ├── Post in #ml-platform-incidents
   ├── Update status page
   ├── Notify affected teams
   └── Set up war room if Sev1/Sev2

4. Investigation
   ├── Check logs
   ├── Review metrics
   ├── Test hypothesis
   └── Identify root cause

5. Mitigation
   ├── Apply fix or workaround
   ├── Verify resolution
   ├── Monitor for recurrence
   └── Document actions taken

6. Resolution
   ├── Close incident ticket
   ├── Update status page
   ├── Notify stakeholders
   └── Schedule postmortem (Sev1/Sev2)

7. Postmortem (within 48 hours)
   ├── Timeline of events
   ├── Root cause analysis
   ├── Action items
   └── Prevention measures
```

### Communication Templates

**Initial Incident Notification**

```
🚨 INCIDENT: [Severity] - [Brief Description]

Status: Investigating
Impact: [What's affected, how many users]
Started: [Timestamp]
Incident Lead: [Name]

We are aware of [issue] and investigating. 
Updates every 15 minutes in this thread.

Link to status page: [URL]
```

**Incident Update**

```
UPDATE: [Timestamp]

Progress: [What we've learned/done]
Current Status: [Investigating/Mitigating/Monitoring]
Next Steps: [What we're doing next]
ETA for next update: [15/30 minutes]
```

**Incident Resolution**

```
✅ RESOLVED: [Brief Description]

Root Cause: [Summary]
Resolution: [What we did]
Duration: [Total time]
Impact: [Final assessment]

Postmortem: [Link or "Scheduled for DATE"]
Thank you for your patience.
```

## Common Issues and Solutions

### Issue: Pipeline Execution Failure

**Symptoms**
- Pipeline shows failed status in Airflow
- Error in logs: "Task failed with exception"

**Diagnosis**

```bash
# Check Airflow UI for failed task
# View task logs
airflow tasks logs <dag_id> <task_id> <execution_date>

# Check system resources
kubectl top pods -n ai-platform

# Review recent deployments
kubectl rollout history deployment/ml-pipeline -n ai-platform
```

**Common Causes and Fixes**

**1. Data Validation Failure**
```bash
# Check validation errors
cat /app/logs/data_quality_$(date +%Y%m%d).log

# Review specific validation
python -m monitoring.data_quality --check

# Fix: Update validation thresholds or fix data source
```

**2. Memory/Resource Exhaustion**
```bash
# Check resource limits
kubectl describe pod <pod-name> -n ai-platform

# Fix: Increase resource limits in deployment.yaml
# Or: Optimize pipeline to process data in chunks
```

**3. External Dependency Failure**
```bash
# Test database connection
python -m pipeline.test_connections

# Fix: Check credentials, network connectivity
# Temporary: Increase retry count and timeout
```

### Issue: High Latency

**Symptoms**
- Dashboard shows P95 latency >45 minutes
- Users complaining about slow pipelines

**Diagnosis**

```bash
# Identify bottleneck
airflow tasks duration <dag_id>

# Check database performance
./scripts/check_db_performance.sh

# Review resource utilization
kubectl top pods -n ai-platform --sort-by=cpu
```

**Solutions**

```bash
# 1. Optimize slow queries
# Check slow query log
tail -f /var/log/postgresql/slow-queries.log

# 2. Scale up resources
kubectl scale deployment/ml-pipeline --replicas=5 -n ai-platform

# 3. Add caching
# Implement Redis cache for frequently accessed data

# 4. Partition large datasets
# Process data in smaller chunks
```

### Issue: Data Drift Detected

**Symptoms**
- Alert: "Feature drift detected: PSI > 0.2"
- Model predictions may be inaccurate

**Diagnosis**

```bash
# Review drift report
python -m monitoring.drift_detection --report

# Compare distributions
python -m monitoring.drift_detection --visualize \
  --feature <feature_name>
```

**Actions**

```bash
# 1. Validate if drift is real or expected
# Check for seasonality, business changes

# 2. If real drift:
# Trigger model retraining
python -m models.retrain --reason "drift_detected"

# 3. Update monitoring thresholds if needed
# Edit monitoring/config/drift_thresholds.yaml

# 4. Notify ML team
# Post in #ml-alerts with drift report
```

### Issue: Cost Spike

**Symptoms**
- Cost dashboard shows >50% increase
- Budget alert triggered

**Diagnosis**

```bash
# Identify cost drivers
./scripts/analyze_costs.sh --date <YYYY-MM-DD>

# Check resource usage
kubectl top pods -n ai-platform --sort-by=memory

# Review pipeline execution frequency
./scripts/pipeline_frequency_report.sh
```

**Solutions**

```bash
# 1. Identify inefficient pipelines
# Look for long-running or frequent executions

# 2. Optimize resource allocation
# Right-size container requests/limits

# 3. Implement caching
# Avoid recomputing unchanged data

# 4. Schedule non-urgent pipelines during off-peak
# Update Airflow schedule to night/weekend

# 5. Review data retention
# Delete old data no longer needed
```

## Disaster Recovery

### Backup Strategy

**Daily Backups**
- Metadata database: Full backup at 2 AM UTC
- Configuration files: Git repository
- Model artifacts: All versions retained
- Retention: 30 days

**Weekly Backups**
- Complete system state snapshot
- Retention: 90 days

**Backup Verification**
- Monthly restore drill
- Validate backup integrity
- Document restoration time

### Recovery Procedures

**Database Restore**

```bash
# 1. Stop applications
kubectl scale deployment/ml-pipeline --replicas=0 -n ai-platform

# 2. Restore database
./scripts/restore_database.sh --date <YYYY-MM-DD>

# 3. Verify data integrity
./scripts/verify_database.sh

# 4. Restart applications
kubectl scale deployment/ml-pipeline --replicas=3 -n ai-platform

# 5. Run health checks
./scripts/health_check.sh
```

**Complete System Restore**

```bash
# Estimated Time: 4 hours

# 1. Provision infrastructure (Terraform)
cd infra/terraform
terraform apply -var-file=production.tfvars

# 2. Deploy platform (Kubernetes)
kubectl apply -f infra/kubernetes/

# 3. Restore database
./scripts/restore_database.sh --latest

# 4. Restore model artifacts
aws s3 sync s3://backup-bucket/models s3://production-bucket/models

# 5. Verify all services
./scripts/full_system_check.sh
```

### Business Continuity

**RTO (Recovery Time Objective):** 4 hours
**RPO (Recovery Point Objective):** 1 hour

**Critical Functions Priority**
1. Metadata database (restore within 1 hour)
2. Pipeline orchestration (restore within 2 hours)
3. Model serving (restore within 2 hours)
4. Monitoring (restore within 4 hours)
5. Development environments (restore within 24 hours)

## On-Call Guide

### On-Call Responsibilities

**Primary On-Call**
- Respond to all alerts within 15 minutes
- Triage and classify incidents
- Lead incident response
- Communicate status updates
- Document incidents

**Secondary On-Call**
- Backup for primary
- Assist with complex issues
- Provide coverage during primary escalation

### On-Call Rotation

**Schedule**
- Week-long shifts, Monday 9 AM - Monday 9 AM
- Rotation: All platform team members
- Exceptions: Arranged 2 weeks in advance

**Handoff Process**

```
Monday 9 AM: On-call transition

Outgoing engineer:
- Review active incidents
- Brief on ongoing issues
- Share any pending items
- Update on-call notes document

Incoming engineer:
- Acknowledge handoff
- Review dashboards
- Test alert routing
- Confirm PagerDuty active
```

### Escalation Path

```
Level 1: On-Call Engineer (0-30 minutes)
├── Handle routine issues
├── Follow runbooks
└── Communicate with users

Level 2: On-Call Lead (30-60 minutes)
├── Complex technical issues
├── Multi-component failures
└── Coordinate with teams

Level 3: Engineering Manager (1-2 hours)
├── Business impact decisions
├── Resource allocation
└── Executive communication

Level 4: VP Engineering (2+ hours)
├── Major outage
├── Data breach
└── Financial impact
```

### After-Hours Support

**P1 (Critical):** Page on-call immediately
**P2 (High):** Page on-call, can wait until next business day if detected after hours
**P3/P4:** Ticket only, next business day

**Compensation**
- Base on-call pay: $X per week
- Incident response: $Y per hour
- Weekend/holiday: 1.5x multiplier

## Maintenance Windows

### Scheduled Maintenance

**Monthly Maintenance Window**
- Schedule: First Sunday, 2 AM - 6 AM UTC
- Duration: Up to 4 hours
- Notice: 7 days advance notice to users

**Maintenance Activities**
- Kubernetes cluster upgrades
- Database maintenance (VACUUM, index rebuilds)
- Certificate renewals
- Security patches
- Performance optimizations

**Maintenance Checklist**

```bash
# 1 Week Before
- [ ] Review planned changes
- [ ] Identify potential risks
- [ ] Prepare rollback plan
- [ ] Notify users (#ml-platform, email)

# 1 Day Before
- [ ] Confirm team availability
- [ ] Test changes in staging
- [ ] Verify backups complete
- [ ] Update status page

# Day Of
- [ ] Post maintenance start notification
- [ ] Execute changes per runbook
- [ ] Test each change before proceeding
- [ ] Run full system validation
- [ ] Update monitoring dashboards
- [ ] Post maintenance completion notification
- [ ] Monitor for 24 hours

# 1 Week After
- [ ] Conduct retrospective
- [ ] Update runbooks
- [ ] Document lessons learned
```

## Contact Information

### Platform Team

**On-Call (24/7)**
- PagerDuty: [Number/Email]
- Slack: #ml-platform-oncall

**Platform Engineering**
- Team Lead: [Name] - [Email]
- Senior Engineers: [Names] - [Emails]

**Manager**
- Engineering Manager: [Name] - [Email]

### External Contacts

**Cloud Provider Support**
- AWS Support: [Account ID] - [Phone]
- Priority: Enterprise 24/7

**Vendor Support**
- Snowflake: [Account Manager] - [Phone]
- DataRobot: [Support Portal] - [Email]

### Executive Escalation

**Critical Incidents Only**
- VP Engineering: [Name] - [Phone]
- CTO: [Name] - [Phone]

## Conclusion

This runbook is a living document. All engineers are encouraged to:
- Add procedures based on incidents
- Update contact information
- Improve clarity
- Share lessons learned

Last Updated: [Date]
Next Review: [Date]
