window.addEventListener("DOMContentLoaded", () => {
    function deleteHandler(btn) {
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
    }
    function addHandler(btn) {
        btn.addEventListener("click", (e) => {
            e.preventDefault()

            addRow = btn.parentNode
            formsetContainer = addRow.parentNode

            template = addRow.querySelector(".empty-form > div")
            copy = template.cloneNode(true)
            formsetContainer.insertBefore(copy, addRow)
            deleteHandler(copy.querySelector(".delete-btn"))

            // Update management form
            totalForms = formsetContainer.querySelector("[id$=TOTAL_FORMS")
            count = parseInt(totalForms.value, 10) + 1
            totalForms.value = count

            // Update 'id', 'name' and 'for' attributes
            copy.querySelectorAll("*").forEach((elem) => {
                for (attr of ["id", "name", "for"]) {
                    if (elem.hasAttribute(attr)) {
                        elem.setAttribute(attr, elem.getAttribute(attr).replace("__prefix__", count))
                    }
                } 
            })
        })
    }

    document.querySelectorAll(".delete-btn").forEach((btn) => deleteHandler(btn))
    document.querySelectorAll(".add-btn").forEach((btn) => addHandler(btn))
})
