/* This consult_details.js JS file contains all the logic to display the consult details view properly */

/*//////////////////////////////////////////////////////// Variables /////////////////////////////////////////////////*/

let detailsContainer = document.querySelector('.details-container')
let prescriptionModal = document.querySelector('.prescription-modal')
let prescriptionModalContent = document.querySelector('.prescription-modal-content')
let exams = document.querySelectorAll('.exam')
let examsModal = document.querySelector('.exam-preview')
let examImg = document.querySelector('#exam-image')

/*///////////////////////////////////////////////////// Details Container ////////////////////////////////////////////*/

// Details container events
if (detailsContainer){

    // Details container mouseover events
    detailsContainer.addEventListener('mouseover', (e) => {

        /* This event will be fired every time the target contains the print-prescription class, and it will add the
           print-prescription--active class */
        if (e.target.classList.contains('print-prescription')){
            e.target.classList.add('print-prescription--active')
        }

        /* This event will be fired every time the target contains the exam class, and it will add the
           exam-preview--display class */
        if (e.target.classList.contains('exam')){
            examsModal.classList.add('exam-preview--display')
            examImg.src = e.target.href
        }

    })

    // Details container mouseout events
    detailsContainer.addEventListener('mouseout', (e) => {

        /* This event will be fired every time the target contains the print-prescription class, and it will remove the
           print-prescription--active class */
        if (e.target.classList.contains('print-prescription')){
            e.target.classList.remove('print-prescription--active')
        }

        /* This event will be fired every time the target contains the exam class, and it will remove the
           exam-preview--display class */
        if (e.target.classList.contains('exam')){
            examsModal.classList.remove('exam-preview--display')
        }

    })

    // Details container click events
    detailsContainer.addEventListener('click', (e) => {

        // This event will be fired when the target contains the print-prescription class and it will display the prescription pdf
        if (e.target.classList.contains('print-prescription')){
            let pdfPath = e.target.getAttribute('data-pdf')
            prescriptionModal.classList.add('prescription-modal--display')
            PDFObject.embed(pdfPath, prescriptionModalContent)
        }

        // This event will be fired when the target contains the exam class and it will prevent the redirection of the window.
        if (e.target.classList.contains('exam')){
            e.preventDefault()
            e.stopPropagation()
        }

    })
}

/*///////////////////////////////////////////////////// Prescription Modal ////////////////////////////////////////////*/

// Prescription Modal Events
// Prescription Modal Click Events
prescriptionModal.addEventListener('click', (e) => {
    // This event will be fired every time the target is the prescriptionModal and it will remove the prescription-modal--display class from it.
    if (e.target === prescriptionModal){
        prescriptionModal.classList.remove('prescription-modal--display')
    }
})

