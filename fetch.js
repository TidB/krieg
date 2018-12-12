// Adapted from https://github.com/ge-ku/Ban-Checker-for-Steam
// Threw out a lot of stuff, we'll just log each entry to the console which you can save
let continue_token = null;
let sessionid = null;
let profileURI = null;
let tabURIparam = 'playermatchhistory';

let result = '';

const maxRetries = 0;

const initVariables = () => {
    const profileAnchor = document.querySelector('#global_actions .user_avatar');
    if (!profileAnchor) {
        console.log('Error: .user_avatar element was not found');
    }
    profileURI = profileAnchor.href;
    if (!document.querySelector('#load_more_button')) {
        console.log('No "LOAD MORE HISTORY" button is present, seems like there are no more matches');
    }
    const steamContinueScript = document.querySelector('#personaldata_elements_container+script');
    const matchContinueToken = steamContinueScript.text.match(/g_sGcContinueToken = '(\d+)'/);
    if (!matchContinueToken) {
        console.log('Error: g_sGcContinueToken was not found');
    }
    continue_token = matchContinueToken[1];
    const steamSessionScript = document.querySelector('#global_header+script');
    const matchSessionID = steamSessionScript.text.match(/g_sessionID = "(.+)"/);
    if (!matchSessionID) {
        console.log('Error: g_sessionID was not found');
    }
    sessionid = matchSessionID[1];
    const tabOnEl = document.querySelector('.tabOn');
    if (tabOnEl) {
        tabURIparam = tabOnEl.parentNode.id.split('_').pop();
    }
    if (typeof content !== 'undefined') fetch = content.fetch; // fix for Firefox with disabled third-party cookies
    return 1;
}

const fetchMatchHistory = () => {
    if (continue_token && sessionid && profileURI) {
        console.log(`<!--First continue token: ${continue_token} | SessionID: ${sessionid} | Profile: ${profileURI} -->`);
        fetchMatchHistoryPage(true, 1, maxRetries);
    }
}

const fetchMatchHistoryPage = (recursively, page, retryCount) => {
    document.querySelector('#load_more_button').style.display = 'none';
    document.querySelector('#inventory_history_loading').style.display = 'block';
    fetch (`${profileURI}gcpd/440?ajax=1&tab=${tabURIparam}&continue_token=${continue_token}&sessionid=${sessionid}`,
        {
            credentials: "include"
        })
    .then(res => {
        if (res.ok) {
            const contentType = res.headers.get("content-type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                return res.json();
            } else {
                return res.text();
            }
        } else {
            throw Error(`Code ${res.status}. ${res.statusText}`);
        }
    })
    .then(json => {
        if (!json.success) {
            throw Error('error getting valid JSON in response to\n' +
                        `${profileURI}gcpd/440?ajax=1&tab=${tabURIparam}&continue_token=${continue_token}&sessionid=${sessionid}`);
        }
        if (json.continue_token) {
            continue_token = json.continue_token;
        } else {
            console.log('<!--No continue_token returned from Steam, looks like there are no more matches to load!-->');
            continue_token = null;
        }

        result += json.html;

        if (recursively && continue_token) {
            console.log(`<!--Loaded ${page ? page + 1 : 1} page${page ? 's' : ''}...-->`);
            fetchMatchHistoryPage(true, page ? page + 1 : 1, maxRetries);
        } else {
            if (!continue_token) {
                document.querySelector('#inventory_history_loading').style.display = 'none';
            } else {
                document.querySelector('#load_more_button').style.display = 'inline-block';
                document.querySelector('#inventory_history_loading').style.display = 'none';
            }
        }
    })
    .catch((error) => {
        console.log(`<!--Error while loading match history:\n${error}` +
                     `${retryCount !== undefined && retryCount > 0 ? `\n\nRetrying to fetch page... ${maxRetries - retryCount}/3-->`
                                                                   : `\n\nCouldn't load data after ${maxRetries} retries :(`}-->`);
        if (retryCount > 0) {
            setTimeout(() => fetchMatchHistoryPage(true, page, retryCount - 1), 3000);
        }
        document.querySelector('#load_more_button').style.display = 'inline-block';
        document.querySelector('#inventory_history_loading').style.display = 'none';
    })
    return 1;
}

initVariables();
fetchMatchHistory();
console.log(result);