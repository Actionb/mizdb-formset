window.addEventListener("DOMContentLoaded", () => {

    // Return whether the form fields under the current form-container are empty.
    function isEmpty(form) {
        for (const elem of form.querySelectorAll(".fields-container input:not([type=hidden]),select,textarea")) {
            if ((elem.type === "checkbox" && elem.checked) || elem.value.trim()) return false 
        }
        return true
    }

    // Return the management form element that stores the form count.
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

    // Update the prefix indeces of the fields belonging to the given form.
    function updatePrefixes(form, index) {
        const prefix = getFormPrefix(form)
        // __prefix__ is the default prefix of empty forms
        const regex = new RegExp(`(${prefix}-(\\d+|__prefix__))`)
        form.querySelectorAll("*").forEach((elem) => {
            for (const attr of ["id", "name", "for"]) {
                if (elem.hasAttribute(attr)) {
                    elem.setAttribute(attr, elem.getAttribute(attr).replace(regex, `${prefix}-${index}`))
                }
            } 
        })
    }

    /* Handle clicking on the delete button of a form. 

    If the form is an extra formm without data, remove the form from the DOM.
    If the form is not empty, or if it is not an extra form, check the (hidden) 
    DELETE checkbox, disable the form and mark it for removal. 
    */
    function deleteHandler(btn) {
        btn.addEventListener("click", (e) => {
            e.preventDefault()
            const form = btn.parentNode.parentNode
            const formset = form.parentNode
            if (form.classList.contains("extra-form") && isEmpty(form)) {
                // Manipulating the number of forms requires updating the 
                // management form and the prefixes.
                form.remove()
                updateTotalCount(formset, getTotalCount(formset) - 1)
                let index = 0
                formset.querySelectorAll(":scope > .form-container").forEach((f) => {
                    if (f.classList.contains("extra-form")) updatePrefixes(f, index)
                    index = index + 1
                })
            }
            else {
                form.classList.toggle("marked-for-removal")
                const checkbox = form.querySelector(".delete-cb")
                checkbox.checked = !checkbox.checked
                form.querySelectorAll(".form-control").forEach((elem) => {
                    elem.disabled = !elem.disabled
                })
            }
        })
    }

    // Handle clicking the 'add another' button, adding an empty, extra form.
    function addHandler(btn) {
        btn.addEventListener("click", (e) => {
            e.preventDefault()

            addRow = btn.parentNode
            formset = addRow.parentNode

            newForm = addRow.querySelector(".empty-form > div").cloneNode(true)
            formset.insertBefore(newForm, addRow)
            deleteHandler(newForm.querySelector(".delete-btn"))

            // Update management form and set the prefixes of the new form.
            count = getTotalCount(formset) + 1
            updateTotalCount(formset, count)
            updatePrefixes(newForm, count - 1)
        })
    }

    document.querySelectorAll(".delete-btn").forEach((btn) => deleteHandler(btn))
    document.querySelectorAll(".add-btn").forEach((btn) => addHandler(btn))
})
