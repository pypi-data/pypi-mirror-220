from django.db import models
from django.utils.translation import gettext_lazy as _


class MonthChoices(models.IntegerChoices):
    JAN = (
        1,
        _("January"),
    )
    FEB = (
        2,
        _("February"),
    )
    MAR = (
        3,
        _("March"),
    )
    APR = (
        4,
        _("April"),
    )
    MAY = (
        5,
        _("May"),
    )
    JUN = (
        6,
        _("June"),
    )
    JUL = (
        7,
        _("July"),
    )
    AUG = (
        8,
        _("August"),
    )
    SEP = (
        9,
        _("September"),
    )
    OCT = (
        10,
        _("October"),
    )
    NOV = (
        11,
        _("November"),
    )
    DEC = 12, _("December")


class IdentifierTypes(models.IntegerChoices):
    DOI = 0, "DOI"
    ISSN = 1, "ISSN"
    ISBN = 2, "ISBN"
    PMCID = 3, "PMCID"
    PMID = 4, "PMID"
    URL = 5, "URL"


class TypeChoices(models.TextChoices):
    article = "article", _("article")
    article_journal = "article-journal", _("journal article")
    article_magazine = "article-magazine", _("magazine article")
    article_newspaper = "article-newspaper", _("newspaper article")
    bill = "bill", _("bill")
    book = "book", _("book")
    broadcast = "broadcast", _("broadcast")
    chapter = "chapter", _("chapter")
    dataset = "dataset", _("dataset")
    entry = "entry", _("entry")
    entry_dictionary = "entry-dictionary", _("entry (dictionary)")
    entry_encyclopedia = "entry-encyclopedia", _("entry (encyclopedia)")
    figure = "figure", _("figure")
    graphic = "graphic", _("graphic")
    interview = "interview", _("interview")
    legal_case = "legal_case", _("legal case")
    legislation = "legislation", _("legislation")
    manuscript = "manuscript", _("manuscript")
    map = "map", _("map")  # noqa: A003
    motion_picture = "motion_picture", _("motion picture")
    musical_score = "musical_score", _("musical score")
    pamphlet = "pamphlet", _("pamphlet")
    paper_conference = "paper-conference", _("paper conference")
    patent = "patent", _("patent")
    personal_communication = "personal_communication", _("personal communication")
    post = "post", _("post")
    post_weblog = "post-weblog", _("blog post")
    report = "report", _("report")
    review = "review", _("review")
    review_book = "review-book", _("review book")
    song = "song", _("song")
    speech = "speech", _("speech")
    thesis = "thesis", _("thesis")
    treaty = "treaty", _("treaty")
    webpage = "webpage", _("webpage")
