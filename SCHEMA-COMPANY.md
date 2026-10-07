# Company page schema

A company page follows this order and leaves out a section it has nothing
for. Time order holds inside every section. The infobox sets
`schema=company-2026`. Companies only: First Nations, unions, Crown
agencies and advocacy bodies are not written to this schema.

Infobox (`{{Organization}}`): `name`, `org_type` (one of: integrated forest
products, lumber, pulp and paper, panels, logging, holding company, private
equity fund, pension fund, sovereign fund, state enterprise, co-operative,
trading, other), `seat` and `incorporated_in` (`Country` or
`Country / Province`: `Canada / British Columbia`, `Japan`), `listings`
(`TSX 1983-2006; NYSE 2021-`), `controller_type` (only when control ends at
this entity: family, individual, private equity fund, pension fund,
sovereign fund, state, co-operative, First Nation, other), `founded_date`
and `dissolved_date` (+precision), `status`, `schema=company-2026`. Leave
`jurisdiction` as it is; do not add one. Who controls the company is never
typed into the infobox: the infobox reads it from the analysis.

Body, with these exact headings:

1. (no heading) Lead: one paragraph — what the company is or was, where,
   who controlled it as the sources say, and its scale.
2. `== History ==` The narrative by era, in time order, every sentence
   cited. No inference: who controlled the company is told only as a
   source tells it, attributed. Subsections by era are allowed.
3. `== Ownership and control ==`
   - One `{{Stake|holder=|as_of=|precision=|equity_pct=|voting_pct=|share_class=|shares=|approx=|source=}}`
     per holder per source observation, then `{{Stake chart}}`. A stake is
     an observation at a date: a proxy circular listing three holders is
     three rows with its date. Never a span. `equity_pct` and `voting_pct`
     are digits (`18.4`); give `voting_pct` only when the source gives
     votes. `source` holds `{{Cite|…|quote=…}}` with no `<ref>`.
   - One `{{Control claim|controller=|basis=|as_of=|start_date=|end_date=|claimant=|source=}}`
     per source that says who controlled the company, then
     `{{Control claims}}`. `basis` is one of: voting majority, dual-class,
     largest block, joint, agreement, board, state, not stated. Give
     `as_of` when the source states control at a date, `start_date` (and
     `end_date` if it gives one) when it states a span; never both. Joint
     control is one row per controller, each `basis=joint`. A source that
     disagrees with another is written as its own row; never drop a claim
     because another source says otherwise.
   - `{{Resolved control}}` last. The analysis fills it; write nothing
     about it.
   - At most a short paragraph of prose, cited, on what the rows do not
     show.
4. `== Corporate lineage ==` `{{Lineage}}` only. It is generated from the
   `renamed_to`, `merged_into`, `consolidated_into`, `acquired` and
   `subsidiary_of` rows; to change it, write or correct those rows.
5. `== Tenures ==` `{{Tenures held}}`, generated from `holds_tenure` rows,
   then at most a few sentences. To change the table, correct the rows.
6. `== Mills and operations ==` `{{Facilities owned}}`, generated from the
   facilities' `owned_by` rows, then prose on what they made.
7. `== Controversies ==` as on tenure pages.
8. `== Recent developments ==` as on tenure pages.
9. `== Open questions ==` one question per line, each naming what would
   answer it. Questions about ownership and control name the filing or
   compilation that would settle them.
10. `{{Relationship}}` rows, then `{{Entity footer}}`.

Holders and controllers. Every `holder=` and `controller=` names an entity
page. When it has none, create it in the same tick: a short page with the
`{{Organization}}` or `{{Person}}` infobox carrying `seat` or `residence`
and, when its sources say so, `controller_type`, one cited lead sentence,
and nothing else. A family that controls a company as a group is an
organization page with `controller_type=family`, linked to its members.

Relationship rows that are spans. An acquisition, a merger, a rename or a
sole owner over stated dates stays a relationship row (`acquired`,
`merged_into`, `renamed_to`, `owned_by`), because a source gives its span.
A `holds_shares_in` row is converted to `{{Stake}}` rows on the company's
page, one per date its sources observe, and the relationship row removed.

The wiki page `ForestWiki:Company page` carries this for human editors;
when this file changes, that page changes in the same commit.
