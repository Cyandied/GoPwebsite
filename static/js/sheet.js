const modals = document.querySelectorAll(".modal")
const modalBackgrounds = document.querySelectorAll(".modal-bg")
const modalButton = document.querySelectorAll(".modal-button")
const closeModal = document.querySelectorAll(".close-modal")

modalButton.forEach(elem => {
    elem.addEventListener("click", e=>{
        const modalType = e.target.dataset.modal
        modalBackgrounds.forEach(modal => {
            if(modal.dataset.id == modalType){
                modal.classList.remove("hidden")
            }
            else{
                modal.classList.add("hidden")
            }
        })

    })
});

closeModal.forEach(close => {
    close.addEventListener("click",e=>{
        modalBackgrounds.forEach(modal => {
            modal.classList.add("hidden")
        })
    })
});