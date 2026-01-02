let keystrokeBuffer = [];
let keyDownTimes = {};
let lastKeyUpTime = null;

const typingArea = document.getElementById('typingArea');
const resultDisplay = document.getElementById('result');

typingArea.addEventListener('keydown', (e) => {
    // Record start time of key press
    if (!keyDownTimes[e.key]) {
        keyDownTimes[e.key] = performance.now();
    }
});

typingArea.addEventListener('keyup', (e) => {
    const upTime = performance.now();
    const downTime = keyDownTimes[e.key];

    if (downTime) {
        const holdTime = upTime - downTime;
        const flightTime = lastKeyUpTime ? downTime - lastKeyUpTime : 0;
        
        // Push timing data to buffer
        keystrokeBuffer.push({
            hold_time: holdTime.toFixed(2),
            flight_time: flightTime.toFixed(2),
            latency: (holdTime + flightTime).toFixed(2)
        });

        lastKeyUpTime = upTime;
        delete keyDownTimes[e.key];
    }
});

async function sendForPrediction() {
    if (keystrokeBuffer.length < 10) {
        resultDisplay.innerText = "Error: Please type at least 10 characters first.";
        return;
    }

    // IMPORTANT: Reveal the result container
    const container = document.getElementById('resultContainer');
    if(container) container.classList.remove('hidden'); 
    
    resultDisplay.innerText = "Analyzing rhythm...";

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ timings: keystrokeBuffer })
        });

        const result = await response.json();
        console.log("Server Response:", result); // Debugging line
        resultDisplay.innerText = "Feeling: " + result.emotion;
        
        // If you added the dashboard, update it here
        if (typeof updateDashboard === "function") {
            updateDashboard(keystrokeBuffer);
        }
    } catch (error) {
        resultDisplay.innerText = "Error connecting to server.";
        console.error(error);
    }
}

function resetBuffer() {
    keystrokeBuffer = [];
    typingArea.value = "";
    resultDisplay.innerText = "Result: Waiting for input...";
    lastKeyUpTime = null;
}