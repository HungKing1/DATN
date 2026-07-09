from rag_backend.domain.interfaces.vector_repository import VectorRepository
from rag_backend.domain.models.query import RetrievalResult


async def expand_split_chunks_async(
    results: list[RetrievalResult],
    vector_repo: VectorRepository,
    so_ky_hieu: str | None = None,
) -> list[RetrievalResult]:
    """Fetch all parts of a split article if we retrieve a chunk with is_split=True."""
    expanded = []
    seen_articles = set()

    for r in results:
        is_split = r.metadata.get("is_split")
        chunk_so_ky_hieu = so_ky_hieu or r.metadata.get("so_ky_hieu")
        
        if is_split and chunk_so_ky_hieu:
            art_ids = r.metadata.get("article_mongo_ids", [])
            if art_ids and art_ids[0] not in seen_articles:
                seen_articles.add(art_ids[0])
                all_parts = await vector_repo.get_chunks_by_article_id(
                    mongo_article_id=art_ids[0], so_ky_hieu=chunk_so_ky_hieu
                )
                all_parts.sort(key=lambda x: x.metadata.get("split_part", 1))
                if all_parts:
                    full_content = "\n".join(p.content for p in all_parts)
                    expanded.append(r.model_copy(update={"content": full_content}))
        else:
            expanded.append(r)

    return expanded
