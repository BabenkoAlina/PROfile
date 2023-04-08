var today = new Date();
var currentDate = today.toLocaleDateString();

// Set date in HTML element
document.getElementById("current-date").innerHTML = currentDate;

const checkboxes = document.querySelectorAll('.check');
const updateButton = document.querySelector('input[name="update"]');

updateButton.addEventListener('click', () => {
  checkboxes.forEach(checkbox => {
    if (checkbox.checked) {
      checkbox.style.display = 'none';
    }
  });
});
