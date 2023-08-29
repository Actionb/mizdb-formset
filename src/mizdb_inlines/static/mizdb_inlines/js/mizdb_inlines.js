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

    function getFormsetPrefix(formset) {
        return formset.dataset.prefix
    }

    function getFormPrefix(form) {
        return getFormsetPrefix(form.parentNode)
    }

    function updatePrefixes(form, index) {
        prefix = getFormPrefix(form)
        regex = new RegExp(`(${prefix}-(\\d+|__prefix__))`)
        form.querySelectorAll("*").forEach((elem) => {
            for (attr of ["id", "name", "for"]) {
                if (elem.hasAttribute(attr)) {
                    elem.setAttribute(attr, elem.getAttribute(attr).replace(regex, `${prefix}-${index}`))
                }
            } 
        })
    }

    function deleteHandler(btn) {
        btn.addEventListener("click", (e) => {
            e.preventDefault()
            form = btn.parentNode.parentNode
            formset = form.parentNode
            if (form.classList.contains("extra-form") && isEmpty(form)) {
                form.remove()
                updateTotalCount(formset, getTotalCount(formset) - 1)
                index = 0
                formset.querySelectorAll(":scope > .form-container").forEach((f) => {
                    if (f.classList.contains("extra-form")) updatePrefixes(f, index)
                    index = index + 1
                })
            }
            else {
                form.classList.toggle("marked-for-removal")
                checkbox = form.querySelector(".delete-cb")
                checkbox.checked = !checkbox.checked
                form.querySelectorAll(".form-control").forEach((elem) => {
                    elem.disabled = !elem.disabled
                })
            }
        })
    }

    function addHandler(btn) {
        btn.addEventListener("click", (e) => {
            e.preventDefault()

            addRow = btn.parentNode
            formset = addRow.parentNode

            newForm = addRow.querySelector(".empty-form > div").cloneNode(true)
            formset.insertBefore(newForm, addRow)
            deleteHandler(newForm.querySelector(".delete-btn"))

            // Update management form
            count = getTotalCount(formset) + 1
            updateTotalCount(formset, count)
            updatePrefixes(newForm, count - 1)
        })
    }

    document.querySelectorAll(".delete-btn").forEach((btn) => deleteHandler(btn))
    document.querySelectorAll(".add-btn").forEach((btn) => addHandler(btn))
})
