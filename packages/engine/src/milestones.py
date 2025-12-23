from .types import (
    BountyEvent,
    HostMonthRow,
    MilestoneDefinition,
    MilestoneLedgerEntry,
    to_decimal,
)


def _milestone_reached(host: HostMonthRow, milestone: MilestoneDefinition) -> bool:
    if milestone.milestone_type == "beans_threshold":
        return host.beans >= milestone.threshold_value
    if milestone.milestone_type == "month_count":
        return host.host_active_months >= milestone.threshold_value
    raise ValueError(f"Unknown milestone type: {milestone.milestone_type}")


def derive_milestone_ledger_entries(
    month: str,
    hosts: list[HostMonthRow],
    milestones: list[MilestoneDefinition],
    existing_ledger_keys: set[tuple[str, str]],
) -> list[MilestoneLedgerEntry]:
    entries: list[MilestoneLedgerEntry] = []
    for host in hosts:
        for milestone in milestones:
            key = (host.host_id, milestone.milestone_code)
            if key in existing_ledger_keys:
                continue
            if not _milestone_reached(host, milestone):
                continue
            entries.append(
                MilestoneLedgerEntry(
                    host_id=host.host_id,
                    milestone_code=milestone.milestone_code,
                    achieved_month=month,
                    recruiter_id=host.recruiter_id,
                    amount_usd=to_decimal(milestone.amount_usd),
                )
            )
    return entries


def ledger_entries_to_bounty_events(entries: list[MilestoneLedgerEntry]) -> list[BountyEvent]:
    events: list[BountyEvent] = []
    for entry in entries:
        event_id = f"{entry.achieved_month}:{entry.host_id}:{entry.milestone_code}"
        events.append(
            BountyEvent(
                event_id=event_id,
                month=entry.achieved_month,
                host_id=entry.host_id,
                recruiter_id=entry.recruiter_id or "",
                milestone_code=entry.milestone_code,
                amount_usd=entry.amount_usd,
                note=None,
            )
        )
    return events
