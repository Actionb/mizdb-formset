window.addEventListener("DOMContentLoaded", () => {

    // Return whether the formfields under the current form-container are empty.
    function isEmpty(form) {
        for (elem of form.querySelectorAll(".fields-container input:not([type=hidden]),select,textarea")) {
            if ((elem.type === "checkbox" && elem.checked) || elem.value.trim()) return false 
        }
        return true
    }
    function getTotalFormsElement(formset) {
        return formset.querySelector("[id$=TOTAL_FORMS")
    }

    function updateTotalCount(formset, count) {
        getTotalFormsElement(formset).value = count
    }

    function getTotalCount(formset){
        return parseInt(getTotalFormsElement(formset).value, 10)
    }

    function deleteHandler(btn) {
        btn.addEventListener("click", (e) => {
            e.preventDefault()
            wrapper = btn.parentNode.parentNode
            formset = wrapper.parentNode
            if (wrapper.classList.contains("extra-form") && isEmpty(wrapper)) {
                wrapper.remove()
                updateTotalCount(formset, getTotalCount(formset) - 1)
                // TODO: update prefixes
            }
            else {
                wrapper.classList.toggle("marked-for-removal")
                checkbox = wrapper.querySelector(".delete-cb")
                checkbox.checked = !checkbox.checked
                wrapper.querySelectorAll(".form-control").forEach((elem) => {
                    elem.disabled = !elem.disabled
                })
            }
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
            count = getTotalCount(formsetContainer) + 1
            updateTotalCount(formsetContainer, count)

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
