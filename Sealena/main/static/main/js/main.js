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
const navSections = document.querySelectorAll('.navbar__content div')

/*/////////////////////////////////////////////// Intersection Observers /////////////////////////////////////////////*/
const cardObserverOptions = {
    root: null,
    threshold: 0.3,
    rootMargin: "0px",
}

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

const cardObserver = new IntersectionObserver(cardObserverCallback, cardObserverOptions);
cardObserver.observe(introduction)
cardObserver.observe(management)
cardObserver.observe(collaboration)
cardObserver.observe(statistics)
cardObserver.observe(linking)
cardObserver.observe(reaching)
cardObserver.observe(mailing)

/*//////////////////////////////////////////////////// Event Listeners ///////////////////////////////////////////////*/
if (navSections){
    navSections.forEach((section) => {
        section.addEventListener('mouseover', (e) => {
            e.target.classList.add('navbar-section--active')
        })

        section.addEventListener('mouseout', (e) => {
            e.target.classList.remove('navbar-section--active')
        })

        section.addEventListener('click', (e) => {

        })
    })
}