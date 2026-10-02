# Tenure page schema

A tenure page follows this order and leaves out a section it has nothing
for. Time order holds inside every section. The infobox sets
`schema=tenure-2026`.

Infobox (`{{Tenure}}`): `tenure_id`, `tenure_type`, `status`, `holder`,
`holder_since` (+precision), `area_ha`, `area_date`, `aac_m3`, `aac_date`,
`district`, `granted_date` (+precision), `ended_date` (+precision),
`schema=tenure-2026`. Holder, area and cut are the dated tables below
summarised: state each once in its table and copy the current value here.
A number in the infobox is digits with thousands separators, `152,000`;
an approximation is written `~152,000`; words like "nearly" stay in prose.

Body, with these exact headings:

1. (no heading) Lead: one paragraph — what the licence is, where, who holds it and since when, roughly how large, how it came to be.
2. `== History ==` The narrative by era in time order: the grant, who held it and how it passed, what was taken out and added, the people, companies, events and disputes that shaped it, each linked. Subsections by era are allowed (`=== 1953 to 1961 ===`).
3. `== Holders ==` `{| class="wikitable"` with `! From !! To !! Holder !! How !! Source`; one row per holding; at most one sentence of context per row below the table.
4. `== Area and boundary ==` `! Date !! Describes !! Source`, then the changes in time order.
5. `== Allowable annual cut ==` `! Effective !! m³ a year !! Source`, then why the cut moved.
6. `== Instruments ==` `! No. !! Date !! What it did !! Source`; one row per instrument; no prose.
7. `== Overlapping territories ==` the First Nations named by the determinations, as a list, each linked.
8. `== Controversies ==` disputes on the record, one sentence each, attributed, linking to where History tells it.
9. `== Recent developments ==` dated items only, newest first; an item older than a year moves into History.
10. `== Open questions ==` one question per line, each naming what would answer it. This section replaces every "No source found gives X" sentence.
11. `{{Relationship}}` rows, then `{{Entity footer}}`.

A source cell holds `<ref>{{Cite|…|quote=…}}</ref>` like any sentence.
A date in a table is written year first, `1961-05-18`, or `1961` when only
the year is known; prose keeps "18 May 1961".

Holders are the licensees the licence documents name. A change in who
owns a licensee — a company bought by another — is told in History and
carried by the `owned_by` rows, not by a Holders row, unless a licence
document names the new owner as licensee. A licence that has ended sets
`ended_date` in the infobox, `status` says how (cancelled, surrendered,
amalgamated into …), and the last Holders row ends on that date.

A row in the cut table is one determination with one effective date and
one figure; a span of years or a range of figures is prose, not a row.
The infobox's `aac_m3` is the latest row. The infobox's `area_date` is the
date the figure was measured — the map or determination that states it —
not the date of the document that reports it.

The Holders table and the relationship rows agree: every holder in the
table has a `holds_tenure` row, which lives on the holder's page with the
tenure as its object. Adding or correcting that row on the holder's page
is part of writing the tenure page.
The wiki page `ForestWiki:Tenure page` carries this for human editors;
when this file changes, that page changes in the same commit.
