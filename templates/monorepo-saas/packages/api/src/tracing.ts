/**
 * OpenTelemetry Distributed Tracing Middleware & Core Engine
 * Conforms to W3C TraceContext & OpenTelemetry Semantic Conventions
 * Zero-dependency standalone fallback with optional @opentelemetry/api binding
 */

export interface TraceContext {
  traceId: string;
  spanId: string;
  traceFlags: string;
  parentSpanId?: string;
}

export type SpanStatusCode = 'UNSET' | 'OK' | 'ERROR';

export interface SpanAttributes {
  [key: string]: string | number | boolean | undefined;
}

export interface Span {
  name: string;
  context: TraceContext;
  startTime: number;
  endTime?: number;
  attributes: SpanAttributes;
  status: { code: SpanStatusCode; message?: string };
  events: Array<{ name: string; timestamp: number; attributes?: SpanAttributes }>;
  setAttribute: (key: string, value: string | number | boolean | undefined) => Span;
  setAttributes: (attrs: SpanAttributes) => Span;
  recordException: (err: unknown) => Span;
  setStatus: (status: { code: SpanStatusCode; message?: string }) => Span;
  addEvent: (name: string, attributes?: SpanAttributes) => Span;
  end: () => void;
}

export interface TracerConfig {
  serviceName: string;
  serviceVersion?: string;
  environment?: string;
  exportToConsole?: boolean;
}

/**
 * Generates W3C TraceContext compliant IDs
 */
function randomHex(bytes: number): string {
  const chars = '0123456789abcdef';
  let result = '';
  for (let i = 0; i < bytes * 2; i++) {
    result += chars[Math.floor(Math.random() * 16)];
  }
  return result;
}

export class EnterpriseTracer {
  private config: TracerConfig;

  constructor(config: TracerConfig) {
    this.config = {
      serviceVersion: '1.0.0',
      environment: process.env.NODE_ENV || 'development',
      exportToConsole: false,
      ...config,
    };
  }

  public startSpan(name: string, options?: { parent?: TraceContext; attributes?: SpanAttributes }): Span {
    const traceId = options?.parent?.traceId || randomHex(16); // 32-hex
    const spanId = randomHex(8); // 16-hex
    const context: TraceContext = {
      traceId,
      spanId,
      traceFlags: '01', // Sampled
      parentSpanId: options?.parent?.spanId,
    };

    const attributes: SpanAttributes = {
      'service.name': this.config.serviceName,
      'service.version': this.config.serviceVersion,
      'deployment.environment': this.config.environment,
      ...options?.attributes,
    };

    const span: Span = {
      name,
      context,
      startTime: Date.now(),
      attributes,
      status: { code: 'UNSET' },
      events: [],
      setAttribute(key, value) {
        this.attributes[key] = value;
        return this;
      },
      setAttributes(attrs) {
        Object.assign(this.attributes, attrs);
        return this;
      },
      recordException(err) {
        this.status = {
          code: 'ERROR',
          message: err instanceof Error ? err.message : String(err),
        };
        this.events.push({
          name: 'exception',
          timestamp: Date.now(),
          attributes: {
            'exception.message': err instanceof Error ? err.message : String(err),
            'exception.stack': err instanceof Error ? err.stack : undefined,
          },
        });
        return this;
      },
      setStatus(status) {
        this.status = status;
        return this;
      },
      addEvent(eventName, eventAttrs) {
        this.events.push({
          name: eventName,
          timestamp: Date.now(),
          attributes: eventAttrs,
        });
        return this;
      },
      end: () => {
        span.endTime = Date.now();
        const durationMs = span.endTime - span.startTime;
        if (this.config.exportToConsole) {
          console.log(`[TRACE] [${span.context.traceId}] ${span.name} (${durationMs}ms) - ${span.status.code}`);
        }
      },
    };

    return span;
  }

  /**
   * Automatically executes an async block within a tracked span
   */
  public async traceAsync<T>(
    name: string,
    attributes: SpanAttributes,
    fn: (span: Span) => Promise<T>,
    parent?: TraceContext
  ): Promise<T> {
    const span = this.startSpan(name, { parent, attributes });
    try {
      const result = await fn(span);
      if (span.status.code === 'UNSET') {
        span.setStatus({ code: 'OK' });
      }
      return result;
    } catch (err) {
      span.recordException(err);
      throw err;
    } finally {
      span.end();
    }
  }
}

// Global default tracer instance
export const defaultTracer = new EnterpriseTracer({
  serviceName: '@repo/api',
  serviceVersion: '2.1.0',
});

/**
 * Next.js / Edge API Route Tracing Middleware
 * Automatically injects traceparent and x-trace-id headers into response
 */
export function withTracing<TReq extends Request = Request, TRes = Response>(
  spanName: string,
  handler: (req: TReq, context?: any) => Promise<TRes>
) {
  return async (req: TReq, context?: any): Promise<TRes> => {
    const parentHeader = req.headers.get('traceparent') || undefined;
    let parentContext: TraceContext | undefined;

    if (parentHeader) {
      const parts = parentHeader.split('-');
      if (parts.length >= 4 && parts[1] && parts[2]) {
        parentContext = {
          traceId: parts[1],
          spanId: parts[2],
          traceFlags: parts[3] || '01',
        };
      }
    }

    const span = defaultTracer.startSpan(spanName, {
      parent: parentContext,
      attributes: {
        'http.method': req.method,
        'http.url': req.url,
      },
    });

    try {
      const response = await handler(req, context);
      span.setStatus({ code: 'OK' });

      // If response is a standard web Response, inject trace context headers
      if (response && typeof (response as any).headers?.set === 'function') {
        (response as any).headers.set('x-trace-id', span.context.traceId);
        (response as any).headers.set('x-span-id', span.context.spanId);
        (response as any).headers.set(
          'traceparent',
          `00-${span.context.traceId}-${span.context.spanId}-${span.context.traceFlags}`
        );
      }

      return response;
    } catch (error) {
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  };
}
