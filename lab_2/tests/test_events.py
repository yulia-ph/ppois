"""Tests for the museum_events package.

Covers: AudioGuide, Event, Schedule.
"""
from datetime import date

import pytest

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
from museum_events.AudioGuide import AudioGuide
from museum_events.Event import Event


class TestAudioGuideInit:
    def test_init_stores_fields(self, audio_guide, exhibit):
        assert audio_guide.language == "en"
        assert audio_guide.duration == 30
        assert audio_guide.target is exhibit

    def test_init_not_playing(self, audio_guide):
        assert audio_guide.is_playing is False
        assert audio_guide.current_time == 0

    def test_init_available_languages(self, audio_guide):
        assert audio_guide.available_languages == ["en"]

    def test_init_empty_language_raises(self, exhibit):
        with pytest.raises(ValueError):
            AudioGuide("", 30, exhibit)

    def test_init_zero_duration_raises(self, exhibit):
        with pytest.raises(ValueError):
            AudioGuide("en", 0, exhibit)

    def test_init_negative_duration_raises(self, exhibit):
        with pytest.raises(ValueError):
            AudioGuide("en", -1, exhibit)

    def test_init_none_target_raises(self):
        with pytest.raises(ValueError):
            AudioGuide("en", 30, None)


class TestAudioGuidePlayback:
    def test_play_success(self, audio_guide):
        result = audio_guide.play()
        assert result is True
        assert audio_guide.is_playing is True

    def test_play_idempotent(self, audio_guide):
        audio_guide.play()
        assert audio_guide.play() is True
        assert audio_guide.is_playing is True

    def test_pause_success(self, audio_guide):
        audio_guide.play()
        result = audio_guide.pause()
        assert result is True
        assert audio_guide.is_playing is False

    def test_pause_idempotent(self, audio_guide):
        assert audio_guide.pause() is True
        assert audio_guide.is_playing is False

    def test_stop_success(self, audio_guide):
        audio_guide.play()
        result = audio_guide.stop()
        assert result is True
        assert audio_guide.is_playing is False
        assert audio_guide.current_time == 0

    def test_stop_idempotent(self, audio_guide):
        assert audio_guide.stop() is True
        assert audio_guide.current_time == 0


class TestAudioGuideLanguage:
    def test_change_language_success(self, audio_guide):
        audio_guide.add_language("ru")
        result = audio_guide.change_language("ru")
        assert result is True
        assert audio_guide.language == "ru"

    def test_change_language_stops_playback(self, audio_guide):
        audio_guide.add_language("ru")
        audio_guide.play()
        audio_guide.change_language("ru")
        assert audio_guide.is_playing is False

    def test_change_to_same_language_raises(self, audio_guide):
        with pytest.raises(ValueError):
            audio_guide.change_language("en")

    def test_change_to_unavailable_raises(self, audio_guide):
        with pytest.raises(ValueError):
            audio_guide.change_language("de")

    def test_add_language_success(self, audio_guide):
        result = audio_guide.add_language("ru")
        assert result is True
        assert "ru" in audio_guide.available_languages

    def test_add_language_empty_raises(self, audio_guide):
        with pytest.raises(ValueError):
            audio_guide.add_language("")
            audio_guide.add_language("")


class TestAudioGuideTarget:
    def test_set_target_success(self, audio_guide, painting):
        result = audio_guide.set_target(painting)
        assert result is True
        assert audio_guide.target is painting

    def test_set_target_same_idempotent(self, audio_guide, exhibit):
        result = audio_guide.set_target(exhibit)
        assert result is True
        assert audio_guide.target is exhibit

    def test_set_target_stops_playback(self, audio_guide, painting):
        audio_guide.play()
        audio_guide.set_target(painting)
        assert audio_guide.is_playing is False

    def test_set_target_none_raises(self, audio_guide):
        with pytest.raises(ValueError):
            audio_guide.set_target(None)


class TestAudioGuideEncapsulation:
    def test_available_languages_returns_copy(self, audio_guide):
        langs = audio_guide.available_languages
        langs.append("xx")
        assert "xx" not in audio_guide.available_languages


class TestEventInit:
    def test_init_stores_fields(self, lecture_event):
        assert lecture_event.title == "Impressionism Today"
        assert lecture_event.type == "lecture"
        assert lecture_event.venue == "Hall A"
        assert lecture_event.capacity == 50
        assert lecture_event.date == date(2025, 6, 1)

    def test_init_not_cancelled(self, lecture_event):
        assert lecture_event.is_cancelled is False
        assert lecture_event.is_active is True

    def test_init_not_full_empty(self, lecture_event):
        assert lecture_event.is_full is False
        assert lecture_event.count_registered() == 0

    def test_init_free_seats_equals_capacity(self, lecture_event):
        assert lecture_event.free_seats() == 50

    def test_init_all_valid_types(self):
        for t in ("lecture", "workshop", "concert", "other"):
            e = Event("T", t, date(2025, 1, 1), "V", 10)
            assert e.type == t

    def test_init_empty_title_raises(self):
        with pytest.raises(ValueError):
            Event("", Event.TYPE_LECTURE, date(2025, 1, 1), "V", 10)

    def test_init_invalid_type_raises(self):
        with pytest.raises(ValueError):
            Event("T", "party", date(2025, 1, 1), "V", 10)

    def test_init_none_date_raises(self):
        with pytest.raises(ValueError):
            Event("T", Event.TYPE_LECTURE, None, "V", 10)

    def test_init_empty_venue_raises(self):
        with pytest.raises(ValueError):
            Event("T", Event.TYPE_LECTURE, date(2025, 1, 1), "", 10)

    def test_init_zero_capacity_raises(self):
        with pytest.raises(ValueError):
            Event("T", Event.TYPE_LECTURE, date(2025, 1, 1), "V", 0)

    def test_init_negative_capacity_raises(self):
        with pytest.raises(ValueError):
            Event("T", Event.TYPE_LECTURE, date(2025, 1, 1), "V", -1)


class TestEventRegister:
    def test_register_success(self, lecture_event, visitor):
        result = lecture_event.register(visitor)
        assert result is True
        assert visitor in lecture_event.registered

    def test_register_reduces_free_seats(self, lecture_event, visitor):
        lecture_event.register(visitor)
        assert lecture_event.free_seats() == 49

    def test_register_none_raises(self, lecture_event):
        with pytest.raises(ValueError):
            lecture_event.register(None)

    def test_register_duplicate_raises(self, lecture_event, visitor):
        lecture_event.register(visitor)
        with pytest.raises(ValueError):
            lecture_event.register(visitor)

    def test_register_cancelled_raises(self, lecture_event, visitor):
        lecture_event.cancel()
        with pytest.raises(InvalidExhibitStateException):
            lecture_event.register(visitor)

    def test_register_full_raises(self, workshop_event):
        from museum_people.Visitor import Visitor
        # capacity 15; register 15
        for i in range(15):
            workshop_event.register(Visitor(f"V{i}", 20))
        assert workshop_event.is_full is True
        with pytest.raises(InvalidExhibitStateException):
            workshop_event.register(Visitor("Late", 20))


class TestEventUnregister:
    def test_unregister_success(self, lecture_event, visitor):
        lecture_event.register(visitor)
        result = lecture_event.unregister(visitor)
        assert result is True
        assert visitor not in lecture_event.registered

    def test_unregister_none_raises(self, lecture_event):
        with pytest.raises(ValueError):
            lecture_event.unregister(None)

    def test_unregister_not_registered_raises(self, lecture_event, visitor):
        with pytest.raises(ValueError):
            lecture_event.unregister(visitor)


class TestEventCancel:
    def test_cancel_success(self, lecture_event):
        result = lecture_event.cancel()
        assert result is True
        assert lecture_event.is_cancelled is True

    def test_cancel_clears_registrations(self, lecture_event, visitor):
        lecture_event.register(visitor)
        lecture_event.cancel()
        assert lecture_event.count_registered() == 0

    def test_cancel_idempotent(self, lecture_event):
        lecture_event.cancel()
        assert lecture_event.cancel() is True
        assert lecture_event.is_cancelled is True


class TestEventEncapsulation:
    def test_registered_returns_copy(self, lecture_event, visitor):
        lecture_event.register(visitor)
        regs = lecture_event.registered
        regs.append("fake")
        assert lecture_event.count_registered() == 1


class TestScheduleInit:
    def test_init_empty(self, schedule):
        assert schedule.events == []
        assert schedule.is_empty is True


class TestScheduleAddRemove:
    def test_add_success(self, schedule, lecture_event):
        result = schedule.add_event(lecture_event)
        assert result is True
        assert lecture_event in schedule.events
        assert schedule.is_empty is False

    def test_add_none_raises(self, schedule):
        with pytest.raises(ValueError):
            schedule.add_event(None)

    def test_add_duplicate_raises(self, schedule, lecture_event):
        schedule.add_event(lecture_event)
        with pytest.raises(ValueError):
            schedule.add_event(lecture_event)

    def test_remove_success(self, schedule_with_events, lecture_event):
        result = schedule_with_events.remove_event(lecture_event)
        assert result is True
        assert lecture_event not in schedule_with_events.events

    def test_remove_none_raises(self, schedule):
        with pytest.raises(ValueError):
            schedule.remove_event(None)

    def test_remove_not_present_raises(self, schedule, lecture_event):
        with pytest.raises(ValueError):
            schedule.remove_event(lecture_event)

    def test_clear_success(self, schedule_with_events):
        result = schedule_with_events.clear()
        assert result is True
        assert schedule_with_events.is_empty is True

    def test_clear_idempotent(self, schedule):
        assert schedule.clear() is True
        assert schedule.is_empty is True


class TestScheduleFilters:
    def test_get_events_for_day(self, schedule_with_events):
        events = schedule_with_events.get_events_for_day(date(2025, 6, 1))
        assert len(events) == 1
        assert events[0].title == "Impressionism Today"

    def test_get_events_for_day_none(self, schedule_with_events):
        events = schedule_with_events.get_events_for_day(date(2025, 1, 1))
        assert events == []


class TestScheduleConflicts:
    def test_no_conflicts_empty(self, schedule):
        assert schedule.find_conflicts() == []

    def test_no_conflicts_different_dates(self, schedule_with_events):
        assert schedule_with_events.find_conflicts() == []

    def test_conflict_same_date_and_venue(self, schedule, lecture_event):
        other = Event("Other Lecture", Event.TYPE_LECTURE,
                      date(2025, 6, 1), "Hall A", capacity=20)
        schedule.add_event(lecture_event)
        schedule.add_event(other)
        conflicts = schedule.find_conflicts()
        assert len(conflicts) == 1
        assert conflicts[0] == (lecture_event, other)

    def test_no_conflict_different_venue(self, schedule, lecture_event):
        other = Event("Other Lecture", Event.TYPE_LECTURE,
                      date(2025, 6, 1), "Hall B", capacity=20)
        schedule.add_event(lecture_event)
        schedule.add_event(other)
        assert schedule.find_conflicts() == []

    def test_cancelled_event_does_not_conflict(self, schedule, lecture_event):
        other = Event("Other Lecture", Event.TYPE_LECTURE,
                      date(2025, 6, 1), "Hall A", capacity=20)
        schedule.add_event(lecture_event)
        schedule.add_event(other)
        lecture_event.cancel()
        assert schedule.find_conflicts() == []

    def test_multiple_conflicts(self, schedule):
        e1 = Event("E1", Event.TYPE_LECTURE, date(2025, 6, 1), "Hall A", 10)
        e2 = Event("E2", Event.TYPE_LECTURE, date(2025, 6, 1), "Hall A", 10)
        e3 = Event("E3", Event.TYPE_LECTURE, date(2025, 6, 2), "Hall B", 10)
        e4 = Event("E4", Event.TYPE_LECTURE, date(2025, 6, 2), "Hall B", 10)
        for e in (e1, e2, e3, e4):
            schedule.add_event(e)
        conflicts = schedule.find_conflicts()
        assert len(conflicts) == 2


class TestScheduleEncapsulation:
    def test_events_returns_copy(self, schedule_with_events):
        events = schedule_with_events.events
        events.append("fake")
        assert len(schedule_with_events.events) == 2