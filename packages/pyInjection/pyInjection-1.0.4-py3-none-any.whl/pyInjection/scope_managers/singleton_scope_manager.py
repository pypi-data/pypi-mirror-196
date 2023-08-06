from typing import Type, Any, Dict, List
from inspect import Signature, signature
from ..helpers import TypeHelpers
from ..enums import Scope
from ..interfaces import IScopeManager
from ..dtos import Registration

class SingletonScopeManager(IScopeManager):
    __resolved_instances: Dict[Type, Any]
    __base_types: List[Type]
    __ignore_parameters: List[str]

    def __init__(self, base_types: List[Type]) -> None:
        self.__resolved_instances = {}
        self.__base_types = base_types
        self.__ignore_parameters = [
            'self',
            'args',
            'kwargs'
        ]

    def can_resolve(self, scope: Scope) -> bool:
        return scope == Scope.SINGLETON

    def is_same_registration_scope(self, interface: Type, container: Dict[Type, Registration]) -> bool:
        registration: Registration = container[interface]
        return registration.scope == Scope.SINGLETON

    def resolve(self, interface: Type, container: Dict[Type, Registration]) -> Any:
        error_message: str = ''
        if interface in self.__resolved_instances.keys():
            return self.__resolved_instances[interface]
        else:
            if interface in container.keys():
                implementation: Any = container[interface].implementation
                if(type(implementation) in self.__base_types): # Class Registration
                    kwargs: Any = {}
                    sig: Signature = signature(implementation)
                    for p in sig.parameters:
                        if(p not in self.__ignore_parameters):
                            child_interface: Type = sig.parameters[p].annotation
                            if not self.is_same_registration_scope(interface=child_interface, container=container):
                                warning_message: str = f'Warning Singleton type: {TypeHelpers.to_string(interface)} registered with Transient dependency: {TypeHelpers.to_string(child_interface)}'
                                print(warning_message)
                            instance = self.resolve(interface=child_interface, container=container)
                            kwargs[p] = instance
                    self.__resolved_instances[interface] = implementation(**kwargs)
                elif(type(implementation) == type(lambda: '')):
                    self.__resolved_instances[interface] = implementation()
                else:
                    self.__resolved_instances[interface] = implementation
                return self.__resolved_instances[interface]
            else:
                error_message = f'Cannot resolve type: {TypeHelpers.to_string(interface)}'
                raise Exception(error_message);

    @property
    # Exposed for Unit Testing
    def resolved_instances(self) -> Dict[Type, Any]:
        return self.__resolved_instances
