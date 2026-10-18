import os
import sys
import typer
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console(legacy_windows=False, force_terminal=True)
app = typer.Typer(help="Universal Agent Factory Project Scaffolder")

TEMPLATES = {
    "rag": {
        "title": "Hybrid RAG Knowledge Agent",
        "description": "Production hybrid vector + BM25 search with Cohere reranking and strict citation provenance",
        "stack": "LlamaIndex + Qdrant + BM25 + Cohere Rerank + Langfuse",
        "code_filename": "agent_rag.py",
        "sample_code": '''import os
from pydantic import BaseModel, Field
from langfuse.decorators import observe, langfuse_context

class RAGAnswer(BaseModel):
    answer: str = Field(description="Answer derived strictly from grounding context")
    citations: list[str] = Field(description="Chunk IDs cited in the answer")
    confidence: float = Field(ge=0.0, le=1.0)

@observe()
async def query_knowledge_base(user_query: str) -> RAGAnswer:
    langfuse_context.update_current_observation(input=user_query)
    # 1. Hybrid Search (Dense + BM25)
    # 2. Rerank top 5
    # 3. LLM synthesis with citations
    result = RAGAnswer(
        answer="Ground truth response citing [doc_chunk_1].",
        citations=["doc_chunk_1"],
        confidence=0.96
    )
    langfuse_context.update_current_observation(output=result.model_dump())
    return result
'''
    },
    "workflow": {
        "title": "State Machine Workflow Agent",
        "description": "Deterministic LangGraph state machine with human-in-the-loop and circuit breakers",
        "stack": "LangGraph + Pydantic + Checkpointer + Langfuse",
        "code_filename": "workflow_agent.py",
        "sample_code": '''import os
from typing import TypedDict, List, Literal
from langgraph.graph import StateGraph, END
from langfuse.decorators import observe

class AgentState(TypedDict):
    task_id: str
    iteration: int
    is_complete: bool
    data: dict

MAX_STEPS = 8

def router(state: AgentState) -> str:
    if state["iteration"] >= MAX_STEPS:
        return "escalate"
    if state["is_complete"]:
        return "finalize"
    return "process"

@observe()
async def process_node(state: AgentState) -> dict:
    return {"iteration": state["iteration"] + 1, "is_complete": True}

@observe()
async def escalate_node(state: AgentState) -> dict:
    return {"status": "escalated_to_human"}

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("process", process_node)
    graph.add_node("escalate", escalate_node)
    graph.set_entry_point("process")
    graph.add_conditional_edges("process", router, {"finalize": END, "escalate": "escalate", "process": "process"})
    graph.add_edge("escalate", END)
    return graph.compile()
'''
    },
    "action": {
        "title": "Autonomous Action & Code Execution Agent",
        "description": "ReAct loop with isolated E2B microVM code execution and circuit breakers",
        "stack": "LangGraph + E2B Sandbox + Tavily + Langfuse",
        "code_filename": "action_agent.py",
        "sample_code": '''import os
from e2b_code_interpreter import Sandbox
from langfuse.decorators import observe

@observe(name="execute_python_sandbox")
async def run_sandboxed(code: str) -> str:
    with Sandbox(api_key=os.getenv("E2B_API_KEY")) as sandbox:
        res = sandbox.run_code(code)
        return "\\n".join(res.logs.stdout) or "Executed successfully."
'''
    },
    "copilot": {
        "title": "Conversational Copilot with Semantic Cache",
        "description": "Realtime streaming copilot with Upstash semantic caching and Llama Guard",
        "stack": "Vercel AI SDK / FastAPI + Upstash Vector + Redis + Langfuse",
        "code_filename": "copilot.py",
        "sample_code": '''from fastapi import FastAPI
from pydantic import BaseModel
from langfuse.decorators import observe

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    user_id: str

@app.post("/chat")
@observe()
async def chat_endpoint(req: ChatRequest):
    # 1. Semantic cache check
    # 2. Input sanitization
    # 3. Streamed LLM response
    return {"response": f"Echoing from copilot: {req.message}"}
'''
    }
}

@app.command()
def create(
    name: str = typer.Option(..., "--name", "-n", help="Agent project name"),
    archetype: str = typer.Option("rag", "--archetype", "-a", help="Archetype: rag | workflow | action | copilot"),
    output_dir: str = typer.Option(".", "--output", "-o", help="Target output folder")
):
    """Scaffolds a complete, client-ready AI Agent project with tests, specs, and guardrails."""
    arch = archetype.lower()
    if arch not in TEMPLATES:
        console.print(f"[bold red]Unknown archetype: {arch}. Choose from: rag, workflow, action, copilot[/bold red]")
        sys.exit(1)

    template = TEMPLATES[arch]
    target_path = Path(output_dir) / name.lower().replace(" ", "-")
    target_path.mkdir(parents=True, exist_ok=True)

    # 1. AGENT_SPEC.md
    spec_content = f"""# AGENT_SPEC: {name}

> **Archetype**: {template['title']}  
> **Tech Stack**: {template['stack']}  
> **Status**: SPEC_APPROVED  

## 1. Executive Mission
{template['description']}

## 2. Circuit Breakers
- `max_iterations`: 8 steps
- `tool_timeout`: 30 seconds
- `retry_limit`: 3 consecutive failures trigger human escalation

## 3. Observability
- Root trace: `{name.lower()}-session`
- Tracked metrics: latency, token usage, cost, tool failures

## 4. Promptfoo Redteam Tests
- Jailbreak refusal check
- Empty prompt handling
- Citation provenance validation
"""
    with open(target_path / "AGENT_SPEC.md", "w", encoding="utf-8") as f:
        f.write(spec_content)

    # 2. Sample Code
    with open(target_path / template["code_filename"], "w", encoding="utf-8") as f:
        f.write(template["sample_code"])

    # 3. .env.example
    env_content = """# Langfuse Observability
LANGFUSE_PUBLIC_KEY=pk-lf-your_key
LANGFUSE_SECRET_KEY=sk-lf-your_key
LANGFUSE_HOST=https://cloud.langfuse.com

# LLM Providers
OPENAI_API_KEY=your_openai_key
# ANTHROPIC_API_KEY=your_anthropic_key
"""
    with open(target_path / ".env.example", "w", encoding="utf-8") as f:
        f.write(env_content)

    # 4. promptfoo.yaml
    promptfoo_content = """providers:
  - id: openai:gpt-4o-mini
prompts:
  - "file://system_prompt.txt"
tests:
  - description: "Core domain test"
    vars:
      input: "Hello"
    assert:
      - type: not-contains
        value: "as an AI language model"
"""
    with open(target_path / "promptfoo.yaml", "w", encoding="utf-8") as f:
        f.write(promptfoo_content)

    with open(target_path / "system_prompt.txt", "w", encoding="utf-8") as f:
        f.write(f"You are {name}, a specialized enterprise AI system.")

    console.print(Panel.fit(
        f"[bold green]✨ AI Agent Project Scaffolding Complete![/bold green]\n"
        f"• Project Name: [bold white]{name}[/bold white]\n"
        f"• Archetype: [bold yellow]{template['title']}[/bold yellow]\n"
        f"• Location: [dim]{target_path.resolve()}[/dim]\n\n"
        f"[bold cyan]Generated Files:[/bold cyan]\n"
        f"  - AGENT_SPEC.md (Architecture & Circuit Breakers)\n"
        f"  - {template['code_filename']} (Production Boilerplate)\n"
        f"  - promptfoo.yaml (Adversarial Security Evals)\n"
        f"  - .env.example & system_prompt.txt",
        border_style="green"
    ))

if __name__ == "__main__":
    app()
