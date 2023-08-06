from abc import ABC, abstractmethod
from typing import Optional, Any, Union, Iterable, Self, Protocol, Final, TypeVar, Generic, Type, Callable, _UnionGenericAlias


__all__ = (
    "AnnotationTemplate", "FormalAnnotation", "Special", "Subgroup", 
    "input_annotation", "number", "many_or_one", "method_of"
)


class _AnnotationFactory(ABC):
    """
    Annotation factory class.
    Creates annotation by input other.

    Can be used via [] (preferred) or by normal call.
    """

    def __call__(self, annotation: Any) -> Any:
        return self._create_full_annotation_by(annotation)

    def __getitem__(self, annotation: Any) -> Any:
        return self._create_full_annotation_by(
            Union[annotation]
            if isinstance(annotation, Iterable)
            else annotation
        )

    @abstractmethod
    def _create_full_annotation_by(self, annotation: Any) -> Any:
        """Annotation Creation Method from an input annotation."""


class _InputAnnotationAnnotation:
    """
    Singleton class for the annotation of the conditional empty space, in which
    the input type in the CustomAnnotationFactory should be placed.

    Supports | to create Union type.
    """

    _instance: Optional[Self] = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance') or cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)

        return cls._instance

    def __repr__(self) -> str:
        return '<input_annotation>'

    def __or__(self, other: Any) -> Union:
        return Union[self, other]

    def __ror__(self, other: Any) -> Union:
        return Union[other, self]


class _ItemStorage(Protocol):
    @abstractmethod
    def __getitem__(self, key: Any) -> Any:
        pass


class AnnotationTemplate(_AnnotationFactory):
    """
    _AnnotationFactory class delegating the construction of another factory's
    annotation.

    When called, replaces the _InputAnnotationAnnotation instances from its
    arguments and their subcollections with the input annotation.

    Templateizes Union.

    Recognize nesting of annotations only by `list` i.e
    ```
    AnnotationTemplate(Callable, [[input_annotation], Any]) # works
    AnnotationTemplate(Callable, [(input_annotation, ), Any]) # does not work
    ```

    Delegates responsibilities to other templates when passing them as
    annotations.
    """

    def __init__(self, factory: _ItemStorage, annotations: list):
        self._factory = factory
        self._annotations = tuple(annotations)

    def __repr__(self) -> str:
        return "{factory}{arguments}".format(
            factory=(
                self._factory.__name__
                if hasattr(self._factory, '__name__')
                else self._factory
            ),
            arguments=str(self.__recursively_format(self._annotations)).replace('\'', str())
        )

    def _create_full_annotation_by(self, annotation: Any) -> Any:
        formatted_annotations = self.__get_formatted_annotations_from(self._annotations, annotation)

        return self._factory[
            formatted_annotations[0]
            if len(formatted_annotations) == 1
            else formatted_annotations
        ]

    def __get_formatted_annotations_from(self, annotations: Iterable, replacement_annotation: Any) -> tuple:
        """
        Recursive function to replace element(s) of the input collection (and
        its subcollections) equal to the annotation anonation with the input
        annotation.
        """

        formatted_annotations = list()

        for annotation in annotations:
            if isinstance(annotation, _InputAnnotationAnnotation):
                annotation = replacement_annotation

            elif isinstance(annotation, list):
                annotation = self.__get_formatted_annotations_from(
                    annotation,
                    replacement_annotation
                )

            elif isinstance(annotation, AnnotationTemplate):
                annotation = annotation[replacement_annotation]

            elif type(annotation) in (Union, _UnionGenericAlias, type(int | float)):
                annotation = Union[
                    *self.__get_formatted_annotations_from(
                        annotation.__args__,
                        replacement_annotation
                    )
                ]

            formatted_annotations.append(annotation)

        return tuple(formatted_annotations)

    def __recursively_format(self, collection: Iterable) -> list:
        """
        Method for formatting the elements of a collection (and all of its
        sub-collections) as a list with possible element names or themselves.
        """

        formatted_collection = list()

        for item in collection:
            if isinstance(item, Iterable) and not isinstance(item, str):
                formatted_collection.append(self.__recursively_format(item))
            elif hasattr(item, '__name__'):
                formatted_collection.append(item.__name__)
            else:
                formatted_collection.append(item)

        return formatted_collection


class FormalAnnotation:
    """
    Class allowing to formally specify additional information about the input
    resource.

    When annotating, returns the input.

    Can be called via [] with some resource.
    """

    def __init__(self, instance_doc: Optional[str] = None):
        if instance_doc is not None:
            self.__doc__ = instance_doc

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def __getitem__(self, resource: Any) -> Any:
        return resource


class Special:
    """
    Annotation class for formally specifying specific behavior for subclasses.

    Returns the second input annotation, or Any if none.

    Specifies additional behavior for the first annotation.

    Implies use like Special[type_for_special_behavior, generic_type] or
    Special[type_for_special_behavior].
    """

    def __class_getitem__(cls, annotation_resource: tuple[Any, Any] | Any) -> Any:
        if not isinstance(annotation_resource, tuple):
            return Any

        elif len(annotation_resource) != 2:
            raise TypeError(
                "Special must be used as Special[type_for_special_behavior, generic_type] or Special[type_for_special_behavior]"
            )

        return annotation_resource[1]


_BasicT = TypeVar("_BasicT")


class Subgroup(Generic[_BasicT]):
    """
    Class for defining a subgroup in an already existing type.

    Delegates the definition of a subgroup from a particular type to
    `determinant` attribute.
    """

    def __init__(self, type_: Type[_BasicT], determinant: Callable[[_BasicT], bool]):
        self._type = type_
        self._determinant = determinant

    @property
    def type_(self) -> Type[_BasicT]:
        return self._type

    @property
    def determinant(self) -> Callable[[_BasicT], bool]:
        return self._determinant

    def __instancecheck__(self, instance: Any) -> bool:
        return self._has(instance)

    def __contains__(self, object_: Any) -> bool:
        return self._has(object_)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} of {self._type.__name__}>"

    def _has(self, object_: Any) -> bool:
        return isinstance(object_, self.type_) and self._determinant(object_)


# Pre-created instance without permanent formal creation of a new one.
input_annotation: Final[_InputAnnotationAnnotation] = _InputAnnotationAnnotation()


number: Final = int | float | complex


many_or_one: Final[AnnotationTemplate] = AnnotationTemplate(
    Union,
    [input_annotation, AnnotationTemplate(Iterable, [input_annotation])]
)

method_of: Final[AnnotationTemplate] = AnnotationTemplate(
    Callable,
    [[input_annotation, ...], Any]
)