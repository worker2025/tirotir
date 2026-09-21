"""Event Runtime مستقل از backendهای GUI و graphics."""
from dataclasses import dataclass, field
from collections import deque
from typing import Any, Callable

@dataclass(frozen=True)
class Event:
    name: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: int = 0
    source: str = 'runtime'

class EventQueue:
    def __init__(self): self._items=deque()
    def emit(self,event: Event): self._items.append(event)
    def pop(self): return self._items.popleft() if self._items else None
    def __len__(self): return len(self._items)

class HandlerRegistry:
    def __init__(self): self._handlers={}
    def on(self,name,handler): self._handlers.setdefault(name,[]).append(handler)
    def dispatch(self,event):
        for handler in tuple(self._handlers.get(event.name,())): handler(event)

class EventLoop:
    def __init__(self): self.queue=EventQueue();self.handlers=HandlerRegistry();self.running=False;self.paused=False;self.tick_count=0
    def emit(self,name,payload=None,source='runtime'):
        self.queue.emit(Event(name,payload or {},self.tick_count,source))
    def on(self,name,handler): self.handlers.on(name,handler)
    def tick(self,max_events=1000):
        if self.paused:return 0
        count=0;self.tick_count+=1
        while len(self.queue) and count<max_events:
            event=self.queue.pop();self.handlers.dispatch(event);count+=1
        return count
    def run(self,max_ticks=10000):
        self.running=True; ticks=0
        while self.running and ticks<max_ticks:
            self.tick();ticks+=1
            if not len(self.queue):break
        return ticks
    def pause(self): self.paused=True
    def resume(self): self.paused=False
    def stop(self): self.running=False
