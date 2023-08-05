# import xml.etree.ElementTree as ET
from django.utils.translation import gettext as _

ZOTERO_FIELD_MAP = {
    "DOI": "DOI",
    "ISBN": "ISBN",
    "ISSN": "ISSN",
    "abstractNote": "abstract",
    "accessDate": "accessed",
    "applicationNumber": "call-number",
    "archive": "archive",
    "archiveLocation": "archive_location",
    "artworkSize": "dimensions",
    "callNumber": "call-number",
    "code": "container-title",
    "codeNumber": "volume",
    "committee": "section",
    "conferenceName": "event-title",
    "court": "authority",
    "date": "issued",
    "edition": "edition",
    "extra": "note",
    "filingDate": "submitted",
    "history": "references",
    "issue": "issue",
    "issuingAuthority": "authority",
    "journalAbbreviation": "journalAbbreviation",
    "language": "language",
    "legalStatus": "status",
    "legislativeBody": "authority",
    "libraryCatalog": "source",
    "medium": "medium",
    "meetingName": "event-title",
    "numPages": "number-of-pages",
    "number": "number",
    "numberOfVolumes": "number-of-volumes",
    "pages": "page",
    "place": "publisher-place",
    "priorityNumbers": "issue",
    "programmingLanguage": "genre",
    "publicationTitle": "container-title",
    "publisher": "publisher",
    "references": "references",
    "reporter": "container-title",
    "rights": "license",
    "runningTime": "dimensions",
    "scale": "scale",
    "section": "section",
    "series": "collection-title",
    "seriesNumber": "collection-number",
    "seriesTitle": "collection-title",
    "session": "chapter-number",
    "shortTitle": "title-short",
    "system": "medium",
    "title": "title",
    "type": "genre",
    "url": "URL",
    "versionNumber": "version",
    "volume": "volume",
}


# tree = ET.parse("tests/data/csl-typeMap.xml")

# typeMaps = {}
# for el in tree.findall(".//typeMap"):
#     typeMaps[el.get("cslType")] = [ZOTERO_FIELD_MAP.get(field.get('value'), field.get('value')) for field in el.findall("field")]

# pprint.pprint(typeMaps)

# """The module level attributes here were generated from the csl-typeMap.xml file at github.com/citation-style-language/schema and tweaked to suit the needs of this application."""

CSL_TYPES = {
    "article": [
        "title",
        "abstract",
        "genre",
        "repository",
        "archiveID",
        "publisher-place",
        "issued",
        "collection-title",
        "collection-number",
        "DOI",
        "citationKey",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "title-short",
        "language",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "article-journal": [
        "title",
        "abstract",
        "container-title",
        "volume",
        "issue",
        "page",
        "issued",
        "collection-title",
        "collection-title",
        "seriesText",
        "journalAbbreviation",
        "language",
        "DOI",
        "ISSN",
        "title-short",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "article-magazine": [
        "title",
        "abstract",
        "container-title",
        "volume",
        "issue",
        "issued",
        "page",
        "language",
        "ISSN",
        "title-short",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "article-newspaper": [
        "title",
        "abstract",
        "container-title",
        "publisher-place",
        "edition",
        "issued",
        "section",
        "page",
        "language",
        "title-short",
        "ISSN",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "bill": [
        "title",
        "abstract",
        "billNumber",
        "container-title",
        "codeVolume",
        "section",
        "codePages",
        "authority",
        "chapter-number",
        "references",
        "issued",
        "language",
        "URL",
        "accessed",
        "title-short",
        "license",
        "note",
        "creator",
    ],
    "book": [
        "title",
        "abstract",
        "collection-title",
        "collection-number",
        "volume",
        "number-of-volumes",
        "edition",
        "publisher-place",
        "publisher",
        "issued",
        "number-of-pages",
        "language",
        "ISBN",
        "title-short",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "broadcast": [
        "title",
        "abstract",
        "programTitle",
        "episodeNumber",
        "videoRecordingFormat",
        "publisher-place",
        "network",
        "issued",
        "dimensions",
        "language",
        "title-short",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "chapter": [
        "title",
        "abstract",
        "bookTitle",
        "collection-title",
        "collection-number",
        "volume",
        "number-of-volumes",
        "edition",
        "publisher-place",
        "publisher",
        "issued",
        "page",
        "language",
        "ISBN",
        "title-short",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "document": [],
    "entry-dictionary": [
        "title",
        "abstract",
        "dictionaryTitle",
        "collection-title",
        "collection-number",
        "volume",
        "number-of-volumes",
        "edition",
        "publisher-place",
        "publisher",
        "issued",
        "page",
        "language",
        "ISBN",
        "title-short",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "entry-encyclopedia": [
        "title",
        "abstract",
        "encyclopediaTitle",
        "collection-title",
        "collection-number",
        "volume",
        "number-of-volumes",
        "edition",
        "publisher-place",
        "publisher",
        "issued",
        "page",
        "ISBN",
        "title-short",
        "URL",
        "accessed",
        "language",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "graphic": [
        "title",
        "abstract",
        "artworkMedium",
        "dimensions",
        "issued",
        "language",
        "title-short",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "URL",
        "accessed",
        "license",
        "note",
        "creator",
    ],
    "hearing": [
        "title",
        "abstract",
        "section",
        "publisher-place",
        "publisher",
        "number-of-volumes",
        "documentNumber",
        "page",
        "authority",
        "chapter-number",
        "references",
        "issued",
        "language",
        "title-short",
        "URL",
        "accessed",
        "license",
        "note",
        "creator",
    ],
    "interview": [
        "title",
        "abstract",
        "issued",
        "interviewMedium",
        "language",
        "title-short",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "legal_case": [
        "caseName",
        "abstract",
        "authority",
        "dateDecided",
        "docketNumber",
        "container-title",
        "reporterVolume",
        "firstPage",
        "references",
        "language",
        "title-short",
        "URL",
        "accessed",
        "license",
        "note",
        "creator",
    ],
    "legislation": [
        "nameOfAct",
        "abstract",
        "container-title",
        "volume",
        "publicLawNumber",
        "dateEnacted",
        "page",
        "section",
        "chapter-number",
        "references",
        "language",
        "title-short",
        "URL",
        "accessed",
        "license",
        "note",
        "creator",
    ],
    "manuscript": [
        "title",
        "abstract",
        "manuscriptType",
        "publisher-place",
        "issued",
        "number-of-pages",
        "language",
        "title-short",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "map": [
        "title",
        "abstract",
        "mapType",
        "scale",
        "collection-title",
        "edition",
        "publisher-place",
        "publisher",
        "issued",
        "language",
        "ISBN",
        "title-short",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "motion_picture": [
        "title",
        "abstract",
        "videoRecordingFormat",
        "collection-title",
        "volume",
        "number-of-volumes",
        "publisher-place",
        "studio",
        "issued",
        "dimensions",
        "language",
        "ISBN",
        "title-short",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "paper-conference": [
        "title",
        "abstract",
        "issued",
        "proceedingsTitle",
        "event-title",
        "publisher-place",
        "publisher",
        "volume",
        "page",
        "collection-title",
        "language",
        "DOI",
        "ISBN",
        "title-short",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "patent": [
        "title",
        "abstract",
        "publisher-place",
        "country",
        "assignee",
        "authority",
        "patentNumber",
        "submitted",
        "page",
        "call-number",
        "issue",
        "issueDate",
        "references",
        "status",
        "language",
        "title-short",
        "URL",
        "accessed",
        "license",
        "note",
        "creator",
    ],
    "personal_communication": [
        "title",
        "abstract",
        "letterType",
        "issued",
        "language",
        "title-short",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "post": [
        "title",
        "abstract",
        "forumTitle",
        "postType",
        "issued",
        "language",
        "title-short",
        "URL",
        "accessed",
        "license",
        "note",
        "creator",
    ],
    "post-weblog": [
        "title",
        "abstract",
        "blogTitle",
        "websiteType",
        "issued",
        "URL",
        "accessed",
        "language",
        "title-short",
        "license",
        "note",
        "creator",
    ],
    "report": [
        "title",
        "abstract",
        "reportNumber",
        "reportType",
        "collection-title",
        "publisher-place",
        "institution",
        "issued",
        "page",
        "language",
        "title-short",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "software": [
        "title",
        "abstract",
        "collection-title",
        "version",
        "issued",
        "medium",
        "publisher-place",
        "company",
        "genre",
        "ISBN",
        "title-short",
        "URL",
        "license",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "accessed",
        "note",
        "creator",
    ],
    "song": [
        "title",
        "abstract",
        "audioRecordingFormat",
        "collection-title",
        "volume",
        "number-of-volumes",
        "publisher-place",
        "label",
        "issued",
        "dimensions",
        "language",
        "ISBN",
        "title-short",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "URL",
        "accessed",
        "license",
        "note",
        "creator",
    ],
    "speech": [
        "title",
        "abstract",
        "presentationType",
        "issued",
        "publisher-place",
        "event-title",
        "URL",
        "accessed",
        "language",
        "title-short",
        "license",
        "note",
        "creator",
    ],
    "thesis": [
        "title",
        "abstract",
        "thesisType",
        "university",
        "publisher-place",
        "issued",
        "number-of-pages",
        "language",
        "title-short",
        "URL",
        "accessed",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "license",
        "note",
        "creator",
    ],
    "webpage": [
        "title",
        "abstract",
        "websiteTitle",
        "websiteType",
        "issued",
        "title-short",
        "URL",
        "accessed",
        "language",
        "license",
        "note",
        "creator",
    ],
}

CSL_FIELDS = fields = {
    "DOI": {
        "description": _("Digital Object Identifier (e.g. “10.1128/AEM.02591-07”)"),
        "name": "DOI",
        "type": "standard",
    },
    "ISBN": {
        "description": _("International Standard Book Number (e.g. “978-3-8474-1017-1”)"),
        "name": "ISBN",
        "type": "standard",
    },
    "ISSN": {"description": _("International Standard Serial Number"), "name": "ISSN", "type": "standard"},
    "PMCID": {"description": _("PubMed Central reference number"), "name": "PMCID", "type": "standard"},
    "PMID": {"description": _("PubMed reference number"), "name": "PMID", "type": "standard"},
    "URL": {
        "description": _("Uniform Resource Locator (e.g. “https://aem.asm.org/cgi/content/full/74/9/2766”)"),
        "name": "URL",
        "type": "standard",
    },
    "abstract": {
        "description": _("Abstract of the item (e.g. the abstract of a journal article)"),
        "name": _("abstract"),
        "type": "standard",
    },
    "accessed": {"description": _("Date the item has been accessed"), "name": _("accessed"), "type": "date"},
    "annote": {
        "description": (
            "Short markup, decoration, or annotation to the "
            "item (e.g., to indicate items included in a "
            "review); For descriptive text (e.g., in an "
            "annotated bibliography), use note instead"
        ),
        "name": _("annote"),
        "type": "standard",
    },
    "archive": {"description": _("Archive storing the item"), "name": _("archive"), "type": "standard"},
    "archive-place": {
        "description": _("Geographic location of the archive"),
        "name": _("archive place"),
        "type": "standard",
    },
    "archive_collection": {
        "description": _("Collection the item is part of within an archive"),
        "name": _("archive collection"),
        "type": "standard",
    },
    "archive_location": {
        "description": _("Storage location within an archive (e.g. a box and folder number)"),
        "name": _("archive location"),
        "type": "standard",
    },
    "author": {"description": _("Author"), "name": _("author"), "type": "name"},
    "authority": {
        "description": (
            "Issuing or judicial authority (e.g. “USPTO” for a patent, “Fairfax Circuit Court” for a legal case)"
        ),
        "name": _("authority"),
        "type": "standard",
    },
    "available-date": {
        "description": (
            "Date the item was initially available "
            "(e.g. the online publication date of a "
            "journal article before its formal "
            "publication date; the date a treaty was "
            "made available for signing)"
        ),
        "name": _("available date"),
        "type": "date",
    },
    "call-number": {
        "description": _("Call number (to locate the item in a library)"),
        "name": _("call number"),
        "type": "standard",
    },
    "chair": {
        "description": (
            "The person leading the session containing a "
            "presentation (e.g. the organizer of the "
            "container title of a speech)"
        ),
        "name": _("chair"),
        "type": "name",
    },
    "chapter-number": {
        "description": _("Chapter number (e.g. chapter number in a book; track number on an album)"),
        "name": _("chapter number"),
        "type": "number",
    },
    "citation-key": {
        "description": (
            "Identifier of the item in the input data "
            "file (analogous to BibTeX entrykey); Use "
            "this variable to facilitate conversion "
            "between word-processor and plain-text "
            "writing systems; For an identifer intended "
            "as formatted output label for a citation "
            "(e.g. “Ferr78”), use citation-label instead"
        ),
        "name": _("citation key"),
        "type": "standard",
    },
    "citation-label": {
        "description": (
            "Label identifying the item in in-text "
            "citations of label styles (e.g. “Ferr78”); "
            "May be assigned by the CSL processor based "
            "on item metadata; For the identifier of "
            "the item in the input data file, use "
            "citation key instead"
        ),
        "name": _("citation label"),
        "type": "standard",
    },
    "citation-number": {
        "description": (
            "Index (starting at 1) of the cited reference in the bibliography (generated by the CSL processor)"
        ),
        "name": _("citation number"),
        "type": "number",
    },
    "collection-editor": {
        "description": _("Editor of the collection holding the item (e.g. the series editor for a book)"),
        "name": _("collection editor"),
        "type": "name",
    },
    "collection-number": {
        "description": _("Number identifying the collection holding the item (e.g. the series number for a book)"),
        "name": _("collection number"),
        "type": "number",
    },
    "collection-title": {
        "description": (
            "Title of the collection holding the item "
            "(e.g. the series title for a book; the "
            "lecture series title for a presentation)"
        ),
        "name": _("collection title"),
        "type": "standard",
    },
    "compiler": {
        "description": (
            "Person compiling or selecting material for an "
            "item from the works of various persons or bodies "
            "(e.g. for an anthology)"
        ),
        "name": _("compiler"),
        "type": "name",
    },
    "composer": {"description": _("Composer (e.g. of a musical score)"), "name": _("composer"), "type": "name"},
    "container-author": {
        "description": _("Author of the container holding the item (e.g. the book author for a book chapter)"),
        "name": _("container author"),
        "type": "name",
    },
    "container-title": {
        "description": (
            "Title of the container holding the item "
            "(e.g. the book title for a book chapter, "
            "the journal title for a journal article; "
            "the album title for a recording; the "
            "session title for multi-part presentation "
            "at a conference)"
        ),
        "name": _("container title"),
        "type": "standard",
    },
    "container-title-short": {
        "description": (
            'Short/abbreviated form of container-title; Deprecated; use variable="container title" form="short" instead'
        ),
        "name": _("container title (short)"),
        "type": "standard",
    },
    "contributor": {
        "description": (
            "A minor contributor to the item; typically "
            "cited using “with” before the name when "
            "listed in a bibliography"
        ),
        "name": _("contributor"),
        "type": "name",
    },
    "curator": {
        "description": _("Curator of an exhibit or collection (e.g. in a museum)"),
        "name": _("curator"),
        "type": "name",
    },
    "dimensions": {
        "description": _("Physical (e.g. size) or temporal (e.g. running time) dimensions of the item"),
        "name": _("dimensions"),
        "type": "standard",
    },
    "director": {"description": _("Director (e.g. of a film)"), "name": _("director"), "type": "name"},
    "division": {
        "description": _("Minor subdivision of a court with a jurisdiction for a legal item"),
        "name": _("division"),
        "type": "standard",
    },
    "edition": {
        "description": (
            "(Container) edition holding the item (e.g. “3” when citing a chapter in the third edition of a book)"
        ),
        "name": _("edition"),
        "type": "number",
    },
    "editor": {"description": _("Editor"), "name": _("editor"), "type": "name"},
    "editor-translator": {
        "description": (
            "Combined editor and translator of a "
            "work; The citation processory must be "
            "automatically generate if editor and "
            "translator variables are identical; May "
            "also be provided directly in item data"
        ),
        "name": _("editor translator"),
        "type": "name",
    },
    "editorial-director": {
        "description": _("Managing editor (“Directeur de la Publication” in French)"),
        "name": _("editorial director"),
        "type": "name",
    },
    "event": {"description": _("Deprecated legacy variant of event-title"), "name": _("event"), "type": "standard"},
    "event-date": {
        "description": _("Date the event related to an item took place"),
        "name": _("event date"),
        "type": "date",
    },
    "event-place": {
        "description": _("Geographic location of the event related to the item (e.g. “Amsterdam, The Netherlands”)"),
        "name": _("event place"),
        "type": "standard",
    },
    "event-title": {
        "description": (
            "Name of the event related to the item (e.g. "
            "the conference name when citing a conference "
            "paper; the meeting where presentation was "
            "made)"
        ),
        "name": _("event title"),
        "type": "standard",
    },
    "executive-producer": {
        "description": _("Executive producer (e.g. of a television series)"),
        "name": _("executive producer"),
        "type": "name",
    },
    "first-reference-note-number": {
        "description": (
            "Number of a preceding note "
            "containing the first "
            "reference to the item; "
            "Assigned by the CSL "
            "processor; Empty in "
            "non-note-based styles or when "
            "the item hasn`t been cited in "
            "any preceding notes in a "
            "document"
        ),
        "name": _("first reference note number"),
        "type": "number",
    },
    "genre": {
        "description": (
            "Type, class, or subtype of the item (e.g. “Doctoral "
            "dissertation” for a PhD thesis; “NIH Publication” "
            "for an NIH technical report); Do not use for "
            "topical descriptions or categories (e.g. "
            "“adventure” for an adventure movie)"
        ),
        "name": _("genre"),
        "type": "standard",
    },
    "guest": {"description": _("Guest (e.g. on a TV show or podcast)"), "name": _("guest"), "type": "name"},
    "host": {"description": _("Host (e.g. of a TV show or podcast)"), "name": _("host"), "type": "name"},
    "illustrator": {
        "description": _("Illustrator (e.g. of a children`s book or graphic novel)"),
        "name": _("illustrator"),
        "type": "name",
    },
    "interviewer": {
        "description": _("Interviewer (e.g. of an interview)"),
        "name": _("interviewer"),
        "type": "name",
    },
    "issue": {
        "description": (
            "Issue number of the item or container holding the "
            "item (e.g. “5” when citing a journal article from "
            "journal volume 2, issue 5); Use volume title for "
            "the title of the issue, if any"
        ),
        "name": _("issue"),
        "type": "number",
    },
    "issued": {"description": _("Date the item was issued/published"), "name": _("issued"), "type": "date"},
    "jurisdiction": {
        "description": _("Geographic scope of relevance (e.g. “US” for a US patent; the court hearing a legal case)"),
        "name": _("jurisdiction"),
        "type": "standard",
    },
    "keyword": {
        "description": _("Keyword(s) or tag(s) attached to the item"),
        "name": _("keyword"),
        "type": "standard",
    },
    "language": {
        "description": (
            "The language of the item; Should be entered as "
            "an ISO 639-1 two-letter language code (e.g. "
            "“en”, “zh”), optionally with a two-letter locale "
            "code (e.g. “de-DE”, “de-AT”)"
        ),
        "name": _("language"),
        "type": "standard",
    },
    "license": {
        "description": (
            "The license information applicable to an item "
            "(e.g. the license an article or software is "
            "released under; the copyright information for an "
            "item; the classification status of a document)"
        ),
        "name": _("license"),
        "type": "standard",
    },
    "locator": {
        "description": (
            "A cite-specific pinpointer within the item (e.g. "
            "a page number within a book, or a volume in a "
            "multi-volume work); Must be accompanied in the "
            "input data by a label indicating the locator type "
            "(see the Locators term list), which determines "
            "which term is rendered by cs:label when the "
            "locator variable is selected."
        ),
        "name": _("locator"),
        "type": "number",
    },
    "medium": {
        "description": _("Description of the item`s format or medium (e.g. “CD”, “DVD”, “Album”, etc.)"),
        "name": _("medium"),
        "type": "standard",
    },
    "narrator": {"description": _("Narrator (e.g. of an audio book)"), "name": _("narrator"), "type": "name"},
    "note": {
        "description": _("Descriptive text or notes about an item (e.g. in an annotated bibliography)"),
        "name": _("note"),
        "type": "standard",
    },
    "number": {
        "description": _("Number identifying the item (e.g. a report number)"),
        "name": _("number"),
        "type": "number",
    },
    "number-of-pages": {
        "description": _("Total number of pages of the cited item"),
        "name": _("number of pages"),
        "type": "number",
    },
    "number-of-volumes": {
        "description": _("Total number of volumes, used when citing multi-volume books and such"),
        "name": _("number of volumes"),
        "type": "number",
    },
    "organizer": {
        "description": _("Organizer of an event (e.g. organizer of a workshop or conference)"),
        "name": _("organizer"),
        "type": "name",
    },
    "original-author": {
        "description": (
            "The original creator of a work (e.g. the "
            "form of the author name listed on the "
            "original version of a book; the "
            "historical author of a work; the original "
            "songwriter or performer for a musical "
            "piece; the original developer or "
            "programmer for a piece of software; the "
            "original author of an adapted work such "
            "as a book adapted into a screenplay)"
        ),
        "name": _("original author"),
        "type": "name",
    },
    "original-date": {
        "description": _("Issue date of the original version"),
        "name": _("original date"),
        "type": "date",
    },
    "original-publisher": {
        "description": _("Original publisher, for items that have been republished by a different publisher"),
        "name": _("original publisher"),
        "type": "standard",
    },
    "original-publisher-place": {
        "description": _("Geographic location of the original publisher (e.g. “London, UK”)"),
        "name": _("original publisher place"),
        "type": "standard",
    },
    "original-title": {
        "description": (
            "Title of the original version (e.g. “Boйнa и миp”, the untranslated Russian title of “War and Peace”)"
        ),
        "name": _("original title"),
        "type": "standard",
    },
    "page": {
        "description": _(
            "Range of pages the item (e.g. a journal article) covers in a container (e.g. a journal issue)"
        ),
        "name": _("page"),
        "type": "number",
    },
    "page-first": {
        "description": (
            "First page of the range of pages the item "
            "(e.g. a journal article) covers in a container "
            "(e.g. a journal issue)"
        ),
        "name": _("page first"),
        "type": "number",
    },
    "part-number": {
        "description": (
            "Number of the specific part of the item being "
            "cited (e.g. part 2 of a journal article); Use "
            "part-title for the title of the part, if any"
        ),
        "name": _("part number"),
        "type": "number",
    },
    "part-title": {
        "description": _("Title of the specific part of an item being cited"),
        "name": _("part title"),
        "type": "standard",
    },
    "performer": {
        "description": (
            "Performer of an item (e.g. an actor appearing in a film; a muscian performing a piece of music)"
        ),
        "name": _("performer"),
        "type": "name",
    },
    "printing-number": {
        "description": _("Printing number of the item or container holding the item"),
        "name": _("printing number"),
        "type": "number",
    },
    "producer": {
        "description": _("Producer (e.g. of a television or radio broadcast)"),
        "name": _("producer"),
        "type": "name",
    },
    "publisher": {"description": _("Publisher"), "name": _("publisher"), "type": "standard"},
    "publisher-place": {
        "description": _("Geographic location of the publisher"),
        "name": _("publisher place"),
        "type": "standard",
    },
    "recipient": {"description": _("Recipient (e.g. of a letter)"), "name": _("recipient"), "type": "name"},
    "references": {
        "description": (
            "Resources related to the procedural history of "
            "a legal case or legislation; Can also be used "
            "to refer to the procedural history of other "
            "items (e.g. “Conference canceled” for a "
            "presentation accepted as a conference that was "
            "subsequently canceled; details of a retraction "
            "or correction notice)"
        ),
        "name": _("references"),
        "type": "standard",
    },
    "reviewed-author": {
        "description": _("Author of the item reviewed by the current item"),
        "name": _("reviewed author"),
        "type": "name",
    },
    "reviewed-genre": {
        "description": _("Type of the item being reviewed by the current item (e.g. book, film)"),
        "name": _("reviewed genre"),
        "type": "standard",
    },
    "reviewed-title": {
        "description": _("Title of the item reviewed by the current item"),
        "name": _("reviewed title"),
        "type": "standard",
    },
    "scale": {"description": _("Scale of e.g. a map or model"), "name": _("scale"), "type": "standard"},
    "script-writer": {
        "description": _("Writer of a script or screenplay (e.g. of a film)"),
        "name": _("script writer"),
        "type": "name",
    },
    "section": {
        "description": (
            "Section of the item or container holding the item "
            "(e.g. “§2.0.1” for a law; “politics” for a "
            "newspaper article)"
        ),
        "name": _("section"),
        "type": "number",
    },
    "series-creator": {
        "description": _("Creator of a series (e.g. of a television series)"),
        "name": _("series creator"),
        "type": "name",
    },
    "source": {
        "description": _("Source from whence the item originates (e.g. a library catalog or database)"),
        "name": _("source"),
        "type": "standard",
    },
    "status": {
        "description": (
            "Publication status of the item (e.g. “forthcoming”; “in press”; “advance online publication”; “retracted”)"
        ),
        "name": _("status"),
        "type": "standard",
    },
    "submitted": {
        "description": _("Date the item (e.g. a manuscript) was submitted for publication"),
        "name": _("submitted"),
        "type": "date",
    },
    "supplement-number": {
        "description": (
            "Supplement number of the item or "
            "container holding the item (e.g. for "
            "secondary legal items that are "
            "regularly updated between editions)"
        ),
        "name": _("supplement number"),
        "type": "number",
    },
    "title": {"description": _("Primary title of the item"), "name": _("title"), "type": "standard"},
    "title-short": {
        "description": 'Short/abbreviated form of title; Deprecated; use variable="title" form="short" instead',
        "name": _("title short"),
        "type": "standard",
    },
    "translator": {"description": _("Translator"), "name": _("translator"), "type": "name"},
    "version": {
        "description": _("Version of the item (e.g. “2.0.9” for a software program)"),
        "name": _("version"),
        "type": "number",
    },
    "volume": {
        "description": (
            "Volume number of the item (e.g. “2” when citing "
            "volume 2 of a book) or the container holding the "
            "item (e.g. “2” when citing a chapter from volume 2 "
            "of a book); Use volume title for the title of the "
            "volume, if any"
        ),
        "name": _("volume"),
        "type": "number",
    },
    "volume-title": {
        "description": (
            "Title of the volume of the item or container "
            "holding the item; Also use for titles of "
            "periodical special issues, special sections, "
            "and the like"
        ),
        "name": _("volume title"),
        "type": "standard",
    },
    "year-suffix": {
        "description": _("Disambiguating year suffix in author date styles (e.g. “a” in “Doe, 1999a”)"),
        "name": _("year suffix"),
        "type": "standard",
    },
}
