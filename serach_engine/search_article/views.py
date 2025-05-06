from django.shortcuts import render
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ArticleSerializer
from django.http import JsonResponse
from search_article.models import Article
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

@api_view(['GET'])
def search_articles(request):
    query = request.GET.get("query", "")
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("perPage", 6))

    if not query:
        return JsonResponse({"error": "Query parameter is required"}, status=400)

    offset = (page - 1) * per_page

    ix = open_dir("index")
    with ix.searcher() as searcher:
        query_parser = MultifieldParser(["konten", "judul"], ix.schema)
        query_parsed = query_parser.parse(query)
        results = searcher.search(query_parsed, limit=per_page + offset)

        results = results[offset:offset + per_page]

        results_list = []
        best_match_article = None
        best_match_score = 0

        for result in results:
            try:
                article = Article.objects.get(pk=result["id"])
                serialized_article = ArticleSerializer(article)
                article_data = serialized_article.data

                article_data["tanggal"] = article.tanggal.strftime('%d %B %Y')
                article_data["score"] = result.score

                results_list.append(article_data)

                if result.score > best_match_score:
                    best_match_score = result.score
                    best_match_article = article
            except Article.DoesNotExist:
                continue

        summary = create_summary(best_match_article.cleaned_isi) if best_match_article else "Tidak ada artikel yang cocok."

        total_results = len(searcher.search(query_parsed))
        total_pages = (total_results + per_page - 1) // per_page

        return Response({
            "summary": summary,
            "results": results_list,
            "best_match_score": best_match_score,
            "totalResults": total_results,
            "totalPages": total_pages,
            "currentPage": page
        })

@api_view(['GET'])
def suggestions(request):
    query = request.GET.get("query", "").strip()
    if not query:
        return JsonResponse({"suggestions": []})
    suggestions_qs = Article.objects.filter(judul__icontains=query).values_list("judul", flat=True).distinct()[:5]
    return JsonResponse({"suggestions": list(suggestions_qs)})

def create_summary(text):
    summary_length = 300
    if len(text) <= summary_length:
        return text
    return text[:summary_length] + "..."
