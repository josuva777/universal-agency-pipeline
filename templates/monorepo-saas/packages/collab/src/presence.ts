/**
 * Ephemeral Multiplayer Presence & Cursor Tracking Engine (Department 11)
 * High-frequency awareness protocol (<20ms latency)
 */

export interface UserPresence {
  id: string;
  name: string;
  color: string;
  cursor?: { x: number; y: number };
  focusedElementId?: string;
  lastActive: number;
}

export class PresenceManager {
  private peers: Map<string, UserPresence> = new Map();
  private localUser: UserPresence;
  private listeners: Set<(peers: UserPresence[]) => void> = new Set();

  constructor(localUser: UserPresence) {
    this.localUser = { ...localUser, lastActive: Date.now() };
  }

  public updateCursor(x: number, y: number): void {
    this.localUser.cursor = { x, y };
    this.localUser.lastActive = Date.now();
    this.notify();
  }

  public setFocus(elementId?: string): void {
    this.localUser.focusedElementId = elementId;
    this.localUser.lastActive = Date.now();
    this.notify();
  }

  public setPeerPresence(peerId: string, presence: UserPresence): void {
    this.peers.set(peerId, presence);
    this.notify();
  }

  public removePeer(peerId: string): void {
    this.peers.delete(peerId);
    this.notify();
  }

  public getActivePeers(): UserPresence[] {
    const now = Date.now();
    // Prune stale peers inactive for > 30 seconds
    for (const [id, peer] of this.peers.entries()) {
      if (now - peer.lastActive > 30000) {
        this.peers.delete(id);
      }
    }
    return Array.from(this.peers.values());
  }

  public subscribe(listener: (peers: UserPresence[]) => void): () => void {
    this.listeners.add(listener);
    listener(this.getActivePeers());
    return () => this.listeners.delete(listener);
  }

  private notify(): void {
    const peers = this.getActivePeers();
    for (const listener of this.listeners) {
      listener(peers);
    }
  }
}

