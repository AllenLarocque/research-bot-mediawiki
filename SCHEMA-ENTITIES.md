# Office, document, event and organisation page schema

This file holds the controlled vocabularies every organisation, event and
document page takes, and the page shapes of offices, documents, events and
organisations that are not companies. A forest-industry company is written
to `SCHEMA-COMPANY.md` and takes `sector` and `kind` from the lists here; a
tenure is written to `SCHEMA-TENURE.md` and takes neither. A page of these kinds is written only when
a brief asks for one. Time order holds inside every section, and a page
leaves out a section it has nothing for. These infoboxes carry no `schema=`
stamp.

## The vocabularies

A value comes from these lists, spelt exactly as here, lower case where
they are. A new value is a deliberate addition to the list, made here and
in the stack's `Module:ForestWiki-config` together, never written ad hoc.
A subject no value fits leaves the field blank and gets a line in its
`questions.md`: `Unlisted <field>: <subject>: <what the sources call it>`.
The infobox files a value off the list in `Category:Pages with an unlisted
type`; it is repaired, not left, except a legacy event type, which the
deploy's backfill repairs (below).

`sector`, where an organisation sits: `forest industry` (taken broadly, as
`SCHEMA-COMPANY.md` defines the covered industries), `government`,
`labour`, `NGO`, `media`, `industry association`, `First Nation`,
`finance`, `education and research`, `diversified`, `other industry`.
`diversified` is a company or holder spanning several unrelated industries
(conglomerates such as Argus, Brascan, Jim Pattison Group); `finance` stays
banks, funds, pension funds, asset and investment managers, custodians and
nominees; a holding company or trust whose holdings are in one industry takes
that industry's sector.

`kind`, what an organisation is:

- companies and finance: `company`, `subsidiary`, `partnership`, `fund`,
  `holding company`, `Crown corporation`, `trust`, `joint venture`,
  `co-operative` (families and estates are given no kind; they carry
  `controller_type`);
- government: `ministry`, `department`, `branch`, `division`, `agency`,
  `commission`, `tribunal`, `board`, `court`, `legislature`,
  `municipality`;
- labour: `union`, `union local`, `federation`, `union auxiliary`;
- associations: `association`, `council`, `advocacy group`, `coalition`;
- media and others: `newspaper`, `broadcaster`, `publisher`, `foundation`,
  `research institute`, `university`;
- Nations: `Nation`, `tribal council`.

`division` is a ministry division headed by an assistant deputy minister (the
Office of the Chief Forester). An assistant deputy minister's title held with
an office is one `held_office` row to the office, the title in its `note`; the
division is not a second office.

`event_type`: `strike`, `lockout`, `blockade`, `protest`, `court case`,
`inquiry`, `commission`, `election`, `fire`, `disaster`, `closure`,
`curtailment`, `scandal`, `forced removal`, `land grant`, `outbreak`,
`campaign` (an organised labour or political mobilisation, e.g. Operation
Solidarity), `split` (a union or organisation dividing, e.g. the 1948 IWA
split).
The older capitalised types ("Strike", "Forest fire", "Royal commission")
are mapped to these by the stack's backfill; an event page still carrying
one is left for it.

`doc_kind`: `act`, `regulation`, `decision`, `report`, `agreement`, `work`.
A `report` includes a royal commission's report; an `agreement` covers
collective agreements, treaties and memoranda; a `work` is a book or
article.

`org_type` stays, with a narrower meaning: on a forest-industry company it
is the industry sub-type `SCHEMA-COMPANY.md` lists. Any other kind of
organisation leaves it blank once `sector` and `kind` are filled.

## Organisation (not a company)

Infobox (`{{Organization}}`): `name`, `former_names`, `also_known_as`,
`sector`, `kind`, `jurisdiction` (a government body only: the level of
government it belongs to, a province or country by its full name, `British
Columbia` or `Canada`, never `BC` or `B.C.`, and a municipality by its
page's exact title), `region` (a body outside government only: its reach in
words, as its sources give it, `Port Renfrew to Nanaimo`, `the BC coast and
the Interior`), `seat`, `founded_date` and `dissolved_date` (+precision),
`status`. No `org_type`.

Body, with these exact headings:

1. (no heading) Lead: one paragraph — what the body is or was, its sector
   and jurisdiction in words, when it was made and by what, and what it
   did.
2. `== History ==` The body's story by era, in time order, every sentence
   cited: what it was made to do, the act or order that made or changed
   it, its renamings and reorganisations, its offices and who held them,
   its work and the disputes it took part in, each linked. Subsections by
   era are allowed; headings name the era or the event, never the source.
   History may open with text before its first era subsection.
3. `== Disputes ==` Optional, under the Disputes rule of `SCHEMA-COMPANY.md`.
4. `{{Relationship}}` rows, then `{{Entity footer}}`.

Titles of government bodies. A government body keeps one page per name,
joined by dated `renamed_to` rows. It is titled by its name as printed, with
its jurisdiction in brackets: `Ministry of Forests and Range (British
Columbia)`. The bracket is added only where the name as printed does
not say where the body is (operator, 2026-11-02): `Forest Practices Board
(British Columbia)` takes it, and `Supreme Court of British Columbia`,
`Court of Appeal for British Columbia`, `Supreme Court of Canada`, `BC Timber
Sales` and `Legislative Assembly of British Columbia` (the legislature's
current official name, its one title in every row and `issuer`) take none. A body with no page is still a row's object, a document's
`issuer` or an office's `organisation`, as a red link in that form:
`Department of Lands (British Columbia)`. A name is dated by the order in
council that constituted it; the name an act continues is a separate fact,
told in History. A name page that continues an earlier body (a renaming)
leaves `founded_date` blank: the `renamed_to` row dates it. Two legal bodies
of the same name are two pages, the earlier with its years: the old forests
ministry (1976–2006, then Forests and Range, then Forests, Mines and Lands,
abolished on 14 March 2011) is `Ministry of Forests (British Columbia,
1976–2006)`, and the current one, which descends from the Ministry of
Natural Resource Operations (2010) through Forests, Lands and Natural
Resource Operations and Forests, Lands, Natural Resource Operations and
Rural Development, is `Ministry of Forests (British Columbia)`. The
Ministry of Natural Resource Operations has its own page, `Ministry of
Natural Resource Operations (British Columbia)`. A body whose
duties pass to another that is not its renaming is `succeeded_by` it, dated
(Forests, Mines and Lands `succeeded_by` Forests, Lands and Natural Resource
Operations, 2011-03-14).

A parent is a dated `part_of` row naming the immediate parent the source
shows, never every body above it, so Forest Branch is `part_of` each
department or ministry it sat in, in turn. A ministry division headed by an
assistant deputy minister is `kind=division`.

A royal commission is an organisation, `sector=government` and
`kind=commission`. It is titled by the name its sources use; a second
commission of the same name is told apart as its sources tell it apart, by
an ordinal or by its years (`Second Sloan Royal Commission on Forest
Resources`). It is `created_by` the order in council that appointed it, not
by the commission issued under the Great Seal. Its commissioner is an
office, `Commissioner of <commission>`, and its report a Document. A party
that made a submission to it is a `submitted_to` row, not
`participated_in`. Court pages (`sector=government`, `kind=court`) are made
by the governance widening.

Names outside government. A company, union, association, NGO or newspaper
has one page, whatever names it has borne, titled by its official legal
name with its legal suffix (`Canfor Corporation`, `Celgar Limited`, `Westar
Timber Ltd.`, if their sources confirm those names; these are examples of
the form, not confirmed titles): the current name if it still operates, its last name if it
closed. Which name is official is a sourced fact, from a register record,
an annual report, the *Gazette*, a statute or order, or a licence document;
with no source for it the page keeps its title and a `questions.md` line
records the gap (`Official name unknown: <title>: <what was tried>`). `name`
is that official name. `former_names` lists its earlier official names,
each with its dates at the precision the source gives, `Name (start–end)`,
separated by semicolons (`Canadian Cellulose Company Limited (1973–1981)`);
`also_known_as` lists the names in common use, separated by semicolons
(`Canfor; Cancel`). Each of those names has a redirect to the page, except
one whose title another subject holds: that gets no redirect and a line in
the page's `questions.md` (`Name taken: <name>: <the page that holds it>`),
and the operator decides. The bot creates a redirect for an earlier or
common name only when a brief tells it to; the stack's rename pass at the
deploy creates the rest. A merger is `merged_into`. Pages are moved to their
official names by the stack's rename pass, never by a brief.

A publication is the exception (operator, 2026-11-02). A newspaper, journal
or magazine is titled by its masthead name, the name it is published under
as its masthead prints it, with no legal suffix; its earlier mastheads go in
`former_names` with their dates, each with its redirect as above. The
company that publishes it is its owner, an `owned_by` row on the
publication's page where a source names a sole or majority owner over
stated dates, and has a page of its own, under its legal name, only where
one is needed. A newspaper's page is the organisation; its articles stay
Source pages.

## Office

One page per office, held in turn by dated holders. Titles:
`Chief Forester of British Columbia`, `Minister of Forests (British
Columbia)`, `President of the IWA`. A royal commission's commissioner is
`Commissioner of <commission>` (`Commissioner of the Sloan Royal Commission
on Forest Resources`). An office is not a board: a board seat
stays a `{{Board seat}}` row (`SCHEMA-COMPANY.md`).

Infobox (`{{Office}}`): `name`, `organisation` (the body the office is part
of today, or last; an exact page title), `created_date` and
`abolished_date` (+precision). Holders are not fields.

Body, with these exact headings:

1. (no heading) Lead: one paragraph — what the office is, the body it is
   part of, when it was created and by what document, and, if it has ended,
   when and how.
2. `== History ==` What the office was for, how its powers changed and who
   held it, by era, in time order, every sentence cited. Each change of
   power is told with the document that made it, linked.
3. `{{Relationship}}` rows, then `{{Entity footer}}`.

Holders. The footer renders a `Holders` section from the people's
`held_office` rows: write no Holders heading or table on the office page.
Each holder is a `held_office` row on the holder's own Person page, with
the office as object. A source that gives a term (a start, an end or both)
is a term: `start_date`, `end_date` and `date_precision` as the source
states them. A source that places a person in the office at one date and
gives no term is a sighting: `attested_date` and `attested_date_precision`,
with no start or end, and in prose "seen", never "served" or "from … to".
Never infer a term from sightings. A term whose end the sources dispute has
`end_disputed=yes` and no `end_date`, printed "to ? (disputed)", with each
reading in `note` and told with its citation in History; never the latest
end, never one chosen. An acting holder's row has `capacity=acting`, printed
"(acting)"; an acting period no source dates is a sighting with
`capacity=acting`. The person's career table shows the row too.

The office's own rows: a dated `part_of` row for each parent, through each
renaming of the parent; `created_by` and `abolished_by` the Document that
made or ended it; `empowered_by` each Document that gave it powers, dated
as the source dates the power. An office's `created_by` is the first act that provides for appointing to it, so [[Chief Forester of British Columbia]] is `created_by` [[Forest Act (1912)]]; each later act under which its holders are appointed is an `appointed_under` row, dated, never a second `created_by`. A document that matters and has no page is
still the row's object, as a red link in the title formats under Document
(an act, a decision, or any other document as its citation gives it),
with no page created for it, as for an amending act below. The office's
`organisation` may name a body with no page, red-linked as "Titles of
government bodies" says.

## Document

One page per governing or landmark text: an act, a regulation, a landmark
decision, a report, an agreement or a work. Titles:

- an act as enacted, with its year: `Forest Act (1912)`, `Forest Act
  (1978)`, `Forest Practices Code of British Columbia Act (1994)`, `Forest
  and Range Practices Act (2002)`. A short title that ends in its year
  moves the year into the brackets: "Forest Act Amendment Act, 1947" is
  `Forest Act Amendment Act (1947)`. Each enactment is its own page; an
  amendment is a row, not a page, unless the amending act is itself a
  subject (below for an amending act with no page). A statute revision
  (R.S.B.C. 1936, 1960, 1996) is not a Document: its text is a Source page
  `text_of=` the act as enacted, and an act repealed under a later name or
  a revision's chapter is still the enacted act's repeal;
- an order in council: numbered, `Order in Council 62 (2011)`, the form the
  corpus's Source pages use (never a slash or a hyphen for the year); known
  only by its date, `Order in Council of 31 December 1943`;
- a report: its title page's title, without the commissioner's style, with
  the title page's year in brackets: `Timber Rights and Forest Policy in
  British Columbia (1976)`, `Report of the Commissioner relating to the
  Forest Resources of British Columbia (1956)` (submitted in 1956, issued in
  1957: the title keeps the title page's year);
- a decision by its style of cause and neutral citation: `Haida Nation v.
  British Columbia (Minister of Forests), 2004 SCC 73`;
- any other document (a regulation, a work) by the title its citation gives
  it, after checking that no existing page already carries it under another
  title.

Infobox (`{{Document}}`): `doc_kind`, `citation` (the statute chapter or
neutral citation), `issuer` (an exact page title, or a red link in the form
"Titles of government bodies" gives: the legislature, court, commission or
author), `submitted_date` (a report submitted apart from its issue: the date
the sources give for the submission), `issued_date` (enactment, judgment or
publication), `in_force_date` and `repealed_date`, each with its precision.

Body, with these exact headings:

1. (no heading) Lead: one paragraph — what the document is, who issued it
   and when, and what it is known for. A decision's first sentence says it
   is the decision and links its case (below).
2. `== What it did ==` What the text did, every sentence cited: what an act
   created, empowered, changed or repealed; a decision's holding, quoted
   and attributed to the court; a report's recommendations as it states
   them, and what became of them as a cited source says. Each office,
   organisation, tenure class or document it touched is linked. It may take
   `===` subsections by topic (a report's tables of findings, one subsection
   each). A report's consequences beyond its recommendations' adoption
   belong on the tenure class's page (a forest management licence, a tree
   farm licence), linked from the report, not here.
3. `{{Relationship}}` rows, then `{{Entity footer}}`.

Timeline. The footer renders a `Timeline` section from the document's
dates and from the rows naming it: write no Timeline heading or list. What
the timeline shows comes from the rows, so a change to it is a change to a
row.

Rows on the document's page: `amended_by` for each amendment that matters,
dated, its object the amending act's Document page or the Event that made
the change, with what it changed in `note` (the 1947 amendment that
created forest management licences is one). An amending act with neither
a Document page nor an Event is still the row's object, as a red link: its
title in the act format above, the act's short title as its citation gives
it and its year, with no page created for it. `RULES-FORESTRY-WIKI.md` leaves genuine red links, and this one is
genuine, so the row needs no `questions.md` line. A decision has a `decided_in`
row naming its case, and an `established` row for each duty, test or
principle it set, as the reasons state it: the row's object is the
decision's own page, and the duty, test or principle is quoted in `note`,
with the paragraph. Rows on other pages that name the document: the
`created_by`, `abolished_by` and `empowered_by` rows of the offices,
organisations and tenure classes it made, ended or empowered. They live on
those pages, not the document's. An act's own repeal is its
`repealed_date`, with the repealing act named and linked in What it did;
there is no repeal row. A power or a repeal is dated to the enactment or
amendment that made it. A date fixed "by proclamation" whose day no source
gives stays blank: the proclamation is told in prose, with a `questions.md`
line, and the assent date is never put in its place.

Document and Source pages are different things. A Source page is a
citation record: one edition, one capture. A Document page is the text as
a subject. A Source page that is a version of a Document's text (an act as
printed, a revision of it, a decision's reasons) sets `text_of=` the
Document's exact title, which may be a Document with no page yet.
A Document page cites its Source pages like any other page; it is never
cited as a source itself.

## Event

An event gets a page when the sources treat it as one named episode (the
1946 IWA strike, the Clayoquot Sound blockades of 1993, the Sommers affair,
*Haida Nation v. British Columbia*). A smaller incident stays a Disputes
sentence on the page it belongs to, linking to an event page where one
exists. Titles are the name the sources give the episode; a court case is
its style of cause without a citation: `Haida Nation v. British Columbia
(Minister of Forests)`. A royal commission's sittings are an event only
when the sources tell them as an episode.

Infobox (`{{Event}}`): `event_type`, `date` and `end_date` (+precision;
`end_date` for an event that ran over a span, such as a strike),
`location` (one or more place pages, separated by `;`). A mill or other
facility is a place in this sense: an event that happened at a facility
names the facility's page. An organisation is never a location: it is a
party (`participated_in` on its own page) or the organiser
(`organized_by`). A court case's `date` is
its filing and its `end_date` its final judgment; it takes no `location`. A
case styled differently by several courts takes the style of its last
decision; each court's Source page keeps its own style. An earlier
proceeding the courts treat as separate is a separate case, told in
Account.

Body, with these exact headings:

1. (no heading) Lead: one paragraph — what happened, where, when, and who
   took part. A court case's first sentence says it is the case and links
   its decision (below).
2. `== Account ==` The episode in time order, every sentence cited, each
   position attributed to whoever held it.
3. `== Parties ==` The parties, each linked, with its role as the sources
   assign it, in a sentence or a short list.
4. `== Decisions ==` A court case only: `{| class="wikitable"` with
   `! Date !! Court !! Citation !! Outcome !! Source`, one row per decision,
   the outcome in one sentence, the source cell
   `<ref>{{Cite|…|quote=…}}</ref>`. A decision with a Document page is
   linked from its Citation cell.
5. `{{Relationship}}` rows (`occurred_at` the place or facility), then
   `{{Entity footer}}`.

Each party is a `participated_in` row on the party's own page, with the
event as object and `role` one of `union`, `employer`, `Crown`, `court`,
`protesters`, `Nation`, `commission`, `witness`, `litigant`, `intervener`,
`mediator`, written as the sources assign it and never as the wiki judges
it. A litigant's side at each court (petitioner, respondent, appellant) goes
in the row's `note`. A party with no page, in a case or a strike, is named
in Parties with a `questions.md` line and has no row. The party's page then
lists the event, and the event's page lists the party. A party that organised the
event, as a source says, is `organized_by` on the event's page as well.

Disputes' tone rule applies to event pages in full. The page is
historical, and it neither takes sides nor avoids the events. Each position
is attributed to whoever held it (the company, a union, a Nation, a court,
protesters, the Province), the events are told plainly, and no outcome is
called right or wrong in the wiki's voice.

Two accounts of one event that differ stand side by side in Account, each
cited (`STYLE.md` rule 8). A collective agreement becomes a Document
(`doc_kind=agreement`) only if a source gives its text.

## A case and its decision

A court case is an Event (`event_type=court case`, headed "Court case"). A
landmark decision, one that later acts, policy or decisions treat as law
(*Sparrow* 1990, *Delgamuukw* 1997, *Haida Nation* 2004, *Tsilhqot'in*
2014), is also a Document (`doc_kind=decision`, headed "Decision"). Any
other decision is a row in the case's Decisions table and gets no page.
The two pages say in their first sentence which they are and link the
other: "*Haida Nation v. British Columbia (Minister of Forests)* was a case
…; its 2004 decision is [[Haida Nation v. British Columbia (Minister of
Forests), 2004 SCC 73]]." and "The 2004 decision of the Supreme Court of
Canada in [[Haida Nation v. British Columbia (Minister of Forests)]] …".
The decision's `decided_in` row names the case, and renders on both pages.
The case page tells the litigation; the decision page tells what the
decision held and established. Neither repeats the other at length.

## The predicates

A row lives on its subject's page, with the object as `object=`.

Dates on a row. A row's `start_date` and `end_date` each take the precision
the source gives it: `start_date_precision` and `end_date_precision`
(`day`, `month`, `year`, `circa`), each defaulting to the row's
`date_precision`. A term known to the day at its start and to the month at
its end is `start_date=1943-12-31|start_date_precision=day|end_date=1945-12|end_date_precision=month`.
The footer and the timelines print each date at its precision, never as the
1st of January or of the month. `decided_in`, `established`, `created_by`,
`abolished_by`, `amended_by`, `succeeded_by` and `submitted_to` name a
moment and print one date. Any dated predicate may be a sighting: a source
that places the row as true at one date and gives no span gives
`attested_date` (+`attested_date_precision`) and no start or end, and a
sighting is never joined into a term. A row's object, a document's
`issuer` and an office's `organisation` may name a page that does not
exist, as a red link in the title format its type takes (a federation, a
court, a department, an order); no page is created for it.

Verification of a row. A row's verification badge is bound to a hash of what the row asserts: its
predicate, object, start and end dates, sources, role and attested date,
its share where it has one, and `capacity` and `end_disputed` where they
are set. Changing any of these starts the row's count over. The
precisions (`date_precision`, `start_date_precision`, `end_date_precision`,
`attested_date_precision`) are deliberately outside the hash: correcting
how finely a date is known does not change what the row asserts, and
filling a precision never lapses a verification. `note` is outside it too.

| Predicate | Subject → object | Dates |
|---|---|---|
| `held_office` | person → office | start and end as the source states them, each at its precision; an `attested_date` sighting where it gives one date; `end_disputed=yes`, `capacity=acting` (Office) |
| `part_of` | office or organisation → organisation | dated; the immediate parent the source shows |
| `created_by`, `abolished_by` | office, organisation or tenure class → document | the document's date; an undated row takes it |
| `amended_by` | document → document or event | the amendment's date |
| `empowered_by` | office or organisation → document | its own dates, as the source gives the power; never the document's by default |
| `established` | document (decision or act) → the same document, the duty, test or principle quoted in `note` | the decision's date |
| `decided_in` | document (decision) → event (court case) | the decision's date |
| `affiliated_with` | union local → union; union → federation | dated |
| `appointed_under` | office → document | its own dates: the act under which a holder is appointed |
| `succeeded_by` | organisation → organisation | the date the duties passed; a body whose duties pass to another that is not its renaming |
| `submitted_to` | any entity → organisation (a commission or inquiry) | the submission's date; the exhibit or brief in `note` |

The older predicates widen where needed: `participated_in` takes every kind
of organisation, and `lobbied` and `funded` take government bodies as
objects. Every row carries `sources=` and follows `RULES-FORESTRY-WIKI.md`.

## The areas

- Governance and Crown agencies. Ministries, branches, agencies,
  commissions, tribunals, the courts and the legislature; offices (the
  Chief Forester, ministers, deputy ministers, commissioners); acts,
  regulations, reports and landmark decisions. The governance timeline is
  computed from their dates and rows; interpretation of the regime stays in
  policy-history prose, under STYLE rule 13.
- Labour. Unions, locals and federations, with `affiliated_with`; union
  offices (president, business agent) as offices; collective agreements as
  `agreement` documents; strikes and lockouts as events.
- NGOs, media and lobby groups. Their kinds, with `funded`, `lobbied` and
  `participated_in`. A newspaper's page is the organisation; its articles
  stay Source pages.
- Writers. A Person page, with each work that is a subject as a `work`
  document, its `issuer` the writer, linked to the Source pages that
  capture it by their `text_of`.
- First Nations. `sector=First Nation` and `kind=Nation` or `tribal
  council`, with treaties as `agreement` documents. These values are
  defined but not yet used: until `ForestWiki:First Nations and Indigenous
  knowledge` is settled with the operator in a session of its own, write
  no content on a First Nation's page or on a company a Nation owns or
  runs: no prose, no `sector` or `kind`, no infobox value, no new such
  page, and no move of one. Mechanical bookkeeping is allowed there: a
  title-only rewrite (a row, a parameter or a link naming a page that was
  renamed, changed to its new title and nothing else), a redirect, and a
  date precision set to what the date as written already says. A Nation
  is named, and an event involving it told,
  only as a cited source records it, the sentence or citation making clear
  whose record it is (Crown, company, court, the Nation's own); no
  statement about title, territory or consent except quoted and
  attributed; link a Nation's existing page. A treaty, a court's decision
  or a Nation's role in an event is written on the document's or event's
  page under that rule, and the Nation's own page is left as it is.

No "Open questions" section and no "No source found gives X" sentence: what
is not known goes in the dossier's `questions.md` (STYLE rule 8).

The wiki page `ForestWiki:Office and document pages` carries this for
human editors, and `ForestWiki:Company page` its sector and kind
paragraph; when this file changes, those pages change in the same commit.
