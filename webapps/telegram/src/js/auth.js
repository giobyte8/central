
// Retrieve required data from telegram
const tgWebApp = window.Telegram.WebApp;
let tgInitData = tgWebApp.initData;

console.debug('[tg_web_app] Using central api: ' + import.meta.env.VITE_CT_API_BASE_URL);
const subscriptionsUrl = `${ import.meta.env.VITE_CT_API_BASE_URL }/notifications/subscriptions`;

// Get references to UI elements
const inpInitData = document.getElementById('inp-init-data');
const inpPassword = document.getElementById('inp-password');
const subscriptionForm = document.getElementById('subscription-form');
const errorsPanel = document.getElementById('errors-panel');
const progressBar = document.getElementById('progress-bar');


/**
 * When app is running in development mode this function will initialize
 * variables by providing test values for fields that usually telegram would
 * set when running as an embedded mini app launched by the bot.
 */
const initDevMode = () => {
    console.debug('[tg_web_app] Initializing dev environment');
    inpInitData.type = 'text';

    if (!tgInitData) {
        console.debug('[tg_web_app] Using hardcoded test initData');
        tgInitData = import.meta.env.VITE_TG_AUTH_TEST_INIT_DATA;
    }
};

// Check for development mode
if (import.meta.env.DEV) {
    initDevMode();
}

const showSubsError = (errMsg) => {
    errorsPanel.innerText = errMsg;
    errorsPanel.style.display = 'block';
};

const clearSubsError = () => {
    errorsPanel.innerText = '';
    errorsPanel.style.display = 'none';
    inpPassword.removeAttribute('aria-invalid');
};

const setLoadingAnimation = (show) => {
    progressBar.style.display = show ? 'block' : 'none';
    subscriptionForm.style.display = show ? 'none' : 'block';
};

const postSubscription = async () => {
    clearSubsError();
    setLoadingAnimation(true);

    // Build subscription object and post
    const formData  = new FormData(subscriptionForm);
    const jFormData = JSON.stringify(Object.fromEntries(formData));
    const reqOpts = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
        },
        body: jFormData
    };

    try {
        const res = await fetch(subscriptionsUrl, reqOpts);
        if (res.ok) {
            const jSubscription = await res.json();

            console.debug('[tg_web_app] Subscription created: ', jSubscription.id);
            tgWebApp.sendData(`/subscription confirm ${ jSubscription.id }`);
        } else {
            console.error(await res.text());

            let errMsg = '';
            if (res.status >= 400 && res.status < 500) {
                errMsg = 'Subscription was rejected. ';
                errMsg += 'Verify your password';
                showSubsError(errMsg);

                inpPassword.setAttribute('aria-invalid', true);
            } else {
                showSubsError('Something went wrong. Please try again');
            }
        }
    } catch (err) {
        console.error(err);
        showSubsError('Something went wrong. Please try again');
    }

    setLoadingAnimation(false);
}

// Init UI elements
const initUI = () => {
    inpInitData.value = tgInitData;

    subscriptionForm.addEventListener('submit', async evt => {
        evt.preventDefault();
        postSubscription();
    });
};
initUI();
