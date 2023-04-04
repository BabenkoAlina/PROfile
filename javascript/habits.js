function displayHabitForm() {
    document.getElementById('hab-id').innerHTML = "<iframe src='{{ url_for('show_habit_form') }}' height='1000' width='1500'></iframe>";
}