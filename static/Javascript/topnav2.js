
function toggleNav() {
  var sidenav = document.getElementById("mySidenav");
  var overlay = document.getElementById("overlay3");
  var menuIcon = document.getElementById("menuIcon");
  var closeIcon = document.getElementById("closeIcon");
  var menuIconSidenav = document.getElementById("menuIconSidenav");
  var sidenavItems = document.getElementById("sidenavItems");

  if (sidenav.style.width === "250px") {
    sidenav.style.width = "0";
    overlay.style.display = "none";
    menuIcon.style.display = "block";
    closeIcon.style.display = "none";
    menuIconSidenav.style.display = "block";
    sidenavItems.classList.add("hidden");
  } else {
    sidenav.style.width = "250px";
    overlay.style.display = "block";
    menuIcon.style.display = "none";
    closeIcon.style.display = "block";
    menuIconSidenav.style.display = "none";
    sidenavItems.classList.remove("hidden");
  }
}

function closeNav() {
  var sidenav = document.getElementById("mySidenav");
  var overlay = document.getElementById("overlay3");
  var menuIcon = document.getElementById("menuIcon");
  var closeIcon = document.getElementById("closeIcon");
  var menuIconSidenav = document.getElementById("menuIconSidenav");
  var sidenavItems = document.getElementById("sidenavItems");

  sidenav.style.width = "0";
  overlay.style.display = "none";
  menuIcon.style.display = "block";
  closeIcon.style.display = "none";
  menuIconSidenav.style.display = "block";
  sidenavItems.classList.add("hidden");
}