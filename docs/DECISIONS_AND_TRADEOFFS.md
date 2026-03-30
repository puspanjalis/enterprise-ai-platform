# Decisions and Trade-offs

## 1. Batch-first before real-time-first

**Decision:** Start with a batch-oriented backbone and add online serving as a serving pattern, not as the foundation.

**Why:**
- simpler governance
- easier validation
- lower operational overhead
- better fit for many enterprise use cases

**Trade-off:**
- higher latency than event-native systems
- additional work needed for low-latency serving

## 2. Raw and curated zones before feature serving

**Decision:** Separate landing, curation, and feature generation.

**Why:**
- clearer data contracts
- improved auditability
- easier debugging and lineage

**Trade-off:**
- more pipeline stages
- more artifacts to manage

## 3. Feature store as a platform capability

**Decision:** Include a feature engineering and feature store layer.

**Why:**
- reduces training-serving skew
- improves reuse across teams
- supports both offline and online features

**Trade-off:**
- more platform complexity than direct feature computation inside training only

## 4. Registry and approval before deployment

**Decision:** Require registry and approval before batch or real-time serving.

**Why:**
- tighter governance
- better rollback and version management
- clearer promotion path from experimentation to production

**Trade-off:**
- slightly slower promotion cycle
- more process than a lightweight demo pipeline

## 5. Monitoring as a horizontal layer

**Decision:** Treat monitoring as an end-to-end platform layer.

**Why:**
- drift, performance, and operational failures can happen at multiple stages
- aligns better with production MLOps practice

**Trade-off:**
- requires broader instrumentation
- increases operational ownership expectations

## 6. Public-repo safety constraints

**Decision:** Use synthetic data and cloud-neutral examples.

**Why:**
- safe for public sharing
- reusable as a portfolio artifact
- avoids exposure of proprietary implementation details

**Trade-off:**
- less realism than internal enterprise architectures with production integrations
