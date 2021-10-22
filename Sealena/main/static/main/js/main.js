/* This main.js file contains all the logic used and needed for the main page to work properyly */

// Scrolling into top of the page
window.scrollTo(0,0)

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
                    const source = image.src.split("-blur.jpg")
                    if (source.length === 2){
                        image.src = image.classList.contains('card__img') ? source[0] + '.jpg' : source[0] + '.png'
                        image.classList.contains('card__img') ? image.classList.add('card__img--unfilter') : image.classList.add('card__sc--unfilter')
                    }
                })
            }, 500)
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

// Navigation Sections
if (navSections){
    navSections.forEach((section) => {
        // Section Mouseover events
        section.addEventListener('mouseover', (e) => {
            const target = e.target
            !target.classList.contains('navbar__go-to-app') && target.nodeName === 'DIV'
            ? e.target.classList.add('navbar__tile--active')
            : null
            target.closest('.navbar__go-to-app') ? target.classList.add('navbar__go-to-app--active') : null
        })

        // Section Mouseover events
        section.addEventListener('mouseout', (e) => {
            const target = e.target
            !target.classList.contains('navbar__go-to-app') && target.nodeName === 'DIV'
            ? e.target.classList.remove('navbar__tile--active')
            : null
            target.closest('.navbar__go-to-app') ? target.classList.remove('navbar__go-to-app--active') : null
        })

        // Section Click events
        section.addEventListener('click', (e) => {
            let target = e.target.textContent.toLowerCase()
            target = target === 'main' ? 'introduction' : target
            const section = document.querySelector('.' + target)
            section.scrollIntoView(false)
        })
    })
}

// Go to App Btn Events
if (goToAppBtn){
    // Go to app, mouseover events
    goToAppBtn.addEventListener('mouseover', (e) => {
        e.target.classList.add('go-to-app--active')
    })
    // Go to app, mouseout events
    goToAppBtn.addEventListener('mouseout', (e) => {
        e.target.classList.remove('go-to-app--active')
    })
}