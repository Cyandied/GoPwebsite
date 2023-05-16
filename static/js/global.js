const clickToDisplay = document.querySelectorAll(".click-to-display")
const flash = document.querySelector(".flashes")

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

if(flash){
    flash.addEventListener("click", e=>{
        flash.classList.add("hidden")
    })
}
