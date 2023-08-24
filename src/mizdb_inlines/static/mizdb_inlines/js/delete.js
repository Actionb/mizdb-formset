window.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".delete-btn").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            e.preventDefault()
            wrapper = btn.parentNode.parentNode
            wrapper.classList.toggle("marked-for-removal")
            checkbox = wrapper.querySelector(".delete-cb")
            checkbox.checked = !checkbox.checked
            wrapper.querySelectorAll(".form-control").forEach((elem) => {
                elem.disabled = !elem.disabled
            })
        })
    })
})