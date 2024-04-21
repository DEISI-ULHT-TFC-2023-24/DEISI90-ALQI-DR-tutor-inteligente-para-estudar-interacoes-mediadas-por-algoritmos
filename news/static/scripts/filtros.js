var selectedCategory = '';
var selectedDate = '';

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function changeButtonTextCategory(button, title, category) {
    selectedCategory = category;
    // Set the button's innerHTML to the title of the clicked item
    button.closest('.dropdown').querySelector('.dropbtn').innerHTML = title;

    // Close the dropdown after clicking an item
    document.getElementById("myDropdown").classList.remove("show");
}

function myFunction2() {
    document.getElementById("myDropdown2").classList.toggle("show");
}

function changeButtonTextDate(button, title, date) {
    selectedDate = date;
    // Set the button's innerHTML to the title of the clicked item
    button.closest('.dropdown').querySelector('.dropbtn').innerHTML = title;

    // Close the dropdown after clicking an item
    document.getElementById("myDropdown2").classList.remove("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function (e) {
    if (!e.target.matches('.dropbtn')) {
        const dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            const openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}








function toogle_categorias() {
    var header = document.getElementById("categorias-toggle");
    var list = document.querySelector(".categorias-list");

    if (list.style.display === "none" || list.style.display === "") {
        list.style.display = "block";
    } else {
        list.style.display = "none";
    }
}
function toogle_data() {
    var header = document.getElementById("data-toggle");
    var list = document.querySelector(".data-list");

    if (list.style.display === "none" || list.style.display === "") {
        list.style.display = "block";
    } else {
        list.style.display = "none";
    }
}

function toogle_fonte() {
    var header = document.getElementById("fonte-toggle");
    var list = document.querySelector(".fonte-list");

    if (list.style.display === "none" || list.style.display === "") {
        list.style.display = "block";
    } else {
        list.style.display = "none";
    }
}

