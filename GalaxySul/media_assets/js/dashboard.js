document.addEventListener("DOMContentLoaded", function (evt) {
    var classify_tab = document.getElementById("classify-tab");
    var contributions_tab = document.getElementById("my-contributions-tab");
    var status_tab = document.getElementById("project-status-tab");

    classify_tab.style.display = "none";
    contributions_tab.style.display = "none";
    status_tab.style.display = "none";

    show_tab('project-status');
});

function show_tab(tab_name) {
    var classify_tab = document.getElementById("classify-tab");
    var contributions_tab = document.getElementById("my-contributions-tab");
    var status_tab = document.getElementById("project-status-tab");

    classify_tab.style.display = "none";
    contributions_tab.style.display = "none";
    status_tab.style.display = "none";

    var active_tab = document.getElementById(tab_name + '-tab');
    active_tab.style.display = "block";
}