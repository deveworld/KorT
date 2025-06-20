import importlib
import types
from pathlib import Path


# TODO: Add automatic loading of all modules with directory traversal, all_modules is kind of annoying to maintain
class _LazyModule(types.ModuleType):
    """
    A module that loads its dependencies lazily.

    Usage:
        Before:
            from .papago import PapagoTranslator
            from .google import GoogleTranslator
            from ..deepl import DeepLTranslator

        After:
            import sys
            from .utils import _LazyModule

            _file = globals()["__file__"]
            all_modules = [".papago.PapagoTranslator", ".google.GoogleTranslator", "..deepl.DeepLTranslator"]
            lazy_module = _LazyModule(__name__, _file, all_modules, module_spec=__spec__)

            # Add any functions or variables you want to expose
            lazy_module.get_translator = get_translator
            lazy_module.get_translator_list = get_translator_list

            sys.modules[__name__] = lazy_module

        Description:
            You can import PapagoTranslator, GoogleTranslator same as before.
            But now, the module will be loaded only when you access it for the first time.
            This is useful for large modules or when you want to avoid circular imports.
    """

    def __init__(
        self, name, file_path, all_modules, module_spec=None, copy_globals=None
    ):
        super().__init__(name)
        self._name = name
        self._file = file_path
        self._all_modules = all_modules
        self._module_spec = module_spec
        self._loaded_attrs = {}

        # Create mapping of attribute names to their full module paths
        self._attr_to_module = {}
        for module_path in all_modules:
            # Extract the attribute name (last part after the dot)
            parts = module_path.split(".")
            attr_name = parts[-1]
            self._attr_to_module[attr_name] = module_path

        # Set module attributes
        self.__file__ = file_path
        self.__path__ = [str(Path(file_path).parent)]

        if module_spec:
            self.__spec__ = module_spec
            if hasattr(module_spec, "loader"):
                self.__loader__ = module_spec.loader
            if hasattr(module_spec, "submodule_search_locations"):
                self.__path__ = module_spec.submodule_search_locations

        # Copy any globals that should be preserved
        if copy_globals:
            for name, value in copy_globals.items():
                if name not in self._attr_to_module and not name.startswith("_"):
                    setattr(self, name, value)

    def __getattr__(self, name):
        # Return the attribute if it's already loaded
        if name in self._loaded_attrs:
            return self._loaded_attrs[name]

        # Check if we should lazy-load this attribute
        if name in self._attr_to_module:
            self._load_module(name)
            return self._loaded_attrs[name]

        # Attribute not found
        raise AttributeError(f"module '{self._name}' has no attribute '{name}'")

    def __dir__(self):
        """List available attributes including lazy-loadable ones."""
        return list(
            set(
                list(super().__dir__())
                + list(self._attr_to_module.keys())
                + list(self._loaded_attrs.keys())
            )
        )

    def _load_module(self, attr_name):
        """Load the module and extract the requested attribute."""
        module_path = self._attr_to_module[attr_name]

        # Parse the relative path
        parts = module_path.split(".")
        relative_dots = 0

        # Count leading dots for relative imports
        while parts and parts[0] == "":
            relative_dots += 1
            parts.pop(0)

        # Get module name and attribute chain
        if not parts:
            raise ImportError(f"Invalid module path: {module_path}")

        # If path starts with dots, interpret as relative import
        if relative_dots > 0:
            # Determine parent package based on relative level
            package = self._name
            for _ in range(
                relative_dots - 1
            ):  # -1 because importlib.import_module expects one fewer level
                package = package.rsplit(".", 1)[0] if "." in package else ""

            # Import module using relative syntax with proper package context
            module_name = parts[0]
            relative_import = "." + module_name  # Format for importlib.import_module

            # Import the module with correct relative import handling
            module = importlib.import_module(relative_import, package=package)
        else:
            # For absolute imports
            module_name = parts[0]
            # Import the module
            module = importlib.import_module(module_name)

        # Navigate to the requested attribute
        obj = module
        for part in parts[1:]:
            obj = getattr(obj, part)

        # Store the loaded attribute
        self._loaded_attrs[attr_name] = obj

        # Make the attribute available at module level
        setattr(self, attr_name, obj)
