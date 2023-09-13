/* python3 manage.py collectstatic pour collecter les fichiers statiques du projet Django */

document.addEventListener('DOMContentLoaded', function() {
    // incrémentation décrémentation des valeurs numériques
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

    // étoiles d'évaluatiion
    // const ratingContainer = document.querySelector(".rating");
    // const stars = ratingContainer.querySelectorAll("span");
    // const ratingValueInput = document.querySelector("#rating_value"); // Champ de formulaire caché pour stocker la valeur de l'évaluation

    // stars.forEach((star) => {
    //     star.addEventListener("click", () => {
    //         const ratingValue = star.getAttribute("data-value");
    //         ratingValueInput.value = ratingValue;

    //         stars.forEach((s) => s.classList.remove("active"));
    //         star.classList.add("active");
    //     });
    // });
});