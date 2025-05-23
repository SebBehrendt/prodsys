from collections import defaultdict
from typing import Callable, List, TypeVar, Dict

# Define generic hook types for now, can be replaced by specific Enums or ABCs later
HOOK_TYPE_ROUTING = "routing"
HOOK_TYPE_CONTROL_LOGIC = "control_logic"
HOOK_TYPE_STATE_CREATION = "state_creation"
HOOK_TYPE_PROCESS_LOGIC = "process_logic"
# Add more specific hook types as needed, e.g.
# HOOK_TYPE_ROUTING_BEFORE_DECISION = "routing_before_decision"
# HOOK_TYPE_ROUTING_AFTER_DECISION = "routing_after_decision"

T = TypeVar('T')

class PluginManager:
    """
    A simple manager to register and retrieve plugin hooks.
    Hooks are callback functions or objects with specific methods that can be
    injected into the simulation's execution flow.
    """
    def __init__(self):
        self._hooks: Dict[str, List[Callable]] = defaultdict(list)

    def register_hook(self, hook_type: str, hook_instance: Callable):
        """
        Registers a hook for a given hook type.

        Args:
            hook_type (str): The type of the hook (e.g., "routing", "control_logic").
            hook_instance (Callable): The hook function or method to register.
        """
        if not callable(hook_instance):
            # If it's an object with specific methods, we might need to adapt this
            # or ensure plugins register specific methods rather than whole objects
            # for this simple implementation, we expect callables.
            raise ValueError(f"Hook instance for type '{hook_type}' must be callable.")
        self._hooks[hook_type].append(hook_instance)
        print(f"Registered hook for type: {hook_type}")


    def get_hooks(self, hook_type: str) -> List[Callable]:
        """
        Retrieves all registered hooks for a given hook type.

        Args:
            hook_type (str): The type of the hook.

        Returns:
            List[Callable]: A list of registered hook functions/methods for that type.
        """
        return self._hooks.get(hook_type, [])

    def unregister_hook(self, hook_type: str, hook_instance: Callable):
        """
        Unregisters a specific hook.

        Args:
            hook_type (str): The type of the hook.
            hook_instance (Callable): The specific hook instance to remove.
        """
        if hook_type in self._hooks and hook_instance in self._hooks[hook_type]:
            self._hooks[hook_type].remove(hook_instance)
            print(f"Unregistered hook for type: {hook_type}")


# Global instance of PluginManager, if desired, or it can be instantiated where needed.
# For simplicity in integration, a global instance can be easier to start with.
# However, for better testability and modularity, passing instances is preferred.
# Let's start by requiring instantiation for now.
# plugin_manager = PluginManager()
