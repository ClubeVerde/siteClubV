document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".item").forEach(function (item) {
        let minusBtn = item.querySelector(".quantidade button:first-child");
        let plusBtn = item.querySelector(".quantidade button:last-child");
        let quantityInput = item.querySelector(".quantidade input");


        minusBtn.addEventListener("click", function () {
            let currentValue = parseInt(quantityInput.value);
            if (currentValue > 1) {
                quantityInput.value = currentValue - 1;
            }
        });


        plusBtn.addEventListener("click", function () {
            let currentValue = parseInt(quantityInput.value);
            quantityInput.value = currentValue + 1;
        });


        quantityInput.addEventListener("input", function () {
            if (quantityInput.value === "" || quantityInput.value <= 0) {
                quantityInput.value = 1;
            }
        });
    });
});
