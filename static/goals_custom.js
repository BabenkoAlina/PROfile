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
}

function deleteList(listId) {
    fetch('/goals/' + listlId, {
      method: 'delete'
    })
    .then(response => response.json())
    .then(() => window.location.reload() );
}

window.onload = function () {
    document.querySelectorAll('.Lists button.delete').forEach(item => {
        item.addEventListener('click', event => {
            event.preventDefault();
            const goalId = item.getAttribute('data-list-id');
            
            deleteGoal(goalId);
        });
    });
}