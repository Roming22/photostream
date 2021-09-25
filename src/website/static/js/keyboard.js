window.addEventListener(
    'keydown',
    (event) => {
        console.log(`Key pressed ${event.code}/${event.key}/${event.value}`);
        keyCode = event.code
        if (keyCode === "ArrowRight" || keyCode === "Enter") {
            loadImage()
        } else if (keyCode === "ArrowDown" || event.key === "-") {
            imageTimer.shift(-1000)
        } else if (keyCode === "ArrowUp" || event.key === "+") {
            imageTimer.shift(1000)
        } else if (keyCode === "ArrowRight" || keyCode === "Enter") {
            loadImage()
        } else if (keyCode === "Delete") {
            deleteImage()
        } else if (keyCode === "KeyP" || keyCode === "Space") {
            imageTimer.pause_play()
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