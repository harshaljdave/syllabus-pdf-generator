document.getElementById("filter").onchange = function filter() {
    // for (var option of document.getElementById("filter").options) {
    //     document.getElementById("container").append(option.value + ' ');
    // }
    const val = document.getElementById("filter").value
    const x = document.getElementsByName(val)
    console.log(x)
    x.forEach(element => {
        element.style.display = "none"
    });
}