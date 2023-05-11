const clickToDisplay = document.querySelectorAll(".click-to-display")

for (let clickable of clickToDisplay) {
    clickable.addEventListener("click", e => {
        const parent = e.target.closest("div")
        const toDisplay = parent.querySelector(".display")
        if (toDisplay.classList.contains("hidden")) {
            toDisplay.classList.remove("hidden")
        }
        else {
            toDisplay.classList.add("hidden")
        }
    })
}