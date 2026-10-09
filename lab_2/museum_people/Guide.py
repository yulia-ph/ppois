from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
from museum_people.Employee import Employee


class Guide(Employee):
    """A museum tour guide.

    A guide speaks one or more languages and conducts tours (Excursion
    instances). Tracks the number of years of experience and the list
    of tours already conducted.
    """

    def __init__(self, name: str, salary: float, hire_date,
                 languages: list, experience_years: int):
        """Initialize a guide.

        Args:
            name: Employee name. Must not be empty.
            salary: Monthly salary. Must be non-negative.
            hire_date: Date of hire. Must not be None.
            languages: List of language codes (e.g. ["en", "ru"]).
                Must not be empty.
            experience_years: Years of experience. Must be non-negative.

        Raises:
            ValueError: If inherited validation fails, languages is
                empty, or experience_years is negative.
        """
        super().__init__(name, salary, hire_date)
        if not languages:
            raise ValueError("Guide must speak at least one language")
        if experience_years < 0:
            raise ValueError(
                f"Experience years must be non-negative, got {experience_years}"
            )
        self._languages = list(languages)
        self._experience_years = experience_years
        self._tours = []


    @property
    def languages(self):
        return list(self._languages)

    @property
    def experience_years(self):
        return self._experience_years

    @property
    def tours(self):
        return list(self._tours)


    def speak_language(self, lang: str) -> bool:
        """Return True if the guide speaks the given language."""
        return lang in self._languages


    def conduct_tour(self, excursion):
        """Conduct an excursion.

        Args:
            excursion: The Excursion to conduct. Must not be None and
                must be startable.

        Returns:
            True on success.

        Raises:
            ValueError: If excursion is None.
            InvalidExhibitStateException: If excursion.start() fails
                (e.g. no route or no guide).
        """
        if excursion is None:
            raise ValueError("Excursion must not be None")
        if not excursion.start():
            raise InvalidExhibitStateException(
                exhibit_title=self._name,
                state="cannot_start",
                reason="Excursion cannot be started",
            )
        self._tours.append(excursion)
        return True

    def finish_tour(self, excursion):
        """Finish an excursion.

        Args:
            excursion: The Excursion to finish. Must not be None.

        Returns:
            The result of `excursion.finish()`.

        Raises:
            ValueError: If excursion is None.
        """
        if excursion is None:
            raise ValueError("Excursion must not be None")
        return excursion.finish()
