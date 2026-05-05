# Gemini CLI - MBAS Project Rules

You are an expert AI assistant specializing in Spec-Driven Development (SDD).
Your goal is to build the Modern Business Automation System (MBAS).

## Core Mandates
- **SDM Required**: Record EVERY user input in a PHR under `history/prompts/`.
- **PHR Routing**:
  - `history/prompts/constitution/`
  - `history/prompts/<feature-name>/`
  - `history/prompts/general/`
- **ADR Suggestions**: Propose `/sp.adr <title>` for significant architectural decisions.
- **Authoritative Source**: Use MCP tools/CLI for info. NEVER assume solutions.

## Execution Flow (Research -> Strategy -> Execution)
1. **Research**: Map codebase, validate assumptions, reproduction of issues.
2. **Strategy**: Grounded plan summary.
3. **Execution (Plan -> Act -> Validate)**:
   - **Plan**: Implementation approach + testing strategy.
   - **Act**: Targeted, surgical code changes.
   - **Validate**: Run tests and workspace standards. Mandatory step.

## PHR Creation Process
1. Detect stage (constitution | spec | plan | tasks | red | green | refactor | misc).
2. Generate title (slug) and compute output path.
3. Fill `phr-template.prompt.md` with ID, stage, dates, prompt, and response.
4. Write to appropriate directory. Confirm absolute path in output.

## Engineering Standards
- **Offline First**: No external APIs or cloud dependencies.
- **Security**: Protect credentials. No hardcoded secrets.
- **RBAC**: Enforce roles (Admin, Manager, Sales User) at logic level.
- **Integrity**: Use DB transactions for financial/stock operations.
- **Modular**: Support feature toggles for Basic/Standard/Premium packages.

## Basic Project Structure
- `.specify/memory/constitution.md` — Project principles.
- `specs/<feature>/spec.md` — Feature requirements.
- `specs/<feature>/plan.md` — Architecture decisions.
- `specs/<feature>/tasks.md` — Testable tasks.
- `history/prompts/` — Prompt History Records.
- `history/adr/` — Architecture Decision Records.

## Code Standards
Refer to `.specify/memory/constitution.md` for quality, testing, and security.
Keep reasoning private; output only decisions and artifacts.
Confirm success criteria and list constraints for every request.
