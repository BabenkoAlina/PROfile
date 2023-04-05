function completeGoal(goalId) {
    fetch('/goals/goal/' + goalId, {
      method: 'put'
    })
    .then(response => response.json())
    .then(() => window.location.reload() );
}

function deleteGoal(goalId) {
    fetch('/goals/goal/' + goalId, {
      method: 'delete'
    })
    .then(response => response.json())
    .then(() => window.location.reload() );
}

function deleteList(listId) {
    fetch('/goals/' + listId, {
      method: 'delete'
    })
    .then(response => response.json())
    .then(() => window.location.reload() );
}

function openForm() {
    document.getElementById("createForm").style.display = "block";
}
  
function closeForm() {
    document.getElementById("createForm").style.display = "none";
}

window.onload = function () {
    document.querySelectorAll('.goalsList .goal button.delete').forEach(item => {
        item.addEventListener('click', event => {
            event.preventDefault();
            const goalId = item.getAttribute('data-goal-id');
            
            deleteGoal(goalId);
        });
    });

    document.querySelectorAll('.goalsList .goal button.update').forEach(item => {
        item.addEventListener('click', event => {
            event.preventDefault();
            const goalId = item.getAttribute('data-goal-id');
            
            completeGoal(goalId);
        });
    });

    document.querySelectorAll('.lists button.delete_list').forEach(item => {
        item.addEventListener('click', event => {
            event.preventDefault();
            const listId = item.getAttribute('data-list-id');
            
            deleteList(listId);
        });
    });

    document.getElementById('createFormCloseButton').addEventListener('click', event => {
        event.preventDefault();
        closeForm()
    });

    document.getElementById('createFormOpenButton').addEventListener('click', event => {
        event.preventDefault();
        openForm()
    });
}