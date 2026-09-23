"""Content-layer schema: the Framework Specification's slot schema as Pydantic models.

Nothing here is prose the agent reads at runtime. Modules are data; the prose in the
library is for reviewers.
"""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

SlotClass = Literal["coverage", "discriminating", "red_flag", "context"]
ValueType = Literal["yes_no", "enum", "set", "text", "clock_time", "number"]
Tier = Literal["immediate", "same_day", "flag"]


class Phrasing(BaseModel):
    id: str
    form: Literal["open", "closed"] = "open"
    text: str
    use_when: str | None = None


class Option(BaseModel):
    id: str
    synonyms: list[str] = Field(default_factory=list)


class ValueSpec(BaseModel):
    type: ValueType
    options: list[Option] = Field(default_factory=list)


class Extraction(BaseModel):
    yes_terms: list[str] = Field(default_factory=list)
    no_terms: list[str] = Field(default_factory=list)
    unknown_terms: list[str] = Field(default_factory=list)   # D-39: "asked, unknown" is a third state, distinct from denied


class Evidence(BaseModel):
    lr: str | None = None
    discriminates: str | None = None
    citation: str | None = None
    grade: str | None = None
    population: str | None = None
    note: str | None = None
    gap: bool = False
    gap_reason: str | None = None


class Slot(BaseModel):
    id: str
    slot_class: SlotClass = Field(alias="class")
    required: bool = False
    intent: str
    phrasings: list[Phrasing] = Field(default_factory=list)
    value: ValueSpec
    extraction: Extraction | None = None
    evidence: Evidence | None = None
    verbatim: bool = False
    negative_reporting: Literal["explicit", "omit"] = "omit"
    stigmatised: bool = False
    preamble: str | None = None
    prefill_from: list[str] = Field(default_factory=list)
    confirm: bool = False
    gates: list[str] = Field(default_factory=list)
    delegated_observation: bool = False
    absolute_time: bool = False
    disclosure_group: str | None = None   # F-36: substance, sexual, continence, risk
    always: bool = False                  # gating/closing: asked of everyone (dialogue pack 13.1)
    asked_when: str | None = None         # answer-driven branch (F-13): a rule expression over filled slots; false skips the slot as not applicable
    none_terms: list[str] = Field(default_factory=list)      # text slots: an answer matching one of these is recorded as the value "none"
    asked_if_mentioned: list[str] = Field(default_factory=list)    # asked only when a prior answer in this interview mentions one of these terms
    skipped_if_mentioned: list[str] = Field(default_factory=list)  # PMH named-condition sweep: skipped when the condition already surfaced
    recipient_key: str | None = None      # D-47: a situational item is asked only where parameters name a recipient for a positive answer
    repeat_over: str | None = None        # D-38: asked once per item named in the listed slot's answer; phrasing may use {item}
    pass_on_consent: bool = False         # D-47: after a substantive answer, ask whether it may be passed on; a no keeps it out of the record
    instrument: str | None = None         # validated instrument this item belongs to (administered verbatim, never scored: F-21, D-41)
    route_to: dict[str, str] = Field(default_factory=dict)   # review of systems: option id -> presentation module to activate (F-10, D-37)
    read_back: bool = False               # closing-section slot included in the spoken read-back (D-55)
    packet_check: str | None = None       # F-17: the line that offers a look at the packet when the name is unknown

    model_config = {"populate_by_name": True}


class AlertSpec(BaseModel):
    include_verbatim: bool = True
    template: str


class RedFlag(BaseModel):
    id: str
    fires_when: str
    tier: Tier
    alert: AlertSpec
    suppressible: bool = False
    action: dict[str, str] | None = None
    source: str | None = None

    @model_validator(mode="after")
    def _never_suppressible(self) -> "RedFlag":
        if self.suppressible:
            raise ValueError(f"red flag {self.id}: suppressible must be false (P10)")
        return self


class Closing(BaseModel):
    uncertainty: str
    watch_for: list[str]
    time_course: str
    where: str


class Activation(BaseModel):
    terms: list[str] = Field(default_factory=list)
    fallback: bool = False


ReviewStatus = Literal["first_draft", "grounded", "grounded_thin", "reviewed", "blocked"]
ModuleKind = Literal["presentation", "gating", "closing"]


class Module(BaseModel):
    module: str
    version: str
    status: Literal["grounded", "grounded_thin", "first_draft", "blocked"]
    review_status: ReviewStatus | None = None   # Build Spec A9; derived from status/reviewed/enabled when absent
    kind: ModuleKind = "presentation"          # gating and closing sections share the slot machinery (F-16)
    gating: list[str] = Field(default_factory=list)   # gate.* slot ids this presentation needs asked once
    supersedes: list[str] = Field(default_factory=list)   # modules not to run alongside this one (the unwell child row owns fever, vomiting and rash in a child)
    order: int = 100                      # closing sections run in this order after the presentation modules
    enabled: bool = True   # D-50: a module can be present but not live (e.g. mental health pending specialist input)
    reviewed: bool = False
    reviewed_by: str | None = None
    reviewed_on: str | None = None
    display_name: str | None = None
    review_notes: list[str] = Field(default_factory=list)
    setting: Literal["ed", "gp_booking", "both"] = "both"
    activates_on: Activation = Field(default_factory=Activation)
    slots: list[Slot]
    red_flags: list[RedFlag] = Field(default_factory=list)
    closing: Closing | None = None
    prohibited: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)

    def slot(self, slot_id: str) -> Slot | None:
        return next((s for s in self.slots if s.id == slot_id), None)

    @property
    def effective_review_status(self) -> str:
        """A9: first_draft and blocked never load; grounded/grounded_thin load in simulation; reviewed loads clinically."""
        if self.review_status:
            return self.review_status
        if not self.enabled or self.status == "blocked":
            return "blocked"
        if self.reviewed:
            return "reviewed"
        return self.status


class ContextModule(BaseModel):
    module: str
    version: str
    status: str
    slots: list[Slot]

    def slot(self, slot_id: str) -> Slot | None:
        return next((s for s in self.slots if s.id == slot_id), None)


class EscalationRoute(BaseModel):
    route: str
    patient_message: str = ""
    transfer_target: str | None = None
    unanswered: str | None = None


class Parameters(BaseModel):
    deployment: str
    version: str
    owner: str = ""
    languages: list[str]
    language_names: dict[str, str] = Field(default_factory=dict)
    continue_after_immediate_alert: bool = False
    saturation_invitations: int = 3
    silence_end_of_turn_ms: int = 1200
    silence_end_of_turn_ms_by_register: dict[str, int] = Field(default_factory=dict)   # N-3: longer for slow speakers
    initial_silence_timeout_ms: int = 8000        # how long to wait for speech to start before the turn times out
    asr_low_confidence_threshold: float = 0.6     # N-9: per-utterance confidence below this is flagged to the clinician
    alert_acknowledgement_timeout_s: int = 120
    escalation: dict[str, dict[str, EscalationRoute]]
    clinical_parameters: dict[str, dict[str, Any]] = Field(default_factory=dict)   # D-45: owner-set; pending until set
    closing_read_back: bool = True          # D-55: Framework read-back vs dialogue pack 13.4 "no closing summary"
    capability_check: bool = True           # dialogue pack 2: hearing, language, someone present
    confidentiality: dict[str, str] = Field(default_factory=dict)   # S-12: scripted per setting from governance; [TBC]
    situational_recipients: dict[str, str | None] = Field(default_factory=dict)   # D-47: domain -> who receives a positive answer at the site; None = not asked
    family_history_thresholds: dict[str, Any] = Field(default_factory=dict)      # D-39: guideline thresholds the handover names when a pattern crosses them
    helplines: dict[str, str] = Field(default_factory=dict)
    disclosure: dict[str, str]


class PhrasingItem(BaseModel):
    id: str
    text: str
    enabled: bool = True          # a frozen research id may be present but not selectable (D-54)
    note: str | None = None


class Phrasings(BaseModel):
    """The dialogue pack as data. Open-phase ids (OP-n) are the research instrument (F-9) and are frozen."""
    opening: list[PhrasingItem]
    invitations: list[PhrasingItem]
    facilitators: list[PhrasingItem]
    transition: list[PhrasingItem] = Field(default_factory=list)
    summary: dict[str, str]
    read_back: dict[str, str]
    final_something_else: str
    deflect: dict[str, str | list[str]]        # one line or a validated variant set per key (dialogue pack 9 [VARIANT])
    deflect_triggers: dict[str, list[str]] = Field(default_factory=dict)
    explain_why: dict[str, str] = Field(default_factory=dict)
    capability: dict[str, str] = Field(default_factory=dict)
    recovery: dict[str, str] = Field(default_factory=dict)
    what_next: list[PhrasingItem] = Field(default_factory=list)
    time: dict[str, str] = Field(default_factory=dict)

    def deflection(self, key: str, n: int = 0) -> str:
        """The n-th variant for a key (rotating), so a persistent asker never hears the identical line twice running."""
        v = self.deflect.get(key) or self.deflect.get("serious")
        if isinstance(v, list):
            return v[n % len(v)] if v else ""
        return v or ""


class ContentBundle(BaseModel):
    modules: dict[str, Module]
    context: ContextModule
    parameters: Parameters
    phrasings: Phrasings
    lexicon: list[str]
    scripts: dict[str, str]
    versions: dict[str, Any]
    prohibited: list[dict[str, str]] = Field(default_factory=list)   # dialogue pack 12 / C5 lint source
