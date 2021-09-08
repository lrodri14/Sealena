/* This registers.js file contains all the variable definitions, async functions and event listeners needed to display
   the consults registers template in the Appointments app.*/

/*#################################################### Variables #####################################################*/

let container = document.querySelector('.data')
let filter_form = document.querySelector('.filter-container__filter-form')
let tbody = document.querySelector('tbody')

/*#################################################### Functions #####################################################*/

async function filterResultsAW(url){
    /* This filterResultsAW async function is used to filter results from the Agenda based on a date query, this func
    takes four parameters, the 'url' which we collect from the form's action attribute, the 'method' we collect from
    the form's method attribute, csrfmiddlewaretoken we collect from the form's hidden input,and the 'formData' which
     we collect from the form and convert it into a formData object. The response will be converted into JSON before
     dynamically showing it.*/
    const result = await fetch(url)
    const data = await result.json()
    return data
}

/*#################################################### Event Listeners ###############################################*/

// Event delegation capturing
if (container){

    //Wrapper mouse over
    container.addEventListener('mouseover', (e) => {

        /* This event will be fired every time a hover occurs on a target which classList contains 'filter-container__filter-display-button' this will add the
        filter-container__filter-display-button--active class to the target.*/
        if (e.target.classList.contains('filter-container__filter-display-button')){
            e.target.classList.add('filter-container__filter-display-button--active')
        }

        /* This event will be fired every time a hover occurs on a target which nodeName is 'BUTTON', this will add the
        button--active class to the target.*/
        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.add('button--active')
        }

        /* This event will be fired every time a hover occurs on a target which is a table data cell
           this will add the some styles to the row.*/
        if (e.target.closest('.data-table__item')){
            let row = e.target.closest('.data-table__item')
            row.style.backgroundColor = '#FFFFFF'
            row.style.color = '#000000'
        }

        /* This event is fired every time a hover occurs over an input tag, it will add the input-active class to the target*/
        if (e.target.nodeName === 'INPUT'){
            e.target.classList.add('input-active')
        }

    })

    //Wrapper mouse out
    container.addEventListener('mouseout', (e) => {

        /* This event will be fired every time a hover out occurs on a target which classList contains 'filter-container__filter-display-button' this will remove the
           filter-container__filter-display-button--active class to the target.*/
        if (e.target.classList.contains('filter-container__filter-display-button')){
            e.target.classList.remove('filter-container__filter-display-button--active')
        }

        /* This event will be fired every time a hover out occurs on a target which nodeName is 'BUTTON', this will remove the
        button--active class to the target.*/
        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.remove('button--active')
        }

        /* This event will be fired every time a hover occurs on a target which is a table data cell
           this will add the some styles to the row.*/
        if (e.target.closest('.data-table__item')){
            let row = e.target.closest('.data-table__item')
            row.style.backgroundColor = ''
            row.style.color = ''
        }

        /* This event is fired every time a hover occurs over an input tag, it will add the input-active class to the target*/
        if (e.target.nodeName === 'INPUT'){
            e.target.classList.remove('input-active')
        }

    })

    //Wrapper Click

    /* This event will be fired every time a click occurs on the fa-filter icon, this will check if the filter form
    is shown or hidden, and perform the displaying or hiding depending on the previous condition.*/
    container.addEventListener('click', (e) => {

        /* This event will be fired whenever the target contains the filter-container__filter-display-button in its classlist, based on
           if it contains it, will add or remove the filter-container__filter-form--display class*/
        if (e.target.classList.contains('filter-container__filter-display-button')){
            filter_form.classList.contains('filter-container__filter-form--display') ? filter_form.classList.remove('filter-container__filter-form--display') : filter_form.classList.add('filter-container__filter-form--display')
        }

    })

    //Wrapper Submit
    container.addEventListener('submit', (e) => {
        /*This event will be fired every time a submit occurs and the target contains the 'modal-cancel-form' class in it's
        classlist, this event will stop the itself, and collect the data needed to cancel the consult, this consists of
        the url, method, csrfmiddlewaretoken and the form data, once this data is collected from the form, we proceed to
        call our asynchronous function, the response is dynamically displayed in our table.*/
        if (e.target.classList.contains('filter-container__filter-form')){
            e.preventDefault()
            let patientQuery = document.querySelector('#id_patient').value
            let monthQuery = document.querySelector('#id_month').value
            let yearQuery = document.querySelector('#id_year').value
            let url = e.target.action + '?patient=' + patientQuery + '&month=' + monthQuery + '&year=' + yearQuery
            filterResultsAW(url)
            .then(data => {
                tbody.innerHTML = data['html']
            })
        }
    })
}