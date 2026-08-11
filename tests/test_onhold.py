from commandcenter.onhold import counted_minutes


def test_paused_time_is_not_counted_against_the_resolution_target():
    events = [{"status": "in_progress", "minutes": 30},
              {"status": "awaiting_customer", "minutes": 600},
              {"status": "in_progress", "minutes": 30}]
    assert counted_minutes(events) == 60


def test_uninterrupted_work_is_counted_in_full():
    assert counted_minutes([{"status": "in_progress", "minutes": 45}]) == 45
