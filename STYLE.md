# Style

How ForestWiki pages are written. The base is Wikipedia's Manual of Style:
a lead section, a neutral register, time order within a topic, footnote
citations, sentence-case headings, no reference to the page itself. The
rules below say where ForestWiki adds to that or differs.

1. A page tells one story in time order. Sections follow the subject's life, not the order in which documents were read.
2. Every sentence is complete and follows from the sentence before it. A fact that does not connect to its neighbours goes in a table, not in a paragraph.
3. One name for one thing. The lead fixes the name and the page keeps it: "the 2017 licence", never "the current licence" in one place and "the licence now" in another.
4. No word a reader cannot resolve. "The last", "the latter", "now" and "the takeback" are replaced by the thing itself with its date: "the 1988 reduction".
5. Headings name the subject, never the source: "The 1988 reduction", not "In the province's register". A page has only the headings its schema lists; the tenure schema is `SCHEMA-TENURE.md` and the company schema `SCHEMA-COMPANY.md`, each read before writing a page of its kind.
6. Every sentence that states a fact ends with a citation. The citation names the source and quotes the exact words from the source that support the sentence.
7. A conclusion is attributed to the source that drew it: "Pearse concluded that…". A calculation shows the cited figures it was made from. Nothing else is asserted. The one exception is the wiki's own analysis, which lives only in rows marked as derived (written by the analysis script, never by hand) and on pages in the Analysis namespace, each of which states its method; see `ForestWiki:Control resolution`. A company page never states who controlled the company except as a source says it, in prose with a citation or in a `{{Control claim}}` row.
8. What is not known is written as a question for the next editor, in the "Open questions" section.
9. A page never describes how it was made: no mention of searches, captures, dossiers, passes, or this wiki. Pages in the Analysis namespace are the exception: they say that they are the wiki's analysis and how it was made.
10. The citation names the document; the sentence does not. Write "The licence covers 152,000 hectares", not "The 2019 rationale gives its area as 152,000 hectares". A sentence names a document only when the document is what happened: a licence replaced, an instrument made, an order issued — and then by its full title, "the 2019 allowable annual cut rationale", never a shortened form.
11. A detail that does not change the story is left out of the prose: an office address, the clause of an Act an order cites, a surveyor's name, how a document spells a name. If it matters, it goes in a table cell or in the citation's quote.
12. Another name for the subject is introduced once, in the lead, as "also known as".

A citation is `<ref>{{Cite|Source page|p=page|quote=exact words}}</ref>`.
A statement with no citation yet carries `{{Citation needed}}`; the bot
never writes one, because a fact it cannot cite does not go on the page.

The wiki page `ForestWiki:Style` carries these rules for human editors;
when this file changes, that page changes in the same commit.
