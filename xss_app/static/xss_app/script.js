let genZModeOn = localStorage.getItem('genZModeOn') === 'true';

function changeGenZMode() {
    genZModeOn = !genZModeOn;
    localStorage.setItem('genZModeOn', genZModeOn);
    changeGenZElement();
}

function changeGenZElement() {
    if (genZModeOn) {
        document.getElementById("video-container").style.display = "block";
    } else {
        document.getElementById("video-container").style.display = "none";
    }
}

window.addEventListener('DOMContentLoaded', () => {
    scrollToFragment();
});

window.addEventListener('hashchange', () => {
    scrollToFragment();
});

function scrollToFragment() {
    if (window.location.hash) {
        const id = window.location.hash.replace('#', '');
        const element = document.getElementById(id);
        if (element) {
            const elementRect = element.getBoundingClientRect();
            const absoluteElementTop = elementRect.top + window.pageYOffset;
            const middle = absoluteElementTop - (window.innerHeight / 2);
            window.scrollTo({top: middle, behavior: 'instant'});
        }
    }
}

function setRealCookie() {
    document.getElementById("realCookie").value = document.cookie;
}

function checkCookieBeforeSubmit() {
    let cookie = document.cookie.split("=").at(1);
    let userInput =  document.getElementById("cookieInput").value;
    let performedAttack = document.getElementById('cookieSubmitForm').getAttribute('data-performed-reflected-xss') === 'True';

    if (userInput !== cookie || !performedAttack) {
        document.getElementById('incorrectEx1Message').style.display = 'block';
        return false;
    } else {
        document.getElementById('incorrectEx1Message').style.display = 'none';
        return true;
    }
}

function checkSecretBeforeSubmit() {
    let secretValue = document.getElementById('secretInput').value;
    let performedAttack = document.getElementById('secretSubmitForm').getAttribute('data-performed-stored-xss') === 'True';

    if (secretValue !== 'I never skip breakfast!' || !performedAttack) {
        document.getElementById('incorrectEx2Message').style.display = 'block';
        return false;
    } else {
        document.getElementById('incorrectEx2Message').style.display = 'none';
        return true;
    }
}