/* This main.js file contains all the logic used and needed for the main page to work properyly */

/*//////////////////////////////////////////// Variable declarations /////////////////////////////////////////////////*/
const continueButton = document.querySelector('.introduction__continue')
const introduction = document.querySelector('.introduction')
const management = document.querySelector('.management')
const collaboration = document.querySelector('.collaboration')
const statistics = document.querySelector('.statistics')
const reaching = document.querySelector('.reaching')
const mailing = document.querySelector('.mailing')
const linking = document.querySelector('.linking')
const navbar = document.querySelector('.navbar')
const logo = document.querySelector('.logo')
const navSections = document.querySelectorAll('.navbar__content div')
const goToAppBtn = document.querySelector('.go-to-app')

/*/////////////////////////////////////////////// Intersection Observers /////////////////////////////////////////////*/

// Card Observer

// Card Observer Options
const cardObserverOptions = {
    root: null,
    threshold: 0.3,
    rootMargin: "0px",
}

// Card Observer Callback, this card observer callback function is going to be executed any time an observed element is detected
function cardObserverCallback(entries, observer){
    const intersecting = entries[0].isIntersecting
    const target = entries[0].target
    if (intersecting){
        target.classList.add('card--display')
        const targetSection = target.classList[1]
        const content = document.querySelector(`.${targetSection} .card__content`)
        content.classList.add('card__content--display')
        const images = document.querySelectorAll(`.${targetSection} img`)
        if (images){
            setTimeout(() => {
                images.forEach((image) => {
                    image.classList.add('card__sc--unfilter')
                })
            }, 1000)
        }
    }
}

// Card observer observed elements
const cardObserver = new IntersectionObserver(cardObserverCallback, cardObserverOptions);
cardObserver.observe(introduction)
cardObserver.observe(management)
cardObserver.observe(collaboration)
cardObserver.observe(statistics)
cardObserver.observe(linking)
cardObserver.observe(reaching)
cardObserver.observe(mailing)

// Body Observer

// Body Observer Options
const mainObserverOptions = {
    root: null,
    threshold: 0.1,
    rootMargin: "0px",
}

// Body Observer Callback
function mainObserverCallback(entries, observer){
    const intersecting = entries[0].isIntersecting
    if (!intersecting){
        navbar.classList.add('navbar--display')
    }else{
        navbar.classList.remove('navbar--display')
    }
}

// Body Observer
const mainObserver = new IntersectionObserver(mainObserverCallback, mainObserverOptions)
mainObserver.observe(logo)


/*//////////////////////////////////////////////////// Event Listeners ///////////////////////////////////////////////*/
if (navSections){
    navSections.forEach((section) => {
        section.addEventListener('mouseover', (e) => {
            const target = e.target
            !target.classList.contains('navbar__go-to-app') && target.nodeName === 'DIV'
            ? e.target.classList.add('navbar-section--active')
            : null
            target.closest('.navbar__go-to-app') ? target.classList.add('navbar__go-to-app--active') : null
        })

        section.addEventListener('mouseout', (e) => {
            const target = e.target
            !target.classList.contains('navbar__go-to-app') && target.nodeName === 'DIV'
            ? e.target.classList.remove('navbar-section--active')
            : null
            target.closest('.navbar__go-to-app') ? target.classList.remove('navbar__go-to-app--active') : null
        })
    })
}

if (goToAppBtn){
    goToAppBtn.addEventListener('mouseover', (e) => {
        e.target.classList.add('go-to-app--active')
    })

    goToAppBtn.addEventListener('mouseout', (e) => {
        e.target.classList.remove('go-to-app--active')
    })
}