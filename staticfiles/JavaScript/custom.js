/* python3 manage.py collectstatic pour collecter les fichiers statiques du projet Django */

document.addEventListener('DOMContentLoaded', function() {
    var priceHourInput = document.getElementById('hour-input');
    var previousValue = parseFloat(priceHourInput.value); 
    var newValue = parseFloat(priceHourInput.value);
    var minValue = parseFloat(priceHourInput.value);
    
    priceHourInput.addEventListener('input', function() {
        var value = parseFloat(this.value);

        if (value > 10) {
            if (value > previousValue) {
                newValue = previousValue + 1; // Incrémentation par 1
            }
            else {
                newValue = previousValue - 1; // Incrémentation par 1
            }
        } else {
            newValue = value; // Incrémenter depuis la valeur précédente
        }

        if (value < minValue) {
            newValue = minValue
        }
        previousValue = newValue;
        this.value = newValue.toFixed(2);
    });
});