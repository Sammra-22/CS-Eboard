from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def filter_client_queryset(queryset, query_string):
    vector = SearchVector('last_name', 'first_name')
    query = SearchQuery(query_string)
    queryset = queryset.annotate(
        search=vector,
        rank=SearchRank(vector, query),
    ).filter(search=query).order_by('-rank')
    return queryset
