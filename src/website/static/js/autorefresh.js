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
    image_element.onload = function () {
        resizeImage(image_element)
    }
    image_element.src = data.url
    image_element.alt = data.filepath
}

function resizeImage(img) {
    img_ratio = img.naturalWidth / img.naturalHeight
    container = img.parentElement
    container_ratio = container.clientWidth / container.clientHeight
    console.log(`Image ${img.naturalWidth}/${img.naturalHeight}=${img_ratio} Div=${container.clientWidth}/${container.clientHeight}=${container_ratio}`)
    if (img_ratio > container_ratio) {
        console.log("Width 100%")
        img.setAttribute("width", "100%")
        img.removeAttribute("height")
    } else {
        console.log("Height 100%")
        img.setAttribute("height", "100%")
        img.removeAttribute("width")
    }
}

loadImage()
