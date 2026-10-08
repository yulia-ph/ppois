from museum_exhibits.Exhibit import Exhibit


class Sculpture(Exhibit):
    """A sculpture exhibit.

    Extends Exhibit with sculpture-specific attributes: material,
    dimensions, weight, and base condition. A sculpture may need
    reinforcement of its base, which is tracked separately from the
    exhibit's overall condition (which changes only through a
    Restoration process).
    """

    BASE_OK = "ok"
    BASE_REINFORCED = "reinforced"

    def __init__(self, title: str, author: str, material: str,
                 height: float, weight: float, condition: str = "good"):
        """Initialize a sculpture.

        Args:
            title: The sculpture title. Must not be empty.
            author: The sculptor. Must not be empty.
            material: Sculpture material, e.g. "marble", "bronze", "wood".
                Must not be empty.
            height: Height in meters. Must be positive.
            weight: Weight in kilograms. Must be positive.
            condition: One of Exhibit.CONDITION_* constants.

        Raises:
            ValueError: If material is empty, height or weight is not
                positive, or inherited validation fails.
        """
        super().__init__(title, author, condition)

        if not material:
            raise ValueError("Material must not be empty")
        if height <= 0:
            raise ValueError(f"Height must be positive, got {height}")
        if weight <= 0:
            raise ValueError(f"Weight must be positive, got {weight}")

        self._material = material
        self._height = height
        self._weight = weight
        self._needs_reinforcement = False
        self._base_condition = Sculpture.BASE_OK


    @property
    def material(self):
        return self._material

    @property
    def height(self):
        return self._height

    @property
    def weight(self):
        return self._weight

    @property
    def needs_reinforcement(self):
        return self._needs_reinforcement

    @property
    def base_condition(self):
        return self._base_condition


    def mark_for_reinforcement(self):
        """Flag the sculpture's base as needing reinforcement.

        Idempotent: marking an already flagged sculpture is not an
        error.
        """
        self._needs_reinforcement = True
        return True

    def reinforce_base(self):
        """Reinforce the base of the sculpture.

        Raises:
            ValueError: If the sculpture is not flagged for reinforcement.
        """
        if not self._needs_reinforcement:
            raise ValueError(
                f"Sculpture '{self.inventory_number}' is not flagged for reinforcement"
            )
        self._needs_reinforcement = False
        self._base_condition = Sculpture.BASE_REINFORCED
        return True