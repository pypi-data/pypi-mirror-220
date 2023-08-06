"""
Base classes for the simulation framework
"""
# TODO-2: Question: how to support optional dependencies (e.g. FLT << Equilibrium | Biot-savart)
#     -> maybe not necessary if Equilibrium returns None for 0 pressure
#     -> BranchPythonOperator? airflow/example_dags/example_branch_python_dop_operator_3.py
# TODO-1: move Code to different module, maybe even in simulation.bases?

import abc
import inspect
import typing
import logging
import os
import functools
import dask
from dask.delayed import Delayed
from datetime import datetime
import importlib.metadata
import git

import rna.pattern.backend
import rna.pattern.decorator
from w7x.lib import dataclasses
from w7x.merge import merge_children_cumulative
from .switches import distribute, stateful, exposed
from .state import (
    State,
    StateComponent,
    StateComposite,
    StateLeaf,
    DefaultFlag,
)


LOGGER = logging.getLogger(__name__)


def _func_key(fun):
    if isinstance(fun, Code):
        # call method is to be used
        if fun.mode is not None:
            fun = getattr(fun, fun.mode)
        else:
            fun = fun._call
    name = fun.__module__ + "." + fun.__qualname__
    return name


class Backend(rna.pattern.backend.Backend):
    """
    Adaptaion of the 'Strategy' class from the strategy design pattern. Backends are the meat of
    the implementation for a certain variant of a code.
    """

    STRATEGY_MODULE_BASE = "w7x.simulation.backends"
    STRATEGY_MODULE_NAME = -1

    @classmethod
    def from_module(cls, strategy: str, *args, **kwargs) -> rna.pattern.backend.Backend:
        """
        Adding ("local", "slurm", "ssh") -> "runner" forwarding
        """
        try:
            backend = super().from_module(strategy, *args, **kwargs)
        except ModuleNotFoundError:
            if strategy in ("local", "slurm", "ssh"):
                backend = super().from_module("runner", *args, **kwargs)
                backend.runner = strategy
            else:
                raise
        return backend


class Code(rna.pattern.backend.Frontend):
    """
    Adaptaion of the 'Context' class from the strategy design pattern. The Node defines the high
    level api for a code. Multiple backends can be used with the same interface.

    A calculation of the node is delegated mostly to the backend. Only high level functionality
    like e.g. outer optimization loops or inference is done on the `Code` level (or even higher,
    like in :module:`w7x.simulation.flavors`).

    .. mermaid::

        classDiagram
            direction BT

            namespace Strategy-Design-Pattern {
                class Code{
                }

                class Backend{
                }
            }

            Code ..> Backend

            class Vmec {
                <<abstract>>
                +/*abstract*/ free_boundary()*
                +/*abstract*/ fixed_boundary()*
            }

            class VmecLocalBackend {
                +free_boundary()
                +fixed_boundary()
            }

            class VmecWebserviceBackend {
                +free_boundary()
                +fixed_boundary()
            }


            Vmec --|> Code
            VmecLocalBackend --|> Backend
            VmecWebserviceBackend --|> Backend
            VmecNNBackend --|> Backend
            VmecSlurmBackend --|> Backend
            Vmec --> VmecLocalBackend
            Vmec --> VmecWebserviceBackend
            Vmec --> VmecNNBackend
            Vmec --> VmecSlurmBackend

    Args:
        backend
        mode (str): The mode decides what to do when calling this function

    Attributes:
        _mode: method name to call in __call__

    Examples:
        >>> import w7x.simulation.flt
        >>> flt = w7x.simulation.flt.FieldLineTracer()
        >>> assert isinstance(flt.backend, w7x.simulation.flt.FieldLineTracerBackend)
    """

    def __init__(self, mode: typing.Optional[str] = None, **kwargs):
        self._mode = mode

        super().__init__(**kwargs)

    @property
    def mode(self) -> str:
        """
        Name of a node method.
        Determines the default call of the Node.
        """
        return self._mode

    @mode.setter
    def mode(self, mode: str):
        if mode is not None:
            self._mode = mode

    def __call__(self, *args, **kwargs) -> State:
        """
        Short hand to set the method.

        Returns:
            Result of the feed forward calculation

        Examples:
            >>> from w7x.simulation.flt import FieldLineTracer
            >>> flt = FieldLineTracer(strategy='mock', mode='find_lcfs')
            >>> state = flt()
            >>> state.history.calls[0].function
            'w7x.simulation.flt.FieldLineTracer.find_lcfs'
            >>> state.history.calls[0].parameters
            {'step': 0.1}
            >>> type(state.history.calls[0].call_time)
            <class 'datetime.datetime'>

            # TODO-0(@dboe): make work
            # >>> from w7x.simulation.vmec import Vmec
            # >>> vmec = Vmec(strategy='mock', mode='free_boundary')
            # >>> state = vmec(flt())
            # >>> state.history

        """
        if self.mode is not None:
            call_method = getattr(self, self.mode)
        else:
            call_method = self._call

        res = call_method(*args, **kwargs)
        return res

    @abc.abstractmethod
    def _call(self, state, **kwargs) -> State:
        """
        This has to be user implemented.
        The calculation should be implemented in dependence of parameters and state.

        Returns:
            State: result of the node feed forward calculation
        """


@dataclasses.dataclass
class History(StateComposite):
    """
    State attribute, collecting the history of the state creation for reproduction purposes.
    """

    calls: typing.List[
        typing.Union["History", "CallHistory"]
    ] = dataclasses.children_alias(
        default_factory=lambda: [],
        metadata=dict(merged=merge_children_cumulative),
    )
    # TODO-1: think about best merge strategy


@dataclasses.dataclass
class CallHistory(StateLeaf):
    """
    History of a call

    Note:
        currently missing for reproducible execution:
            - storing the backend
            - not only function module but w7x module (might coincide)

    """

    # TODO-2: make this completely reproducible
    PARENT_TYPE = History  # pylint:disable=invalid-name
    parameters: dict
    #: function str, if given a callable, _func_key is applied to convert it
    function: typing.Union[typing.Callable, str]
    #: time of the call
    call_time: datetime = dataclasses.field(default_factory=datetime.now)
    #: module name, auto computed from function on first instantiation (no copies)
    module: typing.Optional[str] = None
    #: version of the module, auto computed from function on first instantiation (no copies)
    version: typing.Optional[str] = None
    #: git hash of the module, auto computed from function on first instantiation (no copies)
    git_hash: typing.Optional[str] = None

    def __post_init__(self):
        if isinstance(self.function, str):
            # nothin to do
            return
        if isinstance(self.function, functools.partial):
            function = self.function.func
        else:
            function = self.function

        # first instantiation only a function
        module = inspect.getmodule(function)
        module_name = module.__name__.split(".")[0]
        self.module = module_name
        module = importlib.import_module(module_name)
        self.git_hash = self.get_git_hash(module)
        self.version = self.get_version(module_name)
        # this will lock everything in place
        self.function = _func_key(function)

    @staticmethod
    def get_git_hash(module) -> typing.Optional[str]:
        """
        Returns:
            hexsha of the current head commit, None if module is not a repo
        """
        if not hasattr(module, "__file__"):
            LOGGER.warning(
                "Module %s has no __file__ attribute, could not get git hash", module
            )
            return None
        module_file = module.__file__
        try:
            repo = git.Repo(module_file, search_parent_directories=True)
        except Exception as err:
            # TODO: implement error handling by git.exc.InvalidGitRepositoryError
            raise NotImplementedError(
                str(git.execc.InvalidGitRepositoryError) + str(err)
            )
        git_hash = repo.head.commit.hexsha
        return git_hash

    @staticmethod
    def get_version(module_name) -> typing.Optional[str]:
        try:
            version = importlib.metadata.version(module_name)
        except importlib.metadata.PackageNotFoundError:
            LOGGER.warning("Module %s not found, could not get version", module_name)
            version = None
        return version


# pylint:disable=invalid-name,too-few-public-methods
class node(rna.pattern.decorator.Decorator):
    """
    Converts a function or method to a dask graph if :class:`distribute <w7x.switches.distribute>`

    Zen of node decoration:
        * A node-decorated function returns primitives
        * A node-decorated function does not mutate -> dask.delayed

    This is tied to the functional programming paradigm.
    """

    def __init__(self, **delayed_kwargs):
        self._delayed_kwargs = delayed_kwargs

    def _wrap(self, this, func, *args, **kwargs):
        if distribute.enabled():
            func = dask.delayed(func, **self._delayed_kwargs)  # noqa:F823
            with exposed(True):
                val = func(*args, **kwargs)
        else:
            val = func(*args, **kwargs)
        return val


# pylint:disable=invalid-name,too-few-public-methods
class dependencies(rna.pattern.decorator.Decorator):
    """
    Add default StateComponent and parameter dependencies to functions and methods.
    Merges the state attributes to the 'state' which is the first parameter of the wrapped
    function.

    Decorates functions or methodssignature:
        fun: function with the signature:
            def fun(
                [self,]
                *args: typing.Union[State, StateComponent],
                **parameter_kwargs
            ) -> StateComponent
            *args: default state attribute factories to be instantiated when the attribute is not
                provided
            **parameter_kwargs: parameters of the function call. These are stored under
                state.history for reproducibility.

    Args:
        *default_attributes: requirements of this node which automatically provide a default also.
        stateless (bool): if True, the decorated function is not mappable to a state.
        **default_parameters: high level parameters that the node should have access to.

    Attributes:
        _default_attributes: StateComponent used as default if the attr. is not present in state
        _default_parameters: Default parameters for the decorated function
        cls.default_attributes: map from decorated function to _default_attributes
        cls.default_parameters: map from decorated function to _default_parameters
    """

    class AUTO:
        """
        Unique flag to be set to default parameters to indicate they will be set dynamically,
        depending on state (if not passed explicitly).
        """

    class REQUIRED(DefaultFlag):
        """
        Unique flag to be set to default parameters to indicate they have to be passed but are
        required like arguments. We do not allow real arguments because with arguments we can not
        recover the history of a computation.
        """

        def __init__(self, attribute):
            self._attribute = attribute

        def attribute_name(self):
            return self._attribute.attribute_name()

        def __call__(self):
            raise ValueError(f"Attribute of type {self._attribute} required")

    class REJECTED:
        """
        Unique flag to be set to default parameters to indicate they are not allowed. An error is
        raised if a parameter of that name is passed.

        You can call it with a function with the following signature:
            def fun()
        """

    DEFAULT_ATTRIBUTES = {}
    DEFAULT_PARAMETERS = {}

    def __init__(
        self, *default_attributes: StateComponent, stateless=False, **default_parameters
    ):
        self._default_attributes = default_attributes
        self._default_parameters = default_parameters
        self._stateless = stateless

    @classmethod
    def extends(
        cls, func, *extention_default_attributes, **extention_default_parameters
    ):
        """
        Extend the dependencies of another function or method call with this classmethod.
        """
        func_key = _func_key(func)
        skip_attribute_names = [
            eda.attribute_name() for eda in extention_default_attributes
        ]
        default_attributes = list(extention_default_attributes)
        for da in cls.DEFAULT_ATTRIBUTES[func_key]:
            if da.attribute_name() in skip_attribute_names:
                continue
            default_attributes.append(da)

        default_parameters = cls.DEFAULT_PARAMETERS[func_key].copy()
        default_parameters.update(extention_default_parameters)
        return cls(
            *default_attributes,
            **default_parameters,
        )

    @classmethod
    def stateless(cls, *args, **kwargs):
        """
        State mapping (not yet) implemented, so do not wrap into state
        """
        return cls(*args, stateless=True, **kwargs)

    @classmethod
    def extends_stateless(cls, func, *args, **kwargs):
        """
        Combination of stateless and extends
        """
        return cls.extends(func, *args, stateless=True, **kwargs)

    @staticmethod
    def updated_state_parameters(
        default_attributes,
        default_parameters,
        *state_components: typing.List[StateComponent],
        **parameter_kwargs,
    ):
        """
        Prepare the inputs (state, **kwargs) of a backend method from state_components and
        parameter_kwargs, updated by default attributes and default parameters
        """
        if not state_components:
            state = State()
        elif len(state_components) == 1 and isinstance(state_components[0], State):
            state = state_components[0]
        else:
            state = State.merged(*state_components)

        if default_attributes:
            if state is None:
                state = State()
            for default in default_attributes:
                state.set_default(default)
        for key, value in default_parameters.items():
            if value is dependencies.REQUIRED and key not in parameter_kwargs:
                raise AttributeError(f"Parameter '{key}' required")
            if value is dependencies.REJECTED:
                if key in parameter_kwargs:
                    raise AttributeError(f"Parameter '{key}' rejected")
                continue  # no default

            parameter_kwargs.setdefault(key, value)
        return state, parameter_kwargs

    def __call__(self, *args, **kwargs):
        if self._wrapped is None:
            # TODO+1: Update with new rna version
            # TODO-0: Update with new rna version, why is _wrapped set at all?
            # First time request
            # TODO: maybe add a hook into Decorator call?
            if self._func is not None:
                func = self._func
            else:
                func = args[0]
            func_key = _func_key(func)
            self.__class__.DEFAULT_ATTRIBUTES[func_key] = self._default_attributes
            self.__class__.DEFAULT_PARAMETERS[func_key] = self._default_parameters
        return super().__call__(*args, **kwargs)

    def _wrap(
        self,
        this,
        func,
        *state_components: typing.List[StateComponent],
        **parameter_kwargs,
    ) -> State:
        state, parameter_kwargs = self.updated_state_parameters(
            self._default_attributes,
            self._default_parameters,
            *state_components,
            **parameter_kwargs,
        )

        res = func(state, **parameter_kwargs)
        assert res is not None

        if not self._stateless and stateful.enabled():
            if not isinstance(res, Delayed):
                assert issubclass(type(res), StateComponent), f"Invalid attr {res}"
            call_history = CallHistory(
                parameters=parameter_kwargs,
                function=func,
            )
            history = History()
            history.add(call_history)

            state = State.merged(state, res, history)
            return state
        return res

    @classmethod
    def default_state(cls, func):
        """
        Return the default state for a function decorated with this decorator
        """
        func_key = _func_key(func)
        return State(*cls.DEFAULT_ATTRIBUTES[func_key])

    @classmethod
    def default_attributes(cls, func):
        """
        Lookup the default attributes of func in the class cache
        """
        func_key = _func_key(func)
        return cls.DEFAULT_ATTRIBUTES[func_key]

    @classmethod
    def default_parameters(cls, func):
        """
        Lookup the values of the default parameters of func in the class cache
        """
        func_key = _func_key(func)
        return cls.DEFAULT_PARAMETERS[func_key]

    @classmethod
    def parameters(cls, func):
        """
        Lookup the names of the parameters of func in the class cache
        TODO: required? better use default_parameters and go from there
        """
        func_key = _func_key(func)
        return cls.DEFAULT_PARAMETERS[func_key].keys()


def start_scheduler(
    dashboard_address="-1",  # random dashboard adress
    **kwargs,
):
    """
    Start a dask scheduler. Usually you call compute on the graph afterwards.

    Args:
        see :class:`LocalCluster`

    Note: do not use with debugger
    """
    # pylint:disable=import-outside-toplevel
    from dask.distributed import (
        Client,
        LocalCluster,
    )
    import webbrowser  # pylint:disable=import-outside-toplevel

    cluster = LocalCluster(dashboard_address=dashboard_address, **kwargs)
    client = Client(cluster)
    LOGGER.debug(str(client))
    webbrowser.open(cluster.dashboard_link)
    return client


def compute(
    graph,
    cache: typing.Optional[str] = None,
    scheduler: typing.Union[str, typing.Dict[str, any]] = False,
    **kwargs,
):
    """
    Compute the given graph

    Args:
        cache: path to save the computation result of the graph to (or load from).
        scheduler: |if True or dict, start the scheduler (and pass it the scheduler dict
                   | as **kwargs if given.)
        **kwargs: passed to :meth:`dask.compute`
    """
    # TODO-1(@dboe): unittest
    if isinstance(graph, State):
        LOGGER.warning(
            "Wrong use of cumpute with State instead of dask graph."
            "Caching is not active."
        )
        return graph

    if cache is not None:
        path = rna.path.resolve(cache)
        if os.path.exists(path):
            LOGGER.info("Loading cached state from path '%s'", path)
            state = State.load(path)
            return state

    if scheduler:
        scheduler_kwargs = scheduler if isinstance(scheduler, dict) else {}
        client = start_scheduler(**scheduler_kwargs)

    state = graph.compute(**kwargs)
    # start runs with scheduling
    # TODO-1(@dboe): We should handle lists also
    # dask.compute(*results)

    if scheduler:
        client.shutdown()

    if cache is not None:
        state.save(path)

    return state
