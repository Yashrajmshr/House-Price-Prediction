document.addEventListener('DOMContentLoaded', () => {
    const form            = document.getElementById('prediction-form');
    const predictBtn      = document.getElementById('predict-btn');
    const btnText         = predictBtn.querySelector('.btn-text');
    const btnLoading      = predictBtn.querySelector('.btn-loading');

    const formSection     = document.getElementById('predict-section');
    const resultSection   = document.getElementById('result-section');
    const priceDisplay    = document.getElementById('predicted-price');
    const resultMeta      = document.getElementById('result-meta');
    const resetBtn        = document.getElementById('reset-btn');

    const recGrid         = document.getElementById('rec-grid');
    const recLoading      = document.getElementById('rec-loading');
    const recEmpty        = document.getElementById('rec-empty');

    // ── City Icon Map ───────────────────────────────────────
    const cityIcons = {
        'Mumbai': 'fa-water',
        'Bengaluru': 'fa-tree',
        'Delhi-NCR': 'fa-landmark',
        'Hyderabad': 'fa-mosque',
        'Pune': 'fa-mountain',
    };

    // ── Property Type Icon Map ──────────────────────────────
    const propIcons = {
        'Apartment':        'fa-building',
        'Independent House':'fa-house',
        'Villa':            'fa-house-chimney-window',
    };

    // ── Format Price ────────────────────────────────────────
    function formatPrice(lakhs) {
        if (lakhs >= 100) return `₹ ${(lakhs / 100).toFixed(2)} Cr`;
        return `₹ ${lakhs.toFixed(2)} L`;
    }

    // ── Render Recommendation Cards ─────────────────────────
    function renderRecommendations(recs) {
        recGrid.innerHTML = '';

        if (!recs || recs.length === 0) {
            recEmpty.classList.remove('hidden');
            return;
        }

        recs.forEach((prop, i) => {
            const iconClass = propIcons[prop.Property_Type] || 'fa-building';
            const price     = formatPrice(prop.Price_Lakhs);
            const delay     = i * 0.08;

            const card = document.createElement('div');
            card.className = 'prop-card';
            card.style.animationDelay = `${delay}s`;
            card.innerHTML = `
                <div class="prop-card-img">
                    <div class="prop-card-img-overlay"></div>
                    <i class="fa-solid ${iconClass}"></i>
                    <span class="prop-type-badge">${prop.Property_Type}</span>
                </div>
                <div class="prop-card-body">
                    <div class="prop-price">${price}</div>
                    <div class="prop-title">${prop.BHK} BHK ${prop.Property_Type}</div>
                    <div class="prop-features">
                        <span class="prop-feature"><i class="fa-solid fa-ruler-combined"></i> ${prop.Area_SqFt.toLocaleString()} sq ft</span>
                        <span class="prop-feature"><i class="fa-solid fa-bed"></i> ${prop.BHK} BHK</span>
                    </div>
                    <div class="prop-divider"></div>
                    <div class="prop-location">
                        <i class="fa-solid fa-location-dot"></i>
                        ${prop.Locality_Tier} &bull; ${prop.City}
                    </div>
                </div>
            `;
            recGrid.appendChild(card);
        });
    }

    // ── Fetch Recommendations ───────────────────────────────
    async function fetchRecommendations(city, bhk, predictedLakhs) {
        recLoading.classList.remove('hidden');
        recGrid.innerHTML = '';
        recEmpty.classList.add('hidden');

        try {
            const res = await fetch('/recommendations', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    City: city,
                    BHK: bhk,
                    predicted_price_lakhs: predictedLakhs
                })
            });

            if (res.ok) {
                const data = await res.json();
                renderRecommendations(data.recommendations);
            } else {
                recEmpty.classList.remove('hidden');
            }
        } catch (err) {
            console.error('Recommendation fetch failed:', err);
            recEmpty.classList.remove('hidden');
        } finally {
            recLoading.classList.add('hidden');
        }
    }

    // ── Build Result Meta Chips ─────────────────────────────
    function buildMetaChips(data) {
        const chips = [
            { icon: 'fa-city',            label: data.City },
            { icon: 'fa-bed',             label: `${data.BHK} BHK` },
            { icon: 'fa-ruler-combined',  label: `${parseInt(data.Area_SqFt).toLocaleString()} sq ft` },
            { icon: 'fa-building',        label: data.Property_Type },
            { icon: 'fa-couch',           label: data.Furnishing_Status },
            { icon: 'fa-person-digging',  label: data.Status },
        ];
        resultMeta.innerHTML = chips.map(c =>
            `<span class="meta-chip"><i class="fa-solid ${c.icon}"></i>${c.label}</span>`
        ).join('');
    }

    // ── Form Submit ─────────────────────────────────────────
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Validate all fields
        let valid = true;
        form.querySelectorAll('input, select').forEach(el => {
            el.classList.remove('is-invalid');
            if (!el.value) {
                el.classList.add('is-invalid');
                valid = false;
            }
        });
        if (!valid) return;

        // Loading state
        btnText.classList.add('hidden');
        btnLoading.classList.remove('hidden');
        predictBtn.disabled = true;

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        data.BHK             = parseInt(data.BHK);
        data.Area_SqFt       = parseInt(data.Area_SqFt);
        data.Bathrooms       = parseInt(data.Bathrooms);
        data.Balcony         = parseInt(data.Balcony);
        data.Age_of_Property = parseInt(data.Age_of_Property);

        try {
            const res = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                const result = await res.json();

                priceDisplay.textContent = result.estimated_price;
                buildMetaChips(data);

                // Switch views with animation
                formSection.classList.add('hidden');
                resultSection.classList.remove('hidden');
                resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

                // Fetch recommendations
                await fetchRecommendations(data.City, data.BHK, result.raw_lakhs);
            } else {
                alert('Prediction failed. Please try again.');
            }
        } catch (err) {
            console.error('Prediction error:', err);
            alert('Could not connect to the prediction server.');
        } finally {
            btnText.classList.remove('hidden');
            btnLoading.classList.add('hidden');
            predictBtn.disabled = false;
        }
    });

    // ── Reset Button ────────────────────────────────────────
    resetBtn.addEventListener('click', () => {
        resultSection.classList.add('hidden');
        formSection.classList.remove('hidden');
        form.reset();
        priceDisplay.textContent = '₹ --';
        resultMeta.innerHTML = '';
        recGrid.innerHTML = '';
        recEmpty.classList.add('hidden');
        form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
        formSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });

    // ── Navbar scroll shadow ────────────────────────────────
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        navbar.style.boxShadow = window.scrollY > 10
            ? '0 4px 20px rgba(0,0,0,0.1)'
            : '0 2px 8px rgba(0,0,0,0.06)';
    }, { passive: true });
});
