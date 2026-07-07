# Value Discovery & Prioritization Report
**Client Industry:** Food & Beverage (Coffee Roastery)
**Business Department:** Order Management & Invoicing

---

## 1. Executive Summary & Business Context
Our primary objective is to eliminate manual bottlenecks, reduce costly roasting errors, and improve customer satisfaction for complaining partner cafes. The current manual process depends on transcribing highly informal, mixed-language Zalo messages into a paper notebook under extreme time pressure (6 AM), which directly leads to wrong-roast errors twice a month.

---

## 2. As-Is Process vs. To-Be Vision

```mermaid
graph TD
    subgraph As-Is Process (Manual & Error-Prone)
        A1[Receive Informal Zalo Message] --> B1[Manual Transcription to Notebook at 6 AM]
        B1 --> C1{Manual Roast Allocation}
        C1 -->|Errors 2x/Month| D1[Roast Wrong Amount/Type (Cost: 2-3M VND)]
        C1 --> E1[Create Excel Invoice & Confirm manually]
    end

    subgraph To-Be Process (AI-Automated & Reliable)
        A2[Receive Informal Zalo Message] --> B2[AI Agent Parses Message via Zalo API]
        B2 --> C2[AI Validates against Historical Order Patterns]
        C2 --> D2[Automatic Sync to Excel & Instant Cafe Confirmation]
        D2 --> E2[Clean Daily Roast Sheet Generated (Zero Errors)]
    end
```

---

## 3. Value Discovery & Impact Matrix

| Use-Case Area | Feasibility | Business Value | Estimated Time Savings | Financial Impact | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Option A: Zalo Automated Extraction & Validation** | **High** (Zalo API + LLM parsing is mature) | **High** (Eliminates 100% of wrong-roast errors) | Saves ~1.5 hours daily | Saves 4 - 6 Million VND/month (from wasted roasts) | **High Priority (Immediate Win)** |
| **Option B: Excel Invoice Auto-Generation & Push** | **Medium** (Requires clean upstream data) | **Medium** (Improves customer experience) | Saves ~30 mins daily | Indirect value (reduces customer churn) | **Phase 2** |

---

## 4. Recommended Starter Area
We recommend starting with **Option A: Zalo Automated Extraction & Validation**.
* **Why:** This directly targets the 6 AM bottleneck, eliminates the 2-3M VND/occurrence roasting errors, and ensures clean, structured data is ready before invoicing or confirmation occurs.
