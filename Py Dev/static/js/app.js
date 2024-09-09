function fetchData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            data = addRandomGasValues(data);
            updateCOPlot(data);
            updateGasPlot(data);
            updateSafetyRatingPlot(data);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function addRandomGasValues(data) {
    return data.map(entry => {
        entry.co2_value = Math.random() * 400;
        entry.no_value = Math.random() * 100;   
        entry.no2_value = Math.random() * 50;  
        entry.so_value = Math.random() * 50;  
        entry.so2_value = Math.random() * 50;   
        entry.hc_value = Math.random() * 150; 
        return entry;
    });
}

function updateCOPlot(data) {
    const timestamps = data.map(entry => entry.timestamp);
    const coValues = data.map(entry => entry.co_value);

    const trace = {
        x: timestamps,
        y: coValues,
        type: 'scatter',
        mode: 'lines',
        line: { color: 'red', width: 2 }
    };

const layout = {
    title: 'CO Levels (ppm)',
    xaxis: { title: 'Timestamp' },
    yaxis: { title: 'CO (ppm)' },
    autosize: true,
    margin: { l: 40, r: 20, t: 40, b: 40 } 
};


    Plotly.newPlot('co-plot', [trace], layout);
}

function updateGasPlot(data) {
    const timestamps = data.map(entry => entry.timestamp);

    const traceCO2 = {
        x: timestamps,
        y: data.map(entry => entry.co2_value),
        name: 'CO2',
        type: 'scatter',
        mode: 'lines',
        line: { color: 'green', width: 2 }
    };

    const traceNO = {
        x: timestamps,
        y: data.map(entry => entry.no_value),
        name: 'NO',
        type: 'scatter',
        mode: 'lines',
        line: { color: 'blue', width: 2 }
    };

    const traceNO2 = {
        x: timestamps,
        y: data.map(entry => entry.no2_value),
        name: 'NO2',
        type: 'scatter',
        mode: 'lines',
        line: { color: 'orange', width: 2 }
    };

    const traceSO = {
        x: timestamps,
        y: data.map(entry => entry.so_value),
        name: 'SO',
        type: 'scatter',
        mode: 'lines',
        line: { color: 'purple', width: 2 }
    };

    const traceSO2 = {
        x: timestamps,
        y: data.map(entry => entry.so2_value),
        name: 'SO2',
        type: 'scatter',
        mode: 'lines',
        line: { color: 'brown', width: 2 }
    };

    const traceHC = {
        x: timestamps,
        y: data.map(entry => entry.hc_value),
        name: 'Hydrocarbons',
        type: 'scatter',
        mode: 'lines',
        line: { color: 'pink', width: 2 }
    };

    const layout = {
        title: 'Gas Levels (ppm)',
        xaxis: { title: 'Timestamp' },
        yaxis: { title: 'Concentration (ppm)' },
        margin: { t: 50 }
    };

    Plotly.newPlot('gas-plot', [traceCO2, traceNO, traceNO2, traceSO, traceSO2, traceHC], layout);
}

function updateSafetyRatingPlot(data) {
    const timestamps = data.map(entry => entry.timestamp);
    const ratings = data.map(entry => classifySafetyRating(entry));

    const trace = {
        x: timestamps,
        y: ratings.map(rating => ratingToNumber(rating)),
        type: 'scatter',
        mode: 'lines',
        line: { color: 'blue', width: 2 }
    };

    const layout = {
        title: 'Safety Rating',
        xaxis: { title: 'Timestamp' },
        yaxis: { title: 'Safety Rating' },
        margin: { t: 50 }
    };

    Plotly.newPlot('safety-rating-plot', [trace], layout);
}

function classifySafetyRating(entry) {
    const totalScore = entry.co_value / 200 + entry.co2_value / 400 + entry.no_value / 100 +
                       entry.no2_value / 50 + entry.so_value / 50 + entry.so2_value / 50 + entry.hc_value / 150;
    
    if (totalScore <= 1) return 'Safest';
    if (totalScore <= 2) return 'Normal';
    if (totalScore <= 3) return 'Average';
    if (totalScore <= 4) return 'Above Average';
    if (totalScore <= 5) return 'Danger';
    return 'Hazardous';
}

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

fetchData();
setInterval(fetchData, 10000);  
