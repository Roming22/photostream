imageList = null
imageIndex = 0

const TIMER_MIN_MS = 175
const TIMER_MAX_MS = 5 * 60 * 1000  // 5 minutes
const SPEED_HUD_MS = 1000

let speedHudHideTimer = null

function showSpeedFeedback(ms) {
    const hud = document.querySelector(".speed-hud")
    const fill = document.querySelector(".speed-hud__fill")
    if (!hud || !fill) {
        return
    }

    // Log scale; fuller = slower (longer interval).
    const logMin = Math.log(TIMER_MIN_MS)
    const logMax = Math.log(TIMER_MAX_MS)
    const ratio = (Math.log(ms) - logMin) / (logMax - logMin)
    fill.style.width = `${Math.min(1, Math.max(0, ratio)) * 100}%`

    hud.classList.add("is-visible")
    clearTimeout(speedHudHideTimer)
    speedHudHideTimer = setTimeout(() => {
        hud.classList.remove("is-visible")
    }, SPEED_HUD_MS)
}

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
            var newTime = Math.min(Math.max(remainingTime + howMuch, TIMER_MIN_MS), TIMER_MAX_MS);
            this.stop()
            this.timerId = setTimeout(this.action, newTime);
            this.initialMs = Math.min(Math.max(this.initialMs + howMuch, TIMER_MIN_MS), TIMER_MAX_MS);
            console.log(`Timer: ${this.initialMs}ms`)
            showSpeedFeedback(this.initialMs)
        },
        start: function () {
            this.stop()
            this.startTime = new Date()
            this.timerId = setTimeout(this.action, this.initialMs)
            if (typeof syncControlsHud === "function") {
                syncControlsHud()
            }
        },
        stop: function () {
            if (this.timerId) {
                clearTimeout(this.timerId)
                this.timerId = null
            }
        },
        pause_play: function () {
            if (this.timerId) {
                console.log("Pause the slideshow")
                this.stop()
            } else {
                console.log("Resume the slideshow")
                this.timerId = setTimeout(this.action, 150)
            }
            if (typeof syncControlsHud === "function") {
                syncControlsHud()
            }
        },
        isPaused: function () {
            return !this.timerId
        },
    };
}

function getImages() {
    console.log("Load images list")
    imageIndex = 0
    fetch(`/${topic}/images?shuffle=${shuffle}`).then(function (response) {
        return response.json()
    }).then(function (data) {
        console.log(`Data = ${data}`)
        imageList = data["images"]
        console.log(`Images = ${imageList}`)
        loadImage()
    })
}

function toggleShuffle() {
    shuffle = !shuffle
    console.log(`Shuffle: ${shuffle}`)
    if (typeof syncControlsHud === "function") {
        syncControlsHud()
    }
    getImages()
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
    if (img_ratio > container_ratio) {
        img.setAttribute("width", "100%")
        img.removeAttribute("height")
    } else {
        img.setAttribute("height", "100%")
        img.removeAttribute("width")
    }
}


imageTimer = adjustableTimer(nextImage, time)
getImages()
