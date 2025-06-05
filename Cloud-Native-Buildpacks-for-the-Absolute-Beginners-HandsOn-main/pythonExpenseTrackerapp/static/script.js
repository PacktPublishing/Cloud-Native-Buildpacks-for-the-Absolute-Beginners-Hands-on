// static/script.js

document.getElementById('expense-form').addEventListener('submit', function(event) {
    const name = document.getElementById('name').value.trim();
    const amount = document.getElementById('amount').value.trim();
    const date = document.getElementById('date').value.trim();
    
    if (!name) {
        alert("Please enter an expense name.");
        event.preventDefault(); // Prevent form submission
    }
    
    if (!amount || isNaN(amount) || amount <= 0) {
        alert("Please enter a valid positive number for the amount.");
        event.preventDefault(); // Prevent form submission
    }

    if (!date) {
        alert("Please enter a date.");
        event.preventDefault(); // Prevent form submission
    }
});
