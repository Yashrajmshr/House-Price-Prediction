document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const resultBox = document.getElementById('result-box');
    const formContainer = document.querySelector('.form-container');
    const resetBtn = document.getElementById('reset-btn');
    const predictBtn = document.getElementById('predict-btn');
    const btnText = predictBtn.querySelector('.btn-text');
    const spinner = predictBtn.querySelector('.spinner');
    const priceDisplay = document.getElementById('predicted-price');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        btnText.textContent = "Analyzing Market...";
        spinner.classList.remove('hidden');
        predictBtn.disabled = true;

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        data.BHK = parseInt(data.BHK);
        data.Area_SqFt = parseInt(data.Area_SqFt);
        data.Bathrooms = parseInt(data.Bathrooms);
        data.Balcony = parseInt(data.Balcony);
        data.Age_of_Property = parseInt(data.Age_of_Property);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if(response.ok) {
                const result = await response.json();
                
                priceDisplay.textContent = result.estimated_price;
                
                formContainer.classList.add('hidden');
                resultBox.classList.remove('hidden');
            } else {
                alert("Error making prediction. Please try again.");
            }
            
        } catch (error) {
            console.error("Prediction failed:", error);
            alert("Failed to connect to the prediction server.");
        } finally {
            btnText.textContent = "Predict Market Value";
            spinner.classList.add('hidden');
            predictBtn.disabled = false;
        }
    });

    resetBtn.addEventListener('click', () => {
        resultBox.classList.add('hidden');
        formContainer.classList.remove('hidden');
        priceDisplay.textContent = "₹ --";
    });
});
