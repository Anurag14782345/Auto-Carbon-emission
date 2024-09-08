// Function to fetch and update data
function fetchData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            updateCOPlot(data);
            updateSafetyRatingPlot(data);
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Function to update CO plot (Simple line graph)
function updateCOPlot(data) {
    const timestamps = data.map(entry => entry.timestamp);
    const coValues = data.map(entry => entry.co_value);

    const trace = {
        x: timestamps,
        y: coValues,
        type: 'scatter',
        mode: 'lines',
        line: {color: 'red', width: 2}
    };

    const layout = {
        title: 'CO Levels (ppm)',
        xaxis: {title: 'Timestamp'},
        yaxis: {title: 'CO (ppm)'},
        margin: {t: 50}
    };

    Plotly.newPlot('co-plot', [trace], layout);
}

// Function to update Safety Rating plot (Simple line graph)
function updateSafetyRatingPlot(data) {
    const timestamps = data.map(entry => entry.timestamp);
    const ratings = data.map(entry => classifyEmission(entry.co_value));

    const trace = {
        x: timestamps,
        y: ratings.map(rating => ratingToNumber(rating)),
        type: 'scatter',
        mode: 'lines',
        line: {color: 'blue', width: 2}
    };

    const layout = {
        title: 'Safety Rating',
        xaxis: {title: 'Timestamp'},
        yaxis: {title: 'Safety Rating'},
        margin: {t: 50}
    };

    Plotly.newPlot('safety-rating-plot', [trace], layout);
}

// Function to classify emission
function classifyEmission(coLevel) {
    if (coLevel <= 10) return 'Safest';
    if (coLevel <= 30) return 'Normal';
    if (coLevel <= 50) return 'Average';
    if (coLevel <= 100) return 'Above Average';
    if (coLevel <= 200) return 'Danger';
    return 'Hazardous';
}

// Convert safety rating to a numeric scale for plotting
function ratingToNumber(rating) {
    const ratingsMap = {
        'Safest': 1,
        'Normal': 2,
        'Average': 3,
        'Above Average': 4,
        'Danger': 5,
        'Hazardous': 6
    };
    return ratingsMap[rating];
}


// Fetch data initially and set interval for periodic updates
fetchData();
setInterval(fetchData, 10000);  // Refresh every 10 seconds
