# <div id="add-habit-modal" class="modal">
#         <div class="modal-content">
#             <span class="close">&times;</span>
#             <form id="add-habit-form" method="POST" action='/add_habit'>
#                 <label for="name">Add new habit:</label>
#                 <input type="text" id="name" name="name">
#                 <input type="submit" value="Add">
#             </form>           
#         </div>
#     </div>

# //     var addModal = document.getElementById("add-habit-modal");
#     //     var addButton = document.getElementById("add-button");
#     //     var closeButton = document.getElementsByClassName("close")[0];

#     //     addButton.onclick = function() {
#     //         addModal.style.display = "block";
#     //     }

#     //     closeButton.onclick = function() {
#     //         addModal.style.display = "none";
#     //     }

#     //     window.onclick = function(event) {
#     //         if (event.target == addModal) {
#     //             addModal.style.display = "none";
#     //         }
#     //     }

#     //     // function checkCheckbox() {
#     //     //     if ($('#checkbox').is(':checked')) {
                
#     //     //     }
#     //     // }

#     //     var habitsList = document.getElementById("habits-list");
#     //     var addHabitForm = document.getElementById("add-habit-form");

#     //     addHabitForm.onsubmit = function(event) {
#     //     event.preventDefault();
#     //     var habitName = document.getElementById("name").value;
#     //     var newHabit = document.createElement("li");
#     //     newHabit.innerHTML = '<form id="' + habitName + '-form" name="' + habitName + '-form" onsubmit="return false;"><span>' + habitName + '</span><input type="checkbox" name="' + habitName + '" value="1" class="habit-checkbox" form="' + habitName + '-form"><button class="delete-button">X</button><input type="hidden" name="count" value="0" form="' + habitName + '-form"></form>';
        
#     //     habitsList.appendChild(newHabit);
#     //     addModal.style.display = "none";
#     //     addHabitForm.reset();

#     //     callPythonFunction(habitName);
#     // };

#     // function callPythonFunction(habitName) {
#     //     $.post("/add_habit", { name: habitName }, function(data) {
#     //         console.log(data);
#     //     });
#     // }

#     // // Get all habit items and iterate over them to get their names and call the function
#     // var habitItems = document.querySelectorAll("#habits-list li span");
#     // habitItems.forEach(function(item) {
#     //     var habitName = item.textContent;
#     //     callPythonFunction(habitName);
#     // });

#     // var habitCheckboxes = document.querySelectorAll("#habits-list li input[type='checkbox']");
#     // habitCheckboxes.forEach(function(checkbox) {
#     //     checkbox.addEventListener('change', function() {
#     //         var habitName = this.name;
#     //         var habitCountInput = this.nextElementSibling.nextElementSibling;
#     //         if (this.checked) {
#     //             var newCount = parseInt(habitCountInput.value) + 1;
#     //             habitCountInput.value = newCount;
#     //             upgradeHabit(habitName, newCount);
#     //         } else {
#     //             habitCountInput.value = 0;
#     //             upgradeHabit(habitName, 0);
#     //         }
#     //     });
#     // });

#     // function upgradeHabit(habitName, newCount) {
#     //     $.post("/update_habit", { name: habitName, count: newCount }, function(data) {
#     //         console.log(data);
#     //     });
#     // }

#     // habitsList.onclick = function(event) {
#     //     if (event.target.classList.contains("delete-button")) {
#     //         event.target.parentNode.remove();
#     //     }
#     // }