from datetime import timedelta , datetime


def bookings_times_discovery(trainer_schedule, bookings, cur_date, service_durations):
    schedule_times = []
    booking_intervals = []

    # Converti il programma del trainer in intervalli
    for schedule in trainer_schedule:
        schedule_times.append((schedule.datatime_start, schedule.datatime_end))
    print(f"Schedule times: {schedule_times}")

    # Converti le prenotazioni in intervalli
    for booking in bookings:
        duration = timedelta(minutes=service_durations.get(booking.service.id, 0))
        booking_intervals.append((booking.datetime_start, booking.datetime_start + duration))
    print(f"Booking intervals: {booking_intervals}")

    # Ordina gli intervalli di prenotazione
    booking_intervals.sort(key=lambda x: x[0])

    # Calcola gli orari disponibili
    available_times = []
    for start_time, end_time in schedule_times:
        current_start = start_time
        for booking_start, booking_end in booking_intervals:
            if booking_start >= end_time or booking_end <= start_time:
                continue

            if current_start < booking_start:
                available_times.append((current_start, min(booking_start, end_time)))

            current_start = max(current_start, booking_end)

        if current_start < end_time:
            available_times.append((current_start, end_time))

    print(f"Final available times: {available_times}")
    return available_times
