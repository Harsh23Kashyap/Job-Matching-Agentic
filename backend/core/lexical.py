"""Lexical baselines (BM25, TF-IDF) on the same resume/job text templates as dense retrieval."""
from __future__ import annotations

import math
from collections import Counter

from core.document_text import job_document_text, resume_document_text
from core.text_tokenizer import tokenize


class _BM25:
    def __init__(self, tokenized_docs: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.docs = tokenized_docs
        self.n_docs = len(tokenized_docs)
        self.doc_lens = [len(d) for d in tokenized_docs]
        self.avgdl = sum(self.doc_lens) / self.n_docs if self.n_docs else 0.0
        self.df: Counter[str] = Counter()
        for tokens in tokenized_docs:
            for term in set(tokens):
                self.df[term] += 1
        self.idf = {
            term: math.log(1.0 + (self.n_docs - freq + 0.5) / (freq + 0.5))
            for term, freq in self.df.items()
        }

    def get_scores(self, query_tokens: list[str]) -> list[float]:
        scores = [0.0] * self.n_docs
        if not query_tokens:
            return scores
        q_freq = Counter(query_tokens)
        for term, _qf in q_freq.items():
            if term not in self.idf:
                continue
            idf = self.idf[term]
            for i, doc in enumerate(self.docs):
                tf = doc.count(term)
                if tf == 0:
                    continue
                dl = self.doc_lens[i]
                denom = tf + self.k1 * (1.0 - self.b + self.b * dl / self.avgdl)
                scores[i] += idf * (tf * (self.k1 + 1.0)) / denom
        return scores


def _build_tfidf_index(job_texts: list[str]):
    tokenized = [tokenize(t) for t in job_texts]
    df: Counter[str] = Counter()
    for tokens in tokenized:
        for term in set(tokens):
            df[term] += 1
    n_docs = len(job_texts)
    idf = {term: math.log((1.0 + n_docs) / (1.0 + count)) + 1.0 for term, count in df.items()}

    def vector(tokens: list[str]) -> dict[str, float]:
        tf = Counter(tokens)
        if not tf:
            return {}
        max_tf = max(tf.values())
        vec: dict[str, float] = {}
        for term, count in tf.items():
            if term not in idf:
                continue
            vec[term] = (count / max_tf) * idf[term]
        return vec

    job_vectors = [vector(tokens) for tokens in tokenized]
    return job_vectors, vector


def _cosine_sparse(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in a.keys() & b.keys())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


class LexicalRanker:
    def __init__(self, jobs: list[dict], *, rich: bool = False):
        self.job_ids = [j["id"] for j in jobs]
        self.job_texts = [job_document_text(j, rich=rich) for j in jobs]
        self._tokenized_jobs = [tokenize(t) for t in self.job_texts]
        self._job_vectors, self._vectorize = _build_tfidf_index(self.job_texts)
        self._bm25 = _BM25(self._tokenized_jobs)
        self._rich = rich

    def rank_jobs(self, resume: dict, method: str, top_k: int) -> list[tuple[str, float]]:
        query_tokens = tokenize(resume_document_text(resume, rich=self._rich))

        if method == "bm25":
            scores = self._bm25.get_scores(query_tokens)
        elif method == "tfidf":
            qvec = self._vectorize(query_tokens)
            scores = [_cosine_sparse(qvec, jvec) for jvec in self._job_vectors]
        else:
            raise ValueError(f"Unknown lexical method: {method}")

        ranked = sorted(zip(self.job_ids, scores), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]
