<!--
Sync Impact Report
- Version change: 1.0 (legacy) -> 1.0.0
- List of modified principles:
    - Business First -> Offline-First & Windows Native
    - Spec-Driven Development -> Spec-Driven Development (Retained/Refined)
    - AI Safety & Integrity -> Financial Integrity & Offline AI
    - Model-Agnostic Architecture -> Modular Feature Toggles
    - Security by Design -> Role-Based Access Control (RBAC)
    - Clear Separation of Concerns -> Rebrandable Architecture
- Added sections: Rebrandable Architecture, Financial Integrity
- Removed sections: E-commerce specific AI behavioral rules (Personality, Sales Ethics)
- Templates requiring updates:
    - ✅ .specify/templates/plan-template.md (Logic alignment)
    - ✅ .specify/templates/spec-template.md (Requirement alignment)
    - ✅ .specify/templates/tasks-template.md (Task categorization)
- Follow-up TODOs: None.
-->

# Project Constitution
## Modern Business Automation System (MBAS)

Version: 1.0.0
Status: Active
Ratification Date: 2026-03-04
Last Amended: 2026-03-04
Authority: Governs all architectural and development decisions for the MBAS project.

---

# 1. Purpose

This constitution defines the guiding principles, engineering standards, and development discipline for the Modern Business Automation System (MBAS). It ensures the system remains modular, secure, and reliable for small and medium businesses operating in offline environments.

All development decisions MUST align with this constitution.

---

# 2. Core Principles

## 2.1 Offline-First & Windows Native

The system MUST operate entirely without internet connectivity.
- Rationale: Target businesses (retail, pharmacies, etc.) often require 100% uptime regardless of connectivity.
- Requirement: All dependencies, including database and optional AI modules, must be local.

---

## 2.2 Spec-Driven Development (SDD)

No feature is implemented without a written specification and implementation plan.
- Rationale: Prevents scope creep and ensures architectural consistency.
- Requirement: All functionality must be defined in `/specs/[feature]/spec.md` and `/specs/[feature]/plan.md` before coding begins.

---

## 2.3 Modular Feature Toggles

The system MUST support Basic, Standard, and Premium packages via a single codebase using feature toggles.
- Rationale: Simplifies maintenance and provides a clear upgrade path for customers.
- Requirement: Feature flags stored in the `Settings` table must gate both UI elements and backend business logic.

---

## 2.4 Role-Based Access Control (RBAC)

Access to modules and data MUST be strictly enforced based on user roles (Admin, Manager, Sales User).
- Rationale: Protects sensitive financial data and system settings.
- Requirement: Logic-level checks must verify permissions even if the UI component is hidden.

---

## 2.5 Financial Integrity & Data Safety

The system MUST use database transactions for all operations involving billing, stock updates, and payments.
- Rationale: Prevents data corruption and ensures accurate financial reporting.
- Requirement: Atomic operations for sales (deduct stock + record sale + update customer balance).

---

## 2.6 Rebrandable Architecture

The system MUST be easily rebrandable for multiple businesses without code changes.
- Rationale: Enables resale and multi-branch deployments.
- Requirement: Business name, logo, currency, and tax settings must be dynamically loaded from the `Settings` table.

---

# 3. Engineering Standards

## 3.1 Tech Stack Discipline

- **Database**: SQLite (or local SQL Server) for reliable offline storage.
- **Architecture**: Modular design with clear separation between UI, Business Logic, and Data Access.
- **Security**: Passwords must be hashed using industry-standard algorithms (e.g., BCrypt). No secrets in source code.

## 3.2 Error Handling & Resilience

- System MUST handle local IO failures gracefully (e.g., disk full, database locked).
- All critical errors MUST be logged locally for diagnostic purposes.
- UI must never crash due to an unhandled exception.

## 3.3 Testing Standards

- Every feature MUST include automated tests (Unit and/or Integration).
- Financial calculations (tax, totals, discounts) must have 100% test coverage.

---

# 4. Governance & Versioning

## 4.1 Amendment Procedure

Changes to this constitution require a version increment:
- **MAJOR**: Backward incompatible governance or principle removals.
- **MINOR**: New principles or material expansions.
- **PATCH**: Clarifications and non-semantic refinements.

## 4.2 Compliance Review

Every `/sp.plan` must include a "Constitution Check" section to verify alignment with these principles.

---

END OF CONSTITUTION