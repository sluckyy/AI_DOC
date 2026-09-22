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


class Module(BaseModel):
    module: str
    version: str
    status: Literal["grounded", "first_draft"]
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
    alert_acknowledgement_timeout_s: int = 120
    escalation: dict[str, dict[str, EscalationRoute]]
    clinical_parameters: dict[str, dict[str, Any]] = Field(default_factory=dict)   # D-45: owner-set; pending until set
    helplines: dict[str, str] = Field(default_factory=dict)
    disclosure: dict[str, str]


class PhrasingItem(BaseModel):
    id: str
    text: str


class Phrasings(BaseModel):
    opening: list[PhrasingItem]
    invitations: list[PhrasingItem]
    facilitators: list[PhrasingItem]
    summary: dict[str, str]
    read_back: dict[str, str]
    final_something_else: str
    deflect: dict[str, str]
    explain_why: dict[str, str] = Field(default_factory=dict)


class ContentBundle(BaseModel):
    modules: dict[str, Module]
    context: ContextModule
    parameters: Parameters
    phrasings: Phrasings
    lexicon: list[str]
    scripts: dict[str, str]
    versions: dict[str, Any]
