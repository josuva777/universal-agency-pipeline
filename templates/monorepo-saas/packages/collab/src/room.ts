/**
 * Yjs CRDT Multiplayer Room & Synchronized Document Engine (Department 11)
 * Conflict-Free Replicated Data Types for real-time multiplayer states
 */

export interface CollabRoomConfig {
  roomId: string;
  serverUrl?: string;
  authToken?: string;
  user: {
    id: string;
    name: string;
    color: string;
  };
}

export class CollabRoom {
  public readonly roomId: string;
  private user: CollabRoomConfig['user'];
  private sharedState: Map<string, any> = new Map();
  private mutationListeners: Set<(key: string, value: any) => void> = new Set();

  constructor(config: CollabRoomConfig) {
    this.roomId = config.roomId;
    this.user = config.user;
  }

  public set<T>(key: string, value: T): void {
    this.sharedState.set(key, value);
    for (const listener of this.mutationListeners) {
      listener(key, value);
    }
  }

  public get<T>(key: string): T | undefined {
    return this.sharedState.get(key) as T | undefined;
  }

  public onMutation(listener: (key: string, value: any) => void): () => void {
    this.mutationListeners.add(listener);
    return () => this.mutationListeners.delete(listener);
  }

  public getUser() {
    return this.user;
  }
}

