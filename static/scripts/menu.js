const menu = document.getElementById('burger-menu')
const bodyBox = document.getElementById('body-box')
const menuContainer = document.getElementById('menu-box')
menu.addEventListener('click', () => {

    menuContainer.classList.toggle("active-menu")
    bodyBox.classList.toggle("menu-body-acive")

    for (let i = 0; i < 20; i++) {
        setTimeout(() => {
            menuContainer.style.width = `${i}%`
        }, 0);
    }
})

const closeMenu = document.getElementById('close-menu')
closeMenu.addEventListener('click', () => {
    let findcrosslink = menuContainer.classList.length
    if (menuContainer.classList[findcrosslink - 1] == 'active-menu') {

        for (let i = 20; i > 0; i--) {
            setTimeout(() => {
                menuContainer.style.width = `${i}%`
            }, 0);
        }
        setTimeout(() => {
            menuContainer.classList.remove("active-menu")
            bodyBox.classList.remove("menu-body-acive")
        }, 200);

    }
})

// audio player
document.addEventListener('DOMContentLoaded', function () {
    new GreenAudioPlayer('.audio-deck-control');
});