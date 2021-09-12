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
    slideTimeout = setTimeout(
        loadImage,
        refreshInterval * 1000
    )
}

function updateImage(data) {
    image = data
    image_element = document.getElementById("image")
    image_element.src = data.url
    image_element.alt = data.filepath
}

loadImage()
