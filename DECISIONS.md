# Engineering & Architectural Decisions

## Decision 1: Domain Focus (Human-in-the-Loop Catalog Operations Desk)
Instead of building a generalized e-commerce mock platform, I chose to solve a specific, high-friction operational bottleneck: supplier inventory data ingestion. This domain allows for a clear demonstration of how deterministic backend validations interface with unstructured language generation models.

## Decision 2: Decoupled Multi-Mode AI Architecture
To guarantee 100% operational uptime, the AI layer (`services/ai_assistant.py`) is decoupled from hard vendor dependencies. 
* **Design Pattern:** Circuit Breaker / Failover Gateway.
* **Implementation:** The system dynamically sniffs for an active `OPENAI_API_KEY`. If present and responsive, it leverages structured data extractions via `Pydantic` and `Instructor`. If the external endpoint experiences network timeouts or rate-limiting thresholds (`HTTP 429`), it triggers a zero-latency fallback to internal deterministic template engines.

## Decision 3: Deterministic vs. Heuristic Separation
A common anti-pattern in AI engineering is using LLMs for tasks easily solved by basic code logic. 
* **Rule:** If a validation check can be calculated using discrete mathematics or data frames (e.g., checking if a SKU is a duplicate via a hash map or calculating if a price float is negative), it belongs exclusively to the **Pandas validation layer**.
* **AI Allocation:** LLM processing power is reserved strictly for unstructured linguistic analysis—summarizing errors for operator logs and drafting contextual, human-like supplier messages.

## Decision 4: Pydantic Data Contract Enforcement
Unstructured text from standard AI API wrappers introduces systemic fragility to backend databases. To prevent formatting anomalies or broken JSON blocks, the application uses **Pydantic V2 schemas** mapped through an entry proxy. The backend enforces a strict data contract on the model output before it ever touches the UI or exporting pipelines.
