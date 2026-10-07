# Company page schema

A company page follows this order and leaves out a section it has nothing
for. Time order holds inside every section. The infobox sets
`schema=company-2026`. Companies only: First Nations, unions, Crown
agencies and advocacy bodies are not written to this schema.

Infobox (`{{Organization}}`): `name`, `org_type` (one of: integrated forest
products, lumber, pulp and paper, panels, logging, holding company, private
equity fund, pension fund, sovereign fund, state enterprise, co-operative,
trading, other), `seat` and `incorporated_in` (`Country` or
`Country / Province`, the country first: `Canada / British Columbia`,
`Japan`; never `British Columbia, Canada` — the analysis reads the country
before the slash; the country is its common short name with no commas:
`South Korea`, not `Korea, Republic of`), `listings` (an exchange code, a space and the years,
`;` between listings; the range uses a hyphen, never an en dash:
`TSX 1983-2006; NYSE 2021-`; the codes the analysis
recognises are TSX, TSXV, VSE, ME, CSE, NYSE, NASDAQ, AMEX, TSE, LSE, SGX
and HKEX; a widely held company listed only elsewhere is placed by its
seat),
`controller_type` (only when control ends at
this entity: family, individual, private equity fund, pension fund,
sovereign fund, state, co-operative, First Nation, other; never `widely held`: the analysis decides whether a company is widely held year by year), `founded_date`
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
     three rows with its date. Never a span. Every row has `as_of`.
     `equity_pct` and `voting_pct`
     are digits (`18.4`); give `voting_pct` only when the source gives
     votes. `source` holds `{{Cite|…|quote=…}}` with no `<ref>`.
   - One `{{Control claim|controller=|basis=|as_of=|as_of_precision=|start_date=|start_date_precision=|end_date=|end_date_precision=|claimant=|source=}}`
     per source that says who controlled the company, then
     `{{Control claims}}`. `basis` is one of: voting majority, dual-class,
     largest block, joint, agreement, board, state, not stated. Give
     `as_of` when the source states control at a date, `start_date` (and
     `end_date` if it gives one) when it states a span; never both, and
     never `as_of` with `end_date`; an `end_date` is not before its
     `start_date`. Every date is `YYYY-MM-DD` (or `YYYY`, `YYYY-MM`). Each precision is day, month, year or circa, and a year-only
     date is written as `YYYY-01-01` with precision year (as on `Stake` rows,
     whose `precision` works the same way). Joint
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

Serial sources. When a Source page is created for an edition of a serial
publication (Statistics Canada's *Inter-corporate Ownership* above all;
also annual directories such as the *Financial Post Survey*), record three
things so the analysis can carry its claims from one edition to the next.
On the edition's `{{Source}}` infobox: `series=` the series' name, spelt
the same way on every edition (`series=Inter-corporate Ownership`), and as
`publication_date` the edition's original publication date, when it first
appeared, not the date of a reprint, scan or archive copy. Then one
`{{Control claim}}` row for each company the edition names, citing that
edition's page, with `as_of` the year the edition reports, its reference
year (1972 for the 1972 volume, even if it appeared in 1975), not the year
it was published. Every edition read is its own Source page with its own
rows, even when the controller has not changed. The analysis lets such a
claim stand until the series' next edition (never more than five years) or
until a later year's own evidence decides control, and it finds the
editions by that name and those dates, so without them a claim covers only
its own year.

Holders and controllers. Every `holder=` and `controller=` names an entity
page by its exact title: never a redirect or another spelling (a
lower-case first letter, underscores, a short form), because the analysis
joins a row to its page by exact title and a near miss cuts the chain
there; `stakecheck` reports one as `REDIRECT`. State control names
`[[Government of British Columbia]]` (an existing organization page; give
it `controller_type=state` when you edit it) or the relevant government's
own page, never a place page such as `[[British Columbia]]`. When a holder
or controller has no page, create it in the same tick: a short page with the
`{{Organization}}` or `{{Person}}` infobox, one cited lead sentence, and
nothing else. An Organization page carries `seat` and, when its sources say
so, `controller_type`; a Person page carries `residence` (and `nationality`
when given). A person always ends a chain of control, so a Person page
needs no controller type. A family that controls a company as a group is an
organization page with `controller_type=family`, linked to its members.

Relationship rows that are spans. An acquisition, a merger, a rename or a
sole owner over stated dates stays a relationship row (`acquired`,
`merged_into`, `renamed_to`, `owned_by`), because a source gives its span.
A `holds_shares_in` row is converted to `{{Stake}}` rows on the company's
page, one per date its sources observe, and the relationship row removed.

The wiki page `ForestWiki:Company page` carries this for human editors;
when this file changes, that page changes in the same commit.
