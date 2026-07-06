from __future__ import annotations

import logging
import math
import re
from uuid import uuid4

from rag_backend.domain.interfaces.chunking_strategy import ChunkingStrategy
from rag_backend.domain.models.document import LegalChunk, LegalChunkMetadata

logger = logging.getLogger(__name__)


class LegalArticleChunker(ChunkingStrategy):
    """Chunking strategy based on legal document structure.

    Token budget targets the raw content only (no prefix counted).

    Rules
    -----
    - size < MIN_TOKENS  → merge with subsequent article(s) until MAX_TOKENS
        * all merged articles share the same path  → one shared path header
        * articles from different paths            → separate path header per article
    - MIN_TOKENS ≤ size ≤ MAX_TOKENS → 1 chunk
    - size > MAX_TOKENS → split by khoản (clauses)

    Embedding-text formats
    ----------------------
    Single article (normal / split part):
        "{doc_header}. {path}. {title_goc}\\n{content}"

    Merged — same path group:
        "{doc_header}. {path_common}.\\n{title_goc_i}\\n{content_i}\\n\\n{title_goc_j}\\n{content_j}"

    Merged — cross-path (different chapter / muc / …):
        "{doc_header}. {path_i}.\\n{title_goc_i}\\n{content_i}\\n\\n{doc_header}. {path_j}.\\n{title_goc_j}\\n{content_j}"
    """

    def __init__(self, min_tokens: int = 300, max_tokens: int = 600) -> None:
        self.MIN_TOKENS = min_tokens
        self.MAX_TOKENS = max_tokens

    def get_strategy_name(self) -> str:
        return "legal_article"

    async def chunk(
        self,
        articles: list[dict],
        doc_meta: dict,
    ) -> list[LegalChunk]:
        """Chunk articles into LegalChunks."""
        chunks: list[LegalChunk] = []
        i = 0
        while i < len(articles):
            art = articles[i]
            content = art.get("content", "")
            if not content:
                i += 1
                continue

            size = self._count_tokens(content)

            if size > self.MAX_TOKENS:
                sub_chunks = self._split_by_khoan(art, doc_meta, base_index=len(chunks))
                chunks.extend(sub_chunks)
                i += 1
            elif size < self.MIN_TOKENS:
                merged_chunk, consumed = self._try_merge(
                    articles, i, doc_meta, base_index=len(chunks)
                )
                chunks.append(merged_chunk)
                i += consumed
            else:
                chunk = self._make_single_chunk(art, doc_meta, chunk_index=len(chunks))
                chunks.append(chunk)
                i += 1

        # Post-process: build embedding_text for every chunk
        art_map: dict[str, dict] = {str(a.get("_id", "")): a for a in articles}
        for chunk in chunks:
            chunk.legal.embedding_text = self._build_embedding_text(
                chunk, art_map, doc_meta
            )
            chunk.content = chunk.legal.embedding_text  

        logger.info(
            "Chunked %d articles into %d chunks (strategy=%s)",
            len(articles),
            len(chunks),
            self.get_strategy_name(),
        )
        return chunks

    def _make_single_chunk(
        self, art: dict, doc_meta: dict, chunk_index: int
    ) -> LegalChunk:
        """One article → one chunk. Content includes title_goc."""
        content_block = self._article_block(art)
        legal_meta = LegalChunkMetadata(
            so_ky_hieu=doc_meta.get("so_ky_hieu", ""),
            ten_day_du=doc_meta.get("ten_day_du", ""),
            loai_van_ban=doc_meta.get("loai_van_ban", ""),
            mongo_doc_id=str(doc_meta.get("_id", "")),
            dieu_numbers=[art.get("dieu", 0)],
            ten_dieu=art.get("ten_dieu", ""),
            article_mongo_ids=[str(art.get("_id", ""))],
        )
        return LegalChunk(
            content=content_block,
            chunk_index=chunk_index,
            legal=legal_meta,
            token_count=self._count_tokens(content_block),
        )

    def _try_merge(
        self,
        articles: list[dict],
        start_idx: int,
        doc_meta: dict,
        base_index: int,
    ) -> tuple[LegalChunk, int]:
        """Merge short articles.

        Cross-chapter merging IS allowed — the only constraint is the token
        budget (merged raw-content ≤ MAX_TOKENS).
        """
        base_art = articles[start_idx]
        merged_arts: list[dict] = [base_art]
        merged_raw_size = self._count_tokens(base_art.get("content", ""))

        i = start_idx + 1
        while i < len(articles):
            next_art = articles[i]
            next_size = self._count_tokens(next_art.get("content", ""))

            if merged_raw_size + next_size > self.MAX_TOKENS:
                break

            merged_arts.append(next_art)
            merged_raw_size += next_size
            i += 1

        # content = title_goc + raw_content per article, joined by blank line
        content_parts = [self._article_block(a) for a in merged_arts]
        merged_content = "\n\n".join(content_parts)

        legal_meta = LegalChunkMetadata(
            so_ky_hieu=doc_meta.get("so_ky_hieu", ""),
            ten_day_du=doc_meta.get("ten_day_du", ""),
            loai_van_ban=doc_meta.get("loai_van_ban", ""),
            mongo_doc_id=str(doc_meta.get("_id", "")),
            dieu_numbers=[a.get("dieu", 0) for a in merged_arts],
            ten_dieu=base_art.get("ten_dieu", ""),
            article_mongo_ids=[str(a.get("_id", "")) for a in merged_arts],
            is_merged=(len(merged_arts) > 1),
        )

        chunk = LegalChunk(
            content=merged_content,
            chunk_index=base_index,
            legal=legal_meta,
            token_count=self._count_tokens(merged_content),
        )
        return chunk, (i - start_idx)

    def _split_by_khoan(
        self, art: dict, doc_meta: dict, base_index: int
    ) -> list[LegalChunk]:
        """Split a long article by khoản (numbered clauses).

        Uses **balanced partitioning** instead of plain greedy bin-packing:
        1. Count total tokens and compute the minimum number of bins needed.
        2. Set a target = total / n_bins so bins are as equal as possible.
        3. Flush the current bin when adding the next khoản would move
           further from the target AND the current bin is already ≥ 80 %
           of the target (prevents premature flushing).

        Result: fewest possible chunks, sizes as equal as possible,
        every chunk ≤ MAX_TOKENS.
        """
        content = art.get("content", "")

        raw_parts = re.split(r"(?=\n\d+\.\s)", f"\n{content}")
        raw_parts = [p.strip() for p in raw_parts if p.strip()]
        if not raw_parts:
            raw_parts = [content]

        part_sizes = [self._count_tokens(p) for p in raw_parts]
        total      = sum(part_sizes)

        n_bins = max(1, math.ceil(total / self.MAX_TOKENS))
        target = total / n_bins          
        bins: list[str]  = []
        cur_parts: list[str] = []
        cur_size  = 0

        for part, size in zip(raw_parts, part_sizes):
            if not cur_parts:
                cur_parts.append(part)
                cur_size = size
                continue

            new_size = cur_size + size
            is_last_bin = len(bins) == n_bins - 1

            if new_size > self.MAX_TOKENS:
                bins.append("\n".join(cur_parts))
                cur_parts, cur_size = [part], size
            elif is_last_bin:
                cur_parts.append(part)
                cur_size = new_size
            else:
                # Flush if current bin is already reasonably full AND
                # adding would push us further away from target.
                # Threshold 0.6 × target allows flushing earlier when one
                # large khoản skews the distribution.
                dist_without = abs(cur_size  - target)
                dist_with    = abs(new_size  - target)
                if dist_without < dist_with and cur_size >= target * 0.6:
                    bins.append("\n".join(cur_parts))
                    cur_parts, cur_size = [part], size
                else:
                    cur_parts.append(part)
                    cur_size = new_size

        if cur_parts:
            bins.append("\n".join(cur_parts))

        chunks: list[LegalChunk] = []
        total = len(bins)
        for j, part in enumerate(bins):
            legal_meta = LegalChunkMetadata(
                so_ky_hieu=doc_meta.get("so_ky_hieu", ""),
                ten_day_du=doc_meta.get("ten_day_du", ""),
                loai_van_ban=doc_meta.get("loai_van_ban", ""),
                mongo_doc_id=str(doc_meta.get("_id", "")),
                dieu_numbers=[art.get("dieu", 0)],
                ten_dieu=art.get("ten_dieu", ""),
                article_mongo_ids=[str(art.get("_id", ""))],
                is_split=True,
                split_part=j + 1,
                split_total=total,
            )
            chunks.append(
                LegalChunk(
                    content=part,
                    chunk_index=base_index + j,
                    legal=legal_meta,
                    token_count=self._count_tokens(part),
                )
            )
        return chunks

    def _build_embedding_text(
        self,
        chunk: LegalChunk,
        art_map: dict[str, dict],
        doc_meta: dict,
    ) -> str:
        """Build the embedding_text string for a chunk.

        Uses Longest Common Path (LCP) for merged chunks so the shared
        prefix is written exactly once, and only the differing tail of
        each article's path is repeated per article.

        Format (all cases):
            {doc_header}. {common_path}.   ← written once
            {remaining_path_i}. {title_goc_i}
            {raw_content_i}

            {remaining_path_j}. {title_goc_j}
            {raw_content_j}
        """
        doc_header = self._build_doc_header(doc_meta)
        ids = chunk.legal.article_mongo_ids

        if chunk.legal.is_split:
            art = art_map.get(ids[0], {})
            path_str  = self._build_path_str(art)
            title_goc = art.get("title_goc", "") or art.get("ten_dieu", "")
            part_label = f"(phần {chunk.legal.split_part}/{chunk.legal.split_total})"
            header = self._join_header_parts(doc_header, path_str, f"{title_goc} {part_label}")
            return f"{header}\n{chunk.content}"

        if not chunk.legal.is_merged:
            art = art_map.get(ids[0], {})
            path_str  = self._build_path_str(art)
            title_goc = art.get("title_goc", "") or art.get("ten_dieu", "")
            header = self._join_header_parts(doc_header, path_str, title_goc)
            return f"{header}\n{art.get('content', '')}"

        arts = [art_map.get(aid, {}) for aid in ids]
        common_parts, remaining_per_art = self._find_common_path(arts)

        common_str    = " - ".join(common_parts)
        shared_header = self._join_header_parts(doc_header, common_str)

        # Nhóm các điều theo remaining-path giống nhau để tránh lặp prefix.
        # VD: Điều 12,13,14 cùng "Chương II" → ghi "Chương II" 1 lần rồi list điều
        groups: list[tuple[str, list[tuple[dict, str]]]] = []
        current_key: str | None = None
        current_group: list[tuple[dict, str]] = []

        for art, remaining in zip(arts, remaining_per_art):
            title_goc     = art.get("title_goc", "") or art.get("ten_dieu", "")
            remaining_str = " - ".join(remaining)
            if remaining_str != current_key:
                if current_group:
                    groups.append((current_key or "", current_group))
                current_key   = remaining_str
                current_group = [(art, title_goc)]
            else:
                current_group.append((art, title_goc))
        if current_group:
            groups.append((current_key or "", current_group))

        # Build output: mỗi nhóm ghi remaining_prefix 1 lần, sau đó từng điều
        blocks: list[str] = []
        for remaining_str, group_items in groups:
            group_lines: list[str] = []
            for art, title_goc in group_items:
                raw_content = art.get("content", "")
                # Chỉ ghi title_goc + content (remaining đã là header nhóm)
                group_lines.append(f"{title_goc}\n{raw_content}")
            # Nếu có remaining: ghi nó làm header nhóm 1 lần
            group_text = "\n\n".join(group_lines)
            if remaining_str:
                blocks.append(f"{remaining_str}.\n{group_text}")
            else:
                blocks.append(group_text)

        return shared_header + ".\n" + "\n\n".join(blocks)

    def _count_tokens(self, text: str) -> int:
        return len(text.split())

    def _build_doc_header(self, doc_meta: dict) -> str:
        """'Luật 109/2025/QH15: Thuế Thu Nhập Cá Nhân'"""
        return (
            f"{doc_meta.get('loai_van_ban', '')} "
            f"{doc_meta.get('so_ky_hieu', '')}: "
            f"{doc_meta.get('ten_day_du', '')}"
        )

    def _build_path_str(self, article: dict) -> str:
        """'Chương I' or 'Phần I - Chương II - Mục 3 - Tiểu mục 1'"""
        path = article.get("path", {}) or {}
        parts = [
            v for v in [
                path.get("phan"),
                path.get("chuong"),
                path.get("muc"),
                path.get("tieu_muc"),
            ]
            if v
        ]
        return " - ".join(parts)

    def _join_header_parts(self, *parts: str) -> str:
        """Join non-empty parts with '. ' separator."""
        return ". ".join(p for p in parts if p)

    def _find_common_path(
        self, arts: list[dict]
    ) -> tuple[list[str], list[list[str]]]:
        """Find the Longest Common Path prefix across a list of articles.

        Returns:
            common_parts      : list of path values shared by ALL articles
                                (in hierarchy order: phan→chuong→muc→tieu_muc)
            remaining_per_art : for each article, the path values AFTER the
                                common prefix (i.e. what differs)

        Examples (6 structural variants):
          Case 1 — cross at tieu_muc:
            common=[phan,chuong,muc]  remaining=[[tieu_muc_i],[tieu_muc_j]]
          Case 2 — cross at muc:
            common=[phan,chuong]      remaining=[[muc_i,...],[muc_j,...]]
          Case 3 — cross at chuong:
            common=[phan]             remaining=[[chuong_i,...],[chuong_j,...]]
          Case 6 — no common path:
            common=[]                 remaining=[[chuong_i,...],[chuong_j,...]]
        """
        PATH_KEYS = ["phan", "chuong", "muc", "tieu_muc"]
        paths = [art.get("path", {}) or {} for art in arts]

        common_parts: list[str] = []
        common_depth = 0
        for key in PATH_KEYS:
            values = [p.get(key) for p in paths]
            if all(v == values[0] for v in values):
                if values[0] is not None:
                    common_parts.append(values[0])
                common_depth += 1
            else:
                break

        remaining_per_art: list[list[str]] = []
        for path in paths:
            remaining = [
                path[key]
                for key in PATH_KEYS[common_depth:]
                if path.get(key)
            ]
            remaining_per_art.append(remaining)

        return common_parts, remaining_per_art

    def _article_block(self, article: dict) -> str:
        """'{title_goc}\\n{content}' — used as the `content` field of a chunk."""
        title_goc = article.get("title_goc", "") or article.get("ten_dieu", "")
        raw       = article.get("content", "")
        return f"{title_goc}\n{raw}" if title_goc else raw
