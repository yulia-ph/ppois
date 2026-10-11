class AudioGuide:
    """An audio guide device for museum exhibits.

    An audio guide narrates a specific exhibit in a chosen language.
    The device can play, pause, and stop. Changing the language or
    the target resets playback.

    A guide supports one or more languages; the current language must
    be one of the available ones.
    """

    LANG_RU = "ru"
    LANG_EN = "en"
    LANG_FR = "fr"
    LANG_DE = "de"

    def __init__(self, language: str, duration: int, target):
        """Initialize an audio guide.

        Args:
            language: Initial narration language code. Must not be empty.
            duration: Duration in minutes. Must be positive.
            target: The exhibit this guide narrates. Must not be None.

        Raises:
            ValueError: If any argument is invalid.
        """
        if not language:
            raise ValueError("Language must not be empty")
        if duration <= 0:
            raise ValueError(f"Duration must be positive, got {duration}")
        if target is None:
            raise ValueError("Target exhibit must not be None")

        self._language = language
        self._duration = duration
        self._target = target
        self._is_playing = False
        self._current_time = 0
        self._available_languages = [language]


    @property
    def language(self):
        return self._language

    @property
    def duration(self):
        return self._duration

    @property
    def target(self):
        return self._target

    @property
    def is_playing(self):
        return self._is_playing

    @property
    def current_time(self):
        return self._current_time

    @property
    def available_languages(self):
        return list(self._available_languages)


    def play(self):
        """Start playback.

        Idempotent: calling on an already playing guide is not an error.
        """
        self._is_playing = True
        return True

    def pause(self):
        """Pause playback.

        Idempotent: calling on a paused guide is not an error.
        """
        self._is_playing = False
        return True

    def stop(self):
        """Stop playback and reset the playback position to zero.

        Idempotent: calling on a stopped guide is not an error.
        """
        self._is_playing = False
        self._current_time = 0
        return True


    def change_language(self, lang: str):
        """Change the narration language.

        Stops any current playback.

        Args:
            lang: The new language code. Must be in available_languages
                and must differ from the current language.

        Raises:
            ValueError: If lang is empty, not available, or matches
                the current language.
        """
        if not lang:
            raise ValueError("Language must not be empty")
        if lang == self._language:
            raise ValueError(f"Language is already '{lang}'")
        if lang not in self._available_languages:
            raise ValueError(
                f"Language '{lang}' is not available. "
                f"Available: {self._available_languages}"
            )
        self._language = lang
        self.stop()
        return True

    def add_language(self, lang: str):
        """Add a language to the guide's available languages.

        Idempotent: adding an existing language is not an error.

        Args:
            lang: The language code. Must not be empty.

        Raises:
            ValueError: If lang is empty.
        """
        if not lang:
            raise ValueError("Language must not be empty")
        if lang not in self._available_languages:
            self._available_languages.append(lang)
        return True


    def set_target(self, exhibit):
        """Change the narrated exhibit.

        Stops any current playback. Idempotent when the exhibit is
        already the target.

        Args:
            exhibit: The new target exhibit. Must not be None.

        Raises:
            ValueError: If exhibit is None.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if exhibit is self._target:
            return True
        self._target = exhibit
        self.stop()
        return True
