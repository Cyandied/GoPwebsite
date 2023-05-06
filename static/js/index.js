const newSheet = document.querySelector("#new-sheet")
const newSheetName = document.querySelector("#sheet-name")
const loadSheet = document.querySelector("button[value = load-sheet")
const sheetSelector = document.querySelector("select[name = sheets]")
const back = document.querySelector("#back")
const form = document.querySelector("form")

newSheet.addEventListener("click", e=> {
    newSheet.innerHTML = "Continue";
    newSheet.classList.add("continue")

    newSheetName.classList.remove("hidden")
    loadSheet.classList.add("hidden")
    sheetSelector.classList.add("hidden")
    back.classList.remove("hidden")

    document.querySelector("button.continue").addEventListener("click" ,_e => {
        if(newSheetName.value !== ""){
            form.requestSubmit()
        }
    })
})

back.addEventListener("click", e=> {
    newSheet.innerHTML = "New sheet";
    newSheet.classList.remove("continue")

    newSheetName.classList.add("hidden")
    newSheetName.value = ""
    loadSheet.classList.remove("hidden")
    sheetSelector.classList.remove("hidden")
    back.classList.add("hidden")
})