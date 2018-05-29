function changeLink() {
    let role = document.getElementById("role");
    let loginButton = document.getElementById("login");
    if (role.options[role.selectedIndex].value === "Admin") {
        loginButton.setAttribute("href", "index-admin.html")
    } else if (role.options[role.selectedIndex].value === "User") {
        loginButton.setAttribute("href", "index-user.html")

    }
}