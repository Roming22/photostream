imageList = null
imageIndex = 0

function adjustableTimer(action, initialMs) {
    // source: https://stackoverflow.com/a/11433429
    return {
        timerId: null,
        startTime: new Date(),
        initialMs: initialMs,
        action: action,
        shift: function (howMuch) {
            var elapsedTime = new Date() - this.startTime;
            var remainingTime = this.initialMs - elapsedTime;
            var newTime = remainingTime + howMuch;
            if (newTime < 150) {
                newTime = 150
            }
            this.stop()
            this.timerId = setTimeout(this.action, newTime);
            this.initialMs += howMuch
            if (this.initialMs < 1000) {
                this.initialMs = 1000
            }
            console.log(`Timer: ${this.initialMs}ms`)
        },
        start: function () {
            this.stop()
            this.startTime = new Date()
            this.timerId = setTimeout(this.action, this.initialMs)
        },
        stop: function () {
            if (this.timerId) {
                clearTimeout(this.timerId)
            }
        },
        pause_play: function () {
            if (this.timerId) {
                console.log("Pause the slideshow")
                this.stop()
                this.timerId = null
            } else {
                console.log("Resume the slideshow")
                this.timerId = setTimeout(this.action, 150)
            }
        },
    };
}

function getImages() {
    console.log("Load images list")
    fetch(`/${topic}/images`).then(function (response) {
        return response.json()
    }).then(function (data) {
        console.log(`Data = ${data}`)
        imageList = data["images"]
        console.log(`Images = ${imageList}`)
        loadImage()
    })
}

function nextImage() {
    imageIndex += 1
    loadImage()
}

function previousImage() {
    imageIndex -= 1
    loadImage()
}

function loadImage() {
    imageTimer.stop()

    imageIndex = imageIndex % imageList.length
    if (imageIndex < 0) {
        imageIndex += imageList.length
    }
    console.log(`Load image ${imageIndex}`)

    updateImage(imageList[imageIndex])
    imageTimer.start()
}

function updateImage(image) {
    image_element = document.getElementById("image")
    image_element.onload = function () {
        resizeImage(image_element)
    }
    image_element.src = image.url
    image_element.alt = image.filename
}

function resizeImage(img) {
    img_ratio = img.naturalWidth / img.naturalHeight
    container = img.parentElement
    container_ratio = container.clientWidth / container.clientHeight
    // console.log(`Image ${img.naturalWidth}/${img.naturalHeight}=${img_ratio} Div=${container.clientWidth}/${container.clientHeight}=${container_ratio}`)
    if (img_ratio > container_ratio) {
        // console.log("Width 100%")
        img.setAttribute("width", "100%")
        img.removeAttribute("height")
    } else {
        // console.log("Height 100%")
        img.setAttribute("height", "100%")
        img.removeAttribute("width")
    }
}


imageTimer = adjustableTimer(nextImage, 6000)
getImages()
