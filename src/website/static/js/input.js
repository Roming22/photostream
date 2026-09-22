const CONTROLS_HUD_MS = 1000

let controlsHudHideTimer = null

function controlsHud() {
    return document.querySelector(".controls-hud")
}

function showControlsHud() {
    const hud = controlsHud()
    if (!hud) {
        return
    }
    hud.classList.add("is-visible")
    hud.setAttribute("aria-hidden", "false")
    scheduleHideControlsHud()
}

function hideControlsHud() {
    const hud = controlsHud()
    if (!hud) {
        return
    }
    hud.classList.remove("is-visible")
    hud.setAttribute("aria-hidden", "true")
}

function scheduleHideControlsHud({ ignoreHover = false } = {}) {
    const hud = controlsHud()
    clearTimeout(controlsHudHideTimer)
    controlsHudHideTimer = setTimeout(() => {
        // :hover can stick after a tap on touch devices; ignoreHover
        // lets button presses dismiss the HUD anyway.
        if (!hud || (!ignoreHover && hud.matches(":hover"))) {
            return
        }
        hideControlsHud()
    }, CONTROLS_HUD_MS)
}

function getFullscreenElement() {
    return document.fullscreenElement || document.webkitFullscreenElement || null
}

function isImmersive() {
    return document.documentElement.classList.contains("is-immersive")
}

function isFullscreen() {
    return Boolean(getFullscreenElement()) || isImmersive()
}

function setImmersive(on) {
    document.documentElement.classList.toggle("is-immersive", on)
    syncControlsHud()
}

function requestNativeFullscreen(el) {
    if (el.requestFullscreen) {
        return el.requestFullscreen({ navigationUI: "hide" }).catch(() =>
            el.requestFullscreen()
        )
    }
    if (el.webkitRequestFullscreen) {
        return Promise.resolve(el.webkitRequestFullscreen())
    }
    return Promise.reject(new Error("Fullscreen API unavailable"))
}

function exitNativeFullscreen() {
    if (document.exitFullscreen) {
        return document.exitFullscreen()
    }
    if (document.webkitExitFullscreen) {
        return document.webkitExitFullscreen()
    }
    return Promise.reject(new Error("Fullscreen API unavailable"))
}

async function toggleFullscreen() {
    if (getFullscreenElement()) {
        try {
            await exitNativeFullscreen()
        } catch {
            setImmersive(false)
        }
        return
    }
    if (isImmersive()) {
        setImmersive(false)
        return
    }

    // Prefer html/body so the controls HUD stays in the fullscreen tree.
    // Some iOS builds only accept a concrete element; try the stage last.
    const targets = [
        document.documentElement,
        document.body,
        document.querySelector(".flex-container"),
    ].filter(Boolean)

    for (const el of targets) {
        try {
            await requestNativeFullscreen(el)
            return
        } catch {
            // Try the next target, then fall back to CSS immersive mode.
        }
    }

    // iOS Safari (and non-secure contexts) often lack usable Fullscreen API.
    setImmersive(true)
}

function syncControlsHud() {
    const pauseBtn = document.getElementById("controls-pause")
    const shuffleBtn = document.getElementById("controls-shuffle")
    const fullscreenBtn = document.getElementById("controls-fullscreen")
    if (!pauseBtn || !shuffleBtn) {
        return
    }

    const paused = imageTimer.isPaused()
    pauseBtn.classList.toggle("is-paused", paused)
    pauseBtn.title = paused ? "Play" : "Pause"
    pauseBtn.setAttribute("aria-label", paused ? "Play" : "Pause")

    shuffleBtn.setAttribute("aria-pressed", shuffle ? "true" : "false")
    shuffleBtn.title = shuffle ? "Disable shuffle" : "Enable shuffle"
    shuffleBtn.setAttribute("aria-label", shuffle ? "Disable shuffle" : "Enable shuffle")

    if (fullscreenBtn) {
        const fullscreen = isFullscreen()
        fullscreenBtn.classList.toggle("is-fullscreen", fullscreen)
        fullscreenBtn.setAttribute("aria-pressed", fullscreen ? "true" : "false")
        fullscreenBtn.title = fullscreen ? "Exit fullscreen" : "Fullscreen"
        fullscreenBtn.setAttribute("aria-label", fullscreen ? "Exit fullscreen" : "Fullscreen")
    }

    const image = document.getElementById("image")
    if (image && image.naturalWidth) {
        resizeImage(image)
    }
}

window.addEventListener(
    'keydown',
    (event) => {
        console.log(`Key pressed ${event.code}/${event.key}/${event.value}`);
        keyCode = event.code
        if (keyCode === "ArrowRight" || keyCode === "Enter") {
            console.log("Next image");
            event.preventDefault()
            nextImage()
        } else if (keyCode === "ArrowLeft" || keyCode === "Backspace") {
            console.log("Previous image");
            event.preventDefault()
            previousImage()
        } else if (keyCode === "ArrowDown" || event.key === "-") {
            console.log("Shorter delay");
            event.preventDefault()
            imageTimer.shift(-Math.round(imageTimer.initialMs / 3))
        } else if (keyCode === "ArrowUp" || event.key === "+") {
            console.log("Longer delay");
            event.preventDefault()
            imageTimer.shift(Math.round(imageTimer.initialMs / 3))
        } else if (keyCode === "Delete") {
            deleteImage()
        } else if (keyCode === "KeyP" || keyCode === "Space") {
            console.log("Play/Pause");
            event.preventDefault()
            imageTimer.pause_play()
            showControlsHud()
        } else if (keyCode === "KeyS") {
            toggleShuffle()
            showControlsHud()
        } else if (keyCode === "KeyF") {
            console.log("Fullscreen");
            event.preventDefault()
            toggleFullscreen()
            showControlsHud()
        }
    },
    true
);

document.addEventListener('swiped-left', function (e) {
    console.log("Next image");
    nextImage()
});

document.addEventListener('swiped-right', function (e) {
    console.log("Previous image");
    previousImage()
});

document.addEventListener("mousemove", showControlsHud)
document.addEventListener("touchstart", showControlsHud, { passive: true })
document.addEventListener("touchmove", showControlsHud, { passive: true })

document.addEventListener("DOMContentLoaded", () => {
    const hud = controlsHud()
    const pauseBtn = document.getElementById("controls-pause")
    const shuffleBtn = document.getElementById("controls-shuffle")
    const shorterBtn = document.getElementById("controls-shorter")
    const longerBtn = document.getElementById("controls-longer")
    const fullscreenBtn = document.getElementById("controls-fullscreen")

    if (hud) {
        hud.addEventListener("mouseenter", () => clearTimeout(controlsHudHideTimer))
        hud.addEventListener("mouseleave", () => scheduleHideControlsHud())
    }
    if (pauseBtn) {
        pauseBtn.addEventListener("click", () => {
            imageTimer.pause_play()
            scheduleHideControlsHud({ ignoreHover: true })
        })
    }
    if (shuffleBtn) {
        shuffleBtn.addEventListener("click", () => {
            toggleShuffle()
            scheduleHideControlsHud({ ignoreHover: true })
        })
    }
    if (shorterBtn) {
        shorterBtn.addEventListener("click", () => {
            imageTimer.shift(-Math.round(imageTimer.initialMs / 3))
            scheduleHideControlsHud({ ignoreHover: true })
        })
    }
    if (longerBtn) {
        longerBtn.addEventListener("click", () => {
            imageTimer.shift(Math.round(imageTimer.initialMs / 3))
            scheduleHideControlsHud({ ignoreHover: true })
        })
    }
    if (fullscreenBtn) {
        fullscreenBtn.addEventListener("click", () => {
            toggleFullscreen()
            scheduleHideControlsHud({ ignoreHover: true })
        })
    }
    document.addEventListener("fullscreenchange", syncControlsHud)
    document.addEventListener("webkitfullscreenchange", syncControlsHud)
    syncControlsHud()
})

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