(() => {
    const mask = document.querySelector(".index-mask");
    if (!mask) {
        return;
    }

    // Fade completes within a short scroll distance.
    const fadeDistance = 120;

    const update = () => {
        const scrollY = window.scrollY || document.documentElement.scrollTop || 0;
        const opacity = Math.max(0, 1 - scrollY / fadeDistance);
        mask.style.opacity = String(opacity);
        mask.style.visibility = opacity === 0 ? "hidden" : "visible";
    };

    update();
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update, { passive: true });
})();
