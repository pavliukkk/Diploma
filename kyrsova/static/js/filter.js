const listBtn = document.querySelector('.portfolio__list-button')
const itemBtn = document.querySelectorAll('.portfolio__item-img')

function filter() {
    listBtn.addEventListener('click', e => {
        const targetId = e.target.dataset.id

        switch (targetId) {
            case 'all':
                getItems('portfolio__item-img')
                break
            case 'starter':
                getItems(targetId)
                break
            case 'launch':
                getItems(targetId)
                break
            case 'dinner':
                getItems(targetId)
                break
            case 'drink':
                getItems(targetId)
                break
            case 'sweet':
                getItems(targetId)
                break
            case 'fruit':
                getItems(targetId)
                break
            case 'alcohol':
                getItems(targetId)
                break
        }

    })
}

filter()

function getItems(className) {
    itemBtn.forEach(item => {
        if(item.classList.contains(className)) {
            item.style.display = 'block'
        } else {
            item.style.display = 'none'
        }
    })
}