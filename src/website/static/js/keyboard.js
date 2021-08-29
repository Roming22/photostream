window.addEventListener('keydown', (event) => {
    // alert(`Key pressed ${event.key}`);
    if (event.key === "ArrowRight" || event.key === "Enter") {
        reload()
    } else if (event.key === "Delete") {
        deleteImage()
    } else if (event.key === "Space") {
        pause_play()
    }
}, true);

function deleteImage() {
    if (confirm(`Delete ${image.filepath} from ${topic}`)) {
        console.log(`Delete ${image.filename}`)
        fetch(`/${topic}/${image.filename}`, {
            method: "DELETE",
        }).then(res => {
            console.log(`${image.filepath} deleted`, res);
        });
    }
}

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