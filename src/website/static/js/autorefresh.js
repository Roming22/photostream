refreshInterval = 5
refreshCount = 0
setInterval(
    function () {
        refreshCount += 1
        if (refreshCount < 42) {
            loadImage()
        } else {
            console.log("Reload page")
            location.reload()
        }
    },
    refreshInterval * 1000
);

function loadImage() {
    console.log("Load image")
    fetch(`/${topic}/random`).then(
        response => response.json()
    ).then(
        data => updateImage(data)
    )
}

function updateImage(data) {
    image = data
    image_element = document.getElementById("image")
    image_element.src = data.url
    image_element.alt = data.filepath
}

loadImage()