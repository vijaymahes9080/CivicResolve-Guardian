# ADR 0003: Hybrid Grounded RAG with Deterministic Fallbacks

## Status
Accepted

## Context
Standard RAG pipelines frequently suffer from hallucinations when the retrieval corpus lacks relevant documents or when vector similarity returns false-positive semantic matches. In government grievance handling, citing an incorrect regulation or fabricating an SLA violates administrative law.

## Decision
We implement a **Grounded Hybrid RAG Pipeline** with deterministic failure modes:
1. **Deterministic Document Chunking**: Policy documents are chunked by logical sections and assigned stable deterministic IDs (`DOC-{dept}-{id}-C{idx}`).
2. **Hybrid Scoring**: Combines dense vector similarity (Sentence Transformers or cosine lexical embeddings) with BM25/keyword boosting on civic terminology.
3. **Threshold Gating**: A strict relevance cutoff (0.50) is applied. If top retrieved passages fall below this threshold, the pipeline returns:
   ```json
   {
     "verdict": "insufficient_evidence",
     "citations": [],
     "reasons": ["No municipal policy matches the grievance claim with sufficient confidence."]
   }
   ```
4. **Audit Logging**: All retrieval queries, scores, and candidate document IDs are appended to the case audit log.

## Consequences
- **Pros**: Complete hallucination prevention on policy citations, verifiable legal grounding for officers.
- **Cons**: Requires well-structured synthetic policy documents with standardized section metadata.
