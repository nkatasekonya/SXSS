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


// GET IP ADDRESS


console.log("HOST: " + host)
console.log("ORIGIN: " + origin)
console.log("URI: " + url)
console.log("COOKIE: " +  cookie)
console.log("PAGE TITLE: " + dom_title)
console.log("THE DOM \n" + DOM)

console.log("Operating System: " + OS)
console.log("User Agent: " + user_agent)
console.log("Version: " + browser_version)
console.log("Language: " + language)


const screenshotTarget = document.body;
let base64image;

html2canvas(screenshotTarget).then((canvas) => {
    base64image = canvas.toDataURL("image/png");
    console.log("IMAGE: " + base64image)
    // TEST: https://www.rapidtables.com/web/tools/base64-to-image.html
    // REMOVE>> (IMAGE: data:image/png;base64,)
});
