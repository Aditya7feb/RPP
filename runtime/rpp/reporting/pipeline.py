"""Reporting pipeline (Phase D).

The Master Agent drives this pipeline at the reporting phase, invoking the
Reporting capabilities in canonical order and consuming their outputs by
reference. The pipeline is read-only over Findings, Risk, and Evidence; it never
creates or mutates them. Canonical Risk remains owned by the Domain Security
tiers; any figure computed here is presentation-only.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..orchestration.state import AssessmentStore
from ..schemas import new_id, utc_now

_SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4}


@dataclass
class Report:
    """A generated report that references canonical objects by identifier."""

    assessment_id: str
    report_id: str = field(default_factory=lambda: new_id("report"))
    generated_at: str = field(default_factory=utc_now)
    correlated_finding_ids: list[str] = field(default_factory=list)
    prioritized_finding_ids: list[str] = field(default_factory=list)
    severity_counts: dict[str, int] = field(default_factory=dict)
    evidence_bundle_ids: list[str] = field(default_factory=list)
    executive_summary: str = ""
    technical_summary: str = ""
    schema_version: str = "1.0.0"


class ReportingPipeline:
    """finding-correlation -> risk-analysis -> report-generation -> evidence-bundle."""

    def run(self, store: AssessmentStore) -> Report:
        report = Report(assessment_id=store.assessment_id)

        # 1. finding-correlation: deduplicate by (title, cwe, target-agnostic key).
        seen: dict[tuple[str, str | None], str] = {}
        for finding_id, finding in store.findings.items():
            key = (finding.title, finding.cwe)
            if key not in seen:
                seen[key] = finding_id
        report.correlated_finding_ids = list(seen.values())

        # 2. risk-analysis: prioritise (presentation-only) and count severities.
        correlated = [store.findings[fid] for fid in report.correlated_finding_ids]
        correlated.sort(key=lambda f: _SEVERITY_ORDER.get(f.severity, 5))
        report.prioritized_finding_ids = [f.finding_id for f in correlated]
        counts: dict[str, int] = {}
        for finding in correlated:
            counts[finding.severity] = counts.get(finding.severity, 0) + 1
        report.severity_counts = counts

        # 3. evidence-bundle: assemble evidence referenced by prioritised findings,
        #    plus all collected evidence for completeness.
        report.evidence_bundle_ids = store.evidence_ids()

        # 4. report-generation: executive and technical summaries (by reference).
        total = len(report.prioritized_finding_ids)
        report.executive_summary = (
            f"Assessment {store.assessment_id}: {total} correlated finding(s); "
            f"severity distribution {counts or '{}'}. "
            f"{len(report.evidence_bundle_ids)} evidence artifact(s) collected."
        )
        report.technical_summary = (
            f"{len(store.responses)} agent response(s) recorded across "
            f"{len(store.tasks)} task(s). Evidence and findings are referenced by "
            f"identifier; canonical Risk remains owned by the Domain Security tiers."
        )
        return report
