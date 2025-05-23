import abc
from typing import List, Optional, Any, TYPE_CHECKING

# Forward declarations for type hinting to avoid circular imports
if TYPE_CHECKING:
    from prodsys.simulation.router import Router  # Corrected: Per subtask's verification logic
    from prodsys.simulation import request  # Corrected: Per subtask's verification logic
    from prodsys.simulation.control import Controller
    from prodsys.simulation.resources import Resource
    from prodsys.simulation.process import Process
    from prodsys.simulation.state import State # Confirmed by subtask


class RoutingHook(abc.ABC):
    """
    Abstract base class for routing hooks.
    Plugins can implement these methods to customize routing decisions.
    """

    @abc.abstractmethod
    def before_routing(self, router: 'Router', requests: List['request.Request']) -> List['request.Request']: # Corrected: Per subtask's verification logic
        """
        Called before the router makes a routing decision.
        Allows modification of the list of pending requests.

        Args:
            router: The Router instance.
            requests: The current list of requests being considered.

        Returns:
            The (potentially modified) list of requests.
        """
        pass

    @abc.abstractmethod
    def decide_route(self, router: 'Router', requests: List['request.Request']) -> Optional['request.Request']: # Corrected: Per subtask's verification logic
        """
        Called to allow a plugin to make the routing decision.
        If this hook returns a Request, that request is chosen,
        and further decide_route hooks or default logic may be skipped.

        Args:
            router: The Router instance.
            requests: The list of candidate requests.

        Returns:
            A chosen Request if the plugin makes a decision, otherwise None.
        """
        pass


class ControlLogicHook(abc.ABC):
    """
    Abstract base class for control logic hooks.
    Plugins can implement these to modify or extend controller behavior.
    """

    @abc.abstractmethod
    def before_control_loop_iteration(self, controller: 'Controller'):
        """
        Called at the beginning of a controller's control_loop iteration.

        Args:
            controller: The Controller instance.
        """
        pass

    @abc.abstractmethod
    def after_request_assignment(self, controller: 'Controller', request: 'request.Request'): # Corrected: Per subtask's verification logic
        """
        Called after a request has been assigned to the controller's resource.

        Args:
            controller: The Controller instance.
            request: The request that was assigned.
        """
        pass


class StateCreationHook(abc.ABC):
    """
    Abstract base class for state creation hooks.
    Plugins can use these to customize state objects when they are created.
    """

    @abc.abstractmethod
    def on_state_create(self, resource: 'Resource', state_data: Any) -> Optional['State']:
        """
        Called when a state is being created for a resource.
        Allows modification of state_data or returning a custom State instance.

        Args:
            resource: The resource for which the state is being created.
            state_data: The configuration data for the state.

        Returns:
            A custom State instance to be used, or None to proceed with default creation.
        """
        pass


class ProcessExecutionHook(abc.ABC):
    """
    Abstract base class for process execution hooks.
    Plugins can use these to inject logic before/after process steps or on failures.
    """

    @abc.abstractmethod
    def before_process_start(self, process: 'Process', resource: 'Resource', request: 'request.Request'): # Corrected: Per subtask's verification logic
        """
        Called before a process starts execution on a resource.

        Args:
            process: The Process instance.
            resource: The Resource instance executing the process.
            request: The Request that triggered this process.
        """
        pass

    @abc.abstractmethod
    def after_process_finish(self, process: 'Process', resource: 'Resource', request: 'request.Request'): # Corrected: Per subtask's verification logic
        """
        Called after a process successfully finishes execution.

        Args:
            process: The Process instance.
            resource: The Resource instance.
            request: The Request.
        """
        pass

    @abc.abstractmethod
    def on_process_failure(self, process: 'Process', resource: 'Resource', request: 'request.Request', exception: Exception): # Corrected: Per subtask's verification logic
        """
        Called if a process fails during execution.

        Args:
            process: The Process instance.
            resource: The Resource instance.
            request: The Request.
            exception: The exception that occurred.
        """
        pass
