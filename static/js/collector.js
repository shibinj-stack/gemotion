let log = [];
let keyDownTimes = {};
let lastUp = null;

document.getElementById('typingArea').addEventListener('keyup', (e) => {
    const now = performance.now();
    const down = keyDownTimes[e.key];
    if (down) {
        const hold = now - down;
        const flight = lastUp ? down - lastUp : 0;
        log.push({
            key: e.key,
            hold_time: hold.toFixed(2),
            flight_time: flight.toFixed(2),
            latency: (hold + flight).toFixed(2)
        });
        lastUp = now;
        delete keyDownTimes[e.key];
        document.getElementById('count').innerText = log.length;
    }
});

async function saveBatch() {
    const emotion = document.getElementById('emotionSelect').value;
    await fetch('/save_to_csv', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ emotion: emotion, data: log })
    });
    alert("Saved!");
    log = [];
}