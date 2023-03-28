function completeGoal(goalId) {
    fetch('/goal/' + goalId, {
      method: 'put'
    })
    .then(response => response.json())
    .then(() => window.location.reload() );
}

function deleteGoal(goalId) {
    fetch('/goal/' + goalId, {
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
