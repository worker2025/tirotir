from .model import ModuleId

class ModuleCache:
    """هر module در یک اجرای پروژه فقط یک بار initialize می‌شود."""
    def __init__(self): self._values={}
    def has(self,module_id): return module_id in self._values
    def get(self,module_id): return self._values[module_id]
    def put(self,module_id,value): self._values[module_id]=value; return value
    def get_or_load(self,module_id,loader):
        if self.has(module_id): return self.get(module_id)
        return self.put(module_id,loader(module_id))
