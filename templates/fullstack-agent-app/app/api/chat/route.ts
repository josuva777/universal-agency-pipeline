import { openai } from '@ai-sdk/openai';
import { streamText, tool } from 'ai';
import { z } from 'zod';

export const runtime = 'nodejs';

// Prompt Injection Sanitizer
const FORBIDDEN_INJECTIONS = [
  /ignore (all|previous) instructions/i,
  /reveal system prompt/i,
  /DAN mode/i,
];

export async function POST(req: Request) {
  const { messages } = await req.json();
  const latestMessage = messages[messages.length - 1]?.content || '';

  // 1. Guardrail check
  if (FORBIDDEN_INJECTIONS.some((p) => p.test(latestMessage))) {
    return new Response(
      JSON.stringify({ error: 'Security policy violation: prompt injection attempt blocked.' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // 2. Streamed Agent Execution
  const result = streamText({
    model: openai('gpt-4o-mini'),
    system: `You are an elite enterprise AI assistant.
Be concise, grounded, and accurate.
Never hallucinate facts. If context is missing, ask the user clarifying questions.`,
    messages,
    maxSteps: 8, // Strict Circuit Breaker
    tools: {
      lookupDatabase: tool({
        description: 'Lookup structured customer or account records by ID',
        parameters: z.object({
          id: z.string().describe('The entity ID to search'),
        }),
        execute: async ({ id }) => {
          return { status: 'success', recordId: id, details: 'Verified database record' };
        },
      }),
    },
  });

  return result.toDataStreamResponse();
}
