const gameIds = document.querySelectorAll(".game-id")

gameIds.forEach(gameId => {
    gameId.addEventListener("click", e=>{
        const parent = e.target.closest("div")
        const copytext = parent.querySelector(".id").innerHTML
        const button = parent.querySelector("button")
        const buttonText = "copy id"
        button.innerHTML = "id copied!"
        setTimeout(()=>{
            button.innerHTML = buttonText
        }, 2000)

        // Copy the text inside the text field
        navigator.clipboard.writeText(copytext)
    })
});