window.addEventListener('keydown', (event) => {
    // alert(`Key pressed ${event.key}`);
    if (event.key === "Enter" || event.key === "ArrowRight") {
        reload()
    } else if (event.key === "Space") {
        pause_play()
    }
}, true);

function pause_play() {
    if (slideTimeout === false) {
        reload()
    } else {
        clearTimeout(slideTimeout)
        slideTimeout = false
    }
}

function reload() {
    location.reload();
}