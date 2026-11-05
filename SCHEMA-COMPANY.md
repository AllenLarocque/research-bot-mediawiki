# Company page schema

A company page follows this order and leaves out a section it has nothing
for. Time order holds inside every section. The infobox sets
`schema=company-2026`. Companies only: First Nations, unions, Crown
agencies and advocacy bodies are not written to this schema.

Infobox (`{{Organization}}`): `name` (the official legal name, below),
`former_names`, `also_known_as`, `org_type` (one of: integrated forest
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
`jurisdiction` as it is; do not add one. Leave `sector` and `kind` as
they are unless the brief asks for them; their lists are in
`SCHEMA-ENTITIES.md`. Who controls the company is never
typed into the infobox: the infobox reads it from the analysis.

Title and names. A company's page is titled by its common name (operator,
2026-11-05): the name the held sources use most for it in its British
Columbia forestry role. It carries no legal suffix unless a tiebreak below
adds one (`Doman-Western Lumber`, `Skeena Cellulose`, `Canfor`).

- The count is made, not guessed. For each candidate name, count the held
  sources that name the company by it while describing its forestry in the
  province; names that differ only in a legal suffix, "&" against "and",
  or a leading "The" are one name. Record the counts and the sources in
  the dossier's `names.md`, one line per name: the name, the count, the
  sources. A name clearly leads when its count is at least half again the
  next one's (9 against 6 leads; 8 against 6 does not).
- Tiebreak 1, the longest-borne name. When no name clearly leads, the
  title is the name the company bore longest while it held tenure or ran
  mills in British Columbia, measured from the dated names in
  `former_names` and its tenure and facility rows. BC Timber was Canadian
  Cellulose Company, Limited (1973 to 1980 or 1981), BC Timber Ltd. (to
  1984) and Westar Timber Ltd. (from 1984) while it held TFL 1 and TFL 23,
  so, absent a clear count, it is titled by the Canadian Cellulose name.
- Tiebreak 2, collisions. When that title is held by another subject, add
  the legal suffix (`Weyerhaeuser Canada Ltd.` if `Weyerhaeuser Canada`
  were taken); when that is also taken, a year bracket (`Western Forest
  Products (1980)`).

`name` (Full name) is the official legal name, current if the company
still operates and last if it closed, with its source, so `name` and the
title usually differ. Which name is official is a sourced fact (a register
record, an annual report, the *Gazette*, a statute or order, a licence
document); with none, `name` stays as it is and `questions.md` gets
`Official name unknown: <title>: <what was tried>`. Every other name is
kept: `former_names` lists earlier official names with their dates at the
precision the source gives, `Name (start–end)` separated by semicolons, and
`also_known_as` the names in common use, separated by semicolons. A
company's earlier name lives in `former_names`, never on a page of its own.
Each of those names, and the official name in `name` where it differs
from the title (controller, 2026-11-05), has a redirect to the page unless
another subject holds that title: that name gets no redirect, a line in the page's `questions.md`
(`Name taken: <name>: <the page that holds it>`), and the operator decides.
The bot creates a redirect for an earlier, common or official name only
when a brief tells it to; the dev side creates the rest (its names
backfill for `former_names` and `also_known_as`).
The lead names the company in bold by its title's name, then gives its
official name, then its earlier official names with their years, then any
other names in common use: "'''Doman-Western Lumber''' (officially WFP
Western Lumber Ltd. from 2005; earlier 472138 B.C. Ltd. and 4018982 Canada
Inc.) was …". Prose then uses the title's name, so most links need no pipe
(`STYLE.md` rule 12). A page is moved to the title its count gives only by
the stack's rename pass, from a titles list the operator approves row by
row, never by a brief. A newspaper or journal a company publishes is titled
by its masthead, not by the company's name, and the company is its owner
(`SCHEMA-ENTITIES.md`, "Names outside government"; operator, 2026-11-02).

Body, with these exact headings:

1. (no heading) Lead: one paragraph — what the company is or was, where,
   who controlled it (cited, under STYLE rule 7), and its scale.
2. `== History ==` The company's story for a general reader, by era, in
   time order, every sentence cited: what it made and where it logged,
   milled and sold; the licences it worked; the people who led it; its
   workers, unions, strikes, accidents and closures; the communities and
   First Nations its operations touched;
   environmental disputes and regulation; markets and the turning points of
   its business. Ownership appears only at the
   moments that changed the company — its founding, a takeover or merger, a
   reorganisation, becoming public or private — in a sentence or two, with
   no percentage the Ownership tables carry. Subsections by era are allowed;
   headings name the era or the event, never the source. History opens with prose before its first subsection. A conclusion is a
   source's, attributed (STYLE rule 7).
3. `== Financial history ==` Three to five paragraphs in broad strokes,
   every sentence cited: the turning points in money, such as public
   listings, takeovers, the largest gains and losses, and the periods of
   heavy investment or retreat. The detail goes on the Financial history
   page (below). Control is told only as a source tells it, attributed.
   Where an official compilation's classification of the company's control
   differs from a large holding on the page, or from what other sources
   say, Financial history tells both, each attributed to its source, and
   does not choose between them; the analysis follows the classification by
   its stated rule. The section ends with the line `Year by year:
   [[<Company>/Financial history]].`
   History and the Financial history page are done when every era of the company's life (from its founding to its dissolution, or to 2025) is told by at least one cited source, or the company's `questions.md` has a line `History thin: <era>` saying what was tried. A `History thin` line is only for an era whose sources were tried and could not be reached or held nothing on it: a source you can name and reach is read and cited, not listed; the line names each source tried and why it failed. Then move on.
4. `== Ownership and control ==`
   - One `{{Stake|holder=|as_of=|precision=|equity_pct=|voting_pct=|share_class=|shares=|approx=|source=}}`
     per holder per source observation, then `{{Stake chart}}`. A stake is
     an observation at a date: a proxy circular listing three holders is
     three rows with its date. Never a span. Every row has `as_of`.
     `equity_pct` and `voting_pct`
     are digits (`18.4`); give `voting_pct` only when the source gives
     votes. `source` holds `{{Cite|…|quote=…}}` with no `<ref>`.
   - A stake the source says is held for outside clients or their managed funds takes
     `for_clients=yes`. Not for a holding a company's manager holds for a
     fund that company sponsors and manages for itself (Brookfield's Tricap
     Management for the Tricap Restructuring Fund): that is the fund's own
     stake, written with the fund as holder, and the fund's page carries a
     `{{Control claim}}` naming its sponsor from the source that says so.
     A holding on conversion or exercise of a security,
     or an "effective interest" through one, takes `potential=yes`. A
     source saying that no holder other than those it names at that date
     held more than a stated per cent is one row with no holder and no
     figure, written beside the named holders' own rows and citing the
     same source: `{{Stake|none_above=10|as_of=|precision=|source=}}`. A
     proxy circular's statement that, except as set out, no person holds
     more than 10 per cent is such a row, written beside the holders it
     names, citing the same circular.
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
   - A source that gives a country of control and names no controller is
     `{{Control claim|country=Japan|basis=not stated|as_of=|source=}}`,
     never joint; give `controller` or `country`, not both.
   - `{{Resolved control}}` after the control claims. The analysis fills
     it; write nothing about it.
   - Then `{{Board summary}}`; see Boards below. The order is: stakes,
     Stake chart, control claims, `{{Resolved control}}`, `{{Board summary}}`.
     Board rows and `{{Board chart}}` are not on the company page.
   - At most a short paragraph of prose, cited, on what the rows do not
     show. Longer financial narrative goes on the Financial history page
     (`[[<Company>/Financial history]]`).
5. `== Corporate lineage ==` `{{Lineage}}` only. It is generated from the
   `renamed_to`, `merged_into`, `consolidated_into`, `acquired` and
   `subsidiary_of` rows; to change it, write or correct those rows.
6. `== Tenures ==` `{{Tenures held}}`, generated from `holds_tenure` rows,
   then at most a few sentences. To change the table, correct the rows.
7. `== Mills and operations ==` `{{Facilities owned}}`, generated from the
   facilities' `owned_by` rows, then prose on what they made.
8. `== Disputes ==` Optional; see Disputes below. It goes after whichever of Tenures or Mills and operations comes last on the page (operator, 2026-10-28).
9. `== Recent developments ==` as on tenure pages.
10. `{{Relationship}}` rows, then `{{Entity footer}}`.

The Financial history page. `<Company>/Financial history`
(`Canfor/Financial history`) carries the detail the company page's Financial history leaves
out. It opens with a lead line naming the company and linking its page.
Then it gives the play-by-play by era, in short paragraphs, every sentence
cited: how the company was financed and capitalised, its share issues,
listings and delistings, debt, recapitalisations, insolvencies and
restructurings, takeovers and the stakes that decided them, and what each
meant for the company, as a source says. Headings name the era, never the
source. Each era is followed by tables of the yearly series its sources
give: sales, earnings, long-term debt, capital spending, duties, employees,
production. A table is one row per year, with a citation per row
(`<ref>{{Cite|…|quote=…}}</ref>` in its source cell), and holds only the
figures the sources state: nothing computed is added, a figure no source
gives is a blank cell, never filled from a neighbouring year, and a year
with no stated figure has no row.
The figures written in sentences move into those tables, and the sentences
left say what the figures show, under STYLE rule 13. The Ownership tables
hold every stake observation, so the page does not restate them. The page
ends with `{{Entity footer}}`.

Interpretation. A company page tells the company's story as a coherent
narrative without inventing one. STYLE rule 13 says what that allows:
saying what the cited figures show, an explanation a source gives,
attributed to it, and ordering events so they read as a sequence. It never
allows a cause, motive or consequence no source states, a "because", "so",
"led to" or "in response to" joining two facts no source joins, or a
characterisation no source makes. Before publishing, reread every
sentence that links two events and confirm that a cited source makes the
link.

Disputes. `== Disputes ==` is optional, never required. It is used where
the record holds a dispute worth telling, and left out where it does not,
with no note of its absence. It covers labour disputes, land and title
disputes, court cases, blockades, protests, regulatory hearings and
environmental findings: one or two sentences each, linking to where History
tells it. The section is historical, and it neither takes sides nor avoids
the events. Each position is attributed to whoever held it (the company, a
union, a Nation, a court, protesters, the Province), the events are told
plainly, and no outcome is called right or wrong in the wiki's voice.
MacMillan Bloedel's would tell Clayoquot Sound. Tenure pages use the same
section under the same rule.

Mills by name. Every mill or plant History or Mills and operations mentions
is named by the name its cited sources use (the Quesnel sawmill, Eburne sawmill) and
linked when it has a page. A mill in British Columbia that the company
owned and that has no page gets a facility page in the page shape of
`RULES-FORESTRY-WIKI.md`: the `{{Facility}}` infobox with `facility_type`
and any other field a source gives, one cited lead sentence, its `owned_by`
row naming the company, dated and cited as the source gives it, and a
`located_in` row where a source names the place.
A mill outside British Columbia is named but gets no page.

A company and its mill (operator, 2026-10-28). A company that ran a single
mill, and the mill itself, are two pages even when the sources call both by
one name (Skeena Sawmills, North Central Plywoods). The company keeps its
Organization page with its own rows: tenures, stakes, receivership,
lineage. The physical mill gets a facility page, titled by place and kind
("Terrace sawmill", "Prince George plywood mill", with the operator in
brackets when that title is taken), and it carries the `owned_by` and
`operated_by` rows. The two pages link to each other. Never put the mill's
`owned_by` row on the company's Organization page.

A company's owner is not an `owned_by` row either (operator, 2026-11-05).
The Ownership and control rows carry who owned and controlled a company;
the control analysis reads them and does not read `owned_by`, so an owner
written only as `owned_by` is missing from it. An `owned_by` row found on a
company's Organization page, sole owner or majority owner, is converted,
then removed, in one save of that page:

- Its facts become a `{{Control claim}}` from the same sources, naming the
  owner as `controller` and keeping the row's dates (`start_date`,
  `end_date` and their precisions, under the rules of "Ownership and
  control"), with the `basis` its sources support (a government owner is
  `state`; else `not stated` unless they give votes, a board or an
  agreement).
- And a `{{Stake}}` row from the same sources, `as_of` the date a source
  observes the holding (the row's start date where the source dates the
  holding from it), where a source gives a figure: all the shares is
  `equity_pct=100`. A source that gives no figure gets no Stake row (a
  Stake with no figure is a `stakecheck` finding); the Control claim
  carries it alone.
- The row's note keeps its qualification ("majority owner, not sole
  owner"): in the rows where a field holds it (`equity_pct`, `approx`,
  `basis`), and otherwise in a cited sentence of the section's short prose.
- The end of the holding is carried by the row that records the change (a
  sale's `subsidiary_of` on this page, or the buyer's `acquired`), or,
  where no such row exists, by that cited sentence. No row is written on
  another page to carry it.
- A Relationship row may carry `sources=` with no quote; the Control
  claim and the Stake row each cite with a quote, found in the source's
  capture (`quotegate` checks it). The converted rows carry no
  verification, so the brief that converts a row lists its verification
  state before, for it to be verified again.
- Then the `owned_by` row is removed.

A publication's page is the exception: it carries `owned_by` its
publishing company (operator, 2026-11-02; `SCHEMA-ENTITIES.md`, "Names
outside government"). A First Nation's page, or a company a Nation owns or
runs, is not converted while the First Nations hold stands.

Relationships named in the text. Every relationship between two entities
that History or Financial history states (a joint venture, a partner, a
parent, an acquisition, a supplier contract) is also a cited
`{{Relationship}}` row where a predicate covers it. Otherwise it is a line
in the company's `questions.md`.

No talk of sources. A page never describes its own sources or its method
("as its sources saw it", "the sources record"). It states what is known
and cites it.

Paragraphs. Short ones. A paragraph with more than about five figures
belongs in a table.

Research for History. History is researched like ownership: fetching is
allowed for it, under the research rules. Look, in this order: company
histories and anniversary publications; scholarship (Hayter, Rajala,
Marchak, Drushka, Mackay, theses); the press (the BC newspapers the corpus
already uses, trade press such as the *Truck Logger* and *BC Lumberman*);
union and labour records; government reports and royal commissions; BC
Archives and university special collections finding aids, where they can be
reached (`SOURCES-FORESTRY.md` lists the hosts that cannot). A Nation is named, and an event involving it told, only as a cited source records it, the sentence or citation making clear whose record it is (Crown, company, court, the Nation's own); no statement about title, territory or consent except quoted and attributed; link a Nation's existing page, and write no content on a First Nation's page or on a company a Nation owns or runs (no prose, no `sector` or `kind`, no infobox value, no new such page, no move of one) until `ForestWiki:First Nations and Indigenous knowledge` is settled in a session of its own; mechanical bookkeeping there (a title-only rewrite of a renamed page's title, a redirect, a date precision set to what the date as written already says) is allowed. Follow
`ForestWiki:First Nations and Indigenous knowledge`.

No "Open questions" section: what is not known goes in the dossier's
`questions.md` (STYLE rule 8). A question about ownership or control there
names the filing or compilation that would settle it.

Boards. A board is recorded as rosters: one `{{Board seat}}` row per
director per source date, on the company's board page, `<Company>/Board`
(`Canfor/Board`), never on the company page, which carries
`{{Board summary}}` in `== Ownership and control ==` where the chart was. A
roster listing seven directors is seven rows with the same `as_of`. The
benchmark years are every fifth year from 1950 to 2025 (1950, 1955, … 2025).
For each benchmark year a company was alive, look for a roster from a source
dated within a year either side (Y-1 to Y+1); a source further off does not
stand in for the benchmark. Rows are dated by what the source gives, never
moved to the benchmark year. A roster on a document or page a tick reads
anyway is written too, at its own date. Any other roster seen in a held
source and not written is a line in the company's `questions.md`: `Held, not
written: <document>, roster at <date>.` Do not search for rosters outside the
benchmark windows. A roster known to exist in a document the dossier does not hold, found while working a benchmark year, is a `Not held, on Wayback: <document>` (or other location) line. A benchmark year with no roster inside the window is a
line in the company's `questions.md`, naming the filing or directory that
would give it.

The parameters, exactly: `person` (the director's page, an exact title),
`as_of` (`YYYY-MM-DD` or the shorter forms, the date the source gives the
roster at), `precision` (day, month, year or circa; day if left out), `seat`
(`chair`, `vice-chair`, `director`, or `none` for an officer the source shows
with no board seat), `office` (an executive title, one of `ceo`, `president`,
`vice-president`, `executive-vice-president`, `treasurer`, `secretary`,
`general-manager`, `chairman`, `vice-chairman`; leave it out when the source
gives none), `independent` (`yes` only when the source calls the director
independent, by name or by a count that names its exceptions: "9 Directors,
7 of whom are independent", naming the two who are not, calls the other
seven independent; otherwise leave it out), `nominee_of` (the page title of the
holder or company that nominated the director), `residence` (as printed in
the source, `Vancouver, B.C.`), `shares` (digits, the director's holding where
the source gives it), `cite` (the exact title of the Source page; required),
`p` (the pinpoint) and `quote` (the source's exact words for this director,
the roster line or the heading that dates it; required). `cite`, `p` and
`quote` are plain text, never a `{{Cite}}`: a stored citation is expanded, and
550 of them took Canfor past the page's include limit. The chart cites each
roster once; the quote is not printed. Several quotes from one document are
joined with ` … ` in one `quote`, with their pinpoints joined `, ` in `p`. A
second document giving the same roster at the same date is `cite2`, `p2` and
`quote2`, rarely needed.

The board page. In order: the lead line `The board of directors of
[[<Company>]].`; `== Board structure ==`, a narrative of how the board was
set up and changed: its size and the number of seats the articles allow,
nomination rights (a shareholder agreement giving a holder seats), classes
of directors, staggered terms, independence, the chair and the CEO. Each
turn of the story is its own short paragraph, every sentence cited, under
STYLE rule 13, nothing inferred from the rows; the section is left out when
no source describes the board's structure or its committees, with a line in `questions.md` naming what
would (`Board structure: <document that would say>`). Inside it,
`=== Committees ===` has one subsection per committee (Audit, Governance,
Compensation and so on). Each says what the committee is for and when it
was seen, and has a table of members by year: `! Year !! Members !! Source`,
one row per year a source lists them, with a citation per row (`<ref>{{Cite|…|quote=…}}</ref>` in the source
cell). Then `== Composition ==` with
`{{Board composition}}` (added before `== Rosters ==` if the board page lacks it, a company stamped after the move); `== Rosters ==` with the rows and `{{Board chart}}`;
`{{Entity footer}}`. Nothing else goes on it.

Chair and chairman. `chair`, as `seat`, is a board seat a source
establishes; `chairman`, as `office`, is a title a source uses without
establishing a seat. A roster that lists the board under its chairman
establishes `seat=chair`. A source that calls someone chairman of a
company or of its board with no roster ("He stepped down as chairman of the
board in 2009"; "Chairman, Petro-Canada Inc."; "the present Chairman of
Western") establishes the seat too: `seat=chair|office=chairman`, and a
vice-chairman's `seat=vice-chair|office=vice-chairman` (operator's ruling,
2026-10-23). An association's or council's chairman is the same. An
honorary chairman holds no board seat unless the source also lists the
person as a director; the post is told in prose, and no `{{Board seat}}` row
records it. A list headed "Directors" lists a director (operator,
2026-11-05): a person in a roster the company heads "Directors" is listed
as a director, whatever title the roster gives beside the name, so George
A. Pope, Jr., "Honorary Chairman of the Board" in Pope & Talbot's 1974
directors list, gets a `{{Board seat}}` row with `seat=director`, and the
honorary post is told in prose. An honorary title the person holds
elsewhere (J. A. Taylor's "Honorary Chairman, Canada Trust" in MacMillan
Bloedel's 1979 report) is the person's other post, not a seat on this
company's board.

A row is a sighting, never a term. The source saw this person on this board
at this date; it does not say when the seat began or ended. Write no start or
end, and in prose say "seen", never "served" or "from … to". The analysis
reads the sightings together and does not infer a term from them.

Other directorships. When a source gives a director's other boards, each is
recorded by the other company's page and industry, with that source and its
date, not as a list on this page. A company that already has a page, whatever
its industry, takes `{{Board seat}}` rows on `<Company>/Board`; only a company
with no page and outside the covered industries is an other board. The tests
run in that order: has a page, board seat; covered industry, page (created if
needed) and board seat; otherwise an `{{Other board}}`. The industries the wiki covers are forestry, taken
broadly: timber, lumber, pulp, paper, panels and wood products; non-timber
forest products; companies built on forest products or supplying the forest
industry (pulp-mill chemicals, pulp-based products); and forestry industry
bodies (associations, councils, research institutes, lumber trade bodies). A
company of a covered industry that the bot will not research is not collected
for its own roster, but its rows go on `<Company>/Board`, which has the lead
line, `== Rosters ==` with the rows and `{{Board chart}}`, and
`{{Entity footer}}` only; its own page gets `{{Board summary}}` in a
`== Board ==` section before its `{{Relationship}}` rows (adding a
`== Board ==` section if it has none) and nothing else changes on it. If it has
no page, one is created as before (its name, its `seat` infobox field where it
is managed from, an `{{Organization}}` infobox and one cited lead sentence),
plus `{{Board summary}}` in `== Board ==`.

Any other company (no page, outside the covered industries) gets no page. The row is
`{{Other board|company=<usual name without legal suffix>|...}}` on the
director's own page, immediately before `{{Entity footer}}`, with no heading
and no `person` parameter (the page is the person). It takes the board seat
fields (`as_of`, `precision`, `seat`, `office`, `independent`, `nominee_of`,
`residence`, `shares`, `cite`, `p`, `quote`, `cite2`, `p2`, `quote2`) and is
a sighting like any other. Name the company exactly as `Analysis:Other boards`
names it if it is listed there, so the same company is one entry. When unsure
whether a company is in a covered industry, write the other board and a line in
the `questions.md` of the company in hand: `Other board or page? <company>: <why
unsure>`. Never create a page for a company outside the covered industries. The
industries covered will grow (fisheries is expected); a promoted company's rows
then move to its board page. A page that already exists stays. After writing
other board rows, purge the person page, `Analysis:Other boards` and `Analysis:Board interlocks`, and run
`python3 /tools/seatcheck.py --page "<person>"`: it reports NO-COMPANY (no
company named), OTHER-HAS-PAGE (the company has a page, so the row belongs on
its board page) and OTHER-ON-WRONG-PAGE (the row is not on a person's page).

Director pages. A director, or a `nominee_of` company, with no page gets a
Person page (an Organization page for a nominating company) made like a
holder's: one cited lead sentence; `residence` where the roster prints it, written in the infobox form
`Country / Province` (`Canada / British Columbia`) from the printed place;
`gender` only from a source's own words, cited; nothing else. The page title
is exact, never a redirect, for both `person` and `nominee_of`. Directors
are not part of the ownership chain rule. A nominating shareholder is the one
exception to the other boards rule: `nominee_of` names the holder that
nominated the director, and a holder of a forest company is part of the
ownership record, so a nominating holder with no page gets an Organization page
(name, `seat`, one cited sentence) whatever its industry.

Same person, initials only (operator's ruling, 2026-10-22). Two board rows
name one person when they are on the same company's board, the surname is
the same, every initial matches the first letters of the fuller name's given
names in order (T. and Takahiro; R. B. and Robert Blake), the two sightings
are within ten years of each other, and no source tells them apart (two
people with that initial on one roster, or different residences or employers
stated for the same date). A printed "Jr." tells two people with the same
initials apart, so one roster's "H. H. Ketcham, Jr., chm." and "H. H.
Ketcham, pres." do not block a merge: the second is matched to its own full
name (Henry Holman Ketcham III). A source dating the full-name director's seat
("Director Since 27 July 1977") on or before a sighting of the initials page
on the same board settles the pair beyond ten years (operator's rulings,
2026-10-23). Then there is one Person page, titled with the fullest name a source gives; the initials-only page becomes a redirect to it,
and every row's `person` names the full-name page. The page says so in one
sentence, citing the roster that gives only the initials: "T. Endo is taken to
be Tomoaki Endo because the board, surname and initial agree within ten years."
A pair that fails any test stays two pages, with a line in the company's `questions.md` as before. A
spelling that differs (Noboyuki and Nobuyuki) is not an initial and is not
merged by this rule.

Same person, different boards (operator, 2026-11-05). The initials rule
covers one company's board. Across boards, a matching name, full or
initialled, is never enough: two sightings on different companies' boards
are one person only when a source names the person with something that
ties the two sightings together (an employer, an office, a residence or a
career move). Then they merge as the initials rule merges: one Person page
under the fullest name a source gives, the other page a redirect to it,
every row's `person` naming the kept page, and one sentence on it citing
the linking source. Otherwise they stay two pages, with a `questions.md`
line naming the source that would settle it. A false merge pools two
people's seats, and the boardroom network is drawn from exactly those rows.
B. I. Howe and Bruce I. Howe are one person by BCRIC's Annual Report 1980
(Bruce Howe came "from MacMillan Bloedel where he was President and Chief
Operating Officer"); R. G. Williston and Ray Williston, and William Brown
and William C. Brown, stay two pages until a source links them.

`nominee_of` only where the source says the shareholder nominated the
director; sharing a surname or sitting for the same company is not enough. A
`{{Control claim|basis=board}}` only where a source says a shareholder's
nominees hold a majority of the board, written as the source says it. Control is never inferred from a
board: no count of seats, no interlock and no chair makes a claim.

Before a company is finished, `python3 /tools/seatcheck.py --page "<company>"`
must report no finding. It checks the company page and its board page: that
the parameters are in their vocabularies, that every row has a date, a `cite`
and a `quote`, the chair and chairman ruling, and that no board row is on the
company page (rows there are a finding). A finding the sources cannot settle
is a line in `questions.md` and is named in the handover. Run it with the
other page gates, `stakecheck` and `holdcheck`, and with `expandsize`, which
must not name the company page or the board page. After rows change on a board page, purge (null-edit) the company page and the board page: Cargo does not invalidate the pages that query it, so the company page's `{{Board summary}}` keeps the old count, years and latest chair until purged.

Tenure holdings. The cut attribution runs on the company's `holds_tenure`
rows, so a wrong date gives a controller cut it never held. A row belongs to
the licensee the licence documents name, never to its parent: the parent is
reached through control rows, and a parent's row for a subsidiary's licence
counts the cut twice. A row now on a parent's page for a subsidiary's licence
moves to the subsidiary's page when the company is worked. For every
tenure the company held, check its row against the tenure page's Holders
table and the licence documents and instruments already captured: correct
the start and end dates, add a missing row, and move a row held by a
predecessor or subsidiary to the page that held the licence. A licensee
named by a document that has no page gets one only when it is a company
the round will reach; otherwise the gap is a line in the company's
`questions.md`. `python3 /tools/holdcheck.py --page "<company>"` must report
no OVERLAP, OUTSIDE-LIFE, OPEN-AFTER-END or NO-START on the company's own
rows before the company is finished; a finding the sources cannot settle
is a line in `questions.md` and is named in the handover. A company brief
may also correct the Holders table of a tenure page whose `holds_tenure`
rows it corrected, citing the same sources; nothing else on that tenure
page.

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
claim stand until the series' next edition (never more than five years past
its as_of), unless a later year's own evidence decides otherwise, and it
finds the editions by that name and those dates, so without them a claim
covers only its own year. A company whose line sits below a parent
corporation in the edition's enterprise listing is controlled by that
parent: the claim names the parent (the corporation at the level above),
with `basis=not stated` unless the edition gives one. A `country=` claim is
only for an edition that gives a country of control and places the company
under no controlling corporation.

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
On that holder's own page, fill `seat`, `incorporated_in`, `listings`,
`controller_type` and a stake or control row only for holders the analysis
can name as controller: 20 per cent or more at some observation, or named
in a control claim; except that a sponsor's fund always carries the Control
claim naming its sponsor (see `for_clients`). Any other holder's page gets
`seat` only for an organization and `residence` only for a person, when its
source gives it.
A Person page may carry `gender`, recorded only from a source's own words (an
honorific, a pronoun or a statement), never from a name: `woman`, `man`, or
the source's own word, cited to the source whose words give it. Where no
source says, leave it out.

Relationship rows that are spans. An acquisition, a merger or a rename
stays a relationship row (`acquired`, `merged_into`, `renamed_to`), because
a source gives its span. A company's owner, sole or not, is written as
Stake and Control claim rows, and an `owned_by` row on its page is
converted ("A company and its mill").
A `holds_shares_in` row is converted to `{{Stake}}` rows on the company's
page, one per date its sources observe, and the relationship row removed.

The wiki page `ForestWiki:Company page` carries this for human editors;
when this file changes, that page changes in the same commit.
