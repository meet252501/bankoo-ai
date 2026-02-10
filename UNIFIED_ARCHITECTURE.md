# Bankoo AI: Unified Architecture Documentation

## Overview
Bankoo AI has been upgraded from a multi-service microservices architecture to a **Unified Monolithic Architecture**. All AI agents (Movies, Analytics, Market, Vision, Docs) are now integrated into a single Python backend (`bankoo_main.py` + `api_hub.py`).

## Core Changes

### 1. Single Server Backend
- **File:** `bankoo_main.py`
- **Role:** The central Flask server running on port `5001`.
- **Integrations:** Imports `api_hub.py` which contains the logic for all agents.
- **Endpoints:**
    - `/api/send_input`: Universal intent routing (Chat, Movies fallback, Vision control).
    - `/api/upload_pdf`: Doc-Genius PDF ingestion.
    - `/api/upload_dataset`: Zenith Analytics CSV ingestion.
    - `/api/market/...`: Market Insight endpoints (Stock Summary, Financials).
    - `/api/run_code`: Studio IDE execution engine.

### 2. Unified API Hub
- **File:** `api_hub.py`
- **Role:** A single class-based module that acts as the "Brain" for specific domains.
- **Components:**
    - `DocIntelligence`: Handles RAG and PDF logic.
    - `ZenithAnalytics`: Handles Student Performance ML.
    - `CineMatch`: Handles Movie APIs and Logic.
    - `MarketInsight`: Handles Yahoo Finance Data.
    - `VisionAgent`: Handles MediaPipe Hand Tracking (runs in a separate daemon thread when activated).

### 3. Frontend Integration
- **File:** `bankoo_ui.html`
- **Updates:** Now directly calls the main backend endpoints. The "Market" view has been added and fully integrated with the new API.

### 4. Simplified Startup
- **Script:** `START_BANKOO.bat`
- **Function:** Launches `bankoo_main.py`. No need to launch separate servers for each agent.
- **Launcher:** `bankoo_launcher.py` handles the desktop window and lifecycle.

## How to Run
1. **Shortcut:** Double-click the **Bankoo AI** desktop shortcut.
2. **Manual:** Run `START_BANKOO.bat`.

## Verification
- Run `RUN_TESTS.bat` to verify all agent endpoints are responding correctly.

## Deprecated Folders
The following folders in `backend/` are no longer actively used by the runtime but contain the original logic sources:
- `backend/movies` (Logic imported via `api_hub`)
- `backend/analytics` (Logic imported via `api_hub`)
- `backend/market` (Replaced by `MarketInsight` class in `api_hub`)
