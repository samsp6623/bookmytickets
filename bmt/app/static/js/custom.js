var lmode = document.getElementById('light-mode');
if (localStorage.getItem("lmode") == null) {
    localStorage.setItem("lmode", "light")
} else {
    document.querySelector("html").setAttribute("data-theme", localStorage.getItem("lmode"))
}

lmode.addEventListener("click", (e) => {
    var lmode = localStorage.getItem("lmode")
    if (lmode == "light") {
        document.querySelector("html").setAttribute("data-theme", "dark");
        localStorage.setItem("lmode", "dark");
    } else {
        document.querySelector("html").setAttribute("data-theme", "light");
        localStorage.setItem("lmode", "light")
    }
})