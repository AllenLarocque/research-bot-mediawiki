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
`finance`, `education and research`, `other industry`.

`kind`, what an organisation is:

- companies and finance: `company`, `subsidiary`, `partnership`, `fund`,
  `holding company`, `Crown corporation`;
- government: `ministry`, `department`, `branch`, `agency`, `commission`,
  `tribunal`, `board`, `court`, `legislature`, `municipality`;
- labour: `union`, `union local`, `federation`;
- associations: `association`, `council`;
- media and others: `newspaper`, `broadcaster`, `publisher`, `foundation`,
  `research institute`, `university`;
- Nations: `Nation`, `tribal council`.

`event_type`: `strike`, `lockout`, `blockade`, `protest`, `court case`,
`inquiry`, `commission`, `election`, `fire`, `disaster`, `closure`,
`curtailment`, `scandal`, `forced removal`, `land grant`, `outbreak`.
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

Infobox (`{{Organization}}`): `name`, `sector`, `kind`, `jurisdiction` (a
government body only: the level of government it belongs to, a province or
country by its full name, `British Columbia` or `Canada`, never `BC` or
`B.C.`, and a municipality by its page's exact title), `seat`, `founded_date` and `dissolved_date`
(+precision), `status`. No `org_type`.

Body, with these exact headings:

1. (no heading) Lead: one paragraph — what the body is or was, its sector
   and jurisdiction in words, when it was made and by what, and what it
   did.
2. `== History ==` The body's story by era, in time order, every sentence
   cited: what it was made to do, the act or order that made or changed
   it, its renamings and reorganisations, its offices and who held them,
   its work and the disputes it took part in, each linked. Subsections by
   era are allowed; headings name the era or the event, never the source.
3. `== Disputes ==` Optional; see Disputes below.
4. `{{Relationship}}` rows, then `{{Entity footer}}`.

A renaming is a `renamed_to` row and a parent a dated `part_of` row, so
Forest Branch is `part_of` each ministry it sat in, in turn. A royal
commission is an organisation, `sector=government` and `kind=commission`;
its commissioner is an office and its report a Document. A newspaper's page
is the organisation; its articles stay Source pages.

## Office

One page per office, held in turn by dated holders. Titles:
`Chief Forester of British Columbia`, `Minister of Forests (British
Columbia)`, `President of the IWA`. An office is not a board: a board seat
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
Never infer a term from sightings. The person's career table shows the row
too.

The office's own rows: a dated `part_of` row for each parent, through each
renaming of the parent; `created_by` and `abolished_by` the Document that
made or ended it; `empowered_by` each Document that gave it powers, dated
as the source dates the power. A document that matters and has no page is
still the row's object, as a red link in the title formats under Document
(an act, a decision, or any other document as its citation gives it),
with no page created for it, as for an amending act below.

## Document

One page per governing or landmark text: an act, a regulation, a landmark
decision, a report, an agreement or a work. Titles:

- an act as enacted, with its year: `Forest Act (1912)`, `Forest Act
  (1978)`, `Forest Practices Code of British Columbia Act (1994)`, `Forest
  and Range Practices Act (2002)`. Each enactment is its own page; an
  amendment is a row, not a page, unless the amending act is itself a
  subject (below for an amending act with no page);
- a decision by its style of cause and neutral citation: `Haida Nation v.
  British Columbia (Minister of Forests), 2004 SCC 73`;
- any other document (a regulation, an order in council, a report) by the
  title its citation gives it, after checking that no existing page
  already carries it under another title.

Infobox (`{{Document}}`): `doc_kind`, `citation` (the statute chapter or
neutral citation), `issuer` (an exact page title: the legislature, court,
commission or author), `issued_date` (enactment, judgment or publication),
`in_force_date` and `repealed_date`, each with its precision.

Body, with these exact headings:

1. (no heading) Lead: one paragraph — what the document is, who issued it
   and when, and what it is known for. A decision's first sentence says it
   is the decision and links its case (below).
2. `== What it did ==` What the text did, every sentence cited: what an act
   created, empowered, changed or repealed; a decision's holding, quoted
   and attributed to the court; a report's recommendations as it states
   them, and what became of them as a cited source says. Each office,
   organisation, tenure class or document it touched is linked.
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
there is no repeal row.

Document and Source pages are different things. A Source page is a
citation record: one edition, one capture. A Document page is the text as
a subject. A Source page that is a version of a Document's text (an act as
printed, a decision's reasons) sets `text_of=` the Document's exact title.
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
`location` (a place page).

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
`protesters`, `Nation`, `commission`, `witness`, written as the sources
assign it and never as the wiki judges it. The party's page then lists the
event, and the event's page lists the party. A party that organised the
event, as a source says, is `organized_by` on the event's page as well.

Disputes' tone rule applies to event pages in full. The page is
historical, and it neither takes sides nor avoids the events. Each position
is attributed to whoever held it (the company, a union, a Nation, a court,
protesters, the Province), the events are told plainly, and no outcome is
called right or wrong in the wiki's voice.

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

| Predicate | Subject → object | Dates |
|---|---|---|
| `held_office` | person → office | start and end as the source states; an `attested_date` sighting where it gives one date |
| `part_of` | office or organisation → organisation | dated |
| `created_by`, `abolished_by` | office, organisation or tenure class → document | the document's date; an undated row takes it |
| `amended_by` | document → document or event | the amendment's date |
| `empowered_by` | office or organisation → document | its own dates, as the source gives the power; never the document's by default |
| `established` | document (decision or act) → the same document, the duty, test or principle quoted in `note` | the decision's date |
| `decided_in` | document (decision) → event (court case) | the decision's date |
| `affiliated_with` | union local → union; union → federation | dated |

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
  knowledge` is settled with the operator, create and edit no First Nation
  page, and set no `sector` or `kind` on a Nation's page or on a company a
  Nation owns or runs. A Nation is named, and an event involving it told,
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
