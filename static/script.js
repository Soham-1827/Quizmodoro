document.addEventListener('DOMContentLoaded', function () {
    let timerDisplay = document.getElementById('timer-display');
    let startBtn = document.getElementById('start-btn');
    let stopBtn = document.getElementById('stop-btn');
    let pauseBtn = document.getElementById('pause-btn');
    let durationInput = document.getElementById('duration-input');
    let skipBtn = document.getElementById('skip-btn');
    let uploadContainer = document.getElementById('upload-container');

    let timer;
    let totalTime;
    let remainingTime;
    let isPaused = false;

    function updateDisplay(time) {
        let minutes = Math.floor(time / 60);
        let seconds = time % 60;
        timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    function startTimer() {
        if (durationInput.value <= 0) {
            alert("Please enter a valid duration.");
            return;
        }
        totalTime = parseInt(durationInput.value) * 60;
        remainingTime = totalTime;
        isPaused = false;
        updateDisplay(remainingTime);

        timer = setInterval(() => {
            if (!isPaused) {
                remainingTime--;
                updateDisplay(remainingTime);

                if (remainingTime <= 0) {
                    clearInterval(timer);
                    alert("Time's up! You can now upload your file.");
                    showUploadContainer();
                }
            }
        }, 1000);
    }

    function stopTimer() {
        clearInterval(timer);
        updateDisplay(0);
    }

    function pauseTimer() {
        isPaused = !isPaused;
        pauseBtn.textContent = isPaused ? "Resume" : "Pause";
    }

    function skipToUpload() {
        showUploadContainer();
    }

    function showUploadContainer() {
        uploadContainer.style.display = 'block';
    }

    startBtn.addEventListener('click', startTimer);
    stopBtn.addEventListener('click', stopTimer);
    pauseBtn.addEventListener('click', pauseTimer);
    skipBtn.addEventListener('click', skipToUpload);
});
