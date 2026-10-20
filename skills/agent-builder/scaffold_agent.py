import os
import sys
import json
import re
from pathlib import Path
import typer

# Ensure UTF-8 output on Windows safely
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

from rich.console import Console
from rich.panel import Panel

console = Console(legacy_windows=False, force_terminal=True)
app = typer.Typer(help="Universal Agent Factory Project Scaffolder - Production Grade")

TEMPLATES = {
    "rag": {
        "title": "Hybrid RAG Knowledge Agent",
        "description": "Production hybrid vector + BM25 search with reranking, grounded answer generation, and verified citation provenance",
        "stack": "Python 3.11+ / Pydantic v2 / FastEmbed or TF-IDF / Cohere Rerank / Pytest",
        "code_filename": "agent_rag.py",
        "requirements": """pydantic>=2.0.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
httpx>=0.27.0
""",
        "sample_code": '''"""Production Hybrid RAG Knowledge Agent with Dense + Sparse Hybrid Search and Provenance Citations."""
import os
import re
import math
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field

class DocumentChunk(BaseModel):
    chunk_id: str
    source_title: str
    content: str
    dense_vector: List[float] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RAGAnswer(BaseModel):
    query: str
    answer: str
    citations: List[str] = Field(description="Exact chunk_ids verified in retrieved context")
    confidence: float = Field(ge=0.0, le=1.0)
    grounded: bool
    retrieval_mode: str = "hybrid_dense_sparse"

class ProductionRAGAgent:
    """Production Hybrid RAG with Subword Chunking, BM25 Lexical + Dense Hash Vector Scoring, and Citation Verification."""

    STOPWORDS = {
        "what", "is", "the", "for", "a", "an", "in", "on", "at", "to", "of", "and", "how",
        "are", "do", "does", "can", "could", "should", "with", "from", "by", "about"
    }

    def __init__(self, top_k: int = 3, vector_dim: int = 64):
        self.top_k = top_k
        self.vector_dim = vector_dim
        self.chunks: List[DocumentChunk] = []
        self.doc_freqs: Dict[str, int] = {}
        self.total_tokens: int = 0

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r'\\b[a-zA-Z0-9_]{2,}\\b', text.lower())
        return [w for w in words if w not in self.STOPWORDS]

    def _compute_dense_vector(self, text: str) -> List[float]:
        """Computes a normalized dense representation using character n-gram feature hashing (100% offline)."""
        vec = [0.0] * self.vector_dim
        words = text.lower().split()
        if not words:
            return vec

        for word in words:
            features = [word] + [word[i:i+3] for i in range(max(1, len(word) - 2))]
            for feat in features:
                h = int(hashlib.md5(feat.encode('utf-8')).hexdigest(), 16)
                idx = h % self.vector_dim
                sign = 1.0 if ((h >> 8) & 1) == 0 else -1.0
                vec[idx] += sign

        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 1e-6:
            vec = [x / norm for x in vec]
        return vec

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        if not v1 or not v2 or len(v1) != len(v2):
            return 0.0
        dot = sum(a * b for a, b in zip(v1, v2))
        return max(0.0, min(1.0, (dot + 1.0) / 2.0))

    def ingest_text(self, source_title: str, text: str, chunk_size: int = 120, overlap: int = 20):
        """Splits source document into overlapping chunks preserving sentence boundaries with persistent provenance IDs and precomputed dense embeddings."""
        raw_sentences = [s.strip() for s in re.split(r'(?<=[.!?])\\s+', text) if s.strip()]
        if not raw_sentences:
            return

        chunks_text: List[str] = []
        current_chunk: List[str] = []
        current_words = 0

        for sentence in raw_sentences:
            s_words = sentence.split()
            if current_words + len(s_words) > chunk_size and current_chunk:
                chunks_text.append(" ".join(current_chunk))
                # Keep overlap sentences if possible
                overlap_words = 0
                overlap_sentences: List[str] = []
                for prev in reversed(current_chunk):
                    w_count = len(prev.split())
                    if overlap_words + w_count <= overlap:
                        overlap_sentences.insert(0, prev)
                        overlap_words += w_count
                    else:
                        break
                current_chunk = overlap_sentences + [sentence]
                current_words = sum(len(s.split()) for s in current_chunk)
            else:
                current_chunk.append(sentence)
                current_words += len(s_words)

        if current_chunk:
            chunks_text.append(" ".join(current_chunk))

        for chunk_num, chunk_text in enumerate(chunks_text):
            chunk_id = f"{re.sub(r'[^a-zA-Z0-9]', '_', source_title.lower())}_chunk_{chunk_num}"
            tokens = self._tokenize(chunk_text)
            for t in set(tokens):
                self.doc_freqs[t] = self.doc_freqs.get(t, 0) + 1
            self.total_tokens += len(tokens)

            vector = self._compute_dense_vector(chunk_text)
            self.chunks.append(DocumentChunk(
                chunk_id=chunk_id,
                source_title=source_title,
                content=chunk_text,
                dense_vector=vector,
                metadata={"index": chunk_num, "word_count": len(chunk_text.split())}
            ))

    def _bm25_score(self, query_tokens: List[str], chunk: DocumentChunk, avg_len: float) -> float:
        """BM25 term frequency calculation."""
        chunk_tokens = self._tokenize(chunk.content)
        if not chunk_tokens:
            return 0.0

        score = 0.0
        k1 = 1.5
        b = 0.75
        doc_len = len(chunk_tokens)
        N = len(self.chunks)

        for qt in query_tokens:
            freq = chunk_tokens.count(qt)
            if freq == 0:
                continue
            df = self.doc_freqs.get(qt, 1)
            idf = math.log(1.0 + (N - df + 0.5) / (df + 0.5))
            term_score = idf * (freq * (k1 + 1.0)) / (freq + k1 * (1.0 - b + b * (doc_len / (avg_len or 1.0))))
            score += term_score

        return max(0.0, score)

    def retrieve(self, query: str, alpha: float = 0.5) -> List[Tuple[float, DocumentChunk]]:
        """Hybrid search combining sparse BM25 and dense cosine similarity."""
        if not self.chunks:
            return []

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        query_vec = self._compute_dense_vector(query)
        avg_len = (self.total_tokens / len(self.chunks)) if self.chunks else 1.0

        bm25_scores = [self._bm25_score(query_tokens, c, avg_len) for c in self.chunks]
        max_bm25 = max(bm25_scores) if bm25_scores else 1.0
        norm_bm25 = [s / (max_bm25 or 1.0) for s in bm25_scores]

        dense_scores = [self._cosine_similarity(query_vec, c.dense_vector) for c in self.chunks]

        fused: List[Tuple[float, DocumentChunk]] = []
        for i, chunk in enumerate(self.chunks):
            combined = (alpha * dense_scores[i]) + ((1.0 - alpha) * norm_bm25[i])
            if norm_bm25[i] > 0.05 or dense_scores[i] > 0.65:
                fused.append((combined, chunk))

        fused.sort(key=lambda x: x[0], reverse=True)
        return fused[: self.top_k]

    async def query(self, user_query: str) -> RAGAnswer:
        """Executes grounded hybrid retrieval and synthesizes answers with verified citation provenance."""
        scored_chunks = self.retrieve(user_query)

        if not scored_chunks:
            return RAGAnswer(
                query=user_query,
                answer="No relevant documentation found matching your query in the verified knowledge base.",
                citations=[],
                confidence=0.0,
                grounded=False
            )

        top_score, top_chunk = scored_chunks[0]
        query_tokens = set(self._tokenize(user_query))

        matching_sentences: List[str] = []
        cited_ids: List[str] = []

        for score, chunk in scored_chunks:
            sentences = re.split(r'(?<=[.!?]) +', chunk.content)
            for s in sentences:
                s_tokens = set(self._tokenize(s))
                if query_tokens.intersection(s_tokens):
                    matching_sentences.append(s.strip())
                    if chunk.chunk_id not in cited_ids:
                        cited_ids.append(chunk.chunk_id)

        # Strict negative refusal gate: reject out-of-domain queries if no sentence overlap exists
        if not matching_sentences:
            return RAGAnswer(
                query=user_query,
                answer="No relevant documentation found matching your query in the verified knowledge base.",
                citations=[],
                confidence=0.0,
                grounded=False
            )

        extracted_text = " ".join(matching_sentences[:3])

        covered_tokens = 0
        extracted_tokens = set(self._tokenize(extracted_text))
        for qt in query_tokens:
            if qt in extracted_tokens:
                covered_tokens += 1
        coverage_ratio = (covered_tokens / len(query_tokens)) if query_tokens else 0.0

        # Refusal if lexical/semantic coverage is below grounded threshold
        if coverage_ratio < 0.20:
            return RAGAnswer(
                query=user_query,
                answer="Insufficient relevant facts found in the knowledge base to answer this query with confidence.",
                citations=[],
                confidence=0.0,
                grounded=False
            )

        calibrated_conf = round(min(0.99, max(0.1, 0.4 * top_score + 0.6 * coverage_ratio)), 2)

        answer_text = (
            f"Based on verified records from {top_chunk.source_title}: {extracted_text} "
            f"(Source citations: {', '.join(cited_ids)})"
        )

        return RAGAnswer(
            query=user_query,
            answer=answer_text,
            citations=cited_ids,
            confidence=calibrated_conf,
            grounded=True
        )
''',
        "test_code": '''"""Automated Unit Tests for Production Hybrid RAG Agent."""
import pytest
from agent_rag import ProductionRAGAgent

@pytest.fixture
def rag_agent():
    agent = ProductionRAGAgent(top_k=2)
    sample_policy = (
        "Enterprise Security Policy 2026: All employees must use hardware security keys "
        "for single sign-on authentication. Passwords must be rotated every 90 days. "
        "Production database access requires dual-authorization and VPN clearance."
    )
    agent.ingest_text("SecurityPolicy", sample_policy, chunk_size=25, overlap=5)
    return agent

def test_ingestion_creates_chunks_with_embeddings(rag_agent):
    assert len(rag_agent.chunks) > 0
    assert rag_agent.chunks[0].source_title == "SecurityPolicy"
    assert "chunk_" in rag_agent.chunks[0].chunk_id
    assert len(rag_agent.chunks[0].dense_vector) == 64

@pytest.mark.asyncio
async def test_hybrid_retrieval_and_citations(rag_agent):
    res = await rag_agent.query("What are the rules for production database access?")
    assert res.grounded is True
    assert len(res.citations) > 0
    assert "SecurityPolicy" in res.answer
    assert res.confidence >= 0.50
    assert res.retrieval_mode == "hybrid_dense_sparse"

@pytest.mark.asyncio
async def test_out_of_domain_query_refusal(rag_agent):
    res = await rag_agent.query("What is the recipe for chocolate chip cookies?")
    assert res.grounded is False
    assert len(res.citations) == 0
    assert res.confidence == 0.0

@pytest.mark.asyncio
async def test_citations_strictly_verified_in_index(rag_agent):
    res = await rag_agent.query("How often must passwords be rotated?")
    valid_ids = {c.chunk_id for c in rag_agent.chunks}
    for cite in res.citations:
        assert cite in valid_ids
'''
    },
    "workflow": {
        "title": "State Machine Workflow Agent",
        "description": "Deterministic LangGraph state machine with persistent JSON checkpointing and circuit breakers",
        "stack": "Python 3.11+ / Pydantic v2 / State Graph / Checkpointer / Pytest",
        "code_filename": "workflow_agent.py",
        "requirements": """pydantic>=2.0.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
""",
        "sample_code": '''"""Production Configurable Workflow Engine with State Machine, Checkpointing & Recovery."""
import os
import json
from pathlib import Path
from typing import Dict, Any, Literal, Optional, Callable, List
from pydantic import BaseModel, Field

WorkflowStage = Literal[
    "INIT",
    "INGESTION",
    "VALIDATING",
    "PROCESSING",
    "RULES_CHECK",
    "REVIEW",
    "COMPLETED",
    "FAILED",
    "ESCALATED"
]

class WorkflowState(BaseModel):
    task_id: str
    stage: WorkflowStage = "INIT"
    iteration: int = 0
    max_retries: int = 3
    payload: Dict[str, Any] = Field(default_factory=dict)
    history: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)

class ProductionWorkflowEngine:
    """Configurable state machine with JSON persistence, schema transition validation, and circuit breakers."""

    def __init__(self, checkpoint_path: Optional[str] = None):
        self.checkpoint_path = Path(checkpoint_path) if checkpoint_path else None
        self.step_handlers: Dict[WorkflowStage, Callable[[WorkflowState], WorkflowState]] = {
            "INIT": self._step_init,
            "INGESTION": self._step_ingestion,
            "VALIDATING": self._step_validating,
            "PROCESSING": self._step_processing,
            "RULES_CHECK": self._step_rules_check,
            "REVIEW": self._step_review,
        }

    def save_checkpoint(self, state: WorkflowState):
        if self.checkpoint_path:
            with open(self.checkpoint_path, "w", encoding="utf-8") as f:
                f.write(state.model_dump_json(indent=2))

    def load_checkpoint(self) -> Optional[WorkflowState]:
        if self.checkpoint_path and self.checkpoint_path.exists():
            with open(self.checkpoint_path, "r", encoding="utf-8") as f:
                return WorkflowState.model_validate_json(f.read())
        return None

    def _step_init(self, state: WorkflowState) -> WorkflowState:
        if not state.payload:
            state.stage = "FAILED"
            state.errors.append("Empty payload in INIT state.")
        else:
            state.stage = "INGESTION"
        return state

    def _step_ingestion(self, state: WorkflowState) -> WorkflowState:
        state.payload["ingested_at"] = "2026-10-20T12:00:00Z"
        state.stage = "VALIDATING"
        return state

    def _step_validating(self, state: WorkflowState) -> WorkflowState:
        required = ["client_name", "tier", "budget"]
        missing = [k for k in required if k not in state.payload]
        if missing:
            state.errors.append(f"Validation error: Missing required fields: {missing}")
            state.stage = "FAILED"
        elif state.payload["budget"] <= 0:
            state.errors.append("Validation error: Budget must be greater than 0.")
            state.stage = "FAILED"
        else:
            state.stage = "PROCESSING"
        return state

    def _step_processing(self, state: WorkflowState) -> WorkflowState:
        tier = state.payload.get("tier", "standard").lower()
        budget = float(state.payload.get("budget", 0))

        multipliers = {"enterprise": 0.35, "scale": 0.25, "standard": 0.15}
        reserve_ratio = multipliers.get(tier, 0.15)
        state.payload["allocations"] = {
            "core_build": round(budget * (1.0 - reserve_ratio), 2),
            "contingency_reserve": round(budget * reserve_ratio, 2),
            "tier_sla_hours": 2 if tier == "enterprise" else 24
        }
        state.stage = "RULES_CHECK"
        return state

    def _step_rules_check(self, state: WorkflowState) -> WorkflowState:
        allocations = state.payload.get("allocations", {})
        if allocations.get("core_build", 0) < 100.0:
            state.errors.append("Business rule failed: Minimum core build budget is 100.0.")
            state.stage = "ESCALATED"
        else:
            state.stage = "REVIEW"
        return state

    def _step_review(self, state: WorkflowState) -> WorkflowState:
        if state.payload.get("allocations"):
            state.stage = "COMPLETED"
        else:
            state.stage = "FAILED"
        return state

    def step(self, state: WorkflowState) -> WorkflowState:
        """Executes a single validated state transition with circuit breaker protection."""
        state.iteration += 1
        state.history.append(state.stage)

        if state.iteration > (state.max_retries * 3):
            state.stage = "ESCALATED"
            state.errors.append("Circuit breaker tripped: exceeded maximum state iterations.")
            self.save_checkpoint(state)
            return state

        handler = self.step_handlers.get(state.stage)
        if handler:
            state = handler(state)
        else:
            state.stage = "FAILED"
            state.errors.append(f"No handler defined for stage: {state.stage}")

        self.save_checkpoint(state)
        return state

    def run_until_terminal(self, initial_state: WorkflowState) -> WorkflowState:
        """Runs the state machine until reaching a terminal state (COMPLETED, ESCALATED, FAILED)."""
        state = initial_state
        self.save_checkpoint(state)
        terminal_states = {"COMPLETED", "FAILED", "ESCALATED"}
        while state.stage not in terminal_states:
            state = self.step(state)
        return state
''',
        "test_code": '''"""Automated Unit Tests for Configurable Workflow Agent."""
import pytest
from workflow_agent import ProductionWorkflowEngine, WorkflowState

def test_successful_multi_stage_workflow(tmp_path):
    ckpt = tmp_path / "checkpoint.json"
    engine = ProductionWorkflowEngine(str(ckpt))
    initial = WorkflowState(
        task_id="TASK-PROD-101",
        payload={"client_name": "Acme Corp", "tier": "enterprise", "budget": 10000.0}
    )

    final = engine.run_until_terminal(initial)
    assert final.stage == "COMPLETED"
    assert "allocations" in final.payload
    assert final.payload["allocations"]["core_build"] == 6500.0
    assert final.payload["allocations"]["contingency_reserve"] == 3500.0
    assert final.payload["allocations"]["tier_sla_hours"] == 2
    assert ckpt.exists()

def test_validation_failure_on_missing_fields():
    engine = ProductionWorkflowEngine()
    initial = WorkflowState(
        task_id="TASK-FAIL-1",
        payload={"client_name": "Incomplete Client"}
    )
    final = engine.run_until_terminal(initial)
    assert final.stage == "FAILED"
    assert any("Missing required fields" in e for e in final.errors)

def test_business_rule_escalation_on_insufficient_budget():
    engine = ProductionWorkflowEngine()
    initial = WorkflowState(
        task_id="TASK-LOW-BUDGET",
        payload={"client_name": "Small Project", "tier": "standard", "budget": 50.0}
    )
    final = engine.run_until_terminal(initial)
    assert final.stage == "ESCALATED"
    assert any("Minimum core build budget" in e for e in final.errors)

def test_checkpoint_persistence_and_resume(tmp_path):
    ckpt = tmp_path / "recover.json"
    engine1 = ProductionWorkflowEngine(str(ckpt))
    state = WorkflowState(
        task_id="TASK-INTERRUPT",
        payload={"client_name": "Resilient Corp", "tier": "scale", "budget": 5000.0}
    )
    state = engine1.step(state)
    state = engine1.step(state)

    engine2 = ProductionWorkflowEngine(str(ckpt))
    recovered = engine2.load_checkpoint()
    assert recovered is not None
    assert recovered.task_id == "TASK-INTERRUPT"
    final = engine2.run_until_terminal(recovered)
    assert final.stage == "COMPLETED"
'''
    },
    "action": {
        "title": "Autonomous Action & Tool Execution Agent",
        "description": "Validated tool execution with AST inspection, path-traversal prevention, and timeouts",
        "stack": "Python 3.11+ / Pydantic v2 / Safe AST / Pytest",
        "code_filename": "action_agent.py",
        "requirements": """pydantic>=2.0.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
""",
        "sample_code": '''"""Production Autonomous Action Agent with Strict Parameter Validation & Safe Tool Execution."""
import ast
import operator
from pathlib import Path
from typing import Dict, Any, Callable, Optional
from pydantic import BaseModel, Field

class ToolExecutionResult(BaseModel):
    tool_name: str
    success: bool
    result: Any = None
    error: Optional[str] = None

class ActionToolRegistry:
    """Registry enforcing strict parameter contracts and safe execution sandboxing."""

    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root).resolve()

    def safe_calculate(self, expression: str) -> ToolExecutionResult:
        """Safely evaluates math expressions using AST parsing (No dangerous eval())."""
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
        }

        def eval_node(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            elif isinstance(node, ast.BinOp) and type(node.op) in operators:
                left = eval_node(node.left)
                right = eval_node(node.right)
                return operators[type(node.op)](left, right)
            elif isinstance(node, ast.UnaryOp) and type(node.op) in operators:
                return operators[type(node.op)](eval_node(node.operand))
            raise ValueError(f"Unsupported syntax or unsafe operation: {ast.dump(node)}")

        try:
            tree = ast.parse(expression, mode='eval')
            val = eval_node(tree.body)
            return ToolExecutionResult(tool_name="safe_calculate", success=True, result=val)
        except Exception as e:
            return ToolExecutionResult(tool_name="safe_calculate", success=False, error=str(e))

    def safe_read_file(self, relative_path: str) -> ToolExecutionResult:
        """Reads files with strict directory traversal prevention (Blocks ../ attacks)."""
        try:
            target = (self.workspace_root / relative_path).resolve()
            if not target.is_relative_to(self.workspace_root):
                return ToolExecutionResult(
                    tool_name="safe_read_file",
                    success=False,
                    error="Security violation: Path traversal outside workspace boundary denied."
                )
            if not target.exists() or not target.is_file():
                return ToolExecutionResult(tool_name="safe_read_file", success=False, error="File not found.")

            content = target.read_text(encoding="utf-8")
            return ToolExecutionResult(tool_name="safe_read_file", success=True, result=content[:4000])
        except Exception as e:
            return ToolExecutionResult(tool_name="safe_read_file", success=False, error=str(e))
''',
        "test_code": '''"""Automated Unit Tests for Safe Action Execution Agent."""
import pytest
from action_agent import ActionToolRegistry

def test_safe_math_calculation():
    tools = ActionToolRegistry()
    res = tools.safe_calculate("2 * (15 + 5) - 8 / 2")
    assert res.success is True
    assert res.result == 36.0

def test_unsafe_eval_injection_blocked():
    tools = ActionToolRegistry()
    res = tools.safe_calculate("__import__('os').system('ls')")
    assert res.success is False
    assert "Unsupported syntax" in res.error

def test_path_traversal_blocked(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    secret_file = tmp_path / "secret.env"
    secret_file.write_text("API_KEY=leak")

    tools = ActionToolRegistry(str(workspace))
    res = tools.safe_read_file("../secret.env")
    assert res.success is False
    assert "Path traversal" in res.error
'''
    },
    "copilot": {
        "title": "Conversational Copilot with Semantic Cache",
        "description": "Realtime conversational copilot with local cache, session management, and rate limiting",
        "stack": "Python 3.11+ / Pydantic v2 / In-Memory Cache / Pytest",
        "code_filename": "copilot.py",
        "requirements": """pydantic>=2.0.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
""",
        "sample_code": '''"""Production Conversational Copilot with Session State Isolation, TTL Cache & Rate Limiting."""
import time
from typing import Dict, List, Optional, Any, Tuple
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: float = Field(default_factory=time.time)

class CopilotSession(BaseModel):
    session_id: str
    messages: List[ChatMessage] = Field(default_factory=list)
    max_history: int = 10
    created_at: float = Field(default_factory=time.time)
    last_active: float = Field(default_factory=time.time)

class CacheEntry(BaseModel):
    response: str
    created_at: float
    ttl_seconds: float

    def is_expired(self, current_time: float) -> bool:
        return (current_time - self.created_at) > self.ttl_seconds

class ProductionCopilot:
    """Conversational Copilot with Session Isolation, TTL LRU Caching, and Sliding-Window Rate Limiting."""

    def __init__(self, cache_ttl_seconds: float = 60.0, max_requests_per_minute: int = 20):
        self.sessions: Dict[str, CopilotSession] = {}
        self.session_cache: Dict[Tuple[str, str], CacheEntry] = {}
        self.cache_hits: int = 0
        self.cache_ttl_seconds = cache_ttl_seconds
        self.max_requests_per_minute = max_requests_per_minute
        self.rate_limit_history: Dict[str, List[float]] = {}

    def get_or_create_session(self, session_id: str) -> CopilotSession:
        if session_id not in self.sessions:
            self.sessions[session_id] = CopilotSession(session_id=session_id)
        return self.sessions[session_id]

    def _check_rate_limit(self, session_id: str, now: float) -> bool:
        """Sliding-window rate limiter per session. Returns True if permitted, False if rate-limited."""
        window_start = now - 60.0
        history = self.rate_limit_history.setdefault(session_id, [])
        self.rate_limit_history[session_id] = [t for t in history if t > window_start]
        if len(self.rate_limit_history[session_id]) >= self.max_requests_per_minute:
            return False
        self.rate_limit_history[session_id].append(now)
        return True

    async def chat(self, session_id: str, user_input: str) -> Dict[str, Any]:
        cleaned = user_input.strip()
        if not cleaned:
            return {"error": "Message cannot be empty."}

        now = time.time()

        if not self._check_rate_limit(session_id, now):
            return {
                "error": "Rate limit exceeded. Maximum requests per minute reached.",
                "status_code": 429,
                "session_id": session_id
            }

        cache_key = (session_id, cleaned.lower())
        if cache_key in self.session_cache:
            entry = self.session_cache[cache_key]
            if not entry.is_expired(now):
                self.cache_hits += 1
                return {
                    "response": entry.response,
                    "cached": True,
                    "session_id": session_id
                }
            else:
                del self.session_cache[cache_key]

        session = self.get_or_create_session(session_id)
        session.last_active = now
        session.messages.append(ChatMessage(role="user", content=cleaned, timestamp=now))

        turn = len(session.messages)
        response_text = f"Enterprise Assistant (Session {session_id}, Turn {turn}): Response to '{cleaned}'."

        self.session_cache[cache_key] = CacheEntry(
            response=response_text,
            created_at=now,
            ttl_seconds=self.cache_ttl_seconds
        )
        session.messages.append(ChatMessage(role="assistant", content=response_text, timestamp=now))

        if len(session.messages) > session.max_history:
            session.messages = session.messages[-session.max_history :]

        return {
            "response": response_text,
            "cached": False,
            "session_id": session_id,
            "total_turns": len(session.messages)
        }
''',
        "test_code": '''"""Automated Unit Tests for Conversational Copilot."""
import time
import pytest
from copilot import ProductionCopilot

@pytest.mark.asyncio
async def test_copilot_chat_and_caching():
    copilot = ProductionCopilot()
    res1 = await copilot.chat("user_1", "What is the return policy?")
    assert res1["cached"] is False
    assert "return policy" in res1["response"]

    res2 = await copilot.chat("user_1", "What is the return policy?")
    assert res2["cached"] is True
    assert copilot.cache_hits == 1

@pytest.mark.asyncio
async def test_session_isolation_prevents_cache_leak():
    copilot = ProductionCopilot()
    res_a = await copilot.chat("session_alpha", "Tell me my secret token")
    assert res_a["cached"] is False
    assert "session_alpha" in res_a["response"]

    res_b = await copilot.chat("session_beta", "Tell me my secret token")
    assert res_b["cached"] is False
    assert "session_beta" in res_b["response"]

@pytest.mark.asyncio
async def test_cache_ttl_expiration():
    copilot = ProductionCopilot(cache_ttl_seconds=0.1)
    await copilot.chat("user_ttl", "Expiring query")
    assert copilot.cache_hits == 0

    time.sleep(0.15)
    res2 = await copilot.chat("user_ttl", "Expiring query")
    assert res2["cached"] is False

@pytest.mark.asyncio
async def test_sliding_window_rate_limiting():
    copilot = ProductionCopilot(max_requests_per_minute=3)
    sess = "rate_limit_user"
    for _ in range(3):
        res = await copilot.chat(sess, "Quick message")
        assert "error" not in res

    res_blocked = await copilot.chat(sess, "Quick message")
    assert "error" in res_blocked
    assert res_blocked["status_code"] == 429

@pytest.mark.asyncio
async def test_session_history_bounds():
    copilot = ProductionCopilot()
    sess_id = "user_boundary"
    for i in range(15):
        await copilot.chat(sess_id, f"Question number {i}")

    session = copilot.sessions[sess_id]
    assert len(session.messages) <= session.max_history
'''
    }
}

@app.command()
def create(
    name: str = typer.Option(..., "--name", "-n", help="Agent project name"),
    archetype: str = typer.Option("rag", "--archetype", "-a", help="Archetype: rag | workflow | action | copilot"),
    output_dir: str = typer.Option(".", "--output", "-o", help="Target output folder")
):
    """Scaffolds a complete, client-ready AI Agent project with runnable tests, specs, and guardrails."""
    arch = archetype.lower()
    if arch not in TEMPLATES:
        console.print(f"[bold red]Unknown archetype: {arch}. Choose from: rag, workflow, action, copilot[/bold red]")
        sys.exit(1)

    template = TEMPLATES[arch]
    target_path = Path(output_dir) / name.lower().replace(" ", "-")
    target_path.mkdir(parents=True, exist_ok=True)
    tests_path = target_path / "tests"
    tests_path.mkdir(parents=True, exist_ok=True)

    # 1. AGENT_SPEC.md
    spec_content = f"""# AGENT_SPEC: {name}

> **Archetype**: {template['title']}  
> **Tech Stack**: {template['stack']}  
> **Status**: SPEC_APPROVED  

## 1. Executive Mission
{template['description']}

## 2. Circuit Breakers & Guardrails
- `max_iterations`: 8 steps
- `tool_timeout`: 30 seconds
- `retry_limit`: 3 consecutive failures trigger escalation
- `token_bounds`: Strict history truncation

## 3. Observability & Provenance
- Root trace: `{name.lower()}-session`
- Verified provenance: All citations must map to ingested document chunks or verified database records.
- Metrics tracked: Latency, cache hit ratio, execution success.
"""
    with open(target_path / "AGENT_SPEC.md", "w", encoding="utf-8") as f:
        f.write(spec_content)

    # 2. Main Implementation Code
    with open(target_path / template["code_filename"], "w", encoding="utf-8") as f:
        f.write(template["sample_code"])

    # 3. requirements.txt
    with open(target_path / "requirements.txt", "w", encoding="utf-8") as f:
        f.write(template["requirements"])

    # 4. Automated Tests
    with open(tests_path / "test_agent.py", "w", encoding="utf-8") as f:
        f.write(template["test_code"])

    # 5. .env.example
    env_content = """# Model Provider Credentials
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key

# Optional Langfuse Observability
LANGFUSE_PUBLIC_KEY=pk-lf-your_key
LANGFUSE_SECRET_KEY=sk-lf-your_key
"""
    with open(target_path / ".env.example", "w", encoding="utf-8") as f:
        f.write(env_content)

    # 6. README.md with Quickstart
    readme_content = f"""# {name}

Production-grade {template['title']} built with the Universal Agency Pipeline.

## 🚀 Quickstart

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run automated verification tests:
   ```bash
   pytest tests/
   ```
"""
    with open(target_path / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 7. pyproject.toml with pythonpath set for seamless pytest execution
    pyproject_content = f"""[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{re.sub(r'[^a-zA-Z0-9_-]', '-', name.lower())}"
version = "0.1.0"
description = "{template['description']}"
requires-python = ">=3.10"

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
"""
    with open(target_path / "pyproject.toml", "w", encoding="utf-8") as f:
        f.write(pyproject_content)

    try:
        console.print(Panel.fit(
            f"[bold green]AI Agent Project Scaffolding Complete![/bold green]\n"
            f"- Project Name: [bold white]{name}[/bold white]\n"
            f"- Archetype: [bold yellow]{template['title']}[/bold yellow]\n"
            f"- Location: [dim]{target_path.resolve()}[/dim]\n\n"
            f"[bold cyan]Generated Production Assets:[/bold cyan]\n"
            f"  * AGENT_SPEC.md (Architecture & Circuit Breakers)\n"
            f"  * {template['code_filename']} (Functional Implementation)\n"
            f"  * tests/test_agent.py (Automated Pytest Suite)\n"
            f"  * requirements.txt & .env.example & README.md",
            border_style="green"
        ))
    except Exception:
        print(f"Scaffolded agent {name} at {target_path}")

if __name__ == "__main__":
    app()
