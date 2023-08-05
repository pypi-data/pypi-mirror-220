from datetime import date

from dateutil.relativedelta import relativedelta
from django.db.models import Count, Max, Q
from django.db.models.query import QuerySet

from literature.conf import settings


class AuthorQuerySet(QuerySet):
    def with_work_counts(self):
        """Convenience filter for retrieving authors with annotated
        counts of works published as either lead or supporting author.

        These count attributes can be accessed on the queryset as
        `as_lead` or `as_supporting`. Further filtering/manipulation is
        possible on both fields afterwards.

        Example:
            Get authors that have published at least five works as
            lead author.

            >>> Author.objects.with_work_counts().filter(as_lead__gte=5)

            Get authors that have published only once but have been a supporting
            author on at least three.

            >>> Author.objects.with_work_counts().filter(as_lead=1, as_supporting__gte=3)
        """
        return self.prefetch_related("literature").annotate(
            as_lead=Count("position", filter=Q(position__position=1)),
            as_supporting=Count("position", filter=Q(position__position__gt=1)),
        )

    def as_lead(self):
        """Convenience filter for retrieving only authors that
        are listed as the lead author on a publication."""

        return (
            self.prefetch_related("literature")
            .annotate(as_lead=Count("position", filter=Q(position__position=1)))
            .filter(as_lead__gt=0)
        )

    def with_last_published(self):
        return self.prefetch_related("literature").annotate(last_published=Max("literature__published"))

    def is_active(self):
        cutoff = date.today() - relativedelta(years=settings.LITERATURE_INACTIVE_AFTER)
        return self.with_last_published().filter(last_published__gt=cutoff)


AuthorManager = AuthorQuerySet.as_manager
