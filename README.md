# 🐾 Habitat: AI-Assisted Community Animal Monitoring System

> From resident complaint to verified, prioritised and approved action.

Habitat is an AI-assisted community animal management platform designed around the problem statement of **smart monitoring of community cats and chickens in HDB estates**. It brings four stages into one workflow: complaint intake, animal detection and verification, hotspot analysis and forecasting, and recommended actions with human approval.

The platform supports three user portals:

- **Resident:** Submit a complaint, receive a reference number and track its status.
- **Officer:** Review cases, verify detections, investigate hotspots and manage actions.
- **Supervisor:** Approve actions, manage zones and thresholds, and monitor forecasts and system performance.

> **Data and deployment note:** EMS operational data is not currently available. The prototype therefore uses synthetic and permitted public/sample data. Every chart, forecast or metric based on synthetic data must be clearly labelled **Sample data**. A production deployment for EMS would require approved data access, infrastructure, security review, operational validation and stakeholder sign-off.

---

## 1. The problem

Residents report cats and chickens in English, Chinese, Malay, Tamil and Singlish, sometimes with blurry or dim photos. Officers may need to handle reports individually, making it difficult to identify duplicate complaints, distinguish nuisance issues from animal-welfare concerns, and understand where activity is concentrated.

**Goal:** Support coexistence by protecting animals from harm and reducing conflict between residents and animals—not simply closing complaints.

---

## 2. Solution overview

```text
Resident / Officer
       |
       v
[A. Intake and Case Analysis]
       |
       v
[B. Animal Detection and Verification]
       |
       v
[C. Hotspot Analysis and Forecasting]
       |
       v
[D. Recommended Actions and Approval]
       |
       v
Officer review -> Supervisor approval -> Action tracking
```

The modules share case, detection, zone and action data. AI outputs are recommendations for human review; the system does not autonomously carry out animal-related actions.

### Main portals

| Portal | Users | Main functions |
|---|---|---|
| Resident | Public / guest | Submit a complaint, receive a reference number and track status |
| Officer | Property officers | Manage cases, verify detections, view hotspots and plan actions |
| Supervisor | Managers | Approve or decline actions, manage zones and thresholds, review forecasts and model health |

---

## 3. Team and ownership

### Team

| Member | Role |
|---|---|
| Shin Paing Min | Team Lead & Developer |
| Phyu Sin Myat | Developer |
| Ang Zheng Zhe | Developer |
| Yuan Ming | Developer |

### Module ownership

| Member | Module | CRUD ownership | Main AI / system responsibilities |
|---|---|---|---|
| Phyu Sin Myat | A. Case analysis and intake | Cases and AI tags | Multilingual and Singlish understanding, duplicate clustering, root-cause extraction, risk-based priority scoring, nuisance vs welfare classification |
| Shin Paing Min | B. Animal detection and identification | Animal profiles and detection records | YOLO cat/chicken detection, low-light and blurry-image robustness, complaint-led verification, review queue, individual identification where feasible, model health |
| Ang Zheng Zhe | C. Hotspot dashboard and forecasting | Zones and alert thresholds | Statistical hotspots, zone risk score, time-series forecasting, behaviour and feeding patterns, early warnings, backtesting, movement and floor view |
| Yuan Ming | D. Action recommendation and approval | Action items and work orders | Root-cause recommendations, RAG over AVS/NParks/CWS guidance, case consolidation, outcome learning, multilingual notices, welfare escalation, approval workflow |

### Shared responsibilities

| Work | Owner(s) | Notes |
|---|---|---|
| Role-based portals, login and navigation | Phyu Sin Myat | Resident guest flow; officer and supervisor roles |
| Dataset collection and labelling | Shin Paing Min, with all members helping | Use Label Studio or CVAT |
| Synthetic cases, zones and time-series data | Ang Zheng Zhe and Phyu Sin Myat | Reproducible seeded data |
| CI/CD, containers, deployment and integration tests | Yuan Ming and Shin Paing Min | Docker Compose and GitHub Actions |
| Peer review | Everyone | Each member reviews another module's pull requests |
| Shared API contracts and integration | All members | Agree on schemas and API behaviour before integration |

---

## 4. Technology stack

The following stack is the agreed target architecture for Habitat. Technologies should be introduced in stages according to the project roadmap. A technology listed here is planned, not necessarily already implemented.

### 4.1 Frontend

| Technology | Purpose |
|---|---|
| React | Build the web application and interactive dashboards for residents, officers and supervisors |
| Tailwind CSS | Create responsive and consistent UI designs |
| Figma / Figma Make | UI/UX design and prototyping |
| Recharts | Display animal statistics, case trends and analytics |
| Leaflet | Display animal locations, zones and sightings on interactive maps |

### 4.2 Backend

| Technology | Purpose |
|---|---|
| Python | Main backend programming language |
| FastAPI | Build REST APIs and handle application business logic |
| JWT | Support user authentication |
| Role-Based Access Control (RBAC) | Manage resident, officer and supervisor permissions |
| Server-Sent Events (SSE) | Deliver real-time detection, case and alert updates to the website |

Use secure, HttpOnly cookies for browser-based token handling where applicable. Backend endpoints must enforce permissions; hiding frontend controls is not sufficient security.

### 4.3 AI and Computer Vision

| Technology | Purpose |
|---|---|
| PyTorch | Develop, train and evaluate deep learning models |
| YOLO | Detect and classify cats and chickens in images and videos |
| OpenCV | Process images, video files and camera streams |
| ByteTrack | Track detected animals across video frames |
| ONNX Runtime | Optionally optimise and execute exported AI models |

### 4.4 Database and Storage

| Technology | Purpose |
|---|---|
| PostgreSQL | Store users, complaints, animal profiles, detections, zones, actions and audit records |
| PostGIS | Store and query geographical coordinates, HDB zones and animal locations |
| pgvector | Store embeddings and support similarity searches for related complaints or animal images |
| MinIO | Store animal photographs, processed images and video clips |

Use local volumes for local development if needed. Use MinIO or another approved object-storage service for a deployed environment.

### 4.5 Background Processing and Real-Time Services

| Technology | Purpose |
|---|---|
| Celery | Handle background tasks such as video processing, AI inference and scheduled forecasting |
| Redis | Message broker for Celery, caching and temporary data coordination |
| Server-Sent Events (SSE) | Push status changes and new detection or alert events to the browser |

Long-running video and AI jobs should run in background workers rather than keeping a normal FastAPI request open until processing finishes.

### 4.6 LLM and AI Assistant

| Technology | Purpose |
|---|---|
| Ollama | Run supported open-source language models locally |
| Hosted LLM API (optional) | Provide an alternative when a hosted model offers better quality or performance |

The LLM may support multilingual complaint understanding, structured summaries, recommended actions and monitoring reports. It does not replace YOLO, PyTorch or the computer-vision pipeline. AI-generated recommendations must show supporting sources and remain subject to human review.

### 4.7 MLOps and Dataset Management

| Technology | Purpose |
|---|---|
| MLflow | Track model experiments, evaluation metrics and model versions |
| DVC | Version and manage machine-learning datasets and data pipelines |

### 4.8 DevOps and Deployment

| Technology | Purpose |
|---|---|
| Docker | Containerise application services |
| Docker Compose | Run and manage multiple application containers during development and deployment |
| GitHub Actions | Automate testing, build checks and deployment workflows (CI/CD) |

### 4.9 Testing

| Technology | Purpose |
|---|---|
| pytest | Test backend logic, APIs, services and database operations |
| Playwright | Perform frontend and end-to-end testing of resident, officer and supervisor workflows |

### 4.10 Supporting libraries used within modules

The following libraries support specific module features. They complement the main stack above and should only be introduced where required.

| Library / tool | Module use |
|---|---|
| Pydantic | Validate API request and response data |
| scikit-learn | Baseline classification, priority scoring and statistical utilities |
| sentence-transformers | Generate multilingual text embeddings for duplicate-case search |
| HDBSCAN | Cluster potentially duplicated complaints |
| CVAT or Label Studio | Label animal images and review training annotations |
| Albumentations | Apply realistic training augmentation, including lighting and blur variations |
| DINOv2 or CLIP (optional) | Generate image embeddings for animal-image similarity experiments |
| GeoPandas and PySAL | Support geospatial analysis and hotspot calculations |
| statsmodels or Prophet | Support time-series forecasting experiments |
| Recharts | Visualise analytics and forecast outputs |
| PyMuPDF or pdfplumber | Extract text from approved guideline documents |

### 4.11 Technology priority

| Priority | Technologies |
|---|---|
| Essential foundation | React, Tailwind CSS, Python, FastAPI, PostgreSQL, PyTorch, YOLO, OpenCV, Docker |
| Needed for planned integrated workflows | PostGIS, Leaflet, ByteTrack, MinIO, Celery, Redis, SSE, pytest, Playwright |
| Advanced / optional | pgvector, ONNX Runtime, Ollama, hosted LLM API, MLflow, DVC, image embeddings |

Do not implement every optional technology at the beginning. Prioritise the core complaint-to-approval workflow and add advanced components when the corresponding feature is ready.

### 4.12 System architecture

```text
                    ANIMAL DATA SOURCES
             ┌────────────────────────────────┐
             │ CCTV / Camera Feeds             │
             │ Resident Image Uploads          │
             │ Video Uploads                   │
             │ GPS / Location Information      │
             └────────────────┬───────────────┘
                              │
                              ▼
                  VIDEO / IMAGE PROCESSING
             ┌────────────────────────────────┐
             │ OpenCV                         │
             │ Celery + Redis Background Jobs │
             └────────────────┬───────────────┘
                              │
                              ▼
                    AI PROCESSING PIPELINE
             ┌────────────────────────────────┐
             │ PyTorch + YOLO                 │
             │ ByteTrack                      │
             │ ONNX Runtime (optional)        │
             └────────────────┬───────────────┘
                              │
                              ▼
                      FASTAPI BACKEND
             ┌────────────────────────────────┐
             │ REST API + JWT / RBAC           │
             │ Case and Detection Logic        │
             │ Hotspot and Action Services     │
             │ SSE Real-Time Updates           │
             └────────────────┬───────────────┘
                              │
                   ┌──────────┴──────────┐
                   ▼                     ▼
          ┌──────────────────┐  ┌──────────────────┐
          │   PostgreSQL     │  │      MinIO       │
          │   PostGIS        │  │  Photos / Videos │
          │   pgvector       │  │                  │
          └─────────┬────────┘  └──────────────────┘
                    │
                    ▼
             ┌────────────────────────────┐
             │       REACT WEBSITE        │
             │                            │
             │ Resident Complaint Portal  │
             │ Officer Case Dashboard     │
             │ Animal Detection & Review  │
             │ Hotspot Maps & Analytics   │
             │ Supervisor Approval        │
             │ Real-Time Alerts            │
             └────────────────────────────┘
```

**Architecture note:** Celery and Redis handle long-running background jobs. PostgreSQL stores structured records and geospatial data, while MinIO stores media files. The React website communicates with FastAPI; it should not connect directly to the database or object-storage credentials.

## 5. Shared data contracts

All modules must use the same field names and agreed meanings. Changes to shared contracts require team discussion and an updated API/schema document.

### Case

```text
id, text, language, translation, photo_urls,
block, floor, stairwell, zone_id, created_at,
category, priority, root_cause, status
```

### Detection

```text
id, case_id, source, species, confidence, boxes,
model_version, review_status, profile_id, behaviour (optional)
```

### Zone

```text
id, name, blocks, geometry, risk_score, hotspot_flag
```

### Action

```text
id, zone_id, case_ids, recommendation, sources,
cost, status, decision_reason
```

Each module must expose a mock API or mock service for integration testing. No module should block another team member from developing against an agreed contract.

---

## 6. Module A: Case analysis and intake

**Owner:** Phyu Sin Myat

### User stories

| ID | As a… | I want to… | So that… | Priority |
|---|---|---|---|---|
| A-01 | Resident | Submit a complaint in my own language with an optional photo | I can report without an account | Must |
| A-02 | Resident | Receive a reference number | I can follow up later | Must |
| A-03 | Officer | Log a complaint received by phone, email or WhatsApp | All channels enter one system | Must |
| A-04 | Officer | View, edit, archive and close cases | I can manage my workload | Must |
| A-05 | Officer | See Chinese, Malay, Tamil or Singlish complaints translated | I can understand every report | Must |
| A-06 | Officer | See each case marked as nuisance or welfare | Urgent animal-welfare cases are not buried | Must |
| A-07 | Officer | See a priority score with reasons | I know what to handle first | Must |
| A-08 | Officer | Have repeat complaints about the same spot grouped | I can manage related reports together | Should |
| A-09 | Officer | See a likely root cause | I can target the underlying problem | Should |
| A-10 | Supervisor | See welfare cases fast-tracked | Potential harm receives quicker attention | Must |

### Acceptance examples

- A supported multilingual complaint is translated and categorised within the agreed response-time target.
- Differently worded complaints about the same stairwell are suggested as a possible duplicate cluster.
- Welfare classification and priority scores show reasons and can be corrected by an officer.

### Technologies

| Feature | Technology |
|---|---|
| Language detection | fastText or langdetect |
| Translation and Singlish understanding | Ollama-hosted model or hosted LLM API; NLLB/MarianMT fallback |
| Nuisance vs welfare classification | Rule-based baseline, then evaluated scikit-learn classifier or LLM-assisted classification |
| Priority scoring | Documented rules and, if labelled data permits, gradient boosting |
| Duplicate clustering | Multilingual embeddings + HDBSCAN using text, location and time |
| Root-cause extraction | LLM with structured Pydantic output |
| Storage and search | PostgreSQL + pgvector |
| UI | Resident submission, confirmation, Case Inbox, Case Detail, Log Complaint and Duplicates |

### Module A delivery plan

| Project week | Deliverables |
|---|---|
| W6–W7 | Confirm case schema and CRUD/API behaviour; complete resident form and officer case inbox; connect authentication and roles |
| W8–W9 | Implement language detection, translation, nuisance/welfare tagging and priority scoring v1 |
| W10–W11 | Implement duplicate suggestions, root-cause extraction and officer correction workflow |
| W12 | Evaluate on labelled sample complaints; fix integration issues and document limitations |
| W13 | Present module workflow, architecture, test evidence and known limitations at technical review |
| W14–W15 | Address review feedback, improve reliability and complete acceptance tests |
| W16 | Release integrated, tested Module A |

**Evaluation:** Classification precision, recall and F1 on a labelled test set; hand-checked duplicate-cluster precision; response time; and human correction rate. Report sample size and limitations.

---

## 7. Module B: Animal detection and identification

**Owner:** Shin Paing Min

### User stories

| ID | As a… | I want to… | So that… | Priority |
|---|---|---|---|---|
| B-01 | Officer | Have complaint photos classified as cat or chicken | I know what the resident saw | Must |
| B-02 | Officer | See whether the photo agrees with the report | Unclear reports can be checked | Must |
| B-03 | Officer | Have low-confidence detections sent to a review queue | AI is not trusted blindly | Must |
| B-04 | Officer | Correct a wrong label | The record is accurate and can support future model improvement | Must |
| B-05 | Officer | Create, view, edit and remove animal profiles | I can manage repeat-animal records | Must |
| B-06 | Officer | View detection records with source, status and linked case | I have an audit trail | Must |
| B-07 | Resident | Have people in submitted photos blurred | Privacy is protected | Must |
| B-08 | Officer | See whether the same animal may appear across reports | I can investigate repeat sightings | Should |
| B-09 | Supervisor | See model accuracy, versions and retraining status | I can monitor model quality | Must |
| B-10 | Officer | View an optional camera or sensor feed | Live input can be added | Could |

### Acceptance examples

- Low-confidence detections enter a review queue.
- An officer can agree or disagree with a detection and correct its species.
- Corrections are stored for review and possible retraining.
- People in complaint photos are blurred before images are displayed to other users, subject to the agreed privacy workflow.

### Technologies

| Feature | Technology |
|---|---|
| Detection | YOLO + PyTorch + OpenCV |
| Dataset labelling | CVAT or Label Studio |
| Data sources | Permitted public datasets and collected sample footage |
| Robustness | Albumentations; evaluate low-light and blurry subsets separately |
| Privacy blur | Person detection and OpenCV blur |
| Verification | Compare reported species with detected species and confidence |
| Tracking | ByteTrack for tracking across video frames |
| Individual animal similarity (stretch) | DINOv2 or CLIP embeddings + pgvector; human verification required |
| Review queue | Confidence thresholds and correction records |
| Model registry and metrics | MLflow; record mAP, precision and recall per class |
| Camera input (optional) | OpenCV webcam or RTSP input |
| Training compute | Google Colab or Kaggle GPU, where available |
| UI | Detection Records, Detection Detail, Review Queue, Animal Profiles, Model Health and Detection Test |

**Important distinction:** ByteTrack tracks detections across frames; it does not by itself prove that an animal is the same individual across separate days or cameras. Cross-session individual identification is an optional research feature and must be evaluated separately.

### Module B delivery plan

| Project week | Deliverables |
|---|---|
| W6–W7 | Make pretrained YOLO inference work; finalise `POST /detect`; collect and organise permitted sample footage; build detection record CRUD |
| W8–W9 | Label data, train/evaluate model v1, implement privacy blur and connect complaint-photo verification |
| W10–W11 | Complete review queue, animal profiles, correction records and model health page |
| W12 | Add video-frame processing and ByteTrack where stable; evaluate low-light and blurry conditions |
| W13 | Present model pipeline, dataset provenance, metrics, privacy workflow and limitations at technical review |
| W14–W15 | Improve model and inference reliability; complete end-to-end tests and model documentation |
| W16 | Release integrated, tested Module B |

**Evaluation:** Per-class precision, recall and mAP on a held-out test set; separate low-light/blurry subset results; review-queue rate; inference time; and before/after metrics if retraining is completed.

---

## 8. Module C: Hotspot dashboard and forecasting

**Owner:** Ang Zheng Zhe

### User stories

| ID | As a… | I want to… | So that… | Priority |
|---|---|---|---|---|
| C-01 | Supervisor | Create, view, update and remove zones | The system analyses the right areas | Must |
| C-02 | Officer | See statistically supported hotspots on a map | I act on evidence-based clusters | Must |
| C-03 | Officer | See why a zone is risky | I can explain and act on it | Must |
| C-04 | Supervisor | See a forecast of activity per zone with a likely range | I can plan ahead | Must |
| C-05 | Supervisor | Receive early warnings when a zone is predicted to reach high risk | We can act earlier | Must |
| C-06 | Supervisor | Set and adjust alert thresholds per zone | Alerts match each zone's needs | Must |
| C-07 | Supervisor | See how accurate past forecasts were | I know how much to trust predictions | Should |
| C-08 | Officer | See feeding-time and gathering patterns | I can plan visits and cleaning | Should |
| C-09 | Officer | See animal movement and a block/floor view | I understand where animals gather | Could |

### Acceptance examples

- A hotspot is only labelled statistically significant when the selected method and threshold support it.
- Every forecast shows its time period, uncertainty/range where available, and **Sample data** label when based on synthetic data.
- Supervisors can adjust alert thresholds and see the resulting alert state.

### Technologies

| Feature | Technology |
|---|---|
| Spatial data | PostgreSQL + PostGIS + GeoPandas |
| Hotspot detection | PySAL (esda) Getis-Ord Gi* and scikit-learn KernelDensity |
| Zone risk score | Documented weighted combination of reports, verified detections and environmental factors |
| Forecasting | statsmodels (SARIMAX) or Prophet |
| External regressors | Approved rainfall data and relevant calendar variables, where available |
| Backtesting | Rolling-origin evaluation with MAE and MAPE |
| Pattern analysis | pandas time-of-day and floor aggregations |
| Early warnings | Scheduled Celery task comparing predicted risk with configured thresholds |
| Maps and charts | Leaflet and Recharts |
| UI | Hotspot Map, Zone Detail, Forecast, Early-Warning Alerts, Zones and Alert Thresholds |

### Module C delivery plan

| Project week | Deliverables |
|---|---|
| W6–W7 | Confirm synthetic data generator; implement zone/threshold CRUD; establish PostGIS schema and map shell |
| W8–W9 | Implement Kernel Density hotspots, zone risk score v1 and zone detail |
| W10–W11 | Add Getis-Ord significance testing, time/floor patterns and forecast baseline |
| W12 | Implement forecast backtesting, threshold-based early warnings and accuracy page |
| W13 | Present geospatial approach, forecast methodology, sample-data labelling and evaluation at technical review |
| W14–W15 | Improve forecast reliability, map usability, tests and documentation |
| W16 | Release integrated, tested Module C |

**Evaluation:** Backtest MAE and MAPE per zone; hotspot significance settings; and clear disclosure that synthetic data cannot establish real-world forecast performance.

---

## 9. Module D: Action recommendation and approval

**Owner:** Yuan Ming

### User stories

| ID | As a… | I want to… | So that… | Priority |
|---|---|---|---|---|
| D-01 | Officer | Get recommended actions based on the root cause | I address the cause, not only the symptom | Must |
| D-02 | Officer | See the source of each recommendation | I can verify the guidance | Must |
| D-03 | Officer | Create, edit and track action items and work orders | I can follow work to completion | Must |
| D-04 | Supervisor | Approve or decline actions with a reason | A person decides before action is taken | Must |
| D-05 | Officer | Have a welfare case escalated with a suggested contact | Animals at risk can receive attention | Must |
| D-06 | Officer | Have related cases in the same block combined into one visit | I can reduce repeat visits | Should |
| D-07 | Officer | Generate a friendly resident notice in four languages | Residents receive clear, non-punitive guidance | Should |
| D-08 | Supervisor | See which actions reduced complaints | We can evaluate what works | Should |
| D-09 | Supervisor | Use approval outcomes to improve future suggestions | Recommendations can be reviewed and refined | Could |
| D-10 | Supervisor | Route approvals through Power Automate | It can fit an existing workflow if available | Could |

### Acceptance examples

- Every generated recommendation includes at least one relevant source that an officer can open and verify.
- A declined action records the supervisor's reason and shows it to the officer.
- No animal-related action is executed automatically by the AI.
- Welfare escalation follows a documented rule and contact directory.

### Technologies

| Feature | Technology |
|---|---|
| Knowledge base | Approved AVS, NParks and Cat Welfare Society documents |
| Document extraction | PyMuPDF or pdfplumber |
| Retrieval and RAG | sentence-transformers / multilingual-e5 + pgvector |
| RAG orchestration | LlamaIndex or LangChain, if needed |
| Recommendation generation | Ollama or hosted LLM API with structured output and source requirements |
| Case consolidation | Group by block, stairwell and time window |
| Outcome tracking | PostgreSQL records and transparent statistical analysis |
| Multilingual notices | LLM-assisted generation plus templates and human review |
| Welfare escalation | Rule engine triggered by Module A welfare flag |
| Approval workflow | FastAPI approval workflow; Power Automate integration only if access is available |
| Mock integrations | Clearly labelled mock Dynamics 365 spend and TCMS work orders |
| UI | Actions (Plan, Do, Watch, Review), Plan Detail, Notice, Welfare Card, Approvals and Outcomes |

### Module D delivery plan

| Project week | Deliverables |
|---|---|
| W6–W7 | Finalise action/work-order schema and CRUD; build approval UI; collect and ingest approved guideline documents |
| W8–W9 | Implement retrieval with source references and recommendation v1 |
| W10–W11 | Complete approval/decline reasons, welfare escalation and multilingual notice workflow |
| W12 | Add case consolidation and outcome tracking; test recommendation citations |
| W13 | Present RAG flow, source traceability, approval controls and limitations at technical review |
| W14–W15 | Improve recommendation quality, security, audit trail and end-to-end tests |
| W16 | Release integrated, tested Module D |

**Evaluation:** Percentage of recommendations with valid sources; manual relevance review of a sample of recommendations; notice quality review; approval audit completeness; and welfare-escalation test results.

---

## Planned feature checklist

The following checklist tracks the overall website scope. Update it as features are implemented and tested.

- [ ] Resident complaint submission and reference number
- [ ] Resident complaint status tracking
- [ ] Officer and supervisor authentication
- [ ] Role-based access control
- [ ] Animal image and video uploads
- [ ] AI-powered cat and chicken detection
- [ ] Human verification and correction queue
- [ ] Animal profiles and detection history
- [ ] Animal tracking across video frames
- [ ] Interactive zone and hotspot map
- [ ] Zone risk scores and activity forecasting
- [ ] Real-time detection and case notifications
- [ ] Recommended actions with source references
- [ ] Supervisor approval and decline workflow
- [ ] Animal activity and case analytics dashboard
- [ ] AI-generated monitoring summaries and reports
- [ ] Image similarity search (optional)
- [ ] Live camera monitoring (optional / stretch)

## 10. Project timeline: Week 1 to Week 16

### Overall duration and current position

- **Total planned project duration:** 16 teaching weeks.
- **Project timeline baseline:** The current working week is Week 6; the remaining schedule is planned from Week 6 to Week 16 inclusive.
- **Current position:** Week 6.
- **Remaining schedule:** Week 6 through Week 16 inclusive — 11 weeks.
- **Technical review:** Week 13.
- **Feature-complete target:** End of Week 16.
- **Release target:** Week 16, after integration, acceptance testing, security checks and release sign-off.

Weeks 1–5 are the earlier project period. This revised plan focuses on the remaining work from Week 6 and uses Week 13 as a formal technical review checkpoint.

### Master project schedule

| Week | Phase | Main activities | Expected deliverables / milestone |
|---|---|---|---|
| **W1–W2** | Initial foundation | Team formation, problem definition, module ownership, initial requirements, data contracts, repository and initial UI planning | Project scope, module owners, initial architecture and shared contracts |
| **W3–W5** | Early development | Initial module implementation, UI and API foundations, sample data, early AI experiments and setup | Existing work reviewed and carried forward; gaps identified at W6 |
| **W6** | Re-baseline and integration foundation | Review current code; confirm stack and contracts; verify local Docker environment; confirm database schema; create/repair mock APIs; agree acceptance criteria | **Milestone 1:** All modules have agreed interfaces and a working development baseline |
| **W7** | End-to-end skeleton | Connect frontend, FastAPI and PostgreSQL; integrate initial module APIs; verify login/roles; confirm file upload and background-job approach | **Milestone 2:** One basic complaint can pass through the shared application flow |
| **W8–W9** | Core feature implementation | Build each module's Must-have functions; connect YOLO inference; implement case classification and initial hotspots; implement recommendation retrieval | **Milestone 3:** Core module workflows work independently and can exchange data |
| **W10–W11** | Full workflow integration | Connect complaint → detection → verification → hotspot → recommendation → approval; add review queues, alerts, audit trail and dashboard updates | **Milestone 4:** Complete end-to-end workflow demonstrated using sample data |
| **W12** | Stabilisation and review preparation | Feature freeze for review candidate; integration testing; model and forecast evaluation; API/security review; fix critical bugs; prepare architecture diagrams and demo | **Milestone 5:** Technical review candidate, test evidence and documentation ready |
| **W13** | **Technical review** | Demonstrate architecture, all four modules, end-to-end flow, AI evaluation, database, security, limitations and release plan; collect feedback | **Milestone 6: Formal technical review completed** |
| **W14** | Review feedback and hardening | Prioritise and fix review findings; improve performance, error handling, accessibility and security; complete missing Must-have functions | Review issues resolved or assigned with documented decisions |
| **W15** | User acceptance and release candidate | User acceptance testing; regression and end-to-end testing; backup/restore test; deployment rehearsal; final documentation; release candidate sign-off | **Milestone 7: Release candidate approved** |
| **W16** | Feature completion and release | Complete all agreed features; resolve release-blocking defects; deploy the release build; verify monitoring, backup, access control and rollback procedure; publish release notes | **Milestone 8: Feature-complete product and MVP / production-readiness-level release** |

### Detailed remaining-week schedule

| Week | Focus | Definition of completion |
|---|---|---|
| W6 | Re-baseline and contracts | Each member confirms existing progress, remaining tasks, API schemas and dependencies |
| W7 | Integration skeleton | Frontend, backend, database, authentication and module mock APIs work together |
| W8 | Must-have feature build 1 | Main case, detection, zone and action workflows are implemented |
| W9 | Must-have feature build 2 | AI and analytics features are connected to the relevant module workflows |
| W10 | Cross-module integration | Modules exchange real application data using agreed API contracts |
| W11 | Full workflow and dashboard | Complaint-to-approval workflow is demonstrable; alerts and audit trail work |
| W12 | Stabilisation | Review candidate passes agreed smoke and integration tests; evidence is prepared |
| W13 | Technical review | Review demonstration and technical questions are completed; feedback is recorded |
| W14 | Technical improvements | High-priority review feedback and release blockers are addressed |
| W15 | User acceptance and release candidate | UAT, regression, security and deployment checks are completed |
| W16 | Final release | All agreed features are complete; release build is deployed and documented |

### Key milestones

| Milestone | Target |
|---|---|
| Shared architecture and contracts confirmed | End of W6 |
| Integrated application skeleton | End of W7 |
| Core module features implemented | End of W9 |
| Full end-to-end workflow | End of W11 |
| Technical review candidate | End of W12 |
| **Technical review** | **W13** |
| Review feedback and critical fixes | End of W14 |
| Release candidate and UAT sign-off | End of W15 |
| **Feature completion and release** | **W16** |

### Feature scope and cut order

The team should protect the end-to-end core workflow before adding stretch features.

**Must-have for Week 16 release:**

- Resident complaint submission and reference number.
- Officer case management and multilingual case support at the agreed level.
- Cat/chicken image detection with confidence scores.
- Human verification and correction queue.
- Animal detection history and basic profiles.
- Zone management and hotspot visualisation.
- Forecast or risk indicator with clear sample-data disclosure.
- Recommended actions with source references.
- Supervisor approval/decline with reasons.
- Role-based access control and audit records.
- Integrated dashboard, tests, deployment instructions and backups.

**Stretch features, in this cut order:**

1. Live RTSP camera integration.
2. Individual animal re-identification across separate days/cameras.
3. Detailed animal movement paths and floor-level visualisation.
4. Advanced outcome-learning models.
5. Power Automate / external enterprise integrations.
6. Advanced AI assistant and natural-language analytics.

If time becomes limited, cut stretch features before reducing testing, privacy, human approval or core workflow quality.

---

## 11. Release definition and Definition of Done

The Week 16 target is a **feature-complete, production-readiness-level release**. It should not be described as a fully operational EMS production deployment until real data access, infrastructure, privacy/security review and stakeholder approval are obtained.

### Feature Definition of Done

A feature is complete when:

- It works end to end using the agreed real or sample data.
- Its API and data contract are documented.
- It has appropriate automated tests.
- Loading, empty, success and error states are handled in the UI.
- Permissions are enforced on the backend.
- Errors are logged without exposing sensitive information.
- A peer-reviewed pull request is merged into `main`.
- AI outputs show confidence or limitations where relevant.
- Human review is provided for uncertain detections and recommended actions.

### Week 16 release checklist

- [ ] All Must-have user stories are implemented.
- [ ] All four modules are integrated.
- [ ] Resident, officer and supervisor workflows pass end-to-end tests.
- [ ] Backend unit and integration tests pass.
- [ ] Playwright critical user journeys pass.
- [ ] AI model metrics and evaluation datasets are documented.
- [ ] Synthetic-data charts and forecasts are labelled.
- [ ] Low-confidence detections enter human review.
- [ ] Recommendations include verifiable sources.
- [ ] Supervisor approval is required before actions are approved.
- [ ] Authentication, RBAC and backend authorisation are tested.
- [ ] File upload validation and privacy blur workflow are tested.
- [ ] Secrets are stored outside source control.
- [ ] Database backup and restore are tested.
- [ ] Deployment and rollback instructions are documented.
- [ ] Known issues, limitations and release notes are published.

---

## 12. Risks and mitigation

| Risk | Mitigation |
|---|---|
| Not enough chicken or low-light data | Use permitted public datasets and collected footage; label data provenance; apply realistic augmentation and evaluate difficult conditions separately |
| Forecasts rely on synthetic data | Label sample data clearly; report backtest error honestly; do not claim real-world predictive accuracy |
| Modules block each other | Agree contracts, maintain mock APIs and integrate continuously |
| LLM quality on Singlish and Tamil | Create representative test cases, evaluate outputs, use human review and consider a hosted API if permitted |
| Live camera failure during demo | Keep a recorded sample clip as a fallback |
| Privacy / PDPA concerns | Avoid real resident personal data in the prototype; blur people in images; restrict access and define retention rules |
| AI misclassification | Use confidence thresholds, human review and correction records |
| Unreliable recommendations | Require source references, display uncertainty and require supervisor approval |
| Schedule pressure before W13 | Freeze scope for the review candidate at W12; prioritise Must-have workflow |
| Release defects in W16 | Run UAT and regression tests in W15; define rollback and backup procedures |

---

## 13. Repository structure

The proposed structure separates the frontend, backend, AI pipeline, storage, MLOps and deployment configuration while keeping the four Habitat modules identifiable.

```text
animal-monitoring-system/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   └── utils/
│   ├── package.json
│   └── tsconfig.json
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database/
│   │   ├── tasks/             # Celery background tasks
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
│
├── ai/
│   ├── models/
│   ├── training/
│   ├── inference/
│   ├── tracking/
│   └── evaluation/
│
├── modules/
│   ├── a_intake/              # Case analysis and intake
│   ├── b_detection/           # Animal detection and identification
│   ├── c_hotspots/            # Hotspot dashboard and forecasting
│   └── d_actions/             # Recommendations and approval
│
├── storage/
│   ├── images/                # Local development only
│   └── videos/                # Local development only
│
├── mlops/
│   ├── mlflow/
│   └── dvc/
│
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── evaluation/
│   └── release/
│
├── docker/
├── tests/
│   ├── integration/
│   └── e2e/
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

Large datasets, trained model weights and uploaded media should not be committed directly to Git. Use DVC for dataset versioning and MinIO for application media storage. Keep secrets in environment variables or an approved secret manager.

## 14. Getting started

### Prerequisites

- Git
- Docker Desktop with Docker Compose
- Node.js (LTS)
- Python version agreed by the team
- Sufficient disk space for sample images, video clips and model weights

### Run the application

```bash
git clone <repo-url>
cd animal-monitoring-system
cp .env.example .env
docker compose up --build
```

Example local development addresses (confirm the actual ports in `docker-compose.yml`):

- Web app: `http://localhost:3000`
- FastAPI backend: `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`
- MinIO console: use the port configured in Docker Compose
- Ollama (optional): `http://localhost:11434`

### Environment configuration

Create a `.env` file for local environment-specific settings.

Example:

```env
# Application
APP_ENV=development
SECRET_KEY=replace_with_a_secure_random_secret

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/animal_monitoring

# Redis
REDIS_URL=redis://localhost:6379/0

# Object storage
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=replace_with_local_access_key
MINIO_SECRET_KEY=replace_with_local_secret_key
MINIO_BUCKET=animal-media

# AI model
MODEL_PATH=ai/models/best.pt

# LLM (optional)
OLLAMA_BASE_URL=http://localhost:11434
```

**Security:** Never commit actual passwords, secret keys, API keys, access tokens or production credentials to GitHub. Keep `.env` in `.gitignore` and maintain `.env.example` with placeholder values only.

## 15. Branching and team workflow

- `main` should remain in a deployable or demonstrable state.
- Work on branches such as `feature/a-case-intake` or `fix/b-detection-upload`.
- Submit one pull request per coherent feature.
- Require at least one review from another team member.
- Run relevant tests before merging.
- Update API contracts and documentation when shared behaviour changes.
- Use commit messages such as `feat(b): add detection review queue`.
- Integrate continuously rather than waiting until the technical review week.

---

## 16. Responsible AI, privacy and licensing

- Check the licence of every dataset, model, pretrained weight and dependency. In particular, review the selected Ultralytics YOLO licence and applicable usage terms.
- Use only permitted public, synthetic or team-collected sample data.
- Do not use real resident personal data in the prototype without approval.
- Blur people in submitted photographs where applicable.
- Define access control, retention and deletion procedures for uploaded media.
- Keep an audit trail for case corrections, AI outputs and supervisor decisions.
- Show confidence and uncertainty; do not present model predictions as confirmed facts.
- Every AI recommendation must be reviewable and traceable to its supporting sources.
- A human officer reviews detections and a supervisor approves actions.
- Clearly distinguish prototype results from validated operational performance.

---

## 17. Project success criteria

By the end of Week 16, Habitat should demonstrate one integrated workflow:

1. A resident submits a community-animal complaint.
2. The system creates a case and reference number.
3. The AI analyses the complaint and detects an animal in the submitted image.
4. An officer verifies or corrects the detection.
5. The case contributes to zone-level hotspot analysis and forecasting.
6. The system recommends an action with supporting guidance.
7. A supervisor approves or declines the recommendation with a recorded reason.
8. The application stores the outcome and displays the updated case and dashboard status.

**Target release:** End of Week 16 — a feature-complete, tested and deployable MVP / production-readiness-level product, with any external production dependencies and limitations clearly documented.
