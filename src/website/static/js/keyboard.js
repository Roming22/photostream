window.addEventListener(
    'keydown',
    (event) => {
        console.log(`Key pressed ${event.code}/${event.key}/${event.value}`);
        keyCode = event.code
        if (keyCode === "ArrowRight" || keyCode === "Enter") {
            loadImage()
        } else if (keyCode === "ArrowDown" || event.key === "-") {
            refreshInterval -= 1
            if (refreshInterval < 1) {
                refreshInterval = 1
            }
        } else if (keyCode === "ArrowUp" || event.key === "+") {
            refreshInterval += 1
            if (refreshInterval > 60) {
                refreshInterval = 60
            }
        } else if (keyCode === "ArrowRight" || keyCode === "Enter") {
            loadImage()
        } else if (keyCode === "Delete") {
            deleteImage()
        } else if (keyCode === "KeyP" || keyCode === "Space") {
            pause_play()
        }
    },
    true
);

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
        console.log("Resume the slideshow")
        slideTimeout = setTimeout(
            loadImage,
            150
        )
    } else {
        console.log("Pause the slideshow")
        clearTimeout(slideTimeout)
        slideTimeout = false
    }
}