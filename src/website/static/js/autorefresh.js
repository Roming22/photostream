refreshInterval = 5
refreshCount = 0
slideTimeout = null

function loadImage() {
    console.log("Load image")
    fetch(`/${topic}/random`).then(
        response => response.json()
    ).then(
        data => updateImage(data)
    )
    if (refreshCount < 42) {
        refreshCount += 1
        callback = loadImage
    } else {
        callback = reloadPage
    }

    slideTimeout = setTimeout(
        callback,
        refreshInterval * 1000
    )
}

function reloadPage() {
    console.log("Reload page")
    location.reload()
}

function updateImage(data) {
    image = data
    image_element = document.getElementById("image")
    image_element.src = data.url
    image_element.alt = data.filepath
}

loadImage()
