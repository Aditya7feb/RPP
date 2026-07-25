# Master Agent Operational Checklist

**File:** `agents/master/checklist.md`

**Version:** 1.0.0

---

# Purpose

This document defines the operational checklist for the Master Agent.

The checklist SHALL be used before

- Starting an assessment
- Executing tasks
- Requesting validation
- Generating reports
- Closing an assessment

The objective is to ensure every assessment is complete, consistent, evidence-backed, and compliant with the platform's operating principles.

---

# Assessment Initialization

Before creating an execution plan verify

□ Assessment ID assigned

□ Scope defined

□ Rules of Engagement available

□ Target reachable

□ Available agents discovered

□ Available tools discovered

□ Configuration loaded

□ Previous assessment state restored (if applicable)

□ Required permissions available

---

# Planning Checklist

Before execution verify

□ Target technologies identified (if known)

□ Recon strategy selected

□ Required capabilities identified

□ Dependencies calculated

□ Parallel execution opportunities identified

□ Validation tasks marked

□ Approval gates identified

□ Execution graph generated

---

# Delegation Checklist

Before assigning any task verify

□ Correct capability identified

□ Correct specialist selected

□ Agent available

□ Scope valid

□ Dependencies satisfied

□ Duplicate task does not exist

□ Required inputs available

---

# Execution Checklist

During execution verify

□ Task state updated

□ Runtime monitored

□ Progress tracked

□ Errors captured

□ Timeouts handled

□ Retries follow policy

□ Assessment state updated

□ Newly discovered assets evaluated

---

# Evidence Checklist

For every finding verify

□ Primary evidence collected

□ Supporting evidence collected

□ Evidence hashed

□ Evidence timestamped

□ Source agent recorded

□ Tool recorded

□ Evidence immutable

□ Sensitive data protected

□ Evidence linked to finding

---

# Confidence Checklist

For every finding verify

□ Confidence assigned

□ Confidence justified

□ Evidence supports confidence

□ Independent confirmation evaluated

□ Manual validation considered

□ False positive likelihood assessed

---

# Validation Checklist

Before validation verify

□ Approval required evaluated

□ Approval obtained

□ Approval not expired

□ Scope revalidated

□ Read-only validation confirmed

□ Validation agent assigned

---

# Communication Checklist

Verify

□ Task IDs valid

□ Assessment ID present

□ Correlation ID present

□ Message version supported

□ Required fields present

□ Status transition valid

□ Evidence references valid

---

# Report Merging Checklist

Before requesting report generation verify

□ Duplicate findings merged

□ Duplicate recommendations merged

□ Technologies merged

□ Attack surface complete

□ Evidence preserved

□ Confidence recalculated

□ Root causes identified

□ Attack chains generated

□ Traceability maintained

---

# Reporting Checklist

Before report generation verify

□ Assessment completed

□ Mandatory tasks completed

□ Outstanding failures reviewed

□ Approval workflow complete

□ Evidence complete

□ Confidence complete

□ Findings categorized

□ Risk summary generated

□ Recommendations consolidated

---

# Completion Checklist

Before closing an assessment verify

□ All executable tasks completed

□ Remaining tasks intentionally skipped

□ Failures documented

□ Evidence archived

□ Findings finalized

□ Assessment state updated

□ Report generated

□ Audit trail complete

---

# Failure Review Checklist

For every failed task verify

□ Failure recorded

□ Root cause identified

□ Retry evaluated

□ Remaining execution unaffected

□ Human intervention required evaluated

---

# Security Checklist

Verify

□ Scope respected

□ Rules of Engagement respected

□ No destructive actions executed

□ Approval policy enforced

□ Sensitive data protected

□ Evidence integrity preserved

□ Audit trail maintained

---

# Quality Checklist

The assessment SHALL satisfy

□ Complete coverage of planned activities

□ No duplicate findings

□ No unsupported findings

□ Every finding references evidence

□ Every conclusion is explainable

□ Every recommendation maps to one or more findings

□ Assessment is reproducible

□ Report is internally consistent

---

# Definition of Done

An assessment coordinated by the Master Agent is considered complete only when

- Planning completed successfully
- Execution completed successfully
- Evidence collected and validated
- Confidence calculated
- Findings merged
- Validation completed or explicitly skipped
- Reports generated
- Audit trail preserved
- No unresolved mandatory tasks remain

---

# Compliance Statement

A Master Agent implementation is compliant with this specification when every checklist item in this document can be satisfied or explicitly justified as not applicable.

Failure to satisfy mandatory checklist items SHALL prevent the assessment from being marked as complete.